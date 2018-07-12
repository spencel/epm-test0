import fs from 'fs'
import path from 'path'
import byline from 'byline'
import mongodb from 'mongodb'
import { exec } from 'child_process'
import config from './config.json'

console.log( 'config:' )
console.log( config )

;( async () => {

	var pyScriptPath = path.join( __dirname, config.pyScriptName )

	console.log( 'running py script' )
	new Promise( ( resolve, reject ) => {

		exec( `${config.proPyBatPath} ${pyScriptPath}`, ( error, stdout, stderr ) => {
			if ( error ) console.error( error )
			if ( stdout ) console.log( 'script.js: ' + stdout )
			if ( stderr ) console.error ( stderr )
			console.log( 'py script done' )
			resolve()
		})

	})
	.then( () => {
		return new Promise( ( resolve, reject ) => {

			// get list of file names in current directory
			console.log( 'getting list of file names' )
			fs.readdir( config.dataFileDirectory, async ( error, fileNameArray ) => {
				if ( error ) console.error( error )
				resolve( fileNameArray ) 
			})

		})
	})
	.then( fileNameArray => {
		return new Promise(( resolve, reject) => {

			var dataFileNameArray = []
			for ( var i = 0; i < fileNameArray.length; i++ ) {
				var fileName = fileNameArray[ i ];
				console.log( `if ( ${path.extname( fileName )} === ${config.dataFileExtension} )`)
				if ( path.extname( fileName )  === config.dataFileExtension ) {
					dataFileNameArray.push( fileName );
				}
			}

			mongodb.MongoClient.connect(
				config.mongodbUrl,
				( error, mongodbClient ) => {
					if ( error ) console.error( error )
					console.log( 'connected to database' )
					resolve({ mongodbClient, dataFileNameArray })
				}
			)

		})
	})
	.then( resolution => {
		return new Promise(( resolve, reject ) => {

			asyncRemoveCollections( resolution.mongodbClient, resolution.dataFileNameArray, 0, () => {
				resolve({ dataFileNameArray: resolution.dataFileNameArray, mongodbClient: resolution.mongodbClient })
			})

		})
	})
	.then( resolution => {
		return new Promise(( resolve, reject ) => {

			asyncLineRead( resolution.mongodbClient, resolution.dataFileNameArray, 0, () => {
				resolution.mongodbClient.close()
				resolve()
			})

		})
	})
	.catch( error => {
		console.error( error )
	})

})()


function asyncRemoveCollections( client, dataFileNames, i, callback ) {
	console.log( 'asyncRemoveCollections: i: ' + i );
	if ( i < dataFileNames.length ) {
		console.log( `${i+1}th run of asyncRemoveCollections` );
		var dataFileName = dataFileNames[ i ];
		var collectionName = path.basename( dataFileName, config.dataFileExtension );
		client.db( config.dbName ).dropCollection( collectionName, ( error, result ) => {
			console.log( collectionName + ' collection dropped' );	
			i++;
			new Promise( (resolve, reject ) => {
				asyncRemoveCollections( client, dataFileNames, i, () => {
					console.log( 'resolve asyncRemoveCollections A: i: ' + i );
					resolve();
				});
			}).then( () => {
				callback();
			});
		});
	} else {
		console.log( 'resolve asyncRemoveCollections B: i: ' + i );
		callback();
	}
}

function asyncLineRead( client, dataFileNames, i, callback ) {

	if ( i < dataFileNames.length ) {
		var dataFileName = dataFileNames[ i ]
		var collectionName = path.basename( dataFileName, config.dataFileExtension )
		
		var iLine = 0
		var columnNames = []
		var lineStream = byline( fs.createReadStream( path.join( config.dataFileDirectory, dataFileName ), { encoding: 'utf8' }))

		lineStream.on( 'error', error => {
			process.stdout.write( 'line reader error:\n' )
			process.stdout.write( error )
			process.stdout.write( '\n' )
		});

		lineStream.on( 'data', line => {
			lineStream.pause()
			if ( columnNames.length === 0 ) {
				process.stdout.write( 'getting column names\n' )
				columnNames = line.split( '\t' )
				lineStream.resume()
			} else {
				var arValues = line.split( '\t' )
				var mongoDocument = {}
				for ( var j = 0; j < arValues.length; j++ ) {
					mongoDocument[ columnNames[ j ]] = arValues[ j ]
				}
				client.db( config.dbName ).collection( collectionName ).insertOne( mongoDocument, ( error, result ) => {
					if ( error ) throw error
					iLine++
					process.stdout.write( `${dataFileName}: line no.: ${iLine}\r`)
					lineStream.resume()
				})
			}
		})

		lineStream.on( 'end', () => {
			process.stdout.write( '\n' )
			process.stdout.write( 'line reader end\n' )
			process.stdout.write( `${iLine}\n` )
			i++
			asyncLineRead( client, dataFileNames, i, () => {
				callback()
			})
		})

	} else {
		callback()
	}

}