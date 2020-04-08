#import geopy.geocoder
import logging
import time

import pandas as pd
import openpyxl
import geopy
import os.path

import xlrd
from geopy.extra.rate_limiter import RateLimiter

from tqdm import tqdm

# use google if api key is present else use nominatim
api_key_file = 'google-api-key.txt'
if os.path.isfile(api_key_file):
    from geopy.geocoders import GoogleV3
    with open(api_key_file, 'r') as myfile:
        key = myfile.read()
    geolocator = GoogleV3(api_key=key)
else:
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="geocode_coloss")

# geopy settings
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
