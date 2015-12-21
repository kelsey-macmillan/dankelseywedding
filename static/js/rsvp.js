$(document).ready(function() {
    $('#rsvpForm').submit(function (event){
        var name = $('#nameInput').val()
        $.get('/rsvp-get/' + name, function(data){
            alert(data)
        })
        event.preventDefault()
    })
})