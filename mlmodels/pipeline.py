# -*- coding: utf-8 -*-
"""
Pipeline :


https://www.neuraxio.com/en/blog/neuraxle/2019/10/26/neat-machine-learning-pipelines.html
https://github.com/Neuraxio/Neuraxle


>>> from sklearn.compose import ColumnTransformer
>>> from sklearn.feature_extraction.text import CountVectorizer
>>> from sklearn.preprocessing import OneHotEncoder
>>> column_trans = ColumnTransformer(
...     [('city_category', OneHotEncoder(dtype='int'),['city']),
...      ('title_bow', CountVectorizer(), 'title')],
...     remainder='drop')

>>> column_trans.fit(X)
ColumnTransformer(transformers=[('city_category', OneHotEncoder(dtype='int'),
                                 ['city']),
                                ('title_bow', CountVectorizer(), 'title')])

>>> column_trans.get_feature_names()
['city_category__x0_London', 'city_category__x0_Paris', 'city_category__x0_Sallisaw',
'title_bow__bow', 'title_bow__feast', 'title_bow__grapes', 'title_bow__his',
'title_bow__how', 'title_bow__last', 'title_bow__learned', 'title_bow__moveable',
'title_bow__of', 'title_bow__the', 'title_bow__trick', 'title_bow__watson',
'title_bow__wrath']


"""

import os
import json
from pathlib import Path
import pandas as pd
import numpy as np




from sklearn.decomposition import TruncatedSVD




####################################################################################################
# Helper functions
def os_package_root_path(filepath, sublevel=0, path_add=""):
    """
       get the module package root folder
    """
    from pathlib import Path
    path = Path(os.path.realpath(filepath)).parent
    for i in range(1, sublevel + 1):
        path = path.parent

    path = os.path.join(path.absolute(), path_add)
    return path


def log(*s, n=0, m=1):
    sspace = "#" * n
    sjump = "\n" * m
    print(sjump, sspace, s, sspace, flush=True)



####################################################################################################
def pd_na_values(df, cols=None, default=0.0) :
  cols = cols if cols is not None else list(df.columns)
  for t in cols :
    df[t] = df[t.fillna(default)]

  return df



def pd_concat(df1, df2, colid1) :
  df3 = df1.join( df2.set_index(colid), on=colid, how="left")
  return df3



###################################################################################################
def pipe_split(in_pars, out_pars, compute_pars, **kw) :
    df = pd.read_csv(in_pars['in_path'])
    colid = in_pars['colid']
    path = out_pars['out_path']
    file_list = []
    for colname, cols in in_pars['col_group'].items() :
       dfi =  df[ [colid] + cols ].set_index(colid)
       os.makedirs(   f"{path}/{colname}/", exist_ok=True )
       fname = f'{path}/{colname}/df_{colname}.pkl' 
       dfi.to_pickle( fname)
       log(colname, fname, cols )
       file_list.append( fname )
    return file_list


def pipe_merge(in_pars, out_pars, compute_pars, **kw) :
    for filename in in_pars['file_list'] :
      log(filename)
      dfi = pd.read_pickle(filename)
      dfall = df if dfall is None else pd_concat(dfall, dfi, in_pars['colid'])

    dfall.to_pickle( out_pars['out_path'])
    return dfall



def pipe_load(in_pars) :
    df = pd.read_csv(in_pars['in_path'])
    return df


def pipeline_run( pipe_list, in_pars, out_pars, compute_pars, **kw) :
    """
    :param pipe_list:
    :return:
    """

    dfin = pipe_load(in_pars)
    for (pname, pexec, args) in pipe_list :
        try :
          log(pname, pexec, out_pars['out_path']+  "/{pname}/dfout.pkl" )
          os.makedirs( out_pars['out_path']+  "/{pname}/" )
          dfout = pexec(dfin, **args)
          dfout.to_pickle( out_pars['out_path'] +  "/{pname}/dfout.pkl"  )
          dfin = dfout
        except Exception as e :
          log(pname, e)

    return dfout

"""

pipe_split(in_pars, out_pars, compute_pars, **kw) 

pipeline_run( pipe_list, in_pars={ df_colcat }, out_pars, compute_pars, **kw) 




"""


def test(data_path="/dataset/", pars_choice="json"):
    ### Local test
    root = os_package_root_path(__file__,0)

    log("#### Loading params   ##############################################")
    in_pars  = { "in_path"  :  f"{root}/{data_path}/movielens_sample.txt" ,
                "colid"     :  "user_id",
                "col_group" : { "colnum" :  [   "rating"]   ,
                                "colcat" :  [ "genres", "age", "zip"]     }



     }
    out_pars = { "out_path" :  f"{os.getcwd()}/ztest/pipeline_01/",

              }

    compute_pars = { "cpu" : True }


    def TruncatedSVD_fun(df, n_components) :
       svd = TruncatedSVD(n_components=n_components, n_iter=7, random_state=42)
       return svd.fit_transform(df.values)    


    
    file_list = pipe_split(in_pars, out_pars, compute_pars) 


    in_pars['in_path'] = file_list[0]
    pipe_list = [  ("01_NA_values", pd_na_values, { "default": 0.0 }    ),
                   ("02_SVD",       TruncatedSVD_fun, { "n_components": 5 }    ),
                ]


    pipeline_run( pipe_list, in_pars, out_pars, compute_pars) 


    log("#### Loading dataset   #############################################")


    log("#### Model init, fit   #############################################")


    log("#### save the trained model  #######################################")
    # save(model, data_pars["modelpath"])


    log("#### Predict   ####################################################")


    log("#### metrics   ####################################################")


    log("#### Plot   #######################################################")

    log("#### Save/Load   ##################################################")
    print(model2)






if __name__ == '__main__':
    VERBOSE = True
    test(pars_choice="json")