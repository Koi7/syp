
function initAuthWidjet() {
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
                    hash: data.hash,
                    csrfmiddlewaretoken: getCookie('csrftoken')
                },
                success: function (response) {
                    if (response['success']) {
                        window.location = response['redirect'];
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