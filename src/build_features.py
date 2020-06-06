import re
from collections import defaultdict
import time

import os 
import glob
from pathlib import Path
from tqdm import tqdm
import numpy as np
from scipy.sparse import *
import pandas as pd
import json


def create_a_matrix(app_list,api_list,final_dic):
    """
    Creates A matrx of size NxM, where N is number of apps and M is list of unique API's
    
    Parameters
    ---------
    app_list : list
        List of all apps
    api_list : list
        List of all unique API's
    final_dic : dictionary
        Apps as keys and values as all API's in dictionary 
        
    Returns
    -------
    A matrix : Crs matrix
        A matrix encoding app to api relation 
    """
    print('Creating A matrix')
    start = time.time()
    #initialize lil_matrix
    a = lil_matrix((len(app_list),len(api_list)))
    to_add = 0
    for x,i in enumerate(app_list):
        api_name = set([api for api in final_dic[i]])
        for count,l in enumerate(api_list):
            if l in api_name:
                #add edge
                a[x, count] = 1 
    end = time.time()
    print('time taken to create A matrix = '+ str(end - start))
    return csr_matrix(a)

def create_b_matrix(new_strorage_dic,api_list):
    """
    Creates a matrix of size MxM where M is the list unique API's
    Parameters
    ---------
    api_list : list
        List of all unique API's
    new_strorage_dic : dictionary
        API's as keys and values as all API's in the same code block
        
    Returns
    -------
    B matrix : Crs matrix
        B matrix encoding api to api relation 
    
    """
    print('Creating B matrix')
    start = time.time()
    b = lil_matrix(((len(api_list)),len(api_list)))
    index_dic = defaultdict(int)
    for x,i in enumerate(api_list):
        index_dic[i] = x

    for x,api in enumerate(new_strorage_dic.keys()):
       
        if len(new_strorage_dic[api]) != 0:
            for api_2 in new_strorage_dic[api]:

                index_1 = index_dic[api]
                index_2 = index_dic[api_2]
                b[index_1, index_2] = 1
                b[index_2, index_1] = 1
    b = csr_matrix(b)
    end = time.time()
    print('time taken to create B matrix = '+ str(end - start))
    return b

def create_p_matrix(library_dic, api_list):
    """
    Creates a matrix of size MxM where M is the list unique API's
    
    Parameters
    ---------
    api_list : list
        List of all unique API's
    library_dic : dictionary
        Packages as keys and values as all API's sharing the same code 
        
    Returns
    -------
    P matrix : Crs matrix
        P matrix encoding api to api relation
    
    """
    print('Creating P matrix')
    start = time.time()
    p = lil_matrix(((len(api_list)),len(api_list)))
    index_dic = defaultdict(int)
    for x,i in enumerate(api_list):
        index_dic[i] = x
    library_list = [re.findall('\S+;->', i)[0][:-3] for i in api_list ]
    for x,lib in enumerate(library_list):
        api_list_new = library_dic[lib]
        for api_2 in api_list_new:
            index_2 = index_dic[api_2]
            p[x, index_2] = 1
            p[index_2, x] = 1
    p = csr_matrix(p)
    end = time.time()
    print('time taken to create P matrix = '+ str(end - start))
    return p



def create_a_matrix_test(app_list_test,api_list, final_dic_test):
    """
    Creates a matrix of size MxM where M is the list unique API's
    
    Parameters
    ---------
    app_list_test : list
        List of all apps in the test set 
    api_list : List
        List of all unique API's in the training set
        
    Returns
    -------
    A_test matrix : Crs matrix
        A matrix encoding test apps to training API's
    """
    
    a = lil_matrix((len(app_list_test),len(api_list)))
    for x,i in enumerate(app_list_test):
       
        api_name = set([api for api in final_dic_test[i]])
        for count,l in enumerate(api_list):
            if l in api_name:
                a[x, count] = 1
    return csr_matrix(a)


def save_features(a,b,p,outpath):
    """
    Creates a matrix of size MxM where M is the list unique API's
    
    Parameters
    ---------
    a : Crs matrix
        A matrix 
    b : Crs matrix
        b matrix
    p : Crs matrix
        p matrix
    outpath: str
        Directory where all the matrices are saved
    Returns
    -------
    Saves all matrices to the matrix directory 
    """
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
        
    if not os.path.isdir(outpath + '/matrix'):
        direc = outpath + '/matrix'
        os.mkdir(direc)
    path1 = outpath + '/matrix/' + 'a_matrix'
    path2 = outpath + '/matrix/' + 'b_matrix'
    path3 = outpath + '/matrix/' + 'p_matrix'
    
    save_npz(path1, a)
    save_npz(path2, b)
    save_npz(path3, p)
    
def build_feat(app_list,api_list,final_dic,new_strorage_dic,library_dic,name_list):
    """
    Main method for all 3 processes and saving the structures
    """
    a = create_a_matrix(app_list,api_list,final_dic)
    b = create_b_matrix(new_strorage_dic,api_list)
    p = create_p_matrix(library_dic, api_list)
    save_features(a,b,p,name_list)
    return a,b,p
    
    

