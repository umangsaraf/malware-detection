import numpy as np
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.sparse import *
import json
import os
from itertools import islice

def make_coefficient_chart(df_train,clf, kernel):
    """
    Makes a chart for each app's coefficient
    
    Parameters
    ----------
    df_train : DataFrame
         Dataframe for the kernel to analyze
    clf : LinearSVC model
        model trained on the kernel
    kernel : String
        string of the current kernel for naming saved charts 
    
    Returns
    -------
    weights : List
        A list of all model coefficients 
    """
    weights = clf.coef_[0]
    plt.scatter(df_train.index, weights)
    plt.xlabel('App Index')
    plt.ylabel('Model Coefficient')
    plt.title('Linear SVM Weights For Each App')
    outpath_viz = 'charts'
    if not os.path.isdir(outpath_viz):
        os.mkdir(outpath_viz)
    plt.savefig('charts/svm_weights_' + kernel + '.png')
    return weights

def do_weight_analysis(df_train, weights, matrix, kernel):
    """
    Analyze the coefficients and the apps they correspond to. Find any discrepencies and save their statistics.
    
    Parameters
    ----------
    df_train : DataFrame
         Dataframe for the kernel to analyze
    weights : List
        Model coefficients for the kernel
    matrix : Sparse Matrix
        A matrix for statistic gathering
    kernel : String
        string of the current kernel for naming saved charts 
    
    Returns
    -------
    saves several charts and tables 
    """
    
    # Get extreme weights and their indices

    index_weight_dic = defaultdict(float)
    for i in df_train.index.values:
        index_weight_dic[i] = weights[i]

    max_weights = {k: v for k, v in sorted(index_weight_dic.items(), key=lambda item: item[1], reverse=True)}
    top_max_weights = dict(list(islice(max_weights.items(), 10)))

    min_weights = {k: v for k, v in sorted(index_weight_dic.items(), key=lambda item: item[1])}
    top_min_weights = dict(list(islice(min_weights.items(), 10)))

    mal_pos_weight = []
    num_malware = 0
    for k,v in top_max_weights.items():
        if df_train.iloc[k].values[-1] == 0:
            num_malware += 1
            mal_pos_weight.append(k)


    ben_neg_weight = []
    num_malware = 0
    for k,v in top_min_weights.items():
        if df_train.iloc[k].values[-1] == 0:
            num_malware += 1
        else:
            ben_neg_weight.append(k)


    # Analyze Benign Apps with Negative Weights

    ben_neg_df = pd.DataFrame()
    if len(ben_neg_weight) > 0:
        a4_dims = (24, 24)
        fig, axs = plt.subplots(len(ben_neg_weight), figsize=a4_dims)
        i_plot = 0
        ben_neg = {'App name': [], 
                   'Total APIs': [], 
                   'Avg Vector Value': [],  
                   'Std Vector Value': [], 
                   'Min Vector Value': [], 
                   'Max Vector Value': [], 
                   "Type":[]}
        for i in ben_neg_weight:
            ben_neg['App name'].append(df_train.iloc[i].values[-2])
            ben_neg['Total APIs'].append(matrix[i].todense().sum())
            ben_neg['Avg Vector Value'].append(np.mean(df_train.iloc[i].values[:-2]))
            ben_neg['Std Vector Value'].append(np.std(df_train.iloc[i].values[:-2]))
            ben_neg['Min Vector Value'].append(np.min(df_train.iloc[i].values[:-2]))
            ben_neg['Max Vector Value'].append(np.max(df_train.iloc[i].values[:-2]))
            ben_neg['Type'].append(df_train.iloc[i].values[-1])
            sns.distplot(df_train.iloc[i].values[:-2], ax=axs[i_plot]).set_title('Distribution of Vector Value for Benign Apps Neg Weight')
            i_plot += 1
        ben_neg_df = pd.DataFrame(ben_neg)
        plt.savefig('charts/ben_neg_weight_' + kernel + '.png')


    #ben_neg_df.to_csv('ben_neg_weight_' + kernel + '.csv')

    # Analyze Malware apps with Positive Weights

    mal_pos_df = pd.DataFrame()
    if len(mal_pos_weight) > 0:
        a4_dims = (24, 24)
        fig, axs = plt.subplots(len(mal_pos_weight), figsize=a4_dims)
        i_plot = 0
        mal_pos = {'App name': [], 
                   'Total APIs': [], 
                   'Avg Vector Value': [],  
                   'Std Vector Value': [], 
                   'Min Vector Value': [], 
                   'Max Vector Value': [], 
                   "Type":[]}
        for i in mal_pos_weight:
            mal_pos['App name'].append(df_train.iloc[i].values[-2])
            mal_pos['Total APIs'].append(matrix[i].todense().sum())
            mal_pos['Avg Vector Value'].append(np.mean(df_train.iloc[i].values[:-2]))
            mal_pos['Std Vector Value'].append(np.std(df_train.iloc[i].values[:-2]))
            mal_pos['Min Vector Value'].append(np.min(df_train.iloc[i].values[:-2]))
            mal_pos['Max Vector Value'].append(np.max(df_train.iloc[i].values[:-2]))
            mal_pos['Type'].append(df_train.iloc[i].values[-1])
            sns.distplot(df_train.iloc[i].values[:-2]).set_title('Distribution of Vector Value for Malware Apps Pos Weight')
            i_plot += 1
        mal_pos_df = pd.DataFrame(mal_pos)
        plt.savefig('charts/mal_pos_weight_' + kernel + '.png')

    mal_pos_df.to_csv('results/mal_pos_weight_' + kernel + '.csv')

