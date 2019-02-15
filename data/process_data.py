import sys
import pandas as pd
from sqlalchemy import create_engine
from sklearn.externals import joblib


def load_data(messages_filepath, categories_filepath):
    '''
    load_data
    In:
        messages_filepath: file path to the messages csv file
        categories_filepath: file path to the categories csv file
    Out: 
        df: the dataframe with the comboned data from the csv files

    '''

    #load datasets
    messages = pd.read_csv(messages_filepath, dtype = str)
    categories = pd.read_csv(categories_filepath, dtype = str)
    
    #merge datasets
    df = messages.set_index('id').join(categories.set_index('id'))
    
    return df


def clean_data(df):
    '''
    clean_data
    InOut:
        df: the dataframe to be operated on

    Applies the correct formatting to the column names
    Converts numeric values in the columns to binary
    Drops duplicate rows
    '''

    #clean up the category names 
    categories = df['categories'].str.split(";", expand=True )
    #split off the last two characters of the values
    row = categories.iloc[0]
    category_colnames = row.apply(lambda x: x[:-2])
    
    # rename the columns of `categories`
    categories.columns = category_colnames

    #convert category data to numberic 0 or 1
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1:])
        
        # convert column from string to numeric
        categories[column] = categories[column].apply(lambda x: int(x))
        
        #convert to binary
        categories[column] = categories[column].apply(lambda x: 0 if x == 0 else 1)
        
    # drop the original categories column from `df`
    df = df.drop('categories', axis=1)

    # concatenate the original dataframe with the new `categories` dataframe
    df =  pd.concat([df, categories], axis=1)
    df['related'] = df['related'].apply(lambda x: 0 if x == 0 else 1)
    
    # drop duplicates
    df.drop_duplicates(keep='first', inplace=True)

    return df

def save_data(df, database_filename):
    '''
    save_data
    
    In:
        df: dataframe to save
        database_filename: file path to the SQLite database file to write to
    Out:
        writes to the SQLite database table 'InsertTableName'

    Writes the data in the dataframe to the SQLite database as indicated
    '''
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('message_data', engine, index=False)


def main():
    '''
    main()

    In:
        Three parameters:
            - filepath to messages csv file
            - filepath to categories csv file
            - filepath to SQLite database file

    Out: Console output to inform the user of progress

    Reads the csv files into a dataframe
    Cleans the data
    Writes the clean data to the SQLite database    
    '''
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