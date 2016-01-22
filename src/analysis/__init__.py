import sys
import os
# Ugly hack to import visualize module
sys.path.insert(1, os.path.abspath('..'))
print os.getcwd()

import time
import pandas as pd
import datetime
from scipy.stats import pearsonr
from scipy.spatial.distance import correlation
import numpy as np
import matplotlib.pyplot as plt
import visualize

data_direc = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
plot_direc = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plots')

soybean_futures = 'soybean_futures'
soybean_oil_futures = 'soybean_oil_futures'
soybean_ctr = 'soybean_ctr'
soybean_oil_ctr = 'soybean_oil_ctr'

def daily_returns(df, graph_name, returns_col):
	date_col = 'Date'
	daily_returns_col = 'Daily Returns'
	df[daily_returns_col] = df[returns_col].pct_change(1)
	filename = '%s_daily_returns' %graph_name.lower()
	title = '%s Daily Returns' %graph_name
	visualize.visualize(plot_direc, df, date_col, [daily_returns_col], filename, title=title, ylabel=daily_returns_col, xlabel=date_col)
	return df

def multi_day_features(df, graph_name, returns_col, n):
	date_col = 'Date'
	returns_n = '%s Day Returns' % (str(n))
	roll_n = '%s Day Rolling Average' % (str(n))
	
	df[returns_n] = df[returns_col].pct_change(n)
	df[roll_n] = pd.rolling_mean(df[returns_col], n)
	
	filename_returns = '%s_%s_day_returns' %(graph_name.lower(), str(n))
	title_returns = '%s %s Day Returns' %(graph_name, str(n))

	filename_rolling_average = '%s_%s_day_rolling_average' %(graph_name.lower(), str(n))
	title_rolling_average = '%s %s Day Rolling Average' %(graph_name, str(n))

	visualize.visualize(plot_direc, df, date_col, [returns_n], filename_returns, title=title_returns, ylabel=returns_col, xlabel=date_col)
	visualize.visualize(plot_direc, df, date_col, [roll_n], filename_rolling_average, title=title_rolling_average, ylabel=returns_col, xlabel=date_col)
	return df

def cumulative_daily_returns(df, graph_name, returns_col):
	date_col = 'Date'
	daily_returns_col = 'Cumulative Daily Returns'
	initial_price = df[returns_col][0]
	df[daily_returns_col] = pd.rolling_apply(df[returns_col], 1, lambda x: x / initial_price)
	filename = '%s_cumulative_daily_returns' %graph_name.lower()
	title = '%s Cumulative Daily Returns' %graph_name
	visualize.visualize(plot_direc, df, date_col, [daily_returns_col], filename, title=title, ylabel=daily_returns_col, xlabel=date_col)
	return df

def pearson_correlation(df, col1, col2):
	r_row, p_value = pearsonr(df[col1], df[col2])
	return r_row

def distance_correlation(df, col1, col2):
	return correlation(df[col1], df[col2])

def long_short_ratio(df, graph_name, long_col, short_col):
	date_col = 'Date'
	long_short_ratio_col = 'Long Short Ratio'
	df[long_short_ratio_col] = df[long_col] / df[short_col]
	filename = '%s_long_short_ratio' %graph_name.lower()
	title = '%s Long Short Ratio' %graph_name
	visualize.visualize(plot_direc, df, date_col, [long_short_ratio_col], filename, title=title, ylabel=long_short_ratio_col, xlabel=date_col)
	return df

	df['Long Short Ratio'] = df[long_col] / df[short_col]
	return df

def shift_returns(df, returns_col, n):
	df[returns_col].shift(-n)
	return df

