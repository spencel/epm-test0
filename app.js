/*jshint esversion: 6*/
/* jshint ignore: start */
import fs from 'fs';
import express from 'express';
import mongodb from 'mongodb';

// database
const mongodbUrl = 'mongodb://localhost:27017/';
mongodb.MongoClient.connect(
	mongodbUrl,
	( error, client ) => {
		if ( error ) { console.error( error ); client.close(); return false; }
		console.log( 'database test connection successful' );
		client.close();
	}
);

// App config
const app = express();
app.use( "/public", express.static( __dirname + "/public" )); // make express look in the public directory for assets (css/js/img)

// Routers
app.get( '/', ( request, response ) => {
	console.log( 'getting /index.html' );
	response.sendFile( __dirname + '/index.html' ); 
});
app.get( '/get-wPipe', ( request, response ) => {
	new Promise( ( resolve, reject ) => {
		mongodb
		.MongoClient
		.connect( mongodbUrl, ( error, client ) => {
			if ( error ) { console.error( error ); client.close(); return false;}
			resolve( client );
		});
	})
	.then( client => {
		return new Promise( ( resolve, reject ) => {
			client.db( 'epmTest' ).collection( 'W_PIPE', ( error, collection ) => {
				if ( error ) { console.error( error ); client.close(); return false;}
				resolve({
					client: client,
					collection: collection
				});
			});
		}); 
	})
	.then( resolved => {
		var client = resolved.client;
		var collection = resolved.collection;
		return new Promise(( resolve, reject ) => {
			collection.find().toArray(( error, documents ) => {
				client.close();
				resolve( documents );
			});
		});
	})
	.then( documents => {
		response.send({
			successful: true,
			data: documents
		});
	});
});
app.get( '/get-w-pipe/:fsn', ( request, response ) => {
	mongodb.MongoClient.connect(
		mongodbUrl,
		( error, client ) => {
			if ( error ) { console.error( error ); client.close(); return false; }
			console.log( 'database test connection successful' );
			client
			.db( 'epmTest' )
			.collection( 'wPipe' )
			.findOne( 
				/*{ 'FAC_SEQ_NU': { '$eq': request.params.fsn }},*/
				( error, result ) => {
					if ( error ) { console.error( error ); client.close(); return false; }
					var html = "";
					for ( var key in result ) {
						if ( result.hasOwnProperty( key )) continue;
						
					}
					console.log( result );
					response.send( result );
			});
		}
	);
});
app.get( '/get-excavation/:id', ( request, response ) => {

});

// Exports
export default app;