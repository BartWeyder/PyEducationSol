import pandas as pd

class Parser:
	def csvParseRawToSeasonalCoeffs(filepath: str):
		data = pd.read_csv(filepath, header = None)
		return data
	def xlsParseRawToSeasonalCoeffs(filepath: str):
		data = pd.read_excel(filepath, header = None)
		return data


