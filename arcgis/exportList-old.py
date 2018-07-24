import os
import config

exportFeatureclasses = [
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
	}
]