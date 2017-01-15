/**
 * Created by Измайловы on 15.01.2017.
 */
var init = function  () {
	var input = document.getElementById("place");
		input.value = "";
		var options = {
			types: ['(regions)']
		};
		var autocomplete = new google.maps.places.Autocomplete(input, options);

		google.maps.event.addListener(autocomplete, 'place_changed', function() {
		    var place = autocomplete.getPlace();
            $.ajax({
                type: 'POST',
                url: 'specify_place',
                data: {
                    formatted_address: clear(place.formatted_address),
                    place_id: place.place_id,
                    csrfmiddlewaretoken: getCookie('csrftoken')
                },
                success: function (response) {
                    if (response['success']) {
                        window.location = response['redirect'];
                    }
                },
                dataType: 'json'
            });
	    });
};
google.maps.event.addDomListener(window, 'load', init);

