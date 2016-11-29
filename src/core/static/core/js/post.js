function saveComment (id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var entry = $("textarea[id='id_entry']").val();
	$.post(
		'comments/edit/' + id, 
		{id: id, entry: entry,  csrfmiddlewaretoken: csrf}, 
		function (data) {
			$('.comment-entry[data-comment-id=' + id + ']').html(data);
	});
}

function addComment (post_id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var entry = $("textarea[id='id_entry']").val();
	$.post(
		'comments/add', 
		{post_id: post_id, entry: entry,  csrfmiddlewaretoken: csrf}, 
		function (data) {
			$.get('comments/' + data, function (response) {
				$('.comments').append(response);
				$("textarea[id='id_entry']").val("");
			});
			
	});
}

function deleteComment (id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	$.post(
		'comments/delete', 
		{id: id, csrfmiddlewaretoken: csrf}, 
		function (data) {
			$('.comment[data-comment-id=' + id + ']').remove();
	});
}

function loadForm (id) {
	$('.comment-entry[data-comment-id=' + id + ']').load('comments/edit/' + id);
}
