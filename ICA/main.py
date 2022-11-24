import os
import sys
import argparse
import logging
import boto3
import ICA as ica


def download_file(bucket,key,output_file):
    s3 = boto3.resource('s3')
    try:
        logging.error('Downloading key:%s from bucket: %s' % (key,bucket))
        status = s3.Bucket(bucket).download_file(key, output_file)
        return True
    except Exception as e:
        logging.error('unable to download key:%s from bucket: %s' % (key,bucket))
        logging.error(e)
        return False


def upload_results(outfile,outBucket,outKey=None):
    """ returns resulting geotiff to specified outBucket using provided key
        outBucket by default is the same as inBucket
        outKey by default uses the same prefix as incoming key with naming
        convention 'ica-${input_file_name}.tif'
    """
    # If outKey is not provided use the same prefix with the filename 'ica-${input_file_name}.tif'
    if outKey is None:
        filename = os.path.basename(outfile)
        prefix = os.path.dirname(outfile)
        outname = 'ICA-' + filename
        outKey=os.path.join(prefix,outname)
        logging.info('No outKey. Defaulting to %s' % outKey)
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(outfile, outBucket, outKey) # returns no response at all 
        res = s3_client.list_objects_v2(Bucket=outBucket, Prefix=outKey, MaxKeys=1)
        status = 'Contents' in res
    except Exception as e:
        logging.error(e)
        return False
    return status
    

def main(inBucket,inKey,outBucket=None,outKey=None,**kwargs): #great opportunity for kwargs
    """ Retrieves files from s3, runs ICA library, then returns output to s3 """
    infile = '/work/Data/ica_input.tif'
    outfile = '/work/Data/ica_output.tif'
    status = download_file(inBucket,inKey,infile)
    if status == False:
        return False
    ica.ICA(infile, outfile, **kwargs)
    if outBucket is None:
        logging.info('No outBucket. Defaulting to inBucket')
        outBucket = inBucket
    status = upload_results(outfile,outBucket,outKey)
    return status


def cli():
    """ Parses CLI commands """
    logger.info('Performing ICA using CLI commands')
    args = parse_args(sys.argv[1:])
    imgIn = args.input
    imgOut = args.outfile
    n_bands = args.bands
    ot = args.ft
    logger.setLevel(args.verbose * 10)
    main(imgIn, imgOut, n_bands=n_bands, ot=ot, whiten=True)
    sys.exit(0)


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


if __name__ == '__main__':
    cli()
