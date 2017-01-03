/**
 * Created by Ramazan on 03.01.2017.
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
			getDataAndRedirect(place.name);
	    });
	}
	google.maps.event.addDomListener(window, 'load', init);