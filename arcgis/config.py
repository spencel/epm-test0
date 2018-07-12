import os

thisFilePath = os.path.abspath( __file__ )
arcgisProjectPath = os.path.dirname( thisFilePath )
projectGdbPath = os.path.join( arcgisProjectPath, r'arcgis.gdb' )
atlasSdePath = os.path.join( arcgisProjectPath, r'atlas.sde' )
arcgisInstallPath = r'C:/Program Files/ArcGIS'
propyBatPath = os.path.join( arcgisInstallPath, r'Pro', r'bin', r'Python', r'Scripts', r'propy.bat' )
getDataFieldName = 'get_data'

serverAddress = 'http://10.65.1.173:8840'
