import os
import main
import boto3
import get_params


def test_download_file():
    get_params.main()
    inKey = os.environ['inKey']
    inBucket = os.environ['inBucket']
    infile = os.environ['infile']
    if os.path.exists(infile):
        os.remove(infile)
    status = main.download_file(inBucket,inKey,infile)
    assert status == True
    assert os.path.exists(infile) == True


def test_upload_results():
    get_params.main()
    outKey = os.environ['outKey']
    inBucket = os.environ['inBucket']
    outBucket = os.environ['outBucket']
    outfile = os.environ['outfile']
    main.download_file(inBucket,outKey,outfile)
    status = main.upload_results(outfile,outBucket,outKey=outKey)
    assert status == True


def test_upload_results_noOutKey():
    get_params.main()
    outKey = os.environ['outKey']
    inBucket = os.environ['inBucket']
    outBucket = os.environ['outBucket']
    outfile = os.environ['outfile']
    main.download_file(inBucket,outKey,outfile)
    status = main.upload_results(outfile,outBucket)
    assert status == True
    

def test_main():
    get_params.main()
    inKey = os.environ['inKey']
    outKey = os.environ['outKey']
    inBucket = os.environ['inBucket']
    outBucket = os.environ['outBucket']
    status = main.main(inBucket,inKey,outBucket=outBucket,outKey=outKey)
    assert status == True


