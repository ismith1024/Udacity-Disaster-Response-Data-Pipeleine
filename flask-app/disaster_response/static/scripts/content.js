

var message_types = [] //holds the messages and their types

var update_classes = function(classifier_json){
/*
    update_classes(classifier_results)
    In:
        classifier_results : JSON string from the /classifier route
    Out:
        None
    Callback:
        None
    This function is a callback for the classify message function
    Updates the #classification_results_container DOM element  
*/

    console.log("Updating classes:");
    console.log(classifier_json);

    var new_container_html = '<div id="classification_results_container">';
    
    for(i = 0; i < classifier_json.length; i++){
        new_container_html += '<p>Results:'
        new_container_html += classifier_json[i].class + ':' + classifier_json[i].value;
        //console.log(classifier_json[i].msg_class + ':' + classifier_json[i].prob);
    }    
    
    new_container_html += '</p></div>';

    $("#classification_results_container").replaceWith(new_container_html);
};


var classify_message = function() {
/*
classify_message()
    In: 
        None
    Out:
        HTTP GET request
        Parameters:
            msg_text: the message text
            msg_genre: the message genre
    Callback:
        update_classes()
    
    - Reads the message from the message box element #message_box
    - Sends a HTTP GET request to the server's /classifier route
    - Initiates a callback to update_classes() with the JSON string obtained from the HTTP response
*/
    var msg_string;
    if ($("#message_box").val() != null) {
        msg_string = $("#message_box").val();
    } else msg_string = "";

    var classifierResults = []
    var classifierURL = "http://localhost:5555/classifier?msg_text=" + encodeURIComponent(msg_string);

    if($('#direct_button').prop('checked')) 
        classifierURL += '&msg_genre=direct';
    else if($('#news_button').prop('checked'))
        classifierURL += '&msg_genre=news';
    else classifierURL += '&msg_genre=social';

    console.log("Classify request to : " + classifierURL);

    $.getJSON(classifierURL, classifierResults, function (classifierResults) {
        for (i = 0; i < classifierResults.length; i++) {
            console.log(classifierResults[i].msg_class + classifierResults[i].prob);
        }
        
        update_classes(classifierResults);

    });

    return false;   

};


var update_plots = function(){
/*
update_plots()
    In: none
    Out: none
    Callback: none

    Initiates separate HTTP GET requests to the /msg_by_genre, /msg_by_class, /curr_msgs_genre, /curr_msgs_class routes
        to obtain current and all counts of messages by genre and class
    Initiates a separate callback for each of the four requests:
     - Parse data from the JSON string from the HTTP reponse
     - Format a plotly bar plot object from the data
     - Refresh the plot in the corresponding DOM container

*/

    var msg_results = [];

    //refresh empty plot containers
    $("#messages_by_genre_all").replaceWith('<div id="messages_by_genre_all"></div>');
    $("#messages_by_class_all").replaceWith('<div id="messages_by_class_all"></div>');
    $("#messages_by_genre_curr").replaceWith('<div id="messages_by_genre_curr"></div>');
    $("#messages_by_class_curr").replaceWith('<div id="messages_by_class_curr"></div>');

    //update training set messages by genre plot
    //get the JSON data from teh server
    //callback renders a new plot in the DOM container
    $.getJSON("http://localhost:5555/msg_by_genre", msg_results, function (msg_results) {
        
        var data = [
            {
              x: [],
              y: [],
              type: 'bar'
            }
        ];

        for(i = 0; i < msg_results.length; ++i){
            data[0].x.push(msg_results[i].genre);
            data[0].y.push(msg_results[i].count);
        };
        
        Plotly.newPlot('messages_by_genre_all', data);

    });

    //update training set messages by genre plot
    //get the JSON data from teh server
    //callback renders a new plot in the DOM container
    $.getJSON("http://localhost:5555/msg_by_class", msg_results, function (msg_results) {
        
        var data = [
            {
              x: [],
              y: [],
              type: 'bar'
            }
        ];

        //console.log('All messages by class:')
        for(i = 0; i < msg_results.length; ++i){
            //console.log(data[0]);
            data[0].x.push(msg_results[i].class);
            data[0].y.push(msg_results[i].count);
        };
        
        Plotly.newPlot('messages_by_class_all', data);

    });


    //update current messages by genre plot
    //get the JSON data from teh server
    //callback renders a new plot in the DOM container
    $.getJSON("http://localhost:5555/curr_msgs_genre", msg_results, function (msg_results) {
        
        var data = [
            {
              x: [],
              y: [],
              type: 'bar'
            }
        ];

        for(i = 0; i < msg_results.length; ++i){
            data[0].x.push(msg_results[i].genre);
            data[0].y.push(msg_results[i].count);
        };
        
        Plotly.newPlot('messages_by_genre_curr', data);

    });

    //update current messages by class plot
    //get the JSON data from teh server
    //callback renders a new plot in the DOM container
    $.getJSON("http://localhost:5555/curr_msgs_class", msg_results, function (msg_results) {
        
        console.log(msg_results);

        var data = [
            {
              x: [],
              y: [],
              type: 'bar'
            }
        ];

        //console.log(data);

        for(i = 0; i < msg_results.length; ++i){
            data[0].x.push(msg_results[i].class);
            data[0].y.push(msg_results[i].count);
        };
        
        Plotly.newPlot('messages_by_class_curr', data);

    });
    

    return false;

};



var setup_data = function(){
/*
 setup_data()
 
    In : none
    Out: none
    Callbacks: none
 
    Initiated by a <script> tag in the 'index.html' home page on page load
    Updates the plots with initial class and genre counts
    Adds an on-click listener to the #classify_button element
 */
    
    update_plots();

    //Add a click listener to the submit message button
    //Returns false to prevent page reloads
	$(document).on('click', '#classify_button', function(){
        classify_message();
        update_plots();
        return false;
	});


};



