import os
import requests

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
def requestData(baseurl, input_url, input) :
   headers = {'content-type': 'application/json'} 
   url = baseurl + input_url + input
   req = requests.get(url, headers=headers)
   if req.status_code == 200 :
        features = req.json()
        return features



names = ['Vanellus vanellus', 'Emberiza citrinella', 'Saxicola rubetra']



url_scientific = '/Api/Taxon/ScientificName?ScientificName='
url_scientific_id = '/Api/Taxon/ScientificName/'
url_taxon_id = '/Api/Taxon/'

for name in names :
    baseurl = 'https://artsdatabanken.no'
    name = name.replace(' ', '%20')
    taxonomy = requestData(baseurl, url_scientific, name)[0]

    scientific_name = taxonomy['scientificName']
    url_scientific_name = scientific_name.replace(' ', '%20')
    scientific_id = taxonomy['scientificNameID']

    artsdatabanken_url = 'https://artsdatabanken.no/Taxon/' + str(url_scientific_name) + '/' + str(scientific_id)
    print(artsdatabanken_url)

    # https://www.artsobservasjoner.no/
    lastsightings_url = 'https://www.artsobservasjoner.no/Media/Taxon/' + str(scientific_id) + '/SortOrder/SortBySighting#details'
    print(lastsightings_url)

    taxon_id = taxonomy['taxonID']

    # use the other url to search with the ids
    feature = requestData(baseurl, url_scientific_id, str(scientific_id))
    dynamicproperties = feature['dynamicProperties']
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
    print(scientific_name)
    print(categorydict)

    # fetch observation data based on scientificid
    baseurl = 'https://artskart.artsdatabanken.no/publicapi/api/observations/list?ScientificNameIds='
    pageindex_str = ''


    # test = requestData('')
    baseurl = 'https://artskart.artsdatabanken.no/publicapi/api/observations/list?'
    # scientific_id_url = '/ScientificNameIds='
    # species_url = '/species='
    # observations = requestData(baseurl, scientific_id_url, str(scientific_id))
    # print(observations)


    # artskart.artsdatabanken.no/publicapi/api/observations/list?ScientificNameIds=3654