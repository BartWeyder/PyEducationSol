"""
The flask application package.
"""

UPLOAD_FOLDER = '/ForecastingApp/uploads'
GENERATED_FOLDER = '/ForecastingApp/generated/'

from flask import Flask
from os import getcwd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = getcwd() + GENERATED_FOLDER

import ForecastingApp.views
