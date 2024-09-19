#import sys
#sys.path.insert(1, '/media/hog/fringe1/dev/src/sentinel1helper/')
# caution: path[0] is reserved for script path (or '' in REPL)
# https://www.geeksforgeeks.org/python-import-module-from-different-directory/

#export PYTHONPATH='/media/hog/fringe1/dev/src/sentinel1helper/'

#from sentinel1helper import * 
import sentinel1helper as s1h
import geopandas as gpd

in_file = 'file:///media/hog/fringe1/sc/MSCDATA/Roenne-Overview/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
layer = 'tl5_d_139_01_mscaoi'


gdf = gpd.read_file(in_file, layer=layer)