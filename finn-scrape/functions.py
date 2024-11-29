import requests
# for webscraping
from bs4 import BeautifulSoup
# Regular Expression for splitting strings
import re
# to normalise strings
import unicodedata
# for working with spatial data
from osgeo import ogr, osr
import psycopg2
from datetime import datetime
# normalise strings
import unicodedata

def RequestAndScrape(url) :
    r = requests.get(url)
    if r.status_code == 200 :
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    else :
        print('Bad Request:', r.status_code)

def FetchListingsURL(soup) :
    listing_data = []
    # find the listings in articles with the following class
    listings = soup.find_all('a', {'class':'sf-search-ad-link'} )
    for listing in listings : 
        # get the value of the url
        listing_url = listing['href']
        listing_data.append(listing_url)
    return listing_data

def fetchAvailableKeys(listing_urls) :
    keyinfo = []
    for url in listing_urls : 
        soup = RequestAndScrape(url)
        keyinfodivs = soup.find('section', {'aria-labelledby':'keyinfo-heading'}).find_all('div')
        for div in keyinfodivs : 
            if div.has_attr('data-testid') :
                try :
                    attr = div.find('dt').text
                except Exception as e : 
                    attr = ''
                if attr not in keyinfo :
                    keyinfo.append(attr)
    print('Available keyinformation :')
    print(keyinfo)
def FetchAllListingsURL(url, location) : 
    all_listing_urls = []        
    j = 1
    while True :
        pageurl = f'{url}?location={location}&page={j}'
        # get HTML of main page
        soup = RequestAndScrape(pageurl)
        # get URL's of the different listings pages
        listing_urls = FetchListingsURL(soup)
        # add listing urls to all_listing_urls
        all_listing_urls.extend(listing_urls)

        # if there are less than 50 listings on one page, there are no more listings available
        if len(listing_urls) < 50 : 
            break
        # if there are more pages available, increase pagination
        j += 1
        pageurl = ''
    return all_listing_urls


class Rent : 
    def scrape_finn(conn, cur, location) : 
        kind = 'rentlisting'
        # create dynamic tablename 
        current_date = datetime.now().strftime('%Y%m%d')
        table_name = f'{current_date}_{kind}'
        # create new table using that name
        createDynamicTable(conn, cur, table_name, kind)

        url = 'https://www.finn.no/realestate/businessrent/search.html'
        all_listing_urls = FetchAllListingsURL(url, location)
        print(f'{len(all_listing_urls)} listings found \n')

        for listing_url in all_listing_urls : 
            if 'https' not in listing_url :
                url = 'https://www.finn.no' + listing_url
            else :
                url = listing_url
            soup = RequestAndScrape(url)
            # title of listing
            title = soup.find('h1').text
            # keyinformation
            areal, etasje, overtakelse, bruttoareal, tomt, byggear, renovert_ar, bruksareal, tomteareal, kontorplasser, energimerking, balkong_terasse, parking = Rent.fetchKeyInfo(soup)
            # land registry information
            kommune, gardsnr, bruksnr = fetchCadastreInfo(soup)
            # type of listing
            type_listing = fetchTypeListing(soup, 'rent')
            # fetch metadata of listing
            finn_id, status_date = fetchMetadata(soup)
            # realEstateAgent 
            real_estate_agent_name, img = fetchRealEstateInfo(soup)

            # location
            address = soup.find('span', {'data-testid':'object-address'}).text
            current_day = datetime.today().strftime('%d-%m-%Y')

            try :
                sql = f'insert into "{table_name}" (finn_id, title, date_upload, date_listing, typelisting, address, kommune, gardsnr, bruksnr, areal, bruttoareal, bruksareal, tomteareal, byggear, renovert_ar, overtakelse, tomt, etasje, energimerking, kontorplasser, parking, balkong_terasse, realestate_name, img, listing_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(sql, (finn_id, title, status_date, current_day, type_listing, address, kommune, gardsnr, bruksnr, areal, bruttoareal, bruksareal, tomteareal, byggear, renovert_ar, overtakelse, tomt, etasje, energimerking, kontorplasser, parking, balkong_terasse, real_estate_agent_name, img, listing_url))
                conn.commit()
                print(f'data inserted for {title}')
            except Exception as e : 
                print(e)
                conn.rollback()
            print('Finished scraping rental listings')


    # fetch section of key info. This informtion is located in 'data-testid' divs. 
    def fetchKeyInfo(soup) :
        # defining local variables  
        areal, etasje, overtakelse, bruttoareal, tomt, byggear, renovert_ar, bruksareal, tomteareal, kontorplasser, energimerking, balkong_terasse, parking = [None] * 13

        keyinfodivs = soup.find('section', {'aria-labelledby':'keyinfo-heading'}).find_all('div')
        for div in keyinfodivs :
            if div.has_attr('data-testid') :
                try :
                    attr = div.find('dt').text
                except Exception as e :
                    attr = ''
                # if there is not a 'dt' class in the div the match-case should be skipped
                if len(attr) > 0 :
                    match attr :
                        case 'Areal' :
                            areal = div.find('dd').text
                        case 'Etasje' :
                            etasje = div.find('dd').text
                        case 'Overtakelse' :
                            overtakelse = div.find('dd').text
                        case 'Bruttoareal' :
                            bruttoareal = div.find('dd').text
                        case 'Tomt' :
                            tomt = div.find('dd').text
                        case 'Byggeår' : 
                            byggear = div.find('dd').text
                        case 'Renovert år' :
                            renovert_ar = div.find('dd').text
                        case 'Bruksareal' :
                            bruksareal = div.find('dd').text
                        case 'Tomteareal' : 
                            tomteareal = div.find('dd').text
                        case 'Kontorplasser' : 
                            kontorplasser = div.find('dd').text 
                        case 'Energimerking' :
                            energimerking = div.find('dd').text
                        case 'Balkong/Terrasse' :
                            balkong_terasse = div.find('dd').text
                        case 'P-plasser' :
                            parking = div.find('dd').text
                
        return areal, etasje, overtakelse, bruttoareal, tomt, byggear, renovert_ar, bruksareal, tomteareal, kontorplasser, energimerking, balkong_terasse, parking