def do_fp_analysis(df_test, matrix, kernel):
    """
    Analyze the false positive apps and compiles their distributions and statistics
    
    Parameters
    ----------
    df_train : DataFrame
         Dataframe for the kernel to analyze
    matrix : Sparse Matrix
        A matrix for statistic gathering
    kernel : String
        string of the current kernel for naming saved charts 
    
    Returns
    -------
    saves several charts and tables 
    """
    
    predict_y = df_test['predictions'].values
    test_y = df_test['type'].values
    fp_index = []
    for i in range(len(predict_y)):
        if predict_y[i] != test_y[i] and predict_y[i] == 1:
            fp_index.append(i)


    fps = {'App name': [], 
           'Total APIs': [], 
           'Avg Vector Value': [],  
           'Std Vector Value': [], 
           'Min Vector Value': [], 
           'Max Vector Value': []}
    for i in fp_index:
        fps['App name'].append(df_test.iloc[i].values[-3])
        fps['Total APIs'].append(matrix[i].todense().sum())
        fps['Avg Vector Value'].append(np.mean(df_test.iloc[i][:-3]))
        fps['Std Vector Value'].append(np.std(df_test.iloc[i][:-3]))
        fps['Min Vector Value'].append(np.min(df_test.iloc[i][:-3]))
        fps['Max Vector Value'].append(np.max(df_test.iloc[i][:-3]))

    fps_df = pd.DataFrame(fps)
    fps_df.to_csv('results/'+ kernel + '_fp_analysis.csv')

def make_eda_charts(df_train, kernel):
    """
    Analyze the current kernel and plot the distributions of multiple statistics
    
    Parameters
    ----------
    df_train : DataFrame
         Dataframe for the kernel to analyze
    kernel : String
        string of the current kernel for naming saved charts 
    
    Returns
    -------
    saves several charts
    """
    benign_index = df_train.loc[df_train['type'] == 1].index.values
    malware_index = df_train.loc[df_train['type'] == 0].index.values

    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    avg_shared_apis_benign = []
    avg_shared_apis_malware = []
    for i in benign_index:
        avg_shared_apis_benign.append(np.mean(df_train.iloc[i][:-2]))

    for i in malware_index:
        avg_shared_apis_malware.append(np.mean(df_train.iloc[i][:-2]))

    sns.distplot(avg_shared_apis_benign, label='Benign', ax=ax)
    sns.distplot(avg_shared_apis_malware, label='Malware', ax=ax)


    plt.xlabel('Avg Vector Value')
    plt.title('Distribution of Avg Vector Value for Benign and Malware Apps')
    plt.legend()
    plt.savefig('charts/avg_api_' + kernel + '.png')

    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    min_shared_apis_benign = []
    min_shared_apis_malware = []

    for i in benign_index:
        min_shared_apis_benign.append(np.min(df_train.iloc[i][:-2]))


    for i in malware_index:
        min_shared_apis_malware.append(np.min(df_train.iloc[i][:-2]))

    sns.distplot(min_shared_apis_benign, label='Benign', ax=ax)
    sns.distplot(min_shared_apis_malware, label='Malware', ax=ax)

    plt.xlabel('Min Vector Value')
    plt.title('Distribution of Min Vector Value for Benign and Malware Apps')
    plt.legend()
    plt.savefig('charts/min_api_' + kernel + '.png')

    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    max_shared_apis_benign = []
    max_shared_apis_malware = []
    for i in malware_index:
        max_shared_apis_malware.append(np.max(df_train.iloc[i][:-2]))
    for i in benign_index:
        max_shared_apis_benign.append(np.max(df_train.iloc[i][:-2]))

    sns.distplot(max_shared_apis_benign, label='Benign', ax=ax)
    sns.distplot(max_shared_apis_malware,label='Malware', ax=ax)

    plt.xlabel('Max Shared APIs')
    plt.title('Distribution of Max Vector Value for Benign Apps')
    plt.legend()
    plt.savefig('charts/max_api_' + kernel + '.png')

