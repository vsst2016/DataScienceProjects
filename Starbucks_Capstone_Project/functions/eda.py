import pandas as pd
import numpy as np
import math
import json
from collections import defaultdict
import matplotlib.pyplot as plt

def eda_dataframe(df,pos_val):
    eda_df = pd.DataFrame({'Cols':df.columns,'dtypes':df.dtypes,'Null Values':df.isnull().sum(),'Possible Values':pos_val})
    eda_df.index = range(eda_df.shape[0])
    return eda_df