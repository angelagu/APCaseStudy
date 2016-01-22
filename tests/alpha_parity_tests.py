from nose.tools import *
import unittest
from mock import Mock

import pandas as pd
from src import analysis
from src import quandl

dummy = pd.read_csv('dummy.csv')

def daily_returns_test(df, name, col):
	return analysis.daily_returns(df, name, col)

def cumulative_daily_returns_test(df, name, col):
	return analysis.cumulative_daily_returns(df, name, col)

class testAnalysis(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
    	pass

	def test_daily_returns(self):
		df = analysis.daily_returns(dummy, 'dummy', 'Settle')
		self.assertEqual(df['Daily Returns'][1], 1)

	def test_cumulative_daily_returns(self):
		df = analysis.cumulative_daily_returns(dummy, 'dummy', 'Settle')
		self.assertEqual(df['Cumulative Daily Returns'][-1], 0.95)
 
if __name__ == '__main__':
    unittest.main()