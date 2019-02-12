
///// DOM Element Values
var message_types = [] //holds the messages and their types


/////////////////////////////////////////////////////////////////////////////////////////////
/////DOM Functions
/////////////////////////////////////////////////////////////////////////////////////////////


var updateHighlightedContract = function(){
	var mile = $("#milesOptions").val();
	
	for(var i = 0; i < miles_JSON.length; i++){
        if (miles_JSON[i].milestone == mile) {
            selected_client = miles_JSON[i].client.trim();
            selected_productDesc = miles_JSON[i].productDesc.trim();
            selected_milestone = miles_JSON[i].milestone.trim();

			$("#clientNameText").replaceWith('<p id="clientNameText"><b>Client:</b> ' + miles_JSON[i].client + '</p>');
			$("#productNameText").replaceWith('<p id="productNameText"><b>Product:</b> ' + miles_JSON[i].productDesc + '</p>');
			$("#milestoneText").replaceWith('<p id="milestoneText"><b>Milestone:</b> ' + miles_JSON[i].milestone + '</p>');			
		}
	}
	
};



var resetWarning = function () {
    $('#warning_container').replaceWith('<div id="warning_container"></div >');
};


//////////////////// CLASSIFIER IS HERE

/*
    update_classes(classifier_results)  
*/
var update_classes = function(classifier_json){
    console.log("Updating classes:");
    console.log(classifier_json);

    var new_container_html = '<div id="classification_results_container">';
    
    for(i = 0; i < classifier_json.length; i++){
        new_container_html += '<p>Results:'
        new_container_html += classifier_json[i].msg_class + ':' + classifier_json[i].prob;
        console.log(classifier_json[i].msg_class + ':' + classifier_json[i].prob);
    }    
    
    new_container_html += '</p></div>';

    $("#classification_results_container").replaceWith(new_container_html);

    


};


/*
classify_message()
    - gets the message from the message box element #message_box
    - POSTs a classify request to the server
    - Callback: updates the message classes and probabilities
*/

////// TODO: add the msg_genre query parameter
var classify_message = function() {

    var msg_string;
    if ($("#message_box").val() != null) {
        msg_string = $("#message_box").val(); //.replace(/ /g, "");
    } else msg_string = "";

    var classifierResults = []
    var classifierURL = "http://localhost:5555/classifier?msg_text=" + encodeURIComponent(msg_string);
    console.log(classifierURL);

    $.getJSON(classifierURL, classifierResults, function (classifierResults) {
        for (i = 0; i < classifierResults.length; i++) {
            console.log(classifierResults[i].msg_class + classifierResults[i].prob);
        }
        
        update_classes(classifierResults);

    });

    return false;   

};

/*
update_plots()
gets the current and training set genre and class counts
inserts the plots into the DOM
*/
var update_plots = function(){

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

        console.log('All messages by class:')
        for(i = 0; i < msg_results.length; ++i){
            console.log(data[0]);
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

        console.log(data);

        for(i = 0; i < msg_results.length; ++i){
            data[0].x.push(msg_results[i].class);
            data[0].y.push(msg_results[i].count);
        };
        
        Plotly.newPlot('messages_by_class_curr', data);

    });
    

    return false;

};



/*
 * setup_data()
 * runs when page loads
 * initiates all API calls to set up the DOM
 */
var setup_data = function(){
    
    update_plots();

    //Add a click listener to the submit message button
	$(document).on('click', '#classify_button', function(){
        classify_message();
        update_plots();
        return false;
	});


};



