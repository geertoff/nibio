
create table species (
    id integer primary key,
    speciesname varchar,
    taxonid integer,
    artsdatabanken_url varchar,
    lastsightings_url varchar,
    categories varchar
);

create table observations (
    id serial primary key,
    catelog_id varchar, 
    scientific_id integer,
    speciesname varchar,
    count integer,
    notes varchar,
    precision integer,
    institution varchar,
    collector varchar,
    collected_date varchar, 
    identifier varchar,
    identified_date varchar,
    basisofrecord varchar,
    observation_url varchar,
    image_url varchar,
    geom geometry,
    unique (scientific_id, catelog_id)

);

create view v_buskskvett as 
select
	o.id,
	s.id species_id,
	s.speciesname scientific_name,
	o.speciesname as "name",
	o.count,
	o.precision,
	o.collector,
	o.collected_date,
	o.identifier,
	o.identified_date,
	s.categories,
	o.notes,
	o.institution,
	o.basisofrecord,
	s.artsdatabanken_url,
	s.lastsightings_url,
	o.observation_url,
	o.image_url,
	o.geom
from species s 
left join observations o on s.id = o.scientific_id
where s.speciesname = 'Saxicola rubetra'