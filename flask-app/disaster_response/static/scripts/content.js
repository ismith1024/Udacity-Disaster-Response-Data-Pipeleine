var test = function(){
    console.log("This is the test function");
}


var get_and_replace_classification = function(message_text){
    
    $.post(postURL, mydata, whenItsDone);
    
    var new_div = '<div id="classification_results_container">' + 
        '_____' +
        '</div>';

    $('#classification_results_container').replaceWith(new_div);
};