class Sale :
    def scrape_finn(conn, cur, location) :
        kind = 'salelisting'
        # create dynamic tablename 
        current_date = datetime.now().strftime('%Y%m%d')
        table_name = f'{current_date}_{kind}'
        # create new table using that name
        createDynamicTable(conn, cur, table_name, kind)

        url = 'https://www.finn.no/realestate/businesssale/search.html'
        all_listing_urls = FetchAllListingsURL(url, location)
        print(f'{len(all_listing_urls)} listings found')
    
        for listing_url in all_listing_urls :
            url = 'https://www.finn.no' + listing_url
            soup = RequestAndScrape(url)

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
                totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi = Sale.fetchPricingInfo(soup)
            except Exception as e : 
                print('No pricing information on listing')
            # land registry information
            kommune, gardsnr, bruksnr = fetchCadastreInfo(soup)
            # type of listing
            type_listing = fetchTypeListing(soup, 'sale')

            # fetch metadata of listing
            finn_id, status_date = fetchMetadata(soup)

            # keyinformation
            bruksareal, bruttoareal, etasje, eieform, areal, byggear, tomteareal, overtakelse, tomt, energimerking, primaerrom = Sale.fetchKeyInfo(soup)

            # realEstateAgent 
            real_estate_agent_name, img = fetchRealEstateInfo(soup)
            
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
        print('Finished scraping listings for sale')

    def fetchKeyInfo(soup) :
        # defining local variables  
        bruksareal, bruttoareal, etasje, eieform, areal, byggear, tomteareal, overtakelse, tomt, energimerking, primaerrom = [None] * 11

        keyinfodivs = soup.find('section', {'aria-labelledby':'keyinfo-heading'}).find_all('div')
        for div in keyinfodivs :
            if div.has_attr('data-testid') :
                try :
                    attr = div.find('dt').text
                except Exception as e :
                    attr = ''
                # if there is not a 'dt' class in the div the match-case should be skipped
                if len(attr) > 0 :
                    match attr :
                        case 'Bruksareal' :
                            bruksareal = div.find('dd').text
                        case 'Bruttoareal' :
                            bruttoareal = div.find('dd').text
                        case 'Etasje' :
                            etasje = div.find('dd').text
                        case 'Eieform' :
                            eieform = div.find('dd').text
                        case 'Areal' :
                            areal = div.find('dd').text
                        case 'Byggeår' : 
                            byggear = div.find('dd').text
                        case 'Tomteareal' :
                            tomteareal = div.find('dd').text
                        case 'Overtakelse' :
                            overtakelse = div.find('dd').text
                        case 'Tomt' : 
                            tomt = div.find('dd').text
                        case 'Energimerking' : 
                            energimerking = div.find('dd').text 
                        case 'Primærrom' :
                            primaerrom = div.find('dd').text
                
        return bruksareal, bruttoareal, etasje, eieform, areal, byggear, tomteareal, overtakelse, tomt, energimerking, primaerrom

    def fetchAvailablePricingKeys(listing_urls) :
        keyinfo = []
        for url in listing_urls :
            soup = RequestAndScrape(url)
            pricedivs = soup.find('section', {'data-testid': 'pricing-details'}).find_all('div')
            for div in pricedivs : 
                if div.has_attr('data-testid') :
                    try : 
                        attr = div.find('dt').text
                    except Exception as e :
                        attr = ''
                    if attr not in keyinfo : 
                        keyinfo.append(attr)
        print('Availabe pricing information:')
        print(keyinfo)
    
    def fetchPricingInfo(soup) :
        totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi = [None] * 5 
        pricedivs = soup.find('section', {'data-testid': 'pricing-details'}).find_all('div')
        for div in pricedivs : 
            if div.has_attr('data-testid') :
                try : 
                    attr = div.find('dt').text
                except Exception as e :
                    attr = ''
                 # if there is not a 'dt' class in the div the match-case should be skipped
                if len(attr) > 0 :
                    match attr :
                        case 'Totalpris' :
                            totalpris = div.find('dd').text
                            totalpris = unicodedata.normalize('NFKD', totalpris)
                        case 'Omkostninger' :
                            omkostninger = div.find('dd').text
                            omkostninger = unicodedata.normalize('NFKD', omkostninger)
                        case 'Verditakst' :
                            verditakst = div.find('dd').get_text(strip = True)
                            verditakst = unicodedata.normalize('NFKD', verditakst) 
                        case 'Kommunale avg.' :
                            kommunale_avg = div.find('dd').get_text(strip = True)
                            kommunale_avg = unicodedata.normalize('NFKD', kommunale_avg) 
                        case 'Formuesverdi' :
                            formuesverdi = div.find('dd').get_text(strip = True)
                            formuesverdi = unicodedata.normalize('NFKD', formuesverdi) 
        return  totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi 
            
