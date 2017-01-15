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
			alert(place);
	    });
};
google.maps.event.addDomListener(window, 'load', init);

function clear(place) {
    var index;
    for (var i = 0; i < place.length; i++){
        if (place.charCodeAt(i) == 769){
            index = i;
            return;
        }
    }
    if (index != undefined) return place.substring(0, index).concat(place.substring(index + 1));
}