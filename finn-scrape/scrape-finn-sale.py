# adding data to postgresql database
import psycopg2
from psycopg2.extras import Json
# import local functions
import functions as f
# to normalise strings
import unicodedata


# Sarpsborg location
sarpsborg = '?location=1.20002.20023'

# open PostgreSQL connection
conn = psycopg2.connect("host=localhost dbname=finn user=postgres password=postgres")
cur = conn.cursor()

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
    print(listing_url)
    soup = f.RequestAndScrape(listing_url)

    # title of listing
    title = soup.find('h1').text

    try :
        price = soup.find('div', {'data-testid': 'pricing-indicative-price'}).find('span', class_ = 'font-bold').text
         # normalise string
        price = unicodedata.normalize('NFKD', price)   
    except Exception as e :
        price = None
        
    
    # pricing information
    totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi = f.Sale.fetchPricingInfo(soup)

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

    try :
        sql = 'insert into salelisting (finn_id, title, date, typelisting, address, kommune, gardsnr, bruksnr, price, totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi, areal, bruttoareal, bruksareal, tomteareal, eieform, primaerrom, byggear, overtakelse, tomt, etasje, energimerking, realestate_name, img, listing_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cur.execute(sql, (finn_id, title, status_date, type_listing, address, kommune, gardsnr, bruksnr, price, totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi, areal, bruttoareal, bruksareal, tomteareal, eieform, primaerrom, byggear, overtakelse, tomt, etasje, energimerking, real_estate_agent_name, img, listing_url))
        conn.commit()
        print(f'data inserted for {title}')
    except Exception as e : 
        print(e)
        conn.rollback()
conn.close()

  