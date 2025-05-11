import os
import random
import pickle
import string
import h5py
import urllib.request
import urllib.error
import numpy as np


def to_pickle_wrapper(fname:str='tbd00.pkl'):
    '''wrapper for to_pickle

    Parameters:
        fname (str): pickle file name

    Returns:
        to_pickle (function): function to save key-value pairs to pickle file
    '''
    def to_pickle(**kwargs):
        '''save kwargs to pickle file

        Parameters:
            kwargs (dict): key-value pairs to be saved, key must be string

        Returns:
            ret (NoneType): None
        '''
        assert all(isinstance(k,str) for k in kwargs.keys()), 'keys must be strings'
        if os.path.exists(fname):
            with open(fname, 'rb') as fid:
                z0 = pickle.load(fid)
            z0.update(**kwargs)
        else:
            z0 = kwargs
        with open(fname, 'wb') as fid:
            pickle.dump(z0, fid)
    return to_pickle


def from_pickle_wrapper(fname:str='tbd00.pkl'):
    '''wrapper for from_pickle

    Parameters:
        fname (str): pickle file name

    Returns:
        from_pickle (function): function to load value from pickle file
    '''
    def from_pickle(key:str|None=None):
        '''load value from pickle file

        Parameters:
            key (str): key to be loaded

        Returns:
            ret (any): value corresponding to key
        '''
        assert os.path.exists(fname), f'file "{fname}" not exist'
        with open(fname, 'rb') as fid:
            tmp0 = pickle.load(fid)
            ret = list(tmp0.keys()) if key is None else tmp0[key]
        return ret
    return from_pickle

to_pickle = to_pickle_wrapper()
from_pickle = from_pickle_wrapper()


def pickle_wrapper(fname:str='tbd00.pkl'):
    to_pickle = to_pickle_wrapper(fname)
    from_pickle = from_pickle_wrapper(fname)
    return to_pickle, from_pickle


def to_hdf5_wrapper(fname:str='tbd00.hdf5'):
    def to_hdf5(**kwargs):
        '''save kwargs to hdf5 file (mainly for share data between python and other languages)

        Parameters:
            kwargs (dict): key-value pairs to be saved, key must be string

        Returns:
            ret (NoneType): None
        '''
        assert all(isinstance(k,str) for k in kwargs.keys()), 'keys must be strings'
        with h5py.File(fname, 'a', libver='latest') as fid:
            for key,value in kwargs.items():
                if key in fid.keys():
                    del fid[key]
                fid.create_dataset(key, data=value)
    return to_hdf5


def from_hdf5_wrapper(fname:str='tbd00.hdf5'):
    def from_hdf5(key:str|None=None):
        '''load value from hdf5 file

        Parameters:
            key (str,None): key to be loaded, if None, return all keys

        Returns:
            ret (any): value corresponding to key
        '''
        assert os.path.exists(fname), f'file "{fname}" not exist'
        with h5py.File(fname, 'r') as fid:
            ret = list(fid.keys()) if key is None else fid[key][()]
        return ret
    return from_hdf5

to_hdf5 = to_hdf5_wrapper()
from_hdf5 = from_hdf5_wrapper()

def to_np(x):
    '''convert tensorflow/torch/cupy array to numpy array

    Parameters:
        x (array): array to be converted, could be tensorflow/torch/cupy/numpy array

    Returns:
        ret (numpy.array): converted array
    '''
    # not a good idea to use isinstance()
    # if use isinstance(), here have to import all of them (tf/torch/cupy)
    tmp0 = str(type(x))[8:-2]
    if tmp0.startswith('tensorflow'):
        ret = x.numpy()
    elif tmp0.startswith('torch'):
        ret = x.detach().to('cpu').numpy()
    elif tmp0.startswith('cupy'):
        ret = x.get()
    else:
        ret = np.asarray(x)
    return ret

def hfe(x, y, eps=1e-5):
    r'''calculate relative error

    $$ f(x,y)=\max \frac{|x-y|}{|x|+|y|+\varepsilon} $$

    Parameters:
        x (numpy.array): array to be compared
        y (numpy.array): array to be compared

    Returns:
        ret (float): relative error
    '''
    x = to_np(x)
    y = to_np(y)
    ret = np.max(np.abs(x-y)/(np.abs(x)+np.abs(y)+eps))
    return ret

# a simple hfe()
# hfe = lambda x,y,eps=1e-3: np.max(np.abs(x-y)/(np.abs(x)+np.abs(y)+eps))


def moving_average(np0, num=3):
    '''calculate moving average

    Parameters:
        np0 (numpy.array): array to be averaged
        num (int): number of elements to be averaged

    Returns:
        ret (numpy.array): averaged array
    '''
    # see https://stackoverflow.com/q/13728392/7290857
    kernel = np.ones(num) / num
    ret = np.convolve(np.asarray(np0), kernel, mode='same')
    return ret


def check_internet_available(timeout=1):
    '''check if internet is available (by trying to connect to google.com)

    Parameters:
        timeout (float): timeout in seconds

    Returns:
        ret (bool): True if internet is available, False otherwise
    '''
    host = 'https://www.google.com' #dnsloopup google.com #172.217.161.142 (20190817)
    try:
        urllib.request.urlopen(host, timeout=timeout)
        return True
    except urllib.error.URLError:
        return False


def script_print_lucky():
    '''print lucky message. This function is available in command line `zzz233`

    Parameters:

    Returns:
        ret (NoneType): None
    '''
    print('[zzz233] I am feelly lucky today!')


def load_package_data(file='data00.txt'):
    path = os.path.join(os.path.dirname(__file__), 'data', file)
    if os.path.exists(path):
        with open(path, 'r') as fid:
            ret = fid.read().strip()
    else:
        print(f'package data file "{file}" not exist')
        ret = None
    return ret

def next_tbd_dir(dir0='tbd00', maximum_int=100000, tag_create:bool=True):
    if not os.path.exists(dir0):
        os.makedirs(dir0)
    tmp1 = [x for x in os.listdir(dir0) if x[:3]=='tbd']
    exist_set = {x[3:] for x in tmp1}
    while True:
        tmp1 = str(random.randint(1,maximum_int))
        if tmp1 not in exist_set:
            break
    tbd_dir = os.path.join(dir0, 'tbd'+tmp1)
    if tag_create:
        os.mkdir(tbd_dir)
    return tbd_dir

def rand_str(key:str='Aa1!', len_:tuple[int,int]=(8,12)):
    '''generate random string

    Parameters:
        key (str): characters to include in the random string.
                   'A' for uppercase, 'a' for lowercase, '1' for digits, '!' for special characters.
        len_ (tuple): range of the length of the generated string.

    Returns:
        ret (str): generated random string
    '''
    a,b = len_
    assert (0<a) and (a<=b)
    len_ = random.randint(a, b)
    key = ''.join(set(key))
    assert set(key)<=set('Aa1!'), 'key must be subset of "Aa1!"'
    assert len(key)>0
    choice = ''
    if 'A' in key:
        choice += string.ascii_uppercase
    if 'a' in key:
        choice += string.ascii_lowercase
    if '1' in key:
        choice += string.digits
    if '!' in key:
        choice += '!#$%@+-~'# part of string.punctuation
    ret = ''.join(random.choices(choice, k=len_))
    return ret

