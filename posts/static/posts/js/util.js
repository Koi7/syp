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
  var place = '';
  service.getQueryPredictions({ input: city }, function (array, status) {
    if (status != google.maps.places.PlacesServiceStatus.OK) return city; else place = array[0].description;
  });
  return place;
}

function getDataAndRedirect() {
  VK.Widgets.Auth("vk_auth", {width: "200px", onAuth: function(data) {
              $.ajax({
              type: 'POST',
              url: 'login',
              data: {
                  uid: data.uid,
                  first_name: data.first_name,
                  last_name: data.last_name,
                  photo_rec: data.photo_rec,
                  place: getPlace(getCity(data.uid)),
                  hash: data.hash,
                  csrfmiddlewaretoken: getCookie('csrftoken')
              },
              success: function(response){
                    if (response['success']){
                        window.location = 'posts';
                    }
              },
              dataType: 'json'
          });
          } });
}

function getCity(uid){
  /*city = '';
  $.ajax({
              type: 'GET',
              url: 'https://api.vk.com/method/users.get?user_ids=' + uid + '&fields=city&v=5.60',
              success: function(response){
                    response.forEach(function (item, i, arr) {
                        city = item['city']['title'];
                    })
              },
              dataType: 'json'
          });
  return city;*/
  return "Федосия";
}