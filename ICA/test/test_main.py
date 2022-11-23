import os
import main
import boto3

# set these from the parameter store
imgOut = 'test/testImage_ica.tif'
inKey = 'test/testImage.tif'
outKey = 'test/result1.tif'
inBucket = '195614500004-ica-testing'
outBucket = '195614500004-ica-testing'
infile = '/work/Data/ica_input.tif'
outfile = '/work/Data/ica_output.tif'
ot = 'float16'


def test_download_file():
    if os.path.exists(infile):
        os.remove(infile)
    status = main.download_file(inBucket,inKey,infile)
    assert status == True
    assert os.path.exists(infile) == True


def test_upload_results():
    status = main.upload_results(outfile,outBucket,outKey=outKey)
    assert status == True


def test_upload_results_noOutKey():
    status = main.upload_results(outfile,outBucket)
    assert status == True
    

def test_main():
    status = main.main(inBucket,inKey,outBucket=outBucket,outKey=outKey)
    assert status == True


