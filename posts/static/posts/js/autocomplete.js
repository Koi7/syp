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
			getWeatherByCity(place.name);
	    });
	}
	google.maps.event.addDomListener(window, 'load', init);

	var getWeatherByCity = function (city) {
		/*var httpRequest = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
		httpRequest.onreadystatechange = function () {
			var jsonText = httpRequest.readyState == 4 && httpRequest.status == 200 ? httpRequest.responseText : null;
			var weather = JSON.parse(jsonText);
			if (weather.cod == 404) {
				alert("= ( city not found");
				return;
			}
			var tempView = document.getElementById("temp");
			var tempValue = Math.floor(KtoC(weather.main.temp));
			tempView.innerHTML = tempValue + " C&deg;";
			showThermometer();
			moveRuth(tempValue);
		}
		httpRequest.open("GET", "http://api.openweathermap.org/data/2.5/weather?q=" + city, true);
		httpRequest.send();*/
		alert(city);
	}