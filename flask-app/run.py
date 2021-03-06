
from os import environ
#from disaster_response import app

### Flask Application Imports
from datetime import datetime
from flask import render_template
from flask import request, jsonify
import json
from flask import Response
from flask import Flask, make_response, request, current_app  
from functools import update_wrapper
from flask import Flask, flash, request, redirect, url_for


### Data Science Imports
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
import math
import matplotlib.pyplot as plt
from sklearn.externals import joblib

## sqlite3
import sqlite3
from sqlite3 import Error
import sqlalchemy
from sqlalchemy import create_engine

#app = Flask(__name__)
app = Flask('disaster_response')

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# load data
engine = create_engine('sqlite:///../data/disaster_data.db')
df = pd.read_sql_table('message_data', engine)




def tokenize(text):
    '''
    In:
        url_regex: regex to find and replace URLs
        text: raw text to be tokenized
    Out: 
        clean_tokens: a list containing the tokens

    Replaces URLs with a placeholder
    Word-tokenizes the text
    Lemmatizes the tokens
    Strips and converts tokens to lower case
    '''
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load model
model = joblib.load("model.pkl")
    
def classify(msg_text):
    '''
        classify(msg_text)
        in: 
            msg_text: free message text
        out: 
            return_array: array of {class: __, value: __}

        Predicts the class(es) assiciated to a message
        Provides the results
    '''
    #Tokenize and clean the text
    #msg_tokens = tokenize(msg_text)

    res = model.predict([msg_text])#msg_tokens)

    return_array = []

    print("Classification results:")
    for index, val in enumerate(res[0]):
        #print(category_labels[index] + ":" + str(val))
        row_dict = {}
        row_dict['class'] = category_labels[index]
        row_dict['value'] = int(val)
        return_array.append(row_dict)

        #add to the current message counts

        '''
        curr_messages_class = []
        for label in category_labels:
            msg_row = {}
            msg_row['class'] = label
            msg_row['count'] = 0
        '''

        for row in curr_messages_class:
            #print(category_labels[index] + " : " + str(val))
            if row['class'] == category_labels[index] and val > 0:
                row['count'] = row['count'] + 1
        
    return return_array


#obtain metrics from training data
genre_counts = df['genre'].value_counts().to_dict()
category_labels = ['related', 'request', 'offer', 'aid_related', 'medical_help', 'medical_products', 'search_and_rescue', 'security',
    'military', 'child_alone', 'water', 'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid',
    'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure',
    'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']
category_counts = {}
for label in category_labels:
    category_counts[label] = df[label].sum()

#create array of rows for JSON purposes
all_messages_class = []
for label in category_counts:
    lab_row = {}
    lab_row['class'] = label
    lab_row['count'] = int(category_counts[label])
    all_messages_class.append(lab_row)

all_messages_genre = []
for genre in genre_counts:
    lab_row = {}
    lab_row['genre'] = genre
    lab_row['count'] = int(genre_counts[genre])
    all_messages_genre.append(lab_row)

# load model
#model = joblib.load("../models/model.pkl")

print("Starting server on port 5555")

#the messages that have been received and classified from the current disaster event
curr_messages_genre = []
msg_row = {}
msg_row['genre'] = 'direct'
msg_row['count'] = 0
curr_messages_genre.append(msg_row)
msg_row = {}
msg_row['genre'] = 'news'
msg_row['count'] = 0
curr_messages_genre.append(msg_row)
msg_row = {}
msg_row['genre'] = 'social'
msg_row['count'] = 0
curr_messages_genre.append(msg_row)

curr_messages_class = []
for label in category_labels:
    msg_row = {}
    msg_row['class'] = label
    msg_row['count'] = 0
    curr_messages_class.append(msg_row)

'''
Routes to render HTML templates
'''

@app.route('/')
@app.route('/home')
def home():
    '''
    Renders the home page.
    '''
    return render_template(
        'index.html',
        title='Disaster Response',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    '''
    Renders the contact page.
    Created by the Flask template project, keeping it for now
    '''
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    '''
    Renders the about page.
    Created by the Flask template project, keeping it for now
    '''
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


'''
REST API routes
'''

@app.route('/classifier', methods=['GET'])
def classifier():
    '''
    /classifier route    
    In:
        HTTP GET request
    Out:
        A JSON string with the classification results in [['class': ___, 'value': ___], ...] format

        Handles a classification request
        Adds the results to the current event genre and class counts
        Returns the classification result as a JSON string
    '''
    query_parameters = request.args

    msg_text = query_parameters.get('msg_text')
    genre = query_parameters.get('msg_genre')

    #track the counts of genres received during the current event
    for row in curr_messages_genre:
        if row['genre'] == genre:
            row['count'] = row['count'] + 1

    resp = classify(msg_text)
    
    return jsonify(resp)


@app.route('/msg_by_genre', methods=['GET'])
def msg_by_genre():
    '''
    /msg_by_genre route    
    In:
        HTTP GET request
    Out:
        JSON string with counts of the training set by genre
    '''
    return jsonify(all_messages_genre)


@app.route('/msg_by_class', methods=['GET'])
def msg_by_class():
    '''
    /msg_by_class route    
    In:
        HTTP GET request
    Out:
        JSON string with counts of the training set by class
    '''
    return jsonify(all_messages_class)

@app.route('/curr_msgs_genre', methods=['GET'])
def curr_msgs_genre():
    '''
    /curr_msgs_genre route    
    In:
        HTTP GET request
    Out:
        JSON string with counts of the current messages by genre
    '''
    return jsonify(curr_messages_genre)

@app.route('/curr_msgs_class', methods=['GET'])
def curr_msgs_class():
    '''
    /curr_msgs_class route    
    In:
        HTTP GET request
    Out:
        JSON string with counts of the current messages by class
    '''
    return jsonify(curr_messages_class)


def main():
    '''
    Runs the app on localhost:5555
    '''
    app.run(host='0.0.0.0', port=5555, debug=True)


if __name__ == '__main__':
    main()