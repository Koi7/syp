var toggleRate = 100;

function ToggleSendMessageControls(){
	var post_id = $(this).data('post-id');
	$('div.send-message-controls[data-post-id=' + post_id + ']').toggle(toggleRate);
}


function filter() {
	$('div#post-list-container').empty();
	$('p#filter-loader').toggle(toggleRate);
	// get filter state object
	filterState = getFilterState();
	$.ajax({
		type: "GET",
		url: loadMoreUrl, 			
		data: {
			place: filterState.place,
			tag: filterState.tag,
			order: filterState.order,
			is_anonymous: filterState.is_anonymous
		},
		context: this,
		dataType: "json",
		success: function (data){
			if (data.success){
				$('p#filter-loader').toggle(toggleRate);
				$('div#post-list-container').html(data.rendered_template);
			}
		}
	});
}

function LikeEvent(){
	var post_id = $(this).data('post-id');
	$.ajax({
		type: "POST",
		url: likeUrl, 			
		data: {
			post_id: post_id,
			csrfmiddlewaretoken: getCookie('csrftoken')
		},
		context: this,
		dataType: "json",
		success: function (data){
			if (!data.self_like) {
				if (data.is_created == '0'){
					$(this).removeClass('w3-text-gray');
					$(this).addClass('w3-text-red');
				} else{
					$(this).removeClass('w3-text-red');
					$(this).addClass('w3-text-gray');
				}
				$('span.likes-amount[data-post-id=' + post_id + ']').text(data.likes_amount);
			} else {
				alertify.error('Вы не можете лайкать свои же посты. В этом нет смысла =).');
			}
		}
	});
}

function ClickSendButtonEventHandler(){
	var post_id = $(this).data('post-id');
	var input_value = $.trim($('input.w3-input[data-post-id=' + post_id + ']').val());
	if (input_value){
		$.ajax({
			type: "POST",
			url: leaveMessageUrl, 			
			data: {
				post_id: post_id,
				message: input_value,
				csrfmiddlewaretoken: getCookie('csrftoken')
			},
			context: this,
			dataType: "json",
			success: function (data){
				if (data.success){
					alertify.success('Ваше послание отправлено.');
					// update post state on front end
					// make icon red
					$('i.fa-heart[data-post-id=' + post_id + ']').removeClass('w3-text-gray');
					$('i.fa-heart[data-post-id=' + post_id + ']').addClass('w3-text-red');
					// change amount of likes
					$('span.likes-amount[data-post-id=' + post_id + ']').text(data.likes_amount);
				} else {
					if (data.self_like) {
						alertify.error('Безсмысленно отправлять послание самому себе =).');
					} else {
						alertify.error(data.err_msg);
					}
				}
				$('i.show-send-message-controls[data-post-id=' + $(this).data('post-id') + ']').trigger('click');
			}
		});

	}
}

function loadMore() {
	// hide load more button
	$(this).toggle();
	// show loading
	$('span#load-more-loader').toggle();
	var page = parseInt($(this).data('offset'), 10);
	var onSuccess = function (data) {
				$('ul#post-list').append(data.rendered_template);
				// increment if has next page
				if (data.has_next) {
					// hide loader
					$('span#load-more-loader').toggle();
					//show button
					$(this).toggle();
					// increment 
					$(this).data('offset', data.next_page);
				} else {
					// remove load more section
					$('section#load-more-section').remove();
				}
	};
	if (filterState) {
		$.ajax({
			type: "GET",
			url: loadMoreUrl,
			data: {
				place: filterState.place,
				tag: filterState.tag,
				order: filterState.order,
				is_anonymous: filterState.is_anonymous,
				offset: page
			},
			dataType: "json",
			context: this,
			success: onSuccess
		});
	} else {
		$.ajax({
			type: "GET",
			url: loadMoreUrl,
			data: {
				offset: page
			},
			dataType: "json",
			context: this,
			success: onSuccess
		});
	}

}


$(document).on('click', '.fa-heart', LikeEvent);
$(document).on('click', 'button.message-sender', ClickSendButtonEventHandler);
$(document).on('click', 'i.show-send-message-controls', ToggleSendMessageControls);
$(document).on('click', 'button#load-more-btn', loadMore);

$(document).ready(function () {

	$('div#filters select, div#filters-mobile select').change(filter);

	$('button#filter_panel_toggler').click(function (){
		$('div#filters').toggle(toggleRate);
	});

	$('button#fp-toggler-mobile').click(function () {
		$('div#filters-mobile').toggle(toggleRate);
	})

});