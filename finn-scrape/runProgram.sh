#!/bin/bash

# run sale and rent script
echo "Running script"
python3 main.py

# export rent listing
date=$(date +'%Y%m%d')
echo "Exporting tables as '${date}_salelisting.csv' and '${date}_rentlisting.csv'"
psql -c "\COPY (SELECT finn_id, title, date_upload, date_listing, typelisting, address, osmaddress, kommune, gardsnr, bruksnr, price, totalpris, omkostninger, verditakst, kommunale_avg, formuesverdi, areal, bruttoareal, bruksareal, tomteareal, eieform, primaerrom, byggear, overtakelse, tomt, etasje, energimerking, realestate_name, img, listing_url, georeferenced FROM \"${date}_salelisting\") to './export/${date}_salelisting.csv' CSV HEADER"
psql -c "\COPY (SELECT finn_id, title, date_upload, date_listing, typelisting, address, osmaddress, kommune, gardsnr, bruksnr, areal, bruttoareal, bruksareal, tomteareal, byggear, renovert_ar, overtakelse, tomt, etasje, energimerking, kontorplasser, parking, balkong_terasse, realestate_name, img, listing_url, georeferenced FROM \"${date}_rentlisting\") to './export/${date}_rentlisting.csv' CSV HEADER"

echo "exporting sales and rentlistings in one geopackage"
ogr2ogr "./export/${date}_finnscrape.gpkg" PG:"" "public.${date}_rentlisting" -nln rentlisting -progress
ogr2ogr "./export/${date}_finnscrape.gpkg" PG:"" "public.${date}_salelisting" -nln salelisting -update -progress
