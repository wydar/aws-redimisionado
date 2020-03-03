import flask
from aws_nubes.views.index import index_bp
from config import S3_BUCKET,S3_KEY,S3_SECRET_ACCESS_KEY
import boto3

app = flask.Flask(__name__)
app.secret_key = 'secret'

app.register_blueprint(index_bp, url_prefix = '')

