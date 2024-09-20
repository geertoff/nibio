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
address_parser = AddressParser(model_type='bpemb', device=0)

# fetch listings of sarpsborg
renturl = renturl + sarpsborg
# get HTML of main page
soup = f.RequestAndScrape(renturl)
# get URL's of the different listings pages
listing_urls = f.FetchListingsURL(soup)

# fetch available key information of each listing
# f.fetchAvailableKeys(listing_urls)
'''
The fetchAvailableKeys function can be used to check if the available keyinformation attributes are still up to date.
'''

for listing_url in listing_urls : 
    print(listing_url)
    soup = f.RequestAndScrape(listing_url)
    # title of listing
    title = soup.find('h1').text
    
    # keyinformation
    areal, etasje, overtakelse, bruttoareal, tomt, byggear, renovert_ar, bruksareal, tomteareal, kontorplasser, energimerking, balkong_terasse, parking = f.findKeyInfo(soup)

    # land registry information
    kommune, gardsnr, bruksnr = f.fetchCadastreInfo(soup)
        
    # fetch metadata of listing
    finn_id, status_date = f.fetchMetadata(soup)

    # location
    address = soup.find('span', {'data-testid':'object-address'}).text
    # characteres with å are not geocoded yet...
    try :
        parseaddress, osmaddress, geometry, proj = f.geocodeAddresses(address, address_parser)
    except Exception as e :
        print(e)
        geometry = None
        proj = None 
