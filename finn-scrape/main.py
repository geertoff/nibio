# adding data to postgresql database
import psycopg2
from psycopg2.extras import Json
# import local functions
import functions as f
# to normalise strings
import unicodedata
from datetime import datetime
# for loading environment variables
import os
from dotenv import load_dotenv
# import adress parser
from deepparse.parser import AddressParser

load_dotenv()

host = os.getenv('PGHOST')
port = os.getenv('PGPORT')
user = os.getenv('PGUSER')
pw = os.getenv('PGPASSWORD')
db = os.getenv('PGDATABASE')

# open PostgreSQL connection
conn = psycopg2.connect(f'host={host} dbname={db} user={user} password={pw}')
cur = conn.cursor()

# generate address parser object
adress_parser = AddressParser()
# Østfold  location
location = '0.20002'

# fetch available key information of each listing
# f.fetchAvailableKeys(listing_urls)
# f.Sale.fetchAvailablePricingKeys(listing_urls)

# # scraping sale listings
print('Scraping listings for sale... \n')
f.Sale.scrape_finn(conn, cur, location, adress_parser)
# scraping rental listings
print('Scraping rental listings... \n')
f.Rent.scrape_finn(conn, cur, location, adress_parser)

conn.close()

  