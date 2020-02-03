from flask import Flask
from flask_restful import Api

#directory details
UPLOAD_FOLDER = ''

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
api = Api(app)
