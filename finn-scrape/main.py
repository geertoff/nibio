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
# fetch listings of sarpsborg
saleurl = 'https://www.finn.no/realestate/businesssale/search.html' + sarpsborg

# get HTML of main page
soup = f.RequestAndScrape(saleurl)
# get URL's of the different listings pages
listing_urls = f.FetchListingsURL(soup)

# fetch available key information of each listing
# f.fetchAvailableKeys(listing_urls)
# f.Sale.fetchAvailablePricingKeys(listing_urls)

# scraping sale listings
f.Sale.scrape_finn(conn, cur, listing_urls )
# scraping rental listings
f.Rent.scrape_finn(conn, cur, listing_urls)

conn.close()

  