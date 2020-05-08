#import geopy.geocoder
import logging
import time

import pandas as pd
import openpyxl
import os.path

import xlrd

import geopy
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut

from tqdm import tqdm

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
# progress bar
tqdm.pandas()

# Set your output file name here.
output_filename = 'data/output.xlsx'
# Set your input file here
input_filename = "data/data2.xlsx"

# use google if api key is present else use nominatim
api_key_file = 'google-api-key.txt'
if os.path.isfile(api_key_file):
    from geopy.geocoders import GoogleV3
    with open(api_key_file, 'r') as myfile:
        key = myfile.read()
    print("####################################")
    print("Fetching from Google Geocoder - API")
    print("####################################")
    geolocator = GoogleV3(api_key=key)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.025, max_retries=10)

else:
    from geopy.geocoders import Nominatim
    print("####################################")
    logger.info("Fetching from Using Nominatim Geocoder - API")
    print("####################################")
    geolocator = Nominatim(user_agent="geocode_coloss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=0)

def check_import():
    global input_filename
    if(os.path.isfile(input_filename) == False):
        print("!!!!! WARNING !!!!!")
        logger.warning("Using example excel file, not data file found")
        input_filename = "data/example.xlsx"
    return True

def do_geocode(search_string):
    try:
        print("Geocoding ---- ", search_string)
        x = geocode(search_string)
        return x
    except GeocoderTimedOut:
        print("Time Out ---- ", search_string)
        return False    

def import_excel():
    df = pd.read_excel(input_filename, sheet_name=0, usecols=['id', 'searchstring'])
    print("####################################")
    print("Imported Rows:")
    print(df)
    print("####################################")
    return df

def import_excel_austria():
    df = pd.read_excel(input_filename, sheet_name=0, usecols='G, H, M, W, X', names=['state', 'district', 'id', 'adress', 'zip'], skiprows=2)
    df['search_string'] = df['adress'] + ',' + df['district'] + ',' + df['state'] + ', Austria'
    return df

def geocode_df(df):
    # request by rows in dataframe
    df['location'] = df['searchstring'].progress_apply(do_geocode)
    # extract results from response
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
    print("####################################")
    print("Finished geocoding all addresses")
    print("####################################")
    return df


def export_excel(df):
    try:
        df.to_excel(output_filename, encoding='utf8')
        print("####################################")
        logger.info("Output saved")
        print("####################################")
    except:
        print("####################################")
        logger.warning("Error saving file")
        print("####################################")

def append_excel(df):
    book = openpyxl.load_workbook(output_filename)
    writer = pd.ExcelWriter(output_filename, engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    for sheetname in writer.sheets:
        df.to_excel(writer,sheet_name=sheetname, startrow=writer.sheets[sheetname].max_row, index = True, header= False, encoding='utf8')
    writer.save()


def main():
    import_filename = check_import()
    df = import_excel()
    # df = import_excel_austria()
    # subsett if needed
    # df = df[1:100]
    geocodes = geocode_df(df)
    export_excel(geocodes)
    

if __name__ == "__main__":
   main()

