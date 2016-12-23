$(document).ready(function() {
	//	uploading form for login and logout
	$('.login-form').load('/core/login');

	console.log(gettext('Все норм!'));

	//mySettings = { ... };

	$('textarea').redactor({
		imageUpload: '/core/upload/',
		fileUpload: '/core/upload/',
		callbacks: {
			imageUpload: function (image, json) {
				console.log("OK");
				$(image).attr('width', "50%");
			},
		}
	});

})