import cv2
import logging

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import analysis
import quandl
import visualize

import os

data_direc = ''

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == '__main__':
    data_direc = 'data'


