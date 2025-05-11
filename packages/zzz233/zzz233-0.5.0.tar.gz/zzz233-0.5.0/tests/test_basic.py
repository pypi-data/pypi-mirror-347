import numpy as np

import zzz233

def test_to_pickle_from_pickle():
    a = 233
    b = 0.233
    zzz233.to_pickle(a=a, b=b)
    assert zzz233.from_pickle('a')==a
    assert zzz233.from_pickle('b')==b


def test_to_hdf5_wrapper():
    np_rng = np.random.default_rng()
    np0 = np_rng.uniform(-1, 1, size=(3,4))

    to_hdf5 = zzz233.to_hdf5_wrapper()
    from_hdf5 = zzz233.from_hdf5_wrapper()
    to_hdf5(np0=np0)
    assert 'np0' in from_hdf5()
    tmp0 = from_hdf5('np0')
    assert np.allclose(tmp0, np0)


def test_version():
    assert hasattr(zzz233, '__version__')
    assert hasattr(zzz233, '__version_tuple__')


def test_load_package_data():
    assert zzz233.load_package_data()=='this is the test data'


def test_rand_str_custom_key():
    result = zzz233.rand_str(key='Aa')
    assert 8 <= len(result) <= 12
    assert all(c.isupper() or c.islower() for c in result)
    assert not any(c.isdigit() for c in result)
    assert not any(c in '!#$%@+-~' for c in result)

def test_rand_str_length():
    result = zzz233.rand_str(len_=(5, 5))
    assert len(result) == 5
