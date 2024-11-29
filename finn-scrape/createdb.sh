#/bin/bash
psql -c "CREATE DATABASE finn;"
psql -d finn -c "CREATE EXTENSION postgis;"
psql -d finn -f datamodel.sql 
export PGDATABASE=finn

