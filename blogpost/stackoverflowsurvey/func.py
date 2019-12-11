import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython import display
from collections import defaultdict
import seaborn as sns

df_2018 = pd.read_csv('data/2018/survey_results_public.csv',low_memory=False);
schema_2018 =pd.read_csv('data/2018/survey_results_schema.csv');

def load_data(file):
    """
    This Function loads the data file and converts file into pandas DataFrame.
    INPUT:
        file - the data file which needs to be converted into dataframe
    OUTPUT:
        df - Pandas Dataframe created from the input data file
    """
    # Load file into a dataframe
    df = pd.read_csv(file,low_memory=False)
    
    return df

def num_cat_vars(df):
    """
    This Function takes a dataframe and returns numerical and categorical columns.
    INPUT:
        df - the dataframe with numerical and categorical variables
    OUTPUT:
        num_vars - numerical columns of the dataframe
        cat_vars - categorical columns of the dataframe
    """
    # select all numerical variables of the dataframe
    num_vars = df.select_dtypes(include=['float','int'])
    # select all categorical variables of the dataframe
    cat_vars = df.select_dtypes(include=['object'])
    return num_vars,cat_vars

def status_values_plot(df,col,title=None,plot=False):
    """
    This Function calculates the different values and their counts of a dataframe's column and plots it using matplotlib.
    INPUT:
        df - the dataframe which holds the required column
        col - string - the column name for which status values are required
        title - string - the title of your plot
        plot - bool providing whether or not you want a plot back
    OUTPUT:
        status_vals - returns the series with status values and their counts
    """
    status_vals = df[col].value_counts()
    if plot:
        (status_vals/df.shape[0]).plot(kind="bar")
        plt.title(title);
    return status_vals.reset_index()

def get_description(col,schema=schema_2018):
    """
    This Function returns the question from schema dataframe given a variable.
    INPUT:
        col -  string - the name of the column you would like to know about
        schema - pandas dataframe with the schema of the developers survey
    OUTPUT:
        desc - string - the description of the column 
    """
    desc =  list(schema[schema['Column']==col]['QuestionText'])[0]
    return desc

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

def piechart(df,col):
    """
    This function displays a piechart of the given dataframe column
    INPUT 
        df - a dataframe holding the required column for piechart
        col - string - the column name which needs to a piechart
        
    OUTPUT
        Displays a piechart of pretty things related to the required column.
    """
    data = df[col].value_counts()
    explodes = [0 for i in range(len(data))]
    explodes[0] = 0.1
    explode=tuple(explodes)
    plt.pie(data,labels=data.keys(),explode=explode,
           shadow=True,startangle=0,autopct='%1.1f%%');
    plt.axis('equal');
    #plt.tight_layout();
    plt.show()

