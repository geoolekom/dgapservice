$(document).ready(function() {
	//	uploading form for login and logout
	$('.login-form').load('/core/login');

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