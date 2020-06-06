import re
from collections import defaultdict
import time
import os 
import glob
from pathlib import Path
from tqdm import tqdm
import numpy as np
import json
try:
    from build_features import * 
except:
    from src.build_features import * 
import pickle 




def malware_app_paths():
    """
    Gets path to all the malware apps in the database 
    
    Returns
    -------
    malware_loc: List
        A list of all the paths of malware apps
    type_of_malware: Dictionary 
        Cotains type of malware corresponding to each app
    """
    type_of_malware = defaultdict(list)
   
    malware_loc = []
    dir_list = os.listdir("/datasets/dsc180a-wi20-public/Malware/amd_data_smali")
    for i in dir_list:
        string = '/datasets/dsc180a-wi20-public/Malware/amd_data_smali/' + i
        lis = os.listdir(string)
        for variety in lis:
            new_string = string + '/' + variety
            app_list = os.listdir(new_string)
            for app in app_list:
                final_str = new_string + '/' + app
                malware_loc.append(final_str)
                type_of_malware[i].append(app)
    return malware_loc, type_of_malware

def benign_app_paths_test(outpath):
    """
    Gets paths to all benign apps in the dataset
    
    Parameters
    ---------
    Outpath: string
        Name of folder contaning all the paths
    Returns
    -------
    path_app: List
        List of paths to all benign apps
    """

    path = outpath + "/smali"
    apps_name_list = os.listdir(path)
    apps_name_list = [i for i in apps_name_list if i.split('.')[-1] != 'apk']
    path_app = [outpath+'/smali/' + i for i in apps_name_list]
    
    return path_app


def benign_app_path_list(directory):
    """
    Simlar to benign_app_paths_test but takes in multiple directories instead of one 
    """
    final_app_name = []
    path_app = []
    for dir_ in directory:
        path = dir_ + '/smali'
        apps_name_list =  os.listdir(path)
        for app in apps_name_list:
            if app not in final_app_name:
                final_app_name.append(app)
                new_path = path + '/' + app
                path_app.append(new_path)
    return path_app

def clean_data(path):
    """
    Cleans all smali files in the dataset and then create 3 diffent datastructures 
    
    Parameters
    ----------
    path : List
        A list of all the paths of benign and malware apps
    
    Returns
    -------
    final_dic_ : Dictionary
        Keeps track of apps to api
    new_storage_dic : Dictionary
        keeps tracks of all api's in same code block
    library_dic : Dictionary
        keeps track of all api's with same library 
    """
    
    apps_dic = defaultdict(set)
    code_block_dic = defaultdict(set)
    package_dic = defaultdict(set)
    for x,path in enumerate(tqdm(path)):
        app_name  = path.split('/')[-1]
        pathlist = Path(path).glob('**/*.smali')
        smali_folders = [i for i in pathlist if '$' not in str(i)]
        if len(smali_folders) ==0:
            continue
        block_dic = defaultdict(set)
        counter = 0
        block_id = 1
       
        for i in smali_folders:
            with open(i) as FileObj:
                in_method = False
                for lines in FileObj:
                    if '.method private' in lines:
                        continue
                    if '.end method' in lines:
                        in_method = False
                        counter += 1
                    elif '.method' in lines:
                        in_method = True
                        counter += 1
                    elif in_method:
                        if block_id != counter:
                            block_apis = list(block_dic[block_id])
                            for tracker, api_1 in enumerate(block_apis):
                                for api_2 in block_apis[tracker:]:
                                    if api_1 not in code_block_dic[api_2]:
                                        code_block_dic[api_1].add(api_2)
                            
                        block_id = counter
                        
                        
                        if len(re.findall('\S+;->', lines)) == 0:
                            continue
                        pkg = re.findall('\S+;->', lines)[0][:-3]
                        
                        name = re.findall('\S+;->\S+', lines)[0]
                        index = name.find('(')
                        name = name[:index] + '()'
                        
                        if '$' in name:
                            continue
                       
                        package_dic[pkg].add(name)
                        apps_dic[app_name].add(name)
                           
                        block_dic[counter].add(name)
       
        
    return apps_dic, code_block_dic, package_dic


def save_structures(final_dic_,new_strorage_dic, library_dic,name_list):
    """
    Saves all the structures created in json files
    
    Parameters
    ----------
    final_dic_ : Dictionary
         Keeps track of apps to api
    new_strorage_dic : Dictionary
        keeps tracks of all api's in same code block
    library_dic : Dictionary
        keeps track of all api's with same library 
    name_list : List
        Contains name of all the outpaths
    
    Returns
    -------
    Saves all the structures in a json format 
    """
    
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)


    if not os.path.isdir(name_list[0]):
        os.mkdir(name_list[0])
        
    if not os.path.isdir(name_list[0] + '/processed'):
        direc = name_list[0] + '/processed'
        os.mkdir(direc)
    path1 = name_list[0] + '/processed/' + name_list[1]
    path2 = name_list[0] + '/processed/' + name_list[2]
    path3 = name_list[0] + '/processed/' + name_list[3]
    with open(path1, 'w') as f:
        json.dump(final_dic_, f, default=set_default)
    with open(path2, 'w') as f:
        json.dump(new_strorage_dic, f,default=set_default)
    with open(path3, 'w') as f:
        json.dump(library_dic, f,default=set_default)
        
def unique_api_apps(final_dic):
    """
    Filters all unique API's from the extracted API's
    
    Parameters
    ----------
    final_dic : Dictionary
        Keeps track of apps to api
    
    Returns
    -------
    api_list : List
        A list of all unique API's
    app_list : List
        A list of names of all apps
    """
    
    api_list = []
    app_list = []
    for i in final_dic.keys():
        api_list.extend(final_dic[i])
        app_list.append(i)
   
    api_list = list(set(api_list))
   
    return api_list, app_list


