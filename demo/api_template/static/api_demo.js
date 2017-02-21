$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $(".add").click(function(){
        var data = $("#wordbotform").serialize();
        newMessage(data);
    })
});

function newMessage(message) {
    $.post("/wordbot", message, function(response) {
        var str = JSON.stringify(response);
        $(".output").val(str);
    }, 'json');
}

