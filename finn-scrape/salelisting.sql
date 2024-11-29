create table if not exists salelisting (
     finn_id varchar primary key
    ,title varchar
    ,date_upload varchar
    ,date_listing varchar 
    ,typelisting varchar
    -- address
    ,address varchar
    -- cadastral information
    ,kommune varchar
    ,gardsnr varchar
    ,bruksnr varchar
    -- pricing information
    ,price varchar
    ,totalpris varchar
    ,omkostninger varchar
    ,verditakst varchar
    ,kommunale_avg varchar
    ,formuesverdi varchar
    -- keyinformation
    ,areal varchar
    ,bruttoareal varchar
    ,bruksareal varchar
    ,tomteareal varchar
    ,eieform varchar
    ,primaerrom varchar
    ,byggear varchar
    ,overtakelse varchar
    ,tomt varchar
    ,etasje varchar
    ,energimerking varchar
    -- realestate
    ,realestate_name varchar
    ,img varchar
    ,listing_url varchar
);
