create table listing (
     finn_id varchar primary key
    ,title varchar
    ,date varchar 
    ,kind varchar
    ,typelisting varchar
    -- address
    ,finnaddress varchar
    ,osmaddress varchar
    ,parseaddress jsonb
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
    ,geom geometry
);
