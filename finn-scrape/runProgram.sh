# run sale and rent script
echo "Running script"
python3 main.py

# export rent listing
date=$(date +'%Y%m%d')
echo "Exporting tables as '${date}_salelisting.csv' and '${date}_rentlisting.csv'"
psql -c "\COPY salelisting to '${date}_salelisting.csv' CSV HEADER"
psql -c "\COPY rentlisting to '${date}_rentlisting.csv' CSV HEADER"