create table rentlisting (
     finn_id varchar primary key
    ,title varchar
    ,date varchar 
    ,typelisting varchar
    -- address
    ,address varchar
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
);

create table salelisting (
     finn_id varchar primary key
    ,title varchar
    ,date varchar 
    ,typelisting varchar
    -- address
    ,address varchar
    -- cadastral information
    ,kommune varchar
    ,gardsnr varchar
    ,bruksnr varchar
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
)
