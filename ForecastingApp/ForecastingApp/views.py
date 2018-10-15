"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, send_file
from ForecastingApp import app
import pandas as pd

ALLOWED_EXTENSIONS = set(['xlsx'])

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Seasonal Forecast description.'
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/seasonal-forecast', methods=['GET', 'POST'])
def seasonal_forecast():
	import SeasonalForecaster
	import Parser


	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if request.form['start_date']:
			start_date = pd.Timestamp(request.form['start_date'])
		else: start_date = pd.Timestamp.today()
		if request.form['start_quantity']:
			start_quantity = float(request.form['start_quantity'])
		else: start_quantity = 400
		if request.form['period']:
			forecast_period = int(request.form['period'])
		else: forecast_period = 24
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			f = SeasonalForecaster.SeasonalForecaster(Parser.Parser.xlsParseRawToSeasonalCoeffs(file), 
										 start_quantity, forecast_period, start_date)
			f.forecast()
			returnfilename = f.export_to_xlsx()
			#filename = secure_filename(file.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return send_file(app.config['GENERATED_FOLDER'] + returnfilename)

	return render_template(
		'seasonal-forecast.html',
		title='Seasonal Forecast',
		year=datetime.now().year,
        message='Seasonal Forecast Form'
	)

@app.route('/seasonal-forecast-linear', methods=['GET', 'POST'])
def seasonal_forecast_lin():
	import SeasonalForecaster
	import Parser


	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if request.form['start_date']:
			start_date = pd.Timestamp(request.form['start_date'])
		else: start_date = pd.Timestamp.today()
		if request.form['start_quantity']:
			start_quantity = float(request.form['start_quantity'])
		else: start_quantity = 400
		if request.form['period']:
			forecast_period = int(request.form['period'])
		else: forecast_period = 24
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			f = SeasonalForecaster.SeasonalForecaster(Parser.Parser.xlsParseRawToSeasonalCoeffs(file), 
										 start_quantity, forecast_period, start_date)
			f.forecast_lin()
			returnfilename = f.export_to_xlsx()
			return send_file(app.config['GENERATED_FOLDER'] + returnfilename)

	return render_template(
		'seasonal-forecast.html',
		title='Seasonal Forecast Linear',
		year=datetime.now().year,
        message='Seasonal Forecast Form'
	)