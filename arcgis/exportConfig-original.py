import os
import config

exportFeatureclasses = [
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_PIPE' ),
		'newFeatureclassName': 'SDW_CITY_W_PIPE',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-pipe/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_VALVE' ),
		'newFeatureclassName': 'SDW_CITY_W_VALVE',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-valve/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_SERVICE' ),
		'newFeatureclassName': 'SDW_CITY_W_SERVICE',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-service/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_AIR_VALVE' ),
		'newFeatureclassName': 'SDW_CITY_W_AIR_VALVE',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-air-valve/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_BLOW_OFF' ),
		'newFeatureclassName': 'SDW_CITY_W_BLOW_OFF',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-blow-off/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_AQUEDUCT' ),
		'newFeatureclassName': 'SDW_CITY_W_AQUEDUCT',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-aqueduct/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_HYDRANT' ),
		'newFeatureclassName': 'SDW_CITY_W_HYDRANT',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-hydrant/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_PUMP' ),
		'newFeatureclassName': 'SDW_CITY_W_PUMP',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-pump/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_REDUCER' ),
		'newFeatureclassName': 'SDW_CITY_W_REDUCER',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-reducer/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	},
	{
		'featureclassPath': os.path.join( config.atlasSdePath, r'SDW.CITY.W_REGULATOR_VALVE' ),
		'newFeatureclassName': 'SDW_CITY_W_REGULATOR_VALVE',
		'conservedFielList': [ config.getDataFieldName ],
		'serverRoutes': [
			{
				'route': '/get-w-regulator-valve/',
				'referenceField': 'FAC_SEQ_NUM'
			}
		]
	}
	# {
	# 	'featureclassPath': os.path.join( defaultGdbFullPath, r'W_EXCAVATION' ),
	# 	'conservedFielList': [],
	# 	'serverRoutes': [
	# 		{
	# 			'route':'/get-excavation/',
	# 			'referenceField': 'ID'
	# 		}
	# 	]
	# }
]