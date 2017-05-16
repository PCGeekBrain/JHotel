$( function() {$( "#selectedDate" ).datepicker({
    minDate: 0,
    maxDate: 500
});});
$( function() {
    $( "#selectedDate" ).change(function() {
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                date: $( "#selectedDate" ).val()
            },
            cache: false,
            success: function(msg, status, jqXHR) {
                updateList(msg.list)
            },
            error: function() {
                console.log("Client/Server error: Failed get updated data")
            },
        });
    });
});

function updateList(data){
    for(i=0; i<data.length; i++){
        $('#reservations_'+data[i][0]).html(data[i][1])
    }
}