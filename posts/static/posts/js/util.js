/**
 * Created by Ramazan on 24.11.2016.
 */
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function getPlace(city) {
  var service = new google.maps.places.AutocompleteService();
  service.getQueryPredictions({ input: 'Феодосия' }, function (array, status) {
    if (status != google.maps.places.PlacesServiceStatus.OK) return city; else return array[0].description;
  });
}