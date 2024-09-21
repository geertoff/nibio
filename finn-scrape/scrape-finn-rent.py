# adding data to postgresql database
import psycopg2
from psycopg2.extras import Json
# import local functions
import functions as f
# parse addresses
# from deepparse.parser import AddressParser

# Sarpsborg location
sarpsborg = '?location=1.20002.20023'

# open PostgreSQL connection
conn = psycopg2.connect("host=localhost dbname=finn user=postgres password=postgres")
cur = conn.cursor()

# create address parser object
# address_parser = AddressParser(model_type='bpemb', device=0)

# fetch listings of sarpsborg
renturl = 'https://www.finn.no/realestate/businessrent/search.html' + sarpsborg
# get HTML of main page
soup = f.RequestAndScrape(renturl)
# get URL's of the different listings pages
listing_urls = f.FetchListingsURL(soup)

# fetch available key information of each listing
# f.fetchAvailableKeys(listing_urls)
'''
The fetchAvailableKeys function can be used to check if the available keyinformation attributes are still up to date.
'''

kind = 'rent'
for listing_url in listing_urls : 
    print(listing_url)
    soup = f.RequestAndScrape(listing_url)
    # title of listing
    title = soup.find('h1').text
    # keyinformation
    areal, etasje, overtakelse, bruttoareal, tomt, byggear, renovert_ar, bruksareal, tomteareal, kontorplasser, energimerking, balkong_terasse, parking = f.Rent.fetchKeyInfo(soup)
    # land registry information
    kommune, gardsnr, bruksnr = f.fetchCadastreInfo(soup)
    # type of listing
    type_listing = f.fetchTypeListing(soup, kind)
    # fetch metadata of listing
    finn_id, status_date = f.fetchMetadata(soup)
    # realEstateAgent 
    real_estate_agent_name, img = f.fetchRealEstateInfo(soup)

    # location
    address = soup.find('span', {'data-testid':'object-address'}).text
    # # characteres with å are not geocoded yet...
    # try :
    #     parseaddress, osmaddress, geometry, proj = f.geocodeAddresses(address, address_parser)
    # except Exception as e :
    #     print(e)
    #     parseaddress, osmaddress, geometry, proj = [None] * 4

    try :
        sql = 'insert into rentlisting (finn_id, title, date, typelisting, finnaddress, kommune, gardsnr, bruksnr, areal, bruttoareal, bruksareal, tomteareal, byggear, renovert_ar, overtakelse, tomt, etasje, energimerking, kontorplasser, parking, balkong_terasse, realestate_name, img, listing_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cur.execute(sql, (finn_id, title, status_date, type_listing, address, kommune, gardsnr, bruksnr, areal, bruttoareal, bruksareal, tomteareal, byggear, renovert_ar, overtakelse, tomt, etasje, energimerking, kontorplasser, parking, balkong_terasse, real_estate_agent_name, img, listing_url))
        conn.commit()
        print(f'data inserted for {title}')
    except Exception as e : 
        print(e)
        conn.rollback()
conn.close()
