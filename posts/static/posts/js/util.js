function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function sypConfirm(message) {
	// confirm dialog
	alertify.confirm(message, function () {
	    return true;
	}, function() {
	    return false;
	});
}

/*
return - Object
*/
function getFilterState(){
	return { 
			'place': $('select#filter_place').val(),
	 		'tag': $('select#filter_tags').val(),
	  		'order': $('select#filter_order').val(),
	   		'is_anonymous': $('select#filter_anonymous').val()
	   	   };
}