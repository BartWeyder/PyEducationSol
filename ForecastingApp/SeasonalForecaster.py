import Forecaster
import pandas as pd
import numpy as np
import uuid

class SeasonalForecaster(Forecaster.Forecaster):
	def __init__(self, raw_data, start_quantity = 400, forecast_period = 24, 
			  start_date = pd.Timestamp.today() + pd.DateOffset(months=2)):
		self.__raw_data = raw_data
		self.__proc_data = None
		self.__seasonal_coeffs = None
		self.__start_month = raw_data.iloc[0,1].month
		self.__start_quantity = start_quantity
		self.__forecast_period = forecast_period
		self.__start_date = start_date

	def forecast(self):
		if self.__seasonal_coeffs is None:
			self.get_seasonal_coeffs()
		
		forecast_data = pd.DataFrame(columns=("Predicted quantity", "Date"))
		print(len(forecast_data["Predicted quantity"]))
		forecast_data.loc[0] = [self.__start_quantity, self.__start_date]
		current_date = self.__start_date + pd.DateOffset(months=1)

		for i in range(1, self.__forecast_period + 1):
			forecast_data.loc[i] = [self.__seasonal_coeffs[current_date.month - 1] * \
				forecast_data["Predicted quantity"][i - 1], current_date]
			current_date += pd.DateOffset(months=1)

		forecast_data["Date"] = pd.to_datetime(forecast_data["Date"], format="%m-%Y")
		self.__proc_data = forecast_data
		return forecast_data

	def export_to_csv(self):
		raise NotImplementedError()

	def get_proc_data(self):
		return self.proc_data

	def seasonal_coeffs(self):
		return self.__seasonal_coeffs

	def get_seasonal_coeffs(self):
		fitted_coeffs = np.polyfit(range(1, len(self.__raw_data[0]) + 1), self.__raw_data[0], 1)
		trend_values = []
		diff = []
		i = 1
		for value in self.__raw_data[0]:
			trend_values.append(fitted_coeffs[1] * i + fitted_coeffs[0])
			diff.append(value / trend_values[-1])

		#calculating mean for every month
		mean_by_monthes = np.zeros(12)
		for i in range(12):
			mean_by_monthes[i] = np.mean(diff[i::12])

		cleared_mean = mean_by_monthes / mean_by_monthes.mean()
		if self.__start_month > 1:
			difference = 12 - self.__start_month + 1
			self.__seasonal_coeffs = np.append(cleared_mean[difference:], cleared_mean[:difference])
		else: 
			self.__seasonal_coeffs = cleared_mean

		return self.__seasonal_coeffs

	def export_to_xlsx(self):
		#make name generator later
		name = str(uuid.uuid4()) + '.xlsx'
		writer = pd.ExcelWriter('ForecastingApp/generated/' + name, engine='xlsxwriter', 
						  datetime_format="mm-yyyy", date_format="mm-yyyy")
		self.__proc_data.to_excel(writer, "Prediction", index = False)
		pd.DataFrame(self.__seasonal_coeffs, columns=["Coeffs by months"]).to_excel(writer, 
																					"Coeffs", index = False)
		writer.sheets["Prediction"].set_column(0, 0, 18)
		writer.sheets["Coeffs"].set_column(0, 0, 18)

		writer.save()
		return name
