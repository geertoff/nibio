create table if not exists rentlisting (
     finn_id varchar primary key
    ,title varchar
    ,date_upload varchar
    ,date_listing varchar 
    ,typelisting varchar
    -- address
    ,address varchar
    ,osmaddress varchar
    -- cadastral information
    ,kommune varchar
    ,gardsnr varchar
    ,bruksnr varchar
    -- keyinformation
    ,areal varchar
    ,bruttoareal varchar
    ,bruksareal varchar
    ,tomteareal varchar
    ,byggear varchar
    ,renovert_ar varchar
    ,overtakelse varchar
    ,tomt varchar
    ,etasje varchar
    ,energimerking varchar
    ,kontorplasser varchar
    ,parking varchar
    ,balkong_terasse varchar
    -- realestate
    ,realestate_name varchar
    ,img varchar
    ,listing_url varchar
    ,georeferenced boolean generated always as (geom is not null) stored
    ,geom geometry
);