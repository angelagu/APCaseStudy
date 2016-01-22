import Quandl
import os
import pandas as pd

AUTH_TOKEN = 'WiDQpHCymg8Kyvkx4fir'

data_direc = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')

SYMBOL_TO_NAME = {
	'CHRIS/CME_S1': 'soybean_futures',
	'CHRIS/CME_BO1': 'soybean_oil_futures',
	'CFTC/S_F_ALL': 'soybean_ctr',
	'CFTC/BO_F_ALL': 'soybean_oil_ctr'
}

def download_data(symbol, start_date='', end_date=''):
	df = Quandl.get(symbol, trim_start=start_date, trim_end=end_date, authtoken=AUTH_TOKEN)
	df.to_csv('%s/%s.csv' % (data_direc, SYMBOL_TO_NAME[symbol]))

def download_all_data():
	# TODO: not hard code dates
	download_data('CHRIS/CME_S1', '2004-12-31', '2015-12-31')
	download_data('CHRIS/CME_BO1', '2004-12-31', '2015-12-31')
	download_data('CFTC/S_F_ALL', '2004-12-31', '2015-12-31')
	download_data('CFTC/BO_F_ALL', '2004-12-31', '2015-12-31')

if __name__ == '__main__':
	download_all_data()
