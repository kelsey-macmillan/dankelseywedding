$(document).ready(function() {
    // Guest submits name in RSVP field
    $('#rsvp-form').submit(function (event){
        event.preventDefault()

        // Hide the not on guest list error in case it has been shown
        $('#not-on-guest-list').hide()

        // Get name of guest from form and query backend
        var name = $('#name-input').val()
        $.ajax({
            method: 'GET',
            url: '/rsvp-get/' + name, 
        }).done(function(guest){
            // Once query is successfully returned with guest info
            var guest=JSON.parse(guest);

            // Determine correct form ID based on guest info
            // if the guest does not have couple, and is allowed plus one
            if (guest.name2 == null && guest.plus1_allowed) {
                formID = 'one-guest-plus-one'
            }
            // if the guest does not have couple, and is not allowed plus one
            else if (guest.name2 == null && !guest.plus1_allowed) {
                formID = 'one-guest'
            }
            // otherwise the guest must be a couple
            else {
                formID = 'couple-guest'
                $('#couple-guest .guest1-name').prepend(guest.name1)
                $('#couple-guest .guest2-name').prepend(guest.name2)
            }

            // Update form shown
            $('#rsvp-form .button-primary').hide()
            $('#name-input').prop('readonly', true)
            // update form defaults
            $('#' + formID + ' .plus-one-input').val(guest.plus1_name)
            $('#' + formID + ' .rsvp1-input').val(guest.rsvp1)
            $('#' + formID + ' .rsvp2-input').val(guest.rsvp2)
            $('#' + formID + ' .note-input').val(guest.note)
            $('#' + formID + ' .location-input').val(guest.location)
            // make submit button say "Update RSVP" if they've already submitted once
            if (guest.rsvp1 != null)
                $(".rsvp-button").val("Update RSVP");
            // show the form
            $('#' + formID).show()    
        }).fail(function(){
            // Give error if guest not on list
            $('#not-on-guest-list').show()
        })
    })
                  
    // Post guest RSVP
    var submitCallback = function (event){
        event.preventDefault()
        var formID = event.currentTarget.id
        $('#rsvp-submit-error').hide()
        var name = $('#name-input').val()
        var rsvp1 = $('#' + formID + ' .rsvp1-input').val()
        var rsvp2 = $('#' + formID + ' .rsvp2-input').val()
        var plus1_name = $('#' + formID + ' .plus-one-input').val()
        var note = $('#' + formID + ' .note-input').val()
        var location = $('#' + formID + ' .location-input').val()
        $.ajax({
            method: 'POST',
            url: '/rsvp-set/' + name,
            data: {
                'rsvp1': rsvp1,
                'rsvp2': rsvp2,
                'plus1_name': plus1_name,
                'note': note,
                'location': location
            }
        }).done(function(){
            $(".rsvp-button").prop('value', 'RSVP Sent! Update RSVP');
        }).fail(function(){
            $('#rsvp-submit-error').show()
        })
    }

    // Call post RSVP function for each form
    $('#one-guest-plus-one').submit(submitCallback)
    $('#one-guest').submit(submitCallback)
    $('#couple-guest').submit(submitCallback)
})