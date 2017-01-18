/**
 * Created by Измайловы on 15.01.2017.
 */
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function clear(place) {
    var index;
    for (var i = 0; i < place.length; i++){
        if (place.charCodeAt(i) == 769){
            index = i;
            return;
        }
    }
    if (index != undefined) place = place.substring(0, index).concat(place.substring(index + 1));
    //noinspection JSAnnotator
    return place;
}