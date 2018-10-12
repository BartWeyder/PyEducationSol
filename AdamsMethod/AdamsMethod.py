class AdamsMethod:
	def __init__(self, a, b, y0, h, f):
		# number of pre-calculated values.  It's = 4 by formulae
		n = 4
		self.values = self.eiler_method(a, b, h, y0, n, f)
		xn = self.values[0][n]
		i = n
		while xn <= b:
			i += 1
			try:
				f0 = f(self.values[0][i - 1], self.values[1][i - 1])
				f1 = f(self.values[0][i - 2], self.values[1][i - 2])
				f2 = f(self.values[0][i - 3], self.values[1][i - 3])
				f3 = f(self.values[0][i - 4], self.values[1][i - 4])
			except:
				break
			self.values[0].append(round(h + self.values[0][i - 1], 3))
			self.values[1].append(self.values[1][i - 1] + h / 24 * (55 * f0 - 59 * f1 + 37 * f2 - 9 * f3))
			xn += h
			xn = round(xn, 3)

	def eiler_method(self, a, b, h, y0, n, f):
		i = 0
		values = [[], []]
		values[0].append(a)
		values[1].append(y0)
		while i < n:
			i += 1
			values[0].append((round(values[0][i - 1] + h, 3)))
			values[1].append(values[1][i - 1] + h * f(values[0][i - 1], values[1][i - 1]))

		return values

	def get_value(self, x):
		temp = self.values[0][len(self.values[0]) - 1]
		if x <= temp: return self.values[1][self.values[0].index(x)]
		return float("inf");