import json
import sys
import pickle 
from src.elt import *
from src.make_dataset import *
from src.build_features import *
from src.model import *
from src.multi_kernel import *
from src.coefficient_analysis import *



def main_func(**kwargs):
    name_path = kwargs['outpath']
    if name_path[0] == 'data':
        main_scrape(name_path, kwargs)
    
    #Get paths of all Malware apps
    malware_path, type_of_malware = malware_app_paths() 
    
    #get paths of all newly created benign apps   
    benign_paths = benign_app_paths_test(name_path[0]) 
    malware_apps = malware_path[:len(benign_paths)]
    path = benign_paths[:2] + malware_apps
  
    ## Feature extraction step for all the training apps 
    apps_dic,code_block_dic,package_dic,api_list, app_list = main_train(path, name_path)
    
    ## Creates matrices 
    a_matrix, b_matrix, p_matrix = build_feat(app_list,api_list,apps_dic,code_block_dic,package_dic,name_path[0])

    ## Gets path to all benign apps
    test_benign_paths =  benign_paths[2:4]

    ## Gets path to all malware apps
    malware_apps = []
    for i in malware_path:
        if i.split('/')[-1] not in app_list:
            malware_apps.append(i)

    malware_test_paths = malware_apps[2:4]

    ## Gets all the paths 
    test_paths = test_benign_paths + malware_test_paths
 

    ## Creates structure for the test set 
    print('creating data structure for test set')
    test_apps_dic = get_data_test(test_paths)
    print('------------------------------------')

    ## saves the new test structure created 
    test_save_structures(test_apps_dic, name_path[0])
    
    # gets list of app names
    app_list_test = list(test_apps_dic.keys())
    
    ## Creates the A matrix for the test set 
    a_test_matrix = create_a_matrix_test(app_list_test,api_list,test_apps_dic)
    path_a_test = name_path[0] + '/matrix/' + 'a_test_matrix.npz'
    save_npz(path_a_test, a_test_matrix)

    #Initilaze our linear SVC model
    clf = LinearSVC(max_iter = 10000)
    
    #loop through all the diffrent kernels
    kernel_list = ['A.A^T','A.B.A^T', 'A.P.A^T','A.B.P.A^T']
    
    #get the scores for all the kernels
    scores_df,train_kernel_list, test_kernel_list, labels = get_scores(a_test_matrix,a_matrix, b_matrix, \
                           p_matrix, kernel_list, clf, \
                          benign_paths,app_list,app_list_test,\
                          name_path)
    
    #chose model to learn wieghts
    model_align = Alignf(typ="convex")    
    #create multi kernel for train and test
    df_train_multi, df_test_multi =         get_scores_multi(train_kernel_list,test_kernel_list, linear_kernel, \
                    model_align, labels, benign_paths,app_list, app_list_test)
    print(scores_df)
    #get accuracy score for multik-kernel model
    dic_scores = {}
    dic_scores['multi_kernel'],test_df = run_model(df_train_multi,df_test_multi, clf)
    print(dic_scores)

        
    #save it as a CSV 
    result_path = 'results/'
    if not os.path.isdir(result_path):
        os.mkdir(result_path)
    scrores_path = result_path + '/'+ name_path[4]
    scores_df.to_csv(scrores_path)
    
    print('conducting coefficient analysis for AA^T kernel')
    #make train kernel and train dataframe
    train_kernel_aa  = aa_kernel(a_matrix,a_matrix)
    df_train_aa  = create_df(train_kernel_aa,benign_paths,app_list )

    #make test kernel and test dataframe
    test_kernel_aa =  aa_kernel(a_test_matrix,a_matrix)
    df_test_aa  = create_df(test_kernel_aa,benign_paths,app_list_test )
    
    #run model for the AA^T kernel
    clf = LinearSVC(max_iter = 20000)
    dic_scores,test_df = run_model(df_train_aa,df_test_aa, clf)
    
    run_coefficient_analysis(df_train_aa, df_test_aa,clf, a_matrix, 'aa')
    
    
    print('coefficient analysis complete')
    print('------------------------------------')
    
    print('conducting coefficient analysis for ABA^T kernel')
    #make train kernel and train dataframe
    train_kernel_ab  = ab_or_p_kernel(a_matrix,a_matrix,b_matrix)
    df_train_ab  = create_df(train_kernel_ab,benign_paths,app_list)

    #make test kernel and test dataframe
    test_kernel_ab =  ab_or_p_kernel(a_test_matrix,a_matrix,b_matrix)
    df_test_ab  = create_df(test_kernel_ab,benign_paths,app_list_test)
    
    #run model for the ABA^T kernel
    clf = LinearSVC(max_iter = 20000)
    dic_scores,test_df = run_model(df_train_ab,df_test_ab, clf)
    
    run_coefficient_analysis(df_train_ab ,df_test_ab, clf, a_matrix, 'ab')
    
    print('coefficient analysis complete')
    print('------------------------------------')
    
    print('conducting coefficient analysis for APA^T kernel')
    #make train kernel and train dataframe
    train_kernel_ap  = ab_or_p_kernel(a_matrix,a_matrix,p_matrix)
    df_train_ap  = create_df(train_kernel_ap,benign_paths,app_list )

    #make test kernel and test dataframe
    test_kernel_ap =  ab_or_p_kernel(a_test_matrix,a_matrix,p_matrix)
    df_test_ap  = create_df(test_kernel_ap,benign_paths,app_list_test )
    
    #run model for the APA^T kernel
    clf = LinearSVC(max_iter = 20000)
    dic_scores,test_df = run_model(df_train_ap,df_test_ap, clf)
    
    run_coefficient_analysis(df_train_ap ,df_test_ap, clf, a_matrix, 'ap')
    print('coefficient analysis complete')
    print('------------------------------------')
    
    
    
if __name__=='__main__':
    warnings.filterwarnings("ignore")
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            with open('config/test-params.json') as file:
                cfg = json.load(file)
    else: 
        with open('config/params.json') as file:
            cfg = json.load(file)
        
    main_func(**cfg)




