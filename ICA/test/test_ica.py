import os
import ICA

imgOut = 'test/testImage_ica.tif'
imgIn = 'test/testImage.tif'
ot = 'float16'


def test_readImage():
    img = ICA.readImage(imgIn)
    #assert img is not None
    assert img is not None
    img = None


def test_ica():
    if os.path.exists(imgOut):
        os.remove(imgOut)
    img = ICA.readImage(imgIn)
    ICA.ICA(imgIn, imgOut, n_bands=3, ot=ot, whiten=True)
    assert os.path.exists(imgOut)


def test_parse_args():
    args=['-i', 'test/testImage.tif', '-o', 'test/testImage_ica.tif', '-b', '3', '-ft', 'float16']
    arguments = ICA.parse_args(args)
    assert arguments.input == imgIn
