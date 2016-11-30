$(document).ready(function() {

	//	likes update with timeout
	function updateRating () {
		var postIds = Array();

		$('.post-rating').each(function() {
			postIds.push($(this).data('post-id'));
		})

		$.getJSON('/feed/ratings', {ids: postIds.join(',')} , function(data) {
			for (var i in data) {
				$('.post-rating[data-post-id='+i+']').html('<b>' + data[i] + '</b>');
			}
		});
	}

	window.setInterval(updateRating, 1000);

	//	likes implimentation
	$('.plus-button').click(function () {
		var url = $(this).data('rate-url');
		var id = $(this).data('post-id');

		var postRating = $('.post-rating[data-post-id='+id+']')[0];
		var minusButton = $('.minus-button[data-post-id='+id+']')[0];

		$(this).addClass('btn-success');
		$(minusButton).removeClass('btn-danger');

		var csrf = $("input[name='csrfmiddlewaretoken']").val();
		$.post(
			url, 
			{mark: 1, csrfmiddlewaretoken: csrf}, 
			function (data) {
				$(postRating).html('<b>' + data + '</b>');
		});
	});

	$('.minus-button').click(function () {
		var url = $(this).data('rate-url');
		var id = $(this).data('post-id');

		var postRating = $('.post-rating[data-post-id='+id+']')[0];
		var plusButton = $('.plus-button[data-post-id='+id+']')[0];

		$(plusButton).removeClass('btn-success');
		$(this).addClass('btn-danger');

		var csrf = $("input[name='csrfmiddlewaretoken']").val();
		$.post(
			url, 
			{mark: -1, csrfmiddlewaretoken: csrf}, 
			function (data) {
				$(postRating).html('<b>' + data + '</b>');
		});
	});

});

function deletePost (id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	$.post(
		'posts/delete', 
		{id: id, csrfmiddlewaretoken: csrf}, 
		function (data) {
			if (window.location.href != "/feed") {
				window.location.href = "/feed";
			} else {
				$('.post[data-post-id=' + id + ']').remove();
			}
	});
}