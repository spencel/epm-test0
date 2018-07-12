/* jshint esversion: 6 */
const mongodb = require( 'mongodb' );

const mongodbUrl = 'mongodb://localhost:27017/';
const dbName = 'epmTest';

mongodb.MongoClient.connect(
	mongodbUrl,
	( error, mongoClient ) => {
		mongoClient.db( dbName ).collection( 'W_EXCAVATION' ).find( '*' ).toArray( ( error, documents ) => {
			console.log( documents );
			mongoClient.close();
		});
	}
);
