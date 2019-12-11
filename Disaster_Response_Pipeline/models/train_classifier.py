# import libraries
import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import re
import pickle
import warnings

import nltk
nltk.download(['punkt','wordnet','stopwords'])
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin

def load_data(database_filepath):
    """
    This function takes database filepath, loads the file as dataframe
    and splits it into feature matrix (X)and target vector (y)
    INPUT:
    database_filepath - path to the file in the database
    OUTPUT:
    X - Feature matrix
    y - Target vector
    label - column names (36 categories)
    """
    # load data from database
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('message_category', con=engine)
    
    # split dataframe into features and target 
    X = df['message'].values
    Y = df[df.columns[4:]].values
    label = df.columns[4:]
    
    return X,Y,label


def tokenize(text):
    """
    This function takes a text as input, normalizes case, removes whitespace, tokenizes word, removes stop words and lemmatizes it.
    INPUT:
    text - string of text to be cleaned
    OUTPUT:
    text - cleaned text
    """
    # normalize case and clean text
    text = re.sub(r"[^a-zA-Z0-9]"," ",text.lower()).strip()
    
    # create tokens
    tokens = word_tokenize(text)
    
    # remove stopwords and lemmatize
    lemmed = [WordNetLemmatizer().lemmatize(word) for word in tokens if word not in stopwords.words('english')]
    
    return lemmed

def text_length_extractor(arr):
    """
    This function returns len of the text in an array
    INPUT:
    data - list of text
    OUTPUT:
    array of lens
    """
    return np.array([len(text) for text in arr]).reshape(-1,1)

def build_model():
    """
    This function builds a model by creating pipeline and using Gridsearchcv
    INPUT:
    None
    OUPUT:
    prints evaluation metrics
    """
    # Build pipeline
    pipeline = Pipeline([
    ('features',FeatureUnion([
        ('nlp_pipeline',Pipeline([
            ('vect',CountVectorizer(tokenizer=tokenize)),
            ('tfidf',TfidfTransformer())
        ])),
        ('txt_len',FunctionTransformer(text_length_extractor, validate=False))
    ])),
    ('clf',MultiOutputClassifier(RandomForestClassifier()))
    
])
    # gridsearch to find better parameters
    parameters = {
    'features__nlp_pipeline__vect__ngram_range':[(1,2)],
    'clf__estimator__n_estimators':[10,20],
    'clf__estimator__min_samples_split':[3,5]
}
    # create model
    model = GridSearchCV(pipeline,parameters)
    
    return model

def evaluate_model(model, X_test, Y_test, category_names):
    """
    This function takes a model and evaluates its performance based on precision, recall and f1-score on test set
    INPUT:
    model - model to be evaluated
    X_test - test matrix
    Y_test - test vector
    category_names - labels of categories or output labels
    OUTPUT:
    print the classification report on test set
    """
    # make prediction on test set
    Y_pred = model.predict(X_test)
    
    # print evaluation metrics 
    print(classification_report(Y_test,Y_pred,target_names=category_names))

def save_model(model, model_filepath):
    """
    This function takes a model, pickle it and save to model_filepath
    INPUT:
    model - model to be saved
    model_filepath - path where pickled model is to be saved
    """
    # pickle model to the path
    pickle.dump(model,open(model_filepath,'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()