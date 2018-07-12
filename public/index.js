/* jshin */
/* jshint ignore: start */
jQuery( document ).ready( function () {
	jQuery.ajax({
		url: '/get-wPipe',
		type: 'GET',
		complete: function( response ) {
			var data = JSON.parse( response.responseText );
			console.log( data );
		}
	});

	// get an excavation site
	/*jQuery.ajax({
		url: '/get-excavation',
		type: 'GET',
		data: ''
		complete: function( response ) {
			var data = JSON.parse( response.responseText );
			console.log( data );
		}
	});*/
});