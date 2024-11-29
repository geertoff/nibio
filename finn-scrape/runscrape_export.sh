# run sale and rent script
echo "Scraping sale rentals..."
python3 scrape-finn-sale.py
echo "Scraping rental rentals..."
python3 scrape-finn-rent.py

# export rent listing
date=$(date +'%Y%m%d')
echo "Exporting tables as '${date}_salelisting.csv' and '${date}_rentlisting.csv'"
psql -c "\COPY salelisting to '${date}_salelisting.csv' CSV HEADER"
psql -c "\COPY rentlisting to '${date}_rentlisting.csv' CSV HEADER"