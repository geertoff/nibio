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

load_dotenv()

host = os.getenv('PGHOST')
port = os.getenv('PGPORT')
user = os.getenv('PGUSER')
pw = os.getenv('PGPASSWORD')
db = os.getenv('PGDATABASE')

# open PostgreSQL connection
conn = psycopg2.connect(f'host={host} dbname={db} user={user} password={pw}')
cur = conn.cursor()

# Sarpsborg location
sarpsborg = '?location=1.20002.20023'

# fetch available key information of each listing
# f.fetchAvailableKeys(listing_urls)
# f.Sale.fetchAvailablePricingKeys(listing_urls)

# scraping sale listings
print('Scraping listings for sale... \n')
f.Sale.scrape_finn(conn, cur, sarpsborg )
# scraping rental listings
print('Scraping rental listings... \n')
f.Rent.scrape_finn(conn, cur, sarpsborg)

conn.close()

  