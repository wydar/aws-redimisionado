import os
import boto3


S3_BUCKET = os.environ.get('S3_BUCKET')
S3_KEY = os.environ.get('S3_KEY')
S3_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')

s3 = boto3.setup_default_session(region_name='eu-central-1')
s3 = boto3.client(
    's3',
    aws_access_key_id = 'AKIAZYT5UCPGBRFQW3NV',
    aws_secret_access_key = '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'
)

#boto3.set_stream_logger('')

s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket('proyectofinalnubes')

__TableName__ = "Imagenes"
db = boto3.resource('dynamodb')
table = db.Table(__TableName__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
images_directory = os.path.join(APP_ROOT, 'images_tmp')

if not os.path.isdir(images_directory):
    os.mkdir(images_directory)