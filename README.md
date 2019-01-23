# Disaster Response Pipeline Project

Udacity project - Create a Data Pipeline to triage messages for delivery to correct disaster response teams 


### Table of Contents

1. [Libraries and Installation](#installation)
2. [Project Description](#motivation)
3. [Files](#files)
4. [Findings](#results)

## Libraries and Installation <a name="installation"></a>

The project uses the Flask web framework, whcih does not require any special installation.

sqlalchemy
pandas

## Project Description<a name="motivation"></a>

This project uses a dataset provided by FigureEight consisting of messages sent during various natural disasters.
The purpose is to perform ETL operations, pipeline clean data to a SQL database, and provide a web dashboard that would be usable by disaster response agencies.

## Files <a name="files"></a>

- app
| - template
| |- master.html  # main page of web app
| |- go.html  # classification result page of web app
|- run.py  # Flask file that runs app

- data
|- disaster_categories.csv  # data to process 
|- disaster_messages.csv  # data to process
|- process_data.py
|- InsertDatabaseName.db   # database to save clean data to

- models
|- train_classifier.py
|- classifier.pkl  # saved model 

## Findings<a name="results"></a>

In progress


## Udacity Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
