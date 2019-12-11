import json
import plotly
import pandas as pd
import numpy as np

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Heatmap
from sklearn.externals import joblib
from sqlalchemy import create_engine


app = Flask(__name__)

def tokenize(text):
    """
    This function case normalizes, tokenizes and lemmatizes a text
    
    INPUT
    text - string that needs processing
    OUTPUT
    clean_tokens - list of cleaned tokens
    """
    # create word_tokenizer object
    tokens = word_tokenize(text)
    # create lemmatizer object
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    # loop through tokens
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

def text_length_extractor(arr):
    """
    This function returns len of the each text in an array
    INPUT:
    data - list of text
    OUTPUT:
    array of length
    """
    return np.array([len(text) for text in arr]).reshape(-1,1)

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('message_category', engine)

# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    # Message count by genre
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    # Message count by categories
    cat_counts = df[df.columns[4:]].sum().sort_values()
    cat_counts.sort_values()
    cat_names = list(cat_counts.index)
    
    # Top 10 message categories
    num_vars = df.select_dtypes(include=['int']).columns.drop('id')
    perc_msg_counts = df[num_vars].mean().sort_values(ascending=False).head(10)
    perc_msg_names = list(perc_msg_counts.index)
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [
                Bar(
                    y=cat_names,
                    x=cat_counts,
                    orientation='h'
                )
            ],

            'layout': {
                'title': 'Distribution of Message Categories',
                'yaxis': {
                    'title': "Categories"
                },
                'xaxis': {
                    'title': "Count"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=perc_msg_names,
                    y=perc_msg_counts
                )
            ],

            'layout': {
                'title': 'Top 10 Messages and their percentages',
                'yaxis': {
                    'title': "Counts"
                },
                'xaxis': {
                    'title': "Top Messsages"
                }
            }
        }
        
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()