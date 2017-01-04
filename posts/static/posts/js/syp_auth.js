
var init = function  () {
	var input = document.getElementById("place");
		input.value = "";
		var options = {
			types: ['(regions)']
		};
		var autocomplete = new google.maps.places.Autocomplete(input, options);

		google.maps.event.addListener(autocomplete, 'place_changed', function() {
		    var place = autocomplete.getPlace();
            var index;
            for (var i = 0; i < place.formatted_address.length; i++){
	            if (place.place.formatted_address.charCodeAt(i) == 769){
  	                index = i;
                }
            }
            place.formatted_address = place.formatted_address.substring(0, index).concat(place.formatted_address.substring(index++));
			initAuthWidjet(place.formatted_address);
	    });
};
google.maps.event.addDomListener(window, 'load', init);
function initAuthWidjet(formatted_address) {
    VK.Widgets.Auth("vk_auth", {
        width: "200px", onAuth: function (data) {
            $.ajax({
                type: 'POST',
                url: 'login',
                data: {
                    uid: data.uid,
                    first_name: data.first_name,
                    last_name: data.last_name,
                    photo_rec: data.photo_rec,
                    place: formatted_address,
                    hash: data.hash,
                    csrfmiddlewaretoken: getCookie('csrftoken')
                },
                success: function (response) {
                    if (response['success']) {
                        window.location = 'posts';
                    }
                },
                dataType: 'json'
            });
        }
    });
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}