from scipy.sparse import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import *
import matplotlib.pyplot as plt
import numpy as np
import os
import json

plt.style.use('seaborn-whitegrid')




def aa_kernel(a_test,a):
    """
    creates the kernel A.A^T for training and test
    
    Parameters
    ----------
    a_test - crs matrix
        test or training matrix
    a - crs matrix
        Training matrix 
    
    Returns 
    -------
    A.A^T : Matrix 
        A.A^T kernel 
    """
    return a_test.dot(a.T)

def ab_or_p_kernel(a_test,a,b):
    """
    Creates kernel ABA^T for training and test
    
    Parameters
    ----------
    a_test - crs matrix
        test or training matrix
    a - crs matrix
        Training A matrix 
    b - crs matrix
        Training B matrix 
        
    Returns 
    -------
    ABA^T : Matrix 
        ABA^T kernel 
    """
    return a_test.dot(b.dot(a.T))


def apbpa_kernel(a_test, a,b,p):
    """
    Creates kernel APBP^TA^T for training and test
    
    Parameters
    ----------
    a_test - crs matrix
        test or training matrix
    a - crs matrix
        Training A matrix 
    p - crs matrix
        Training p matrix 
        
    Returns 
    -------
    APBP^TA^T : Matrix 
        APBP^TA^T kernel 
    """
    
    temp = p.T.dot(a.T)
    
    temp = b.dot(temp)
    
    temp = p.dot(temp)
    
  
    temp = a_test.dot(temp)
  
    return temp


def create_df(kernel, benign_paths, app_list):
    """
    Creates Dataframe from the kernal and adds the labels 
    
    Parameters
    ----------
    kernel: Matrix
        Training kernel 
    benign_paths: List
        List of all benign paths 
    app_list: List
        List of all app names
    
    Returns 
    -------
    kernel_df : DataFrame
        A datafarme that contains the kernel with each row corresponding to an app 
    """
    benign_apps  = [i.split('/')[-1] for i in  benign_paths]
    kernel_df = pd.DataFrame(kernel.toarray())
    kernel_df['app_name'] = app_list
    kernel_df['type'] = kernel_df.app_name.apply(lambda x: 1 if x in benign_apps else 0)
 
    return kernel_df

def run_model(df,df_test, clf):
    """
    Runs the passed in model on the kernel converted into a dataframe 
    
    Parameters
    ----------
    df : DataFrame
        Training dataframe 
    df_test : Dataframe
        Testing Dataframe 
    clf : Model
        Initialized model for classification 
    
    Returns
    --------
    dic_scores : Dictionary 
        A dictionary that contains kernels as keys and scores as keys
    test_df : Dataframe
        Updated test dataframe with predictions from the model
    """
    train_x  = df
    train_y = df['type']
    test_x = df_test
    test_y = df_test['type']
    
    clf.fit(train_x.drop({'type','app_name'} , axis = 1), train_y)
    pred = clf.predict(test_x.drop({'type','app_name'} , axis = 1))
    test_df = pd.DataFrame(test_x)
    test_df['predictions'] = pred
    df = pd.DataFrame()
    dic_scores = {}
    dic_scores['accuracy'] = accuracy_score(test_y, pred)
    dic_scores['f1_score'] = f1_score(test_y, pred)
    dic_scores['tn'], dic_scores['fp'], dic_scores['fn'], dic_scores['tp'] = \
                                confusion_matrix(test_y, pred).ravel()


    return dic_scores,test_df


def get_scores(a_test_matrix,a_matrix, b_matrix, p_matrix, kernel_list, clf, \
              benign_paths,app_list,app_list_test, name_path):
    """
    Full pipeline to get create the kernels, initialze the model and returns the predictions 
    """
    scores_dic = {}
    train_kernel_list  = []
    test_kernel_list  = []
    for i,kernel in enumerate(kernel_list):
        if i == 0:
            train_kernel_product = aa_kernel(a_matrix,a_matrix)
            test_kernel_product = aa_kernel(a_test_matrix,a_matrix)
        elif i ==1:
            train_kernel_product = ab_or_p_kernel(a_matrix,a_matrix,b_matrix)
            test_kernel_product = ab_or_p_kernel(a_test_matrix,a_matrix,b_matrix)
        elif i == 2:
            train_kernel_product = ab_or_p_kernel(a_matrix,a_matrix,p_matrix)
            test_kernel_product = ab_or_p_kernel(a_test_matrix,a_matrix,p_matrix)
        else:
            train_kernel_product = apbpa_kernel(a_matrix, a_matrix,b_matrix,p_matrix)
            test_kernel_product = apbpa_kernel(a_test_matrix, a_matrix,b_matrix,p_matrix)
            
        train_kernel_list.append(train_kernel_product)
        test_kernel_list.append(test_kernel_product)
        
        df_train =create_df(train_kernel_product,benign_paths,app_list)
        save_kernel(df_train,kernel,name_path[0])
        
        labels = df_train['type'].values
        
        df_test_aa  = create_df(test_kernel_product,benign_paths,app_list_test)
        name_test = kernel + '_test'
        save_kernel(df_test_aa,name_test,name_path[0])
        
        scores_dic[kernel], test_df = run_model(df_train,df_test_aa, clf)
        
        print('for kernel '+ kernel + ' accuracy')
        print('\n')
        print(scores_dic[kernel])
        print('------------------------------------')
        print('\n')
        
    scores_df = pd.DataFrame(scores_dic)
    scores_df = scores_df.T
    print('saving accuray of model to results/'+ name_path[4])
    return scores_df, train_kernel_list, test_kernel_list, labels


def kernel_viz_func(AAT, name):
    """
    Creates TSNE and PCA visualizations for the kernels 
    
    Parameters
    ----------
    AAT - Kernels for AAT
    name - path to save viz
    
    Returns
    -------
    vizualizations 
    """
    y = AAT["type"].replace({0:"malware", 1:"benign"})
    X = AAT
    X = X.drop( ['app_name', 'type'], axis=1)
    
    print("PCA Plot:")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    data = pd.DataFrame({"X Value": X_pca[:, 0], "Y Value": X_pca[:, 1], "Category": y})
    groups = data.groupby("Category")
    for name, group in groups:
        plt.scatter(group["X Value"], group["Y Value"], marker="o", label=name, s=1)
    plt.legend()
    plt.show()
    name_path = 'pct' + name
    plt.savefig(name_path)
    
    print("T-SNE Plot:")
    X_embedded = TSNE(n_components=2).fit_transform(X)
    data = pd.DataFrame({"X Value": X_embedded[:, 0], "Y Value": X_embedded[:, 1], "Category": y})
    groups = data.groupby("Category")
    for name, group in groups:
        plt.scatter(group["X Value"], group["Y Value"], marker="o", label=name, s=1)
    plt.legend()
    plt.show()
    name_path = 'T-SNE' + name
    plt.savefig(name_path)
    
    print("Both Plot:")
    X_embedded = TSNE(n_components=3).fit_transform(X)
    pca2 = PCA(n_components=2)
    X_pca = pca2.fit_transform(X_embedded)
    data = pd.DataFrame({"X Value": X_pca[:, 0], "Y Value": X_pca[:, 1], "Category": y})
    groups = data.groupby("Category")
    for name, group in groups:
        plt.scatter(group["X Value"], group["Y Value"], marker="o", label=name, s=1)
    plt.legend()
    

    
    
def save_kernel(df,name,directory):
    
    if not os.path.isdir(directory + '/kernels'):
        direc = directory + '/kernels'
        os.mkdir(direc)
    path = directory + '/kernels/' + name + '.csv'
    df.to_csv(path)