def fetchTypeListing(soup, kind) :
        object_type = ''
        if kind == 'rent' : 
            object_type == 'object-propertyTypes' 
        elif kind == 'sale' :
            object_type == 'object-property-type' 
        types_premises = soup.find('section', {'data-testid': object_type}).find_all('div', {'class': 'py-4'})
        types_arr = []
        delimiter = ', '
        # if the listing consists of multiple types
        if len(types_premises) > 1 :
            for type_premise in types_premises : 
                types_arr.append(type_premise.text)
            type_listing = delimiter.join(types_arr)
        else :
            type_listing = types_premises[0].text
        return type_listing

def fetchCadastreInfo(soup) :
    kommune, gardsnr, bruksnr = [None] * 3
    try :
        cadastredivs = soup.find('section', {'data-testid': 'cadastre-info'}).find_all('div')
        i = 0
        for div in cadastredivs :
            # skip the first div in the section
            if i > 0 :
                match div.text :
                    case s if s.startswith('Kommunenr:') :
                        kommune = re.findall('[0-9]+', div.text)[0]
                    case s if s.startswith('Gårdsnr:') :
                        gardsnr = re.findall('[0-9]+', div.text )[0]
                    case s if s.startswith('Bruksnr:') :
                        bruksnr = re.findall('[0-9]+', div.text )[0]
            i += 1
    except Exception as e : 
        e
    return kommune, gardsnr, bruksnr

def fetchRealEstateInfo(soup) :
    real_estate_agent_name, img = [None] * 2
    try : 
        companyprofile = soup.find('company-profile-podlet').find('div')
        real_estate_agent_name = companyprofile.find('h2').string
        img = companyprofile.find('img')['src']
    except Exception as e : 
        e
    return real_estate_agent_name, img
 
def fetchMetadata(soup) :
    metatable = soup.find('h2', id='ad-info-heading').findNext('table').find('td', {'class':'pl-8'})
    finn_id = metatable.text
    status_date = metatable.findNext('td').text
    return finn_id, status_date

# geocode address
def geocodeAddresses(address, address_parser) : 
    address, osmaddress, geometry, epsg = [None] * 4
    address = address_parser(address, with_prob=True).to_dict()
    print(address)
    if address.get('StreetNumber') is None : 
        street = address['StreetName']
    else :
        street = address['StreetName'] + ' ' + address['StreetNumber']

    geocode_url = 'https://nominatim.openstreetmap.org/search?'
    params = dict (
        limit = '1',
        polygon_geojson= '1',
        format = 'geojson',
        street = street,
        postalcode = address['PostalCode'],
    )
    r = requests.get(geocode_url.encode('utf-8'), params=params)
    if r.status_code == 200 :
        features = r.json()['features']
        # check if request returns features
        if len(features) > 0 :
            feature = features[0]
            # fetch address
            osmaddress = feature['properties']['display_name']
            # fetch geometry information
            geometry = ogr.CreateGeometryFromJson(str(feature['geometry']))
            # fetch projection, could be neccessary sometimes...
            source = geometry.GetSpatialReference() 
            epsg =   source.GetAttrValue('AUTHORITY', 1)
            return address, osmaddress, geometry.ExportToWkt(), epsg
        else : 
            print('Request succesful, but no features fetched for request:')
            print(r.url) 
            address, osmaddress, geometry, epsg = [None] * 4
            return address, osmaddress, geometry, epsg
    else : 
        print('The following request failed:')
        print(r.url)
        print('With status code, ', r.status_code)

def createDynamicTable(conn, cur, table_name, kind) : 
    # load salelisting SQL 
    with open(f'{kind}.sql', 'r') as file :
        sql = file.read()
    #replace tablename from SQL-file to dynamic table_name to create a dynamic table
    sql = sql.replace(kind, f'"{table_name}"')
    cur.execute(sql)
    conn.commit()
    print(f'Table {table_name} is created')
