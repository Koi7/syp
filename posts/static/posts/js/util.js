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
function getFilterState() {
	var filterPanel = $('div#filters').is(':visible') ? $('div#filters') : $('div#filters-mobile');

	return { 
			'place': filterPanel.find('select.f-place').val(),
	 		'tag': filterPanel.find('select.f-tag').val(),
	  		'order': filterPanel.find('select.f-order').val(),
	   		'is_anonymous': filterPanel.find('select.f-anonymous').val()
	   	   };
}