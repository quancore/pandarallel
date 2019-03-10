import pandarallel

import pandas as pd
import numpy as np
import math

def func_for_dataframe_apply(x):
    return math.sin(x.a**2) + math.sin(x.b**2)

def func_for_series_map(x):
    return math.log10(math.sqrt(math.exp(x**2)))

def func_for_dataframe_groupby_apply(df):
    dum = 0
    for item in df.b:
        dum += math.log10(math.sqrt(math.exp(item**2)))
        
    return dum / len(df.b)

def test_dataframe_apply():
    df_size = int(1e1)
    df = pd.DataFrame(dict(a=np.random.randint(1, 8, df_size),
                        b=np.random.rand(df_size)))

    res = df.apply(func_for_dataframe_apply, axis=1)
    res_parallel = df.parallel_apply(func_for_dataframe_apply, axis=1)
    assert res.equals(res_parallel)

def test_series_map():
    df_size = int(1e1)
    df = pd.DataFrame(dict(a=np.random.rand(df_size) + 1))

    res = df.a.map(func_for_series_map)
    res_parallel = df.a.parallel_map(func_for_series_map)
    assert res.equals(res_parallel)

def test_dataframe_groupby_apply():
    df_size = int(1e1)
    df = pd.DataFrame(dict(a=np.random.randint(1, 8, df_size),
                           b=np.random.rand(df_size)))

    res = df.groupby("a").apply(func_for_dataframe_groupby_apply)
    res_parallel = (df.groupby("a")
                      .parallel_apply(func_for_dataframe_groupby_apply))
    res.equals(res_parallel.squeeze())
