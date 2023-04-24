import requests
import psycopg2

"""
Accessing the API 

- /Api/Taxon 
returns information on taxa (including their various names)
E.g. /Api/Taxon/83770 for rich taxon info

- /Api/Taxon/ScientificName 
returns information on names (including their taxon)
or /Api/Taxon/ScientificName/48032 for rich name info

- /Api/Taxon/ScientificName/Suggest 
is where you can get suggestions for names that are similar to your input query. Useful for a “Did you mean…” service.


1. first we need to find the id of the species. We want to look at the      following birds: 
    viper eg Vanellus vanellus
    gulspurv eg Emberiza citrinella
    buskskvett eg Saxicola rubetra
2. Use the id to fetch more information 
3. Use the id to fetch images

"""
def requestData(url) :
    headers = {
        'content-type': 'application/json', 
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }

    req = requests.get(url, headers=headers)

    if req.status_code == 200 :
        features = req.json()
        return features
    else :
            print('request failed with error: %s' % str(req.status_code))




names = ['Vanellus vanellus', 'Emberiza citrinella', 'Saxicola rubetra']



url_taxon_id = '/Api/Taxon/'

for name in names :
    url = 'https://artsdatabanken.no/Api/Taxon/ScientificName?ScientificName='
    name = name.replace(' ', '%20')
    taxonomy = requestData(url + name)[0]

    scientific_id = taxonomy['scientificNameID']
    taxon_id = taxonomy['taxonID']
    scientific_name = taxonomy['scientificName']
    # add %20 in the spaces of the species name
    url_scientific_name = scientific_name.replace(' ', '%20')

    # this is the url fo searching up the species in the artsdatabanken
    artsdatabanken_url = 'https://artsdatabanken.no/Taxon/' + str(url_scientific_name) + '/' + str(scientific_id)

    # this is the url where last images of the species are shown
    lastsightings_url = 'https://www.artsobservasjoner.no/Media/Taxon/' + str(scientific_id) + '/SortOrder/SortBySighting#details'

    # make a new request to fetch more information about the species
    url = 'https://artsdatabanken.no/Api/Taxon/ScientificName/'
    feature = requestData(url + str(scientific_id))

    dynamicproperties = feature['dynamicProperties']
    
    # make a dictionary with information about the labels and in which year they have been giving for hte species
    categorydict = {}
    i = 0
    while i < len(dynamicproperties) :
        if dynamicproperties[i]['Name'] == 'Kategori' :
            category = dynamicproperties[i]['Value']

            properties = dynamicproperties[i]['Properties']
            j = 0
            while j < len(properties) : 
                if properties[j]['Name'] == 'Aar' :
                    year = properties[j]['Value']
                    categorydict[category] = year
                j += 1
        i += 1

    """
    Using the following API call: 
    https://artskart.artsdatabanken.no/publicapi/api/observations/list?ScientificNameIds=

    We can fetch the observations corresponding to the species. Howerver, the API is paginated. Therefore we should: 
        1. set the page-index = 0 and page-size to 100 in the URL
        2. fetch the totalcount of pages.
        3. Calculate the amount of times the API can be called for. 
    """

    # set pagesize to 1000 records. Each response will ask 1000 observations 
    pagesize = 100
    # set the date to which date should be fetched
    date = '01.01.2020'

    # fetch the total pages of the species

    url = 'https://artskart.artsdatabanken.no/publicapi/api/observations/list?FromDate=' + date + '&ScientificNameIds=' + str(scientific_id) + '&PageSize=' + str(pagesize)
    feature = requestData(url)
    totalpages = feature['TotalPages']
    totalcount = feature['TotalCount']
    
    print('Requesting data for: \nspecies: %s\nFromdate: %s\nTotalpages: %d\nTotalObservations: %d' % (scientific_name, date, totalpages, totalcount))
    print('Iterating over pages...')
    for page in range(totalpages) :
        print(page)


 