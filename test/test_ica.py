import os
import tgi

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


def test_main():
    if os.path.exists(imgOut):
        os.remove(imgOut)
    tgi.main(ica.ICA(imgIn, imgOut, n_bands=3, ot=ot, whiten=True)
    assert os.path.exists(imgOut)
