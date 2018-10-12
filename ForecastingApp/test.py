import SeasonalForecaster as sf
import Parser
import pandas as pd

data = Parser.Parser.xlsParseRawToSeasonalCoeffs("Test/Book1.xlsx")
forecaster = sf.SeasonalForecaster(data)
coeffs = forecaster.get_seasonal_coeffs()
data_predicted = forecaster.forecast()
