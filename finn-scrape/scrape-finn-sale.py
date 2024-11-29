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


current_date = datetime.now().strftime('%Y%m%d')
# create dynamic table_name
table_name = f'{current_date}_salelisting'

# load salelisting SQL 
sql_file = 'salelisting.sql'

with open(sql_file, 'r') as file :
    sql = file.read()
    
# replace tablename from sql file to dynamic table_name
sql = sql.replace('salelisting', f'"{table_name}"')
# create new dynamic table
cur.execute(sql)
conn.commit()
print(f'Table {table_name} is created')

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
kind = 'sale'
for listing_url in listing_urls :
    url = 'https://www.finn.no' + listing_url
    soup = f.RequestAndScrape(url)

    # title of listing
    title = soup.find('h1').text

    try :
        price = soup.find('div', {'data-testid': 'pricing-indicative-price'}).find('span', class_ = 'font-bold').text
         # normalise string
        price = unicodedata.normalize('NFKD', price)   
    except Exception as e :
        price = None
        
    # pricing information
    try :
        totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi = f.Sale.fetchPricingInfo(soup)
    except Exception as e : 
        print('No pricing information on listing')
    # land registry information
    kommune, gardsnr, bruksnr = f.fetchCadastreInfo(soup)
    # type of listing
    type_listing = f.fetchTypeListing(soup, kind)

    # fetch metadata of listing
    finn_id, status_date = f.fetchMetadata(soup)

    # keyinformation
    bruksareal, bruttoareal, etasje, eieform, areal, byggear, tomteareal, overtakelse, tomt, energimerking, primaerrom = f.Sale.fetchKeyInfo(soup)

    # realEstateAgent 
    real_estate_agent_name, img = f.fetchRealEstateInfo(soup)
    
    address = soup.find('span', {'data-testid':'object-address'}).text
    current_day = datetime.today().strftime('%d-%m-%Y')
    try :
        sql = f'insert into "{table_name}" (finn_id, title, date_upload, date_listing, typelisting, address, kommune, gardsnr, bruksnr, price, totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi, areal, bruttoareal, bruksareal, tomteareal, eieform, primaerrom, byggear, overtakelse, tomt, etasje, energimerking, realestate_name, img, listing_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cur.execute(sql, (finn_id, title, current_day, status_date, type_listing, address, kommune, gardsnr, bruksnr, price, totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi, areal, bruttoareal, bruksareal, tomteareal, eieform, primaerrom, byggear, overtakelse, tomt, etasje, energimerking, real_estate_agent_name, img, listing_url))
        conn.commit()
        print(f'data inserted for {title}')
    except Exception as e : 
        print(e)
        conn.rollback()
conn.close()

  