import pandas as pd
import numpy as np
import math
import json
from collections import defaultdict
import matplotlib.pyplot as plt
#% matplotlib inline


def unique_vals(df,col):
    """
    This Function returns unique values in a column.
    INPUT:
        df - dataframe holding the column to look for unique values
        col - string - the column name for which unique values are required
    OUTPUT:
        uval - a list of unique values in the column 
    """
    uval = list()
    df = df[col].dropna().unique()
    for st in df.astype(str):
        val = st.split(';')
        for item in val:
            if item not in uval:
                uval.append(item)
    return uval

def total_count(df, col1, col2, look_for):
    """
    This Function calculates the total count of individual items in a dataframe column
    INPUT:
    df - the pandas dataframe you want to search
    col1 - the column name you want to look through
    col2 - the column you want to count values from
    look_for - a list of strings you want to search for in each row of df[col]
    OUTPUT:
    new_df - a dataframe of each look_for with the count of how often it shows up
    """
    new_df = defaultdict(int)
    #loop through list of ed types
    for val in look_for:
        #loop through rows
        for idx in range(df.shape[0]):
            #if the ed type is in the row add 1
            if val in df[col1][idx]:
                new_df[val] += int(df[col2][idx])
    new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
    new_df.columns = [col1,col2]
    new_df.sort_values('count',ascending=False,inplace=True)
    return new_df


def clean_and_plot(df,col,possible_vals,title='Method of Educating Suggested',plot=True):
    """
    This Functions cleans and plots bar chart of individual values from the provided column
    INPUT 
        df - a dataframe holding the required column
        col - string - the column name which needs to be cleaned
        title - string - the title of your plot
        plot - bool providing whether or not you want a plot back
        
    OUTPUT
        study_df - a dataframe with the count of how many individuals
        Displays a plot of pretty things related to the required column.
    """
    study = df[col].value_counts().reset_index()
    study.rename(columns={'index':col,col:'count'},inplace=True)
    study_df = total_count(study,col,'count',possible_vals)
    
    study_df.set_index(col,inplace=True)
    if plot:
        if 'Database' in col:
            study_df.rename(index={'Microsoft Azure (Tables, CosmosDB, SQL, etc)':'Microsoft Azure'},inplace=True) 
        (study_df/study_df.sum()).plot(kind='bar',legend=None)
        plt.title(title)
        plt.show()
    props_study_df = study_df/study_df.sum()
    return props_study_df