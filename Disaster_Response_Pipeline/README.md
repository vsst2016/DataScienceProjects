# Disaster Response Pipeline Project

### Background:

This is a text classification project for real messages that were sent during disaster events. We have used disaster data from Figure Eight to build a model for an API that classifies these disaster messages into 36 different categories. We created a ETL pipeline and a machine learning pipeline to categorize these events so that the messages can be sent to an appropriate disaster relief agency.

This project includes a web app where an emergency worker can input a new message and get classification results in several categories.

#### ETL Pipeline:
for etl pipeline we have script process.py. This scripts first merges messages and categories datasets, then splits the values in categories column into separate category columns. It renames all the 36 category columns and converts their values to binary. Then drops categories column, removes duplicates and saves the clean dataset into a sqlite database.

#### ML Pipeline:
This is written in classifier.py file. It initially reads data from sqlite database, does text processing and builds a machine learning pipeline. Fits the pipeline on train set and tests on test dataset. Then improves the model, test and exports as pickle file

### Instructions:

1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

<p align="center">
  <img src="images/intro.png" width="650" title="">
</p>
<p align="center">
  <img src="images/dist_msg_cat.png" width="650" title="">
</p>
<p align="center">
  <img src="images/top10_msg.png" width="650" title="">
</p>
<p align="center">
  <img src="images/classify.png" width="650" title="">
</p>
