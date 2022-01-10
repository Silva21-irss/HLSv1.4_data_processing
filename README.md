# HLSv1.4_data_processing
Useful scripts to use in arcpy for processing HLS version 1.4 tiles

First, use 'v1.4 Composite Processing Script&RasterMask.py' to process raw HLS tiles into composites including all usefu;l bands as well as common metrics 
(including NDVI, NBR, and Tassel Cap Transformations)

Second, use 'v1.4 Mosaic Flow and Raster Clip [to current raster]' to produce the final clipped and mosaicked products. Mosaic to a new raster if using composites with the metrics and use 32-bit float rasters, otherwise, mosaic to the existing Landsat HLS composites.
