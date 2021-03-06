"""
Routes and views for the flask application.
"""




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

'''
SERVER SETUP

'''
# load data
engine = create_engine('sqlite:///../data/InsertDatabaseName.db')
df = pd.read_sql_table('InsertTableName', engine)

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
#placeholder for now
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