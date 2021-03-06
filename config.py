"""
Project configuration file.

Extract environment variables to be used as global constants
in the rest of the project.
"""

import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

URL_NOV_2017_SALE = os.getenv('URL_NOV_2017_SALE')
URL_MAR_2018_SALE = os.getenv('URL_MAR_2018_SALE')

NOV_2017_SALE_DATA_CSV = 'nov_2017_data.csv'
MAR_2018_SALE_DATA_CSV = 'mar_2018_data.csv'

GBP_TO_USD_EXCHANGE_RATE = 1.32

REPORT_CSV = 'report.csv'
