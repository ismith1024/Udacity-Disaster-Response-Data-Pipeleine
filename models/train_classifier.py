'''
Library imports
'''
import sys
import pandas as pd
from sqlalchemy import create_engine
import pickle

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

'''
Loads a SQLite database into a dataframe
In: database_filepath -- file path to the database
Returns: X, Y, category names
'''
def load_data(database_filepath = 'sqlite:///InsertDatabaseName.db'):

    engine = create_engine(database_filepath)
    df = pd.read_sql_table(table_name = 'InsertTableName', con=engine)

    X = df.message
    Y = df[['related', 'request', 'offer', 'aid_related', 'medical_help', 'medical_products', 'search_and_rescue',
        'security', 'military', 'chbest_estimator_ ild_alone', 'water', 'food', 'shelter', 'clothing', 'money', 'missing_people',
        'refugees', 'death', 'other_aid', 'infrastructure_related', 'transport', 'buildings', 'electricity',
        'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods',
        'storm', 'fire', 'earthquake', 'cold', 'other_weather', 'direct_report', ]]
    category_names = []

    for i in df:
        category_names.append(i)

    return X, Y, category_names

'''
Tokenizes a string of text
Replaces urls with a placeholder
Tokenizes on words
Converts to lower, lemmatizes, and strips
Returns a list collection of clean tokens
'''
def tokenize(text):
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

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

'''
Builds a ML pipeline
Returns the pipeline

'''
def build_model():
    rf = RandomForestClassifier()

    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer = tokenize)),
        ('tfidf', TfidfTransformer()),
            ('clf', MultiOutputClassifier(estimator = rf)),#('clf', OneVsRestClassifier(MultiOutputClassifier(estimator = rf))),
    ])

    return pipeline

'''
Evaluates the ML pipeline
Prints the Accuracy, Precision, and Recall metrics for each class

'''
def evaluate_model(model, X_test, Y_test, category_names):
    # evaluate all steps on test set
    y_pred = pipeline.predict(X_test)

    for col in range(y_pred.shape[1]):
        print("Class: " + str(col))
        print(classification_report(y_test.iloc[:, col], y_pred[:, col])


def save_model(model, model_filepath = 'model.pkl'):
    pkl_outfile = open(model_filepath,'wb')
    pickle.dump(model, pkl_outfile)
    pkl_outfile.close()


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        # perform train test split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        # train classifier
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