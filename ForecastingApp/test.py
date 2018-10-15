import SeasonalForecaster as sf
import Parser
import pandas as pd

data = Parser.Parser.xlsParseRawToSeasonalCoeffs("Test/montelucast.xlsx")
forecaster = sf.SeasonalForecaster(data)
#coeffs = forecaster.get_seasonal_coeffs()
data_predicted = forecaster.forecast_lin()
forecaster.export_to_xlsx()
