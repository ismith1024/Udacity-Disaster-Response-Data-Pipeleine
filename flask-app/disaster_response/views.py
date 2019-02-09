"""
Routes and views for the flask application.
"""

### Flask Application Imports
from datetime import datetime
from flask import render_template
from disaster_response import app

### Data Science Imports
import pandas as pd


## Flask Server
from datetime import datetime
from flask import request, jsonify
import json
from flask import Response
from datetime import timedelta  
from flask import Flask, make_response, request, current_app  
from functools import update_wrapper


## Data science 
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

## sqlite3
import sqlite3
from sqlite3 import Error

## sqlite3
import sqlite3
from sqlite3 import Error

##for files
import os
from flask import Flask, flash, request, redirect, url_for
from shutil import copyfile


'''
SERVER SETUP

'''
print("Starting server on port 5555")

#the messages that have been received and classified from the current disaster event
curr_messages_genre = []
msg_row = {}
msg_row['genre'] = 'direct'
msg_row['count'] = 3
curr_messages_genre.append(msg_row)
msg_row = {}
msg_row['genre'] = 'news'
msg_row['count'] = 12
curr_messages_genre.append(msg_row)
msg_row = {}
msg_row['genre'] = 'social'
msg_row['count'] = 9
curr_messages_genre.append(msg_row)

curr_messages_class = []
msg_row = {}
msg_row['class'] = 'medical_help'
msg_row['count'] = 7
curr_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'storm'
msg_row['count'] = 11
curr_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'other_aid'
msg_row['count'] = 4
curr_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'tools'
msg_row['count'] = 5
curr_messages_class.append(msg_row)

all_messages_genre = []
msg_row = {}
msg_row['genre'] = 'direct'
msg_row['count'] = 23
all_messages_genre.append(msg_row)
msg_row = {}
msg_row['genre'] = 'news'
msg_row['count'] = 42
all_messages_genre.append(msg_row)
msg_row = {}
msg_row['genre'] = 'social'
msg_row['count'] = 9
all_messages_genre.append(msg_row)

all_messages_class = []
msg_row = {}
msg_row['class'] = 'medical_help'
msg_row['count'] = 17
all_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'storm'
msg_row['count'] = 51
all_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'other_aid'
msg_row['count'] = 24
all_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'tools'
msg_row['count'] = 65
all_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'earthquake'
msg_row['count'] = 6
all_messages_class.append(msg_row)
msg_row = {}
msg_row['class'] = 'floods'
msg_row['count'] = 33
all_messages_class.append(msg_row)


def classify(msg_text):
    '''
        classify(msg_text)
        in: some message text
        out: array of {class: __, value: __}
    '''
    return_array = []
    return_dict = {}
    return_dict['msg_class'] = 'some class'
    return_dict['prob'] = 0.75
    return_array.append(return_dict)
    return_dict = {}
    return_dict['msg_class'] = 'some other class'
    return_dict['prob'] = 0.15
    return_array.append(return_dict)
    return_dict = {}
    return_dict['msg_class'] = 'yet another class'
    return_dict['prob'] = 0.1
    return_array.append(return_dict)  

    print(return_array)

    return return_array

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
A simple REST API for the application
'''

'''
    /classifier route    

'''
@app.route('/classifier', methods=['GET'])
def classifier():
    query_parameters = request.args

    msg_text = query_parameters.get('msg_text')

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