import os
import sys
import argparse
import numpy as np
import logging
import gdal
import ogr
import osr
from scipy import signal
from sklearn.decomposition import FastICA, PCA


logging.basicConfig()
logger = logging.getLogger(__name__)


def parse_args(args):
    """ Parse arguments for the ICA Transformation """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i',
                        '--input',
                        help='Input image',
                        required=True)
    parser.add_argument('-b',
                        '--bands',
                        help='Number of output transform bands',
                        default=3,
                        nargs=1,
                        type=int)

    parser.add_argument('-o',
                        '--outfile',
                        required=True,
                        help='Output Filename')
    parser.add_argument('-ft',
                        '-filetype',
                        required=False,
                        help='Output Filetype, default=float16')
    h = '0: Quiet, 1: Debug, 2: Info, 3: Warn, 4: Error, 5: Critical'
    parser.add_argument('--verbose', help=h, default=2, type=int)
    return parser.parse_args(args)


def ICA(imgIn, imgOut, n_bands=3, ot='float16', whiten=None):
    """ Performs Independent Component analysis on a tif format image """
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
        logging.info('outType %s not recognized by program' % (ot))
        outImg_rs = outImg.astype(ot)
    saveArrayAsRaster(imgIn, imgOut, outImg_rs)


def resample16bit(img):
    """ Resamples img to 16-bit datatype """
    logging.info('resampling img to 16-bit')
    imgMin = img.min()
    offset = (0-imgMin)
    img = img + offset
    img = ((img * 1.0)/img.max()) * 65535
    img = img.astype('uint16')
    return img


def Atebit(img):
    """ Resamples input img to 8-bit datatype """
    logging.info('resampling img to 8-bit')
    imgMin = img.min()
    offset = (0-imgMin)
    img = img + offset
    img = ((img * 1.0)/img.max()) * 255
    img = img.astype('uint8')
    return img


def readImage(imgPath):
    """ Reads input image to numpy array """
    logging.info('Reading img: %s' % imgPath)
    i1_src = gdal.Open(imgPath)
    i1 = i1_src.ReadAsArray()
    if i1.ndim > 2:
        i1 = np.rollaxis(i1, 0, 3)
    i1_src = None
    return i1


def saveArrayAsRaster(rasterfn, newRasterfn, array):
    """ Saves numpy array to geotiff """
    logging.info('Saving output img as %s' % newRasterfn)
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


def cli():
    """ Performs Independent Component Analysis using CLI commands """
    logger.info('Performing ICA using CLI commands')
    args = parse_args(sys.argv[1:])
    imgIn = args.input
    imgOut = args.outfile
    n_bands = args.bands
    ot = args.ft
    logger.setLevel(args.verbose * 10)
    ICA(imgIn, imgOut, n_bands=n_bands, ot=ot, whiten=True)
    sys.exit(0)


if __name__ == '__main__':
    cli()
