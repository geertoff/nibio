/*
	Input: 
	- Agricultural field (field)
	- building filtered by housing type, point and polygon geometry 
	- information of amount of households that are dependent on the yield of a particular crop
*/

-- join information of bygning
create table bygning as 
select 			b.objid,
				b.objtype, 
				b.naringsgruppe,
				n.description naringsgruppe_descr,
				b.bygningsstatus,
				st.description bygningsstatus_descr,
				b.bygningid,
				typ.description bygningstype_descr,
				b.kommunenummer,
				b.kommunenavn,
				b.bygningstype,
				b.representasjonspunkt as geom,
from matrikkelenbygning.bygning b 
left join matrikkelenbygning.bygningsstatuskode st on b.bygningsstatus = st.identifier 
left join matrikkelenbygning.bygningstypekode typ on b.bygningstype = typ.identifier 
left join matrikkelenbygning.naringsgruppekode n on b.naringsgruppe = n.identifier;

-- add primary key
alter table bygning  add primary key (objid);

-- spatial indexes
create index bygning_geom_idx on bygning using GIST (geom);
create index buildings_geom_idx on buildings_nibio using GIST (geom);

-- filter objects to housing objects
create view v_bygning_bolig as 
select * from bygning b where naringsgruppe = 'X';

-- spatial joining the housing objects with the naringsgruppe. Multiple points can be in one polygon
create view v_bolig_building as 
select 		row_number() over ()  objectid,
			b.id,
			vb.objid,
			vb.objtype,
			vb.naringsgruppe,
			vb.naringsgruppe_descr,
			vb.bygningsstatus,
			vb.bygningsstatus_descr,
			vb.bygningid,
			vb.bygningstype_descr,
			vb.kommunenummer,
			vb.kommunenavn,
			vb.bygningstype,
			vb.geom as centroid,
			b.geom
from v_bygning_bolig vb
join buildings_nibio b 
on ST_CONTAINS(b.geom, vb.geom);

-- generate spatial area of field
select st_area(geom) from field f;

-- nearest neighbour of points
select * from v_bygning_bolig vbb; 

/* 
   use the centroid of the agricultural field and calculate the distance between a household and the field
   the limit depends on the amount of households that can be 'fet'
*/

create or replace function __distance_households(limit_count int) 
returns table (
	 objectid bigint,
	 dist double precision,
	 geom geometry
) 
as
$$
BEGIN
	return query
	select 
				row_number() over ()  objectid, 
				st_distance(vb.geom_25833, st_centroid(f.geom)) as dist,
				vb.geom as geom
	from 
		field f, v_bygning_bolig vb
	order by 
		vb.geom_25833 <->  st_centroid(f.geom)
	-- count of amount of households
	limit 
		limit_count;
end;
$$
language plpgsql;

-- create convex hull of points per vegetable-scenario
select st_convexhull(st_collect(h.geom)) from __distance_households(2854) as h;

-- only show no overlap points
select 
p.objectid,
p.geom
from results.potato_carrot  p
left join results.carrot pc  on  st_intersects(p.geom, pc.geom)
where pc.geom is null;