def correlations_vs_shifted_returns(df, feature_col, returns_col):
	x = range(1, 200)
	pearsons = []
	distances = []

	for n in x:
		temp = shift_returns(df, returns_col, n)
		temp = temp[:-n]
		pearsons.append(pearson_correlation(temp, feature_col, returns_col))
		distances.append(distance_correlation(temp, feature_col, returns_col))
	
	filename = 'correlations_vs_%s' %'_'.join((feature_col.lower()).split(' '))
	title = 'Correlations vs Days Shifted for %s' %(feature_col)
	new_df = pd.DataFrame({'Days Shifted': x, 'Pearson Correlations': pearsons, 'Distance Correlations': distances})
	visualize.visualize(plot_direc, new_df, 'Days Shifted', ['Pearson Correlations', 'Distance Correlations'], filename, title=title, ylabel='Correlation', xlabel='Days Shifted')

if __name__ == '__main__':
	soybean_futures = pd.read_csv('%s/%s.csv' %(data_direc, soybean_futures))
	soybean_ctr = pd.read_csv('%s/%s.csv' %(data_direc, soybean_ctr))
	soybean_oil_futures = pd.read_csv('%s/%s.csv' %(data_direc, soybean_oil_futures))
	soybean_oil_ctr = pd.read_csv('%s/%s.csv' %(data_direc, soybean_oil_ctr))

	soybean = pd.merge(soybean_futures, soybean_ctr, how='inner', on='Date')
	soybean_oil = pd.merge(soybean_oil_futures, soybean_oil_ctr, how='inner', on='Date')

	correlations_vs_shifted_returns(soybean, 'Total Reportable Shorts', 'Settle')
	correlations_vs_shifted_returns(soybean, 'Total Reportable Longs', 'Settle')

	soybean = daily_returns(soybean, 'Soybean', 'Settle')
	soybean_oil = daily_returns(soybean_oil, 'Soybean Oil', 'Settle')

	soybean = cumulative_daily_returns(soybean, 'Soybean', 'Settle')
	soybean_oil = cumulative_daily_returns(soybean_oil, 'Soybean_Oil', 'Settle')

	long_short_ratio(soybean_ctr, 'Soybean', 'Total Reportable Longs', 'Total Reportable Shorts')
	long_short_ratio(soybean_oil_ctr, 'Soybean_Oil', 'Total Reportable Longs', 'Total Reportable Shorts')

	soybean = multi_day_features(soybean, 'Soybean', 'Settle', 5)
	soybean_oil = multi_day_features(soybean_oil, 'Soybean_Oil', 'Settle', 5)

	soybean = multi_day_features(soybean, 'Soybean', 'Settle', 10)
	soybean_oil = multi_day_features(soybean_oil, 'Soybean_Oil', 'Settle', 10)

	soybean = shift_returns(soybean, 'Settle', 1)
	soybean = soybean[:-1]

	soybean = shift_returns(soybean, 'Settle', 1)
	soybean_oil = soybean_oil[:-1]

	soybean.to_csv('%s/%s.csv' %(data_direc, 'soybean_merged'))
	soybean_oil.to_csv('%s/%s.csv' %(data_direc, 'soybean_oil_merged'))

	# Combining the soybean data and soybean oil data to see correlation
	combined = pd.merge(soybean_futures, soybean_oil_futures, suffixes=[' Soybean', ' Soybean Oil'], how='inner', on='Date')
	# Normalizing both datasets so they're the same scale
	combined['Settle Soybean'] = (combined['Settle Soybean'] - combined['Settle Soybean'].mean()) / (combined['Settle Soybean'].max() - combined['Settle Soybean'].min())
	combined['Settle Soybean Oil'] = (combined['Settle Soybean Oil'] - combined['Settle Soybean Oil'].mean()) / (combined['Settle Soybean Oil'].max() - combined['Settle Soybean Oil'].min())
	print 'Pearson Correlation between Soybean and Soybean'
	print pearson_correlation(combined, 'Settle Soybean', 'Settle Soybean Oil')
	visualize.visualize(plot_direc, combined, 'Date', ['Settle Soybean', 'Settle Soybean Oil'], 'soybean_and_oil_price', title='Soybean and Soybean Oil Price', ylabel='Settle', xlabel='Date')


