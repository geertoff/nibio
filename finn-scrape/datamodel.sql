create table listing (
    finn_id integer primary key,
    title varchar,
    date varchar, 
    type varchar,
    address varchar,
    ownershiptype varchar,
    construction_year varchar,
    -- area integers
    area int,
    plot_area int,
    usable_area int, 
    gross_area int,
    -- realestate
    realestate_name varchar,
    img varchar,
    listing_url varchar,
    geom geometry
);
