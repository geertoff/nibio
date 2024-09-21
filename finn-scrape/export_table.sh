#!/bin/bash
# Export sale listings
docker exec -it postgis psql -U postgres -d finn -c '\COPY salelisting to '/tmp/salelisting.csv' CSV HEADER'
docker cp postgis:/tmp/salelisting.csv . 
docker exec -it postgis bash -c 'rm /tmp/salelisting.csv'

# Export rent listings
docker exec -it postgis psql -U postgres -d finn -c '\COPY rentlisting to '/tmp/rentlisting.csv' CSV HEADER'
docker cp postgis:/tmp/rentlisting.csv . 
docker exec -it postgis bash -c 'rm /tmp/rentlisting.csv'