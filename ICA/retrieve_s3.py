import argparse
import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys
import error_status as es

logging.basicConfig()
logging.root.setLevel(20)


def list_files_in_bucket(bucket='breaklines',prefix=''):
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(bucket)
    summaries = mybucket.objects.all()
    filelist = []
    position = len(prefix)
    for file in summaries:
        if file.key[:position] == prefix:
            filelist.append(file.key)
    return filelist


def download_file(bucket,key,output_file):
    s3 = boto3.resource('s3')
    try:
        status = s3.Bucket(bucket).download_file(key, output_file)
        return True
    except:
        return False

def download_all(bucket,filelist,output_folder=''):
    status = True
    if len(output_folder) > 0:
        if output_folder[-1:] != '/':
            output_folder = output_folder + '/'
    logging.info('Downloading files')
    for file in filelist:
        base_name = file[file.rfind('/')+1:]
        if base_name[-3:] == 'zip':
            continue
        output_file = '%s%s' % (output_folder,base_name)
        check = download_file(bucket,file,output_file)
        if check is False:
            status = False
            logging.info('Error downloading %s' % file)
            return status
    return status


def main(bucket='breaklines',prefix='',output_folder='/work/Data'):
    filelist = list_files_in_bucket(bucket='breaklines',prefix=prefix)
    status = download_all(bucket,filelist,output_folder)
    if status == False:
        logging.info('Error: Unable to download files')
    return status

def parse_args(args):
    """ Parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--prefix',
                        required=False,
                        help='s3 folder string',
                        default=None)

    parser.add_argument('--bucket',
                        required=False,
                        help='s3 bucket',
                        default=None)
    parser.add_argument('--folder',
                        required=False,
                        help='folder location for download',
                        default='/work/Data')
    return parser.parse_args(args)

def cli():
    logging.info('Downloading inputs from s3 to container/local storage using CLI commands')
    args = parse_args(sys.argv[1:])
    bucket = args.bucket
    prefix = args.prefix
    output_folder = args.folder
    main(bucket,prefix,output_folder)
    sys.exit(0)


if __name__ == '__main__':
    cli()
