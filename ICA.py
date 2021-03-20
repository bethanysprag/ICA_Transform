import os
import sys
import numpy as np

# check if gdal is installed
try:
    import gdal
    import ogr
    import osr
except:
    try:
        from osgeo import gdal, ogr, osr
    except:
        print 'Error: gdal not installed on this machine'
        exit

#import matplotlib.pyplot as plt
from scipy import signal
from sklearn.decomposition import FastICA, PCA


def ICA(imgIn, imgOut, n_bands=3, ot='float16', whiten=None):
    img = readImage(imgIn)
    x, y, z = img.shape
    test = np.reshape(img, ((x * y), z))
    if whiten is not None:
        ica = FastICA(n_components=n_bands, whiten=True)
    else:
        ica = FastICA(n_components=n_bands)
    S_ = ica.fit_transform(test)
    outImg = np.reshape(S_, (x, y, n_bands))
    if ot == 'float16':
        outImg_rs = outImg.astype('float16')
        rs = 1
    if ot == 'uint8':
        outImg_rs = Atebit(outImg)
        rs = 1
    if ot == 'uint16':
        outImg_rs = resample16bit(outImg)
        rs = 1
    if rs != 1:
        print 'outType %s not recognized by program' % (ot)
        outImg_rs = outImg.astype(ot)
    saveArrayAsRaster(imgIn, imgOut, outImg_rs)


def resample16bit(img):
    imgMin = img.min()
    offset = (0-imgMin)
    img = img + offset
    img = ((img * 1.0)/img.max()) * 65535
    img = img.astype('uint16')
    return img


def Atebit(img):
    imgMin = img.min()
    offset = (0-imgMin)
    img = img + offset
    img = ((img * 1.0)/img.max()) * 255
    img = img.astype('uint8')
    return img


def readImage(imgPath):
    i1_src = gdal.Open(imgPath)
    i1 = i1_src.ReadAsArray()
    if i1.ndim > 2:
        i1 = np.rollaxis(i1, 0, 3)
    i1_src = None
    return i1


def saveArrayAsRaster(rasterfn, newRasterfn, array):
    raster = gdal.Open(rasterfn)
    # nBands = raster.count
    checksum = array.ndim
    if checksum == 3:
        temp = array.shape
        nBands = temp[2]
    else:
        nBands = 1
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    if array.dtype == 'uint8':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Byte)
    elif array.dtype == 'int16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Int16)
    elif array.dtype == 'float16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Float32)
    elif array.dtype == 'float32':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Float32)
    elif array.dtype == 'int32':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Int32)
    elif array.dtype == 'uint16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_UInt16)
    else:
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_CFloat64)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0,
                               pixelHeight))
    if nBands > 1:
        for i in range(1, (nBands + 1)):
            outband = outRaster.GetRasterBand(i)
            x = i-1
            outband.WriteArray(array[:, :, x])
    else:
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


def usage():
    print("Usage: " + sys.argv[0] + "<imgIn> <imgOut> <n_bands> <outType>\n")
    sys.exit(1)

if __name__ == "__main__":
    imgIn = None
    imgOut = None
    n_bands = None
    ot = None

    if 5 != len(sys.argv):
        usage()

    imgIn = sys.argv[1]
    imgOut = sys.argv[2]
    n_bands = int(sys.argv[3])
    ot = sys.argv[4]
    # print n_bands
    # if n_bands > 10:
    #    print n_bands
    #    sys.exit(1)
    result = ICA(imgIn, imgOut, n_bands=n_bands, ot=ot, whiten=True)