def make_bivariate_plots(df_train, weights, kernel):
    """
    Create summarizing plots for the model coefficient compared to statistics of average and max vector value
    
    Parameters
    ----------
    df_train : DataFrame
         Dataframe for the kernel to analyze
    weights : List
        Model coefficients for the kernel
    kernel : String
        string of the current kernel for naming saved charts 
    
    Returns
    -------
    saves several charts
    """
    benign_index = df_train.loc[df_train['type'] == 1].index.values
    malware_index = df_train.loc[df_train['type'] == 0].index.values
    
    benign_info = defaultdict(list)
    malware_info = defaultdict(list)
    for i in df_train.index:
        if i in benign_index:
            benign_info[i].append(weights[i])
            benign_info[i].append(np.mean(df_train.iloc[i][:-2]))
        elif i in malware_index:
            malware_info[i].append(weights[i])
            malware_info[i].append(np.mean(df_train.iloc[i][:-2]))

    benign_coef = []
    benign_avg_api = []
    for k,v in benign_info.items():
        benign_coef.append(v[0])
        benign_avg_api.append(v[1])
    malware_coef = []
    malware_avg_api = []
    for k,v in malware_info.items():
        malware_coef.append(v[0])
        malware_avg_api.append(v[1])

    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    sns.scatterplot(x=benign_avg_api, y=benign_coef, label='Benign', ax=ax).set_title('SVM Weights Compared to the Average Vector Value')
    sns.scatterplot(x=malware_avg_api, y=malware_coef, label='Malware', ax=ax)
    plt.ylabel('Model Coefficient')
    plt.xlabel('Avergae Vector Value')
    plt.legend()
    plt.savefig('charts/weights_vs_values_avg_' + kernel + '.png')


    benign_info = defaultdict(list)
    malware_info = defaultdict(list)
    for i in df_train.index:
        if i in benign_index:
            benign_info[i].append(weights[i])
            benign_info[i].append(np.max(df_train.iloc[i][:-2]))
        elif i in malware_index:
            malware_info[i].append(weights[i])
            malware_info[i].append(np.max(df_train.iloc[i][:-2]))

    benign_coef = []
    benign_avg_api = []
    for k,v in benign_info.items():
        benign_coef.append(v[0])
        benign_avg_api.append(v[1])
    malware_coef = []
    malware_avg_api = []
    for k,v in malware_info.items():
        malware_coef.append(v[0])
        malware_avg_api.append(v[1])

    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    sns.scatterplot(x=benign_avg_api, y=benign_coef, label='Benign', ax=ax).set_title('SVM Weights Compared to the Max Vector Value')
    sns.scatterplot(x=malware_avg_api, y=malware_coef, label='Malware', ax=ax)
    plt.ylabel('Model Coefficient')
    plt.xlabel('Max Vector Value')
    plt.legend()
    plt.savefig('charts/weights_vs_values_max_' + kernel +'.png')

def run_coefficient_analysis(df_train,df_test,clf, matrix, kernel):
    #make the chart showing coefficients for each app
    weights = make_coefficient_chart(df_train, clf, kernel)
    
    #make the chart showing coefficients for each app
    do_weight_analysis(df_train, weights, matrix, kernel)
    
    #create tables and charts for FP apps
    do_fp_analysis(df_test, matrix, kernel)
    
    #create plots for the EDA of the kernel
    make_eda_charts(df_train, kernel)
    
    #make summarizing bivariate plots for the kernel
    make_bivariate_plots(df_train, weights, kernel)