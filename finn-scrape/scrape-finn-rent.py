# adding data to postgresql database
import psycopg2
from psycopg2.extras import Json
# import local functions
import functions as f
# parse addresses
from deepparse.parser import AddressParser

saleurl = 'https://www.finn.no/realestate/businesssale/search.html'
renturl = 'https://www.finn.no/realestate/businessrent/search.html'
# Sarpsborg location
sarpsborg = '?location=1.20002.20023'

# open PostgreSQL connection
# conn = psycopg2.connect("host=localhost dbname=finn user=postgres password=postgres")
# cur = conn.cursor()

# create address parser object
# address_parser = AddressParser(model_type='bpemb', device=0)

# fetch listings of sarpsborg
renturl = renturl + sarpsborg
# get HTML of main page
soup = f.RequestAndScrape(renturl)
# get URL's of the different listings pages
listing_urls = f.FetchListingsURL(soup)

f.fetchAvailableKeys(listing_urls)