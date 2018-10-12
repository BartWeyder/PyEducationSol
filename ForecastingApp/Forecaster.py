class Forecaster:
	def __init__(self, raw_data):
		self.__raw_data = raw_data
		self.__proc_data = None
	def forecast(self):
		raise NotImplementedError()

	def export_to_csv(self):
		raise NotImplementedError()

	def get_proc_data(self):
		return self.proc_data

	def export_to_xlsx(self):
		raise NotImplementedError()

	
