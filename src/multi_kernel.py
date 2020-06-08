from mklaren.kernel.kernel import linear_kernel
try:
    from mklaren.mkl.alignf import Alignf
except:
    from mklaren.mkl.alignf import Alignf
from mklaren.mkl.align import Align

from mklaren.kernel.kinterface import Kinterface
import pandas as pd 


def create_kinterfce(kernel_list, type_k):
    """
    Creates a kinterface of type_k
    
    Parameters
    ----------
    kernel_list : List
        A list of all kernels
    type_k : Tran
        Type of transformation for kernels 
    
    Returns
    --------
    train_array : list
        A list of all training kernels as array 
    kinterface_kernel : Kinterface 
        Kernel of type kinterface
    """
    kinterface_kernel = []
    train_array = []
    for ker in kernel_list:
        arr = ker.toarray()
        train_array.append(arr)
        k_arr = Kinterface(data=arr, kernel=type_k)  
        kinterface_kernel.append(k_arr)
    return train_array, kinterface_kernel

def test_create_kernel(kernel_list):
    """
    Creates the csr matix into an array 
    
    Parameters
    ----------
    kernel_list : List
        A list of all test kernels
   
    Returns
    --------
    array_kernel : List
        All kenrels as arrays 
    """
    array_kernel = []
    for ker in kernel_list:
        array_kernel.append(ker.toarray())
    return array_kernel

def get_wieghts(kernel_list,labels, model_multi):
    """
    Gets weights from each kernel from the multi kernel learning algorithm 
    
    Parameters
    ----------
    kernel_list : List
        A list of all test kernels
    labels : List
        A list containing all lables for each app
    model_multi : str
        Type of multi kernel learning algorithm 
    Returns
    --------
    array_kernel : List
       All weights in a list
    """
    model_multi.fit(kernel_list, labels)
    return model_multi.mu


def multi_kernel(kernel_list, w):
    """
    Creates a multi-kernel by combing all kernels 
    
    Parameters
    ----------
    kernel_list : List
        A list of all test kernels
    w : List
        A list containing all weights
        
    Returns
    --------
    new_kernel : Array
       A multi-kernel
    """
    new_kernel = kernel_list[0]*w[0] + kernel_list[1]*w[1] \
    + kernel_list[2]*w[2] + kernel_list[3]*w[3]
    return new_kernel
    
def create_multi(kernel, benign_paths, app_list):
    """
    Creates Dataframe from the kernal and adds the labels 
    """
    benign_apps  = [i.split('/')[-1] for i in  benign_paths]
    kernel_df = pd.DataFrame(kernel)
    kernel_df['app_name'] = app_list
    kernel_df['type'] = kernel_df.app_name.apply(lambda x: 1 if x in benign_apps else 0)
 
    return kernel_df

def get_scores_multi(train_k, test_k, type_k, k_model,labels, \
                     benign_paths, app_list, app_list_test):
    
    train_array, train_kintreface = create_kinterfce(train_k,type_k)
    test_array  = test_create_kernel(test_k)
    
    w = get_wieghts(train_kintreface,labels, k_model)
    
    train_multi_kernel = multi_kernel(train_array, w)
    test_multi_kernel = multi_kernel(test_array, w)
    
    df_train_multi  = create_multi(train_multi_kernel,benign_paths,app_list )
    df_test_multi  = create_multi(test_multi_kernel,benign_paths,app_list_test )
    
    return df_train_multi, df_test_multi
    





