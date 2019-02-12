
from os import environ
#from disaster_response import app

### Flask Application Imports
from datetime import datetime
from flask import render_template
from flask import request, jsonify
import json
from flask import Response
from datetime import timedelta  
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
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
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
from sklearn.ensemble import AdaBoostClassifier

from sklearn.externals import joblib
import numpy as np
import math
import matplotlib.pyplot as plt
#import train_classifier
#from train_classifier import tokenize

## sqlite3
import sqlite3
from sqlite3 import Error
import sqlalchemy
from sqlalchemy import create_engine

##for files
import os
from shutil import copyfile

#app = Flask(__name__)
app = Flask('disaster_response')

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def tokenize(text):
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
    
# load data
engine = create_engine('sqlite:///../data/InsertDatabaseName.db')
df = pd.read_sql_table('InsertTableName', engine)

# load model
model = joblib.load("../models/model.pkl")



def classify(msg_text):
    '''
        classify(msg_text)
        in: some message text
        out: array of {class: __, value: __}
    '''

    res = model.predict([msg_text])

    return_array = []

    for index, val in enumerate(res[0]):
        #print(category_labels[index] + ":" + str(val))
        row_dict = {}
        row_dict['class'] = category_labels[index]
        row_dict['value'] = val

        #add to the current message counts
        for row in curr_messages_class:
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
    lab_row['count'] = category_counts[label]
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




'''
Routes to render HTML templates
'''
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Disaster Response',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


'''
REST API routes
'''

'''
    /classifier route    

'''
@app.route('/classifier', methods=['GET'])
def classifier():
    query_parameters = request.args

    msg_text = query_parameters.get('msg_text')
    genre = query_parameters.get('msg_genre')

    #track the counts of genres received during the current event
    for row in curr_messages_genre:
        if row['genre'] == genre:
            row['count'] = row['count'] + 1

    resp = classify(msg_text)
    
    return jsonify(resp)


'''
    /msg_by_genre route    
    Returns the training set by genre
'''
@app.route('/msg_by_genre', methods=['GET'])
def msg_by_genre():

    return jsonify(all_messages_genre)

'''
    /msg_by_class route   
    Returns the training set by class
'''
@app.route('/msg_by_class', methods=['GET'])
def msg_by_class():
    
    return jsonify(all_messages_class)

'''
    /curr_msgs_genre route
    returns counts of message genres for the current disaster event
'''
@app.route('/curr_msgs_genre', methods=['GET'])
def curr_msgs_genre():
  
    return jsonify(curr_messages_genre)

'''
    /curr_msgs_class route
    returns counts of message classes for the current disaster event
'''
@app.route('/curr_msgs_class', methods=['GET'])
def curr_msgs_class():
    
    return jsonify(curr_messages_class)


def main():
    app.run(host='0.0.0.0', port=5555, debug=True)


if __name__ == '__main__':
    main()