def get_index_of_api(a,api_list,n):
    """
    Returns list of all api's with api's in less than n apps 
    
    Parameters
    ----------
    a : crs matrix
        A matrix encoding apps to api relation 
    api_list : list
        List of all unique API's
    n : Integer 
        Number of apps API's occur in 
    
    Returns
    -------
    low_ocurring_api : List
        A list containing all the API's occuring in fewer than n apps
    """
    sum_a = a.sum(axis=0)
    list_api = sum_a.tolist()
    list_api = list_api[0]

    index_list = []
    for x,index in enumerate(list_api):
        if index < n:
            index_list.append(x)
    
    return [api_list[i] for i in index_list]

def main_train(path, name_path):
    """
    Main method that executes all the feature extraction process for training apps
    """
    #Clean all smali files and extract diffrent structures to construct the matrix 
    print('Creating data structure for train data')
    print('------------------------------------')
    apps_dic,code_block_dic,package_dic = clean_data(path)
    
    ## Gets all the unique API's in the data structure
    api_list_inter, app_list = unique_api_apps(apps_dic)
    
    
    ## Creates an intermediate A structure to find the count of each API
    print('creating intermediate A structure ')
    print('------------------------------------')
    a_matrix_inter = create_a_matrix\
    (app_list,api_list_inter, apps_dic)
    print('------------------------------------')
    
    ## Gets the index of all API's that occur less in less then n apps
    extra_api_list = get_index_of_api\
    (a_matrix_inter,api_list_inter,2)
    
     ## removes all the API's from the 3 data structures
    apps_dic,code_block_dic,package_dic = remove_apis\
    (extra_api_list,apps_dic,code_block_dic,package_dic)
    
    ## Gets the new list of unique API's
    api_list, app_list = unique_api_apps(apps_dic)

    ## Saves these datastructures again 
    save_structures(apps_dic,code_block_dic,package_dic,name_path )
    
    ## Saves unique api_list
    
    api_path = name_path[0] + '/processed/unique_api.text'
    with open(api_path, "wb") as fp: 
        pickle.dump(api_list, fp)
    
    return apps_dic,code_block_dic,package_dic,api_list, app_list

def remove_apis(small_api_list,final_dic,new_strorage_dic,library_dic):
    """
    Removes all the extra API's from all the new structures extracted 
    
    Parameters
    ---------
    small_api_list : List
        Contains all api's occuring in few apps
    final_dic_ : Dictionary
        Keeps track of apps to api
    new_storage_dic : Dictionary
        keeps tracks of all api's in same code block
    library_dic : Dictionary
        keeps track of all api's with same library 
    
    Returns
    --------
    new_final_dic : Dictionary
        New structure with all low occuring API's removed
    code_block : Dictionary
        New structure with all low occuring API's removed
    lib_dic : Dictionary
        New structure with all low occuring API's removed
    
    """
    set_small_api_list = set(small_api_list)
    new_final_dic = {}
    for i in final_dic.keys():
        new_final_dic[i] = set(final_dic[i]).difference(set_small_api_list)
    

    code_block = {}
    for key in new_strorage_dic.keys():
        if key in set_small_api_list:
            continue 
        else:
            new_set = set(new_strorage_dic[key]).difference(set_small_api_list)
            code_block[key] = new_set



    lib_dic = {}
    for lib in library_dic:
        set_diff = set(library_dic[lib]).difference(set_small_api_list)
        if len(set_diff) == 0:
            continue
        else:
            lib_dic[lib] = set_diff

  
    return new_final_dic,code_block, lib_dic

def get_data_test(path):
    """
    To create structure for test set 
    Parameters
    ----------
    path : List
        A list of all the paths of benign and malware test apps
    
    Returns
    -------
    final_dic_ : Dictionary
        Keeps track of apps to api for all test set apps
    
    """
    apps_dic = defaultdict(set)
    for x,path in enumerate(tqdm(path)):
        app_name  = path.split('/')[-1]
        pathlist = Path(path).glob('**/*.smali')
        smali_folders = [i for i in pathlist if '$' not in str(i)]
        if len(smali_folders) == 0:
            continue
        block_dic = defaultdict(set)
        counter = 0
        block_id = 1
        for i in smali_folders:
            with open(i) as FileObj:
                in_method = False
                for lines in FileObj:
                    if '.method private' in lines:
                        continue
                    if '.end method' in lines:
                        in_method = False
                        counter += 1
                    elif '.method' in lines:
                        in_method = True
                        counter += 1
                    elif in_method:
                    
                        
                        
                        if len(re.findall('\S+;->', lines)) == 0:
                            continue
                        
                        name = re.findall('\S+;->\S+', lines)[0]
                        index = name.find('(')
                        name = name[:index] + '()'
                        
                        if '$' in name:
                            continue
                            
                        apps_dic[app_name].add(name)
                           
    return apps_dic

def test_save_structures(final_dic_, outpath):
    """
    Saves all the structures created in json files
    
    Parameters
    ----------
    final_dic_ : Dictioanry 
        Test set dictionary 
    outpath : string 
        Name of directory where final_dic_ gets saved
    
    Returns
    -------
    Saves test structure in a json format 
    """
    
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)


    if not os.path.isdir(outpath):
        os.mkdir(outpath)
        
    if not os.path.isdir(outpath + '/processed'):
        direc = outpath + '/processed'
        os.mkdir(direc)
    path1 = outpath + '/processed/' + 'test_app_api.json'
    with open(path1, 'w') as f:
        json.dump(final_dic_, f, default=set_default)
        

  
        
