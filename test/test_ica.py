import os
import ICA

imgOut = 'test/testImage_ica.tif'
imgIn = 'test/testImage.tif'
ot = 'float16'



def test_readImage():
    img = tgi.readImage(imgIn)
    #assert img is not None
    assert img is not None
    img = None


def test_ica():
    img = ica.readImage(imgIn)
    green = ica.ICA(imgIn, imgOut, n_bands=3, ot=ot, whiten=True)
    assert ica is not None
    ica=None


def test_parse_args():
    args=['-i', 'test/testImage.tif', '-o', 'test/testImage_ica.tif', '-b', 3, -ft 'float16']
    arguments = tgi.parse_args(args)
    assert arguments.input == 'inputImage.tif'
