import sys
import os
import time
import datetime
import arcpy # definable when script called by propy.bat
import config
import exportList

# arcpy.env.addOutputsToMap = False
# arcpy.env.overwriteOutput = True
# arcpy.env.parallelProcessingFactor = '0'
# arcpy.env.qualifiedFieldNames = False
# arcpy.env.workspace = gdbPath
# arcpy.env.scratchWorkspace = gdbPath


gdbPath = config.projectGdbPath

logFilePath = os.path.join( config.arcgisProjectPath, os.path.basename( __file__ ) + '.log' )

logFile = open( logFilePath, 'a+' )

# process feature classes
try:

	for item in exportList.exportFeatureclasses:
		featureclassPath = item[ 'featureclassPath' ]
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'featureclassPath: ' + str( featureclassPath ))
		newFeatureclassName = item[ 'newFeatureclassName' ]
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'newFeatureclassName: ' + newFeatureclassName )
		newFeatureclassPath = os.path.join( gdbPath, newFeatureclassName )
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'newFeatureclassPath: ' + newFeatureclassPath )
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'deleting existing ' + newFeatureclassName + ' from ' + gdbPath + ' if it exists' )
		arcpy.Delete_management( newFeatureclassPath )
		conservedFieldList = item[ 'conservedFielList' ]
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'conservedFieldList: ' + str( conservedFieldList ))
		serverRoutes = item[ 'serverRoutes' ]
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'serverRoutes: ' + str( serverRoutes ))
		# export feature class to temp gdb
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'exporting ' + featureclassPath + ' to ' + gdbPath + ' as newFeatureclassName' )
		
		arcpy.FeatureClassToFeatureClass_conversion( \
			in_features = featureclassPath, \
			out_path = gdbPath, \
			out_name = newFeatureclassName \
		)
		# get its field list
		fieldList = arcpy.ListFields( newFeatureclassPath )
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'fieldList:' )
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + str( fieldList ))
		# export table data to tab delimited text file
		# set data file full path
		dataFilePath = os.path.join( config.arcgisProjectPath, newFeatureclassName + '.data' )
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'dataFilePath: ' + str( dataFilePath))
		
		with open( dataFilePath, 'w' ) as file: # 'w' overwrites anything already in file
			# write field names
			for i, field in enumerate( fieldList ):
				file.write( field.name )
				if i != ( len( fieldList ) - 1 ):
					file.write( '\t' )
			file.write( '\n' )
			# write table data
			# get total rows first
			rowCount = 0
			with arcpy.da.SearchCursor( newFeatureclassPath, '*' ) as cursor:
				for row in cursor:
					rowCount = rowCount + 1
			with arcpy.da.SearchCursor( newFeatureclassPath, '*' ) as cursor:
				for i, row in enumerate( cursor ):
					for j, value in enumerate( row ):
						file.write( str( value ) )
						if j != ( len( row ) - 1 ):
							file.write( '\t' )
					if i != ( rowCount - 1 ):
						file.write( '\n' )
			
			#################################
			# import data file into mongodb #
			#################################

		for serverRoute in serverRoutes:
			route = serverRoute[ 'route' ]
			referenceField = serverRoute[ 'referenceField' ]
			# add field (for linking to web app)
			logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'adding field to ' + newFeatureclassPath )
			arcpy.AddField_management( \
				in_table = newFeatureclassPath, \
				field_name = config.getDataFieldName, \
				field_alias = 'Click', \
				field_type = 'TEXT', \
				field_length = 300 )
			# set get data field using field calculator
			# should come up with, e.g.: '<a href="http://10.65.0.212:8840/get-excavation/' + str( !ID! ) + '" >Here</a>'
			link = '\'' + str( config.serverAddress ) + str( route ) + '\' + str( !' + str( referenceField ) + '! )'
			#logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'link: ' + link )
			#expression = '\'<a href=\"' + link + '\" >Here</a>\''
			expression = link
			logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + expression )
			logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'calculating reference to web app field' )
			arcpy.CalculateField_management( \
				in_table = newFeatureclassPath, \
				field = config.getDataFieldName, \
				expression_type = 'PYTHON', \
				expression = expression )
		# make list of fields to delete
		fieldDeletionList = []
		#logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + str( fieldDeletionList ))
		for field in fieldList:
			#logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'field.required: ' + str( field.required ) )
			if field.name not in conservedFieldList and field.required == False:
				#logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + field.name + ' not in field deletion lists' )
				fieldDeletionList.append( field.name )
		# delete fields
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'deleting fields in ' + newFeatureclassPath )
		logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + 'fieldDeletionList: ' + str( fieldDeletionList))
		arcpy.DeleteField_management( newFeatureclassPath, fieldDeletionList )

	logFile.close()

except Exception as exception:
	logFile.write( '\n' + datetime.datetime.fromtimestamp( time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' - ' + str( exception ))

finally:
	logFile.close()