# import libraries
import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    This Function loads and merges datasets and return a dataframe
    INPUT: 
    messages_filepath: path for the messages.csv file
    categories_filepath: path for the categories.csv file
    OUTPUT: 
    Dataframe created by merging messages and categories file
    """
    # load messages dataset
    messages = pd.read_csv(messages_filepath)
    
    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    
    # merge datasets and drop original and genre columns
    df = messages.merge(categories,on='id')
    
    return df

def clean_data(df):
    """
    This function takes a dataframe, splits categories column on its        values to become separate column and converts them into binary.
    INPUT:
        Dataframe containing messages and categories
    OUTPUT:
        Cleaned dataframe
    """
    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(';',expand=True)

    # select the first row of the categories dataframe
    row = categories.iloc[0]
    
    # use this row to extract a list of new column names for            categories.
    # one way is to apply a lambda function that takes everything 
    # up to the second to last character of each string with slicing
    category_colnames = row.apply(lambda x: x[:-2]).values
    
    # rename the columns of `categories`
    categories.columns = category_colnames
    
    # convert categroy values to binary (0 or 1)
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
    
        # convert column from string to numeric
        categories[column] = pd.to_numeric(categories[column])
        categories[column] = categories[column].apply(lambda x: 1 if x > 1 else x)
    
    # drop the original categories column from `df`
    df.drop('categories',axis=1,inplace=True)   
    
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df,categories],axis=1)  
    
    # drop duplicates
    df.drop_duplicates(inplace=True)
    
    return df
    
def save_data(df, database_filename):
    """
    This function takes a dataframe and loads it to a SQLite Database
    with the provided database name
    INPUT:
    df - dataframe to be loaded into SQLite database
    database_filename - string of the filename for saving df
    """
    #save the clean dataset into an sqlite database
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('message_category', engine, index=False, if_exists='replace')

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()