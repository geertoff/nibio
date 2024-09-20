import requests
# for webscraping
from bs4 import BeautifulSoup
# Regular Expression for splitting strings
import re

# for working with spatial data
from osgeo import ogr, osr

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
    i = 0
    for listing in listings : 
        # get the value of the url
        listing_url = listing['href']
        listing_data.append(listing_url)
        i += 1
    # count listings
    print('%d listings available' % i)
    return listing_data

def fetchAvailableKeys(listing_urls) :
    keyinfo = []
    for url in listing_urls : 
        soup = RequestAndScrape(url)
        keyinfodivs = soup.find('section', {'aria-labelledby':'keyinfo-heading'}).find_all('div')
        for div in keyinfodivs : 
            if div.has_attr('data-testid') :
                attr = div.find('dt').text
                if attr not in keyinfo :
                    keyinfo.append(attr)
    print('Available keyinformation :')
    print(keyinfo)

# fetch section of key info. This informtion is located in 'data-testid' divs. 
def findKeyInfo(soup) :
    # defining local variables  
    usable_area, gross_area, ownership_type, area, construction_year, plot_area = [None] * 6
    # regex pattern for extracting values
    
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
                        usable_area = extractAreaInt(div.find('dd').text)
                    case 'Bruttoareal' :
                        gross_area = extractAreaInt(div.find('dd').text)
                    case 'Eieform' :
                        ownership_type = div.find('dd').text
                    case 'Areal' :
                        area = extractAreaInt(div.find('dd').text)
                    case 'Byggeår' :
                        construction_year = div.find('dd').text
                    case 'Tomteareal' :
                        plot_area = extractAreaInt(div.find('dd').text) 
    return usable_area, gross_area, ownership_type, area, construction_year, plot_area
    
def fetchRealEstateInfo(soup) :
    companyprofile = soup.find('company-profile-podlet').find('div')
    name = str(companyprofile.find('h2').text)
    img = companyprofile.find('img')['src']
    return name, img
    
def fetchMetadata(soup) :
    metatable = soup.find('h2', id='ad-info-heading').findNext('table').find('td', {'class':'pl-8'})
    finn_id = metatable.text
    status_date = metatable.findNext('td').text
    return finn_id, status_date


# extract the number of a string with the format '[number] m2'
def extractAreaInt(area) :
    # split the string on a whitespace and pick the first item and convert it into an integer
    area = int(re.split('\s', area)[0])
    return area


# geocode address
def geocodeAddresses(address, address_parser) : 
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
