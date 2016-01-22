import matplotlib.pyplot as plt
from matplotlib import gridspec
import pandas as pd
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import datetime

def visualize(data_direc, df, x_col, y_col, filename, title='', ylabel='', xlabel=''):
    gs = gridspec.GridSpec(2, 1)
    gs.update(hspace=0.5, right=0.9)

    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    make_line_plot(
        ax,
        df,
        x_col,
        y_col,
        title=title,
        ylabel=ylabel,
        xlabel=xlabel,
        )
    fig.autofmt_xdate()
    plt.savefig('%s/%s.png' % (data_direc, filename))

def make_line_plot(ax, df, x_col, y_col, 
        title='', 
        ylabel='',
        xlabel='',
        ):

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if x_col == 'Date':
        dates = [datetime.datetime.strptime(x, "%Y-%m-%d").date() for x in df[x_col]]
        for col in y_col:
            ax.plot(dates, df[col], label=col)
        years = YearLocator()
        months = MonthLocator()
        yearsFmt = DateFormatter('%Y')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.fmt_xdata = DateFormatter(yearsFmt)
    else:
        for col in y_col:
            ax.plot(df[x_col], df[col], label=col)

    if len(y_col) > 1:
        ax.legend(bbox_to_anchor=(1.05, 1))

