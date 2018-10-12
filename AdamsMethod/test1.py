import coverage

cov = coverage.coverage()

import unittest
import AdamsMethod
import math

def func(x, y):
	return (0.3 * x) + (y ** 2)

class Test_test1(unittest.TestCase):
	def setUp(self):
		cov.start()
		self.am = AdamsMethod.AdamsMethod(0, 3, 0.4, 0.001, func)
		cov.stop()
		cov.save()
		cov.html_report()

	def test_value_1(self):
		cov.start()
		self.assertTrue(abs(self.am.get_value(1) - 0.9056) < 0.001)
		cov.stop()
		cov.save()
		cov.html_report()

	def test_value_2(self):
		cov.start()
		self.assertTrue(self.am.get_value(1.98) == float("inf"))
		cov.stop()
		cov.save()
		cov.html_report()

		

if __name__ == '__main__':
    unittest.main()