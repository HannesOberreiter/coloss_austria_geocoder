#import geopy.geocoder
import logging
import time

import pandas as pd
import openpyxl
import geopy

import xlrd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from tqdm import tqdm

# geopy settings
geolocator = Nominatim(user_agent="geocode_coloss")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=0)

# progress bar
tqdm.pandas()

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

# Set your output file name here.
output_filename = 'data/output.xlsx'
# Set your input file here
input_filename = "data/data.xlsx"

# read file
df = pd.read_excel(input_filename, sheet_name=0, usecols='G, H, M, W, X', names=['state', 'district', 'id', 'adress', 'zip'], skiprows=2)

# create search string
df['search_string'] = df['adress'] + ',' + df['district'] + ',' + df['state'] + ', Austria'

# request by rows in dataframe
df['location'] = df['search_string'].progress_apply(geocode)
# extract results from response
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

logger.info("Finished geocoding all addresses")

df.to_excel(output_filename, encoding='utf8')
