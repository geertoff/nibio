-- join information of bygning
create table nibio.bygning as 
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
				st_transform( b.representasjonspunkt, 5973) as geom_5973 
from matrikkelenbygning.bygning b 
left join matrikkelenbygning.bygningsstatuskode st on b.bygningsstatus = st.identifier 
left join matrikkelenbygning.bygningstypekode typ on b.bygningstype = typ.identifier 
left join matrikkelenbygning.naringsgruppekode n on b.naringsgruppe = n.identifier;

-- add primary key
alter table nibio.bygning  add primary key (objid);


-- spatial indexes
create index bygning_geom_idx on nibio.bygning using GIST (geom);
create index bygning_geom_5973_idx on nibio.bygning using GIST (geom_5973);
create index buildings_geom_idx on nibio.buildings_nibio using GIST (geom);


-- filter housing objects with a view
create view nibio.v_bygning_bolig as 
select * from bygning b where naringsgruppe = 'X';

-- spatial joining the housing objects with the naringsgruppe. Multiple points can be in one polygon
create view nibio.v_bolig_building as 
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
		--	count(vb.geom_5973) as count_bygning,
			vb.geom_5973 as centroid,
			b.geom
from nibio.v_bygning_bolig vb
join buildings_nibio b 
on ST_CONTAINS(b.geom, vb.geom_5973);

-- generate spatial are
select st_area(geom) from jordbruk j;

-- nearest neighbour of points
select * from v_bygning_bolig vbb; \


-- centroid of jordbruk
select st_distance(vb.geom_5973, st_centroid(j.geom)) as dist from jordbruk j, v_bygning_bolig vb
order by dist asc; 

/* use the centroid of the agricultural parcel and calculate the distance between a household and the parcel
 *  potato households: 6623
	bread households; 2,293
 * 
 */
select 
			vb.objid, 
			st_distance(vb.geom_5973, st_centroid(j.geom)) as dist,
			vb.geom_5973,
			bn.geom
			
from 		jordbruk j, v_bygning_bolig vb
join 		buildings_nibio bn on ST_Contains(bn.geom, vb.geom_5973)			
order by 	vb.geom_5973 <->  st_centroid(j.geom)
limit 6623;

-- creating a convex hull for the points
select 
	st_convexhull(st_collect(qry.geom))
from (
select 
			
		--	st_distance(vb.geom_5973, st_centroid(j.geom)) as dist,
			vb.geom_5973 as geom
			from nibio.jordbruk j, nibio.v_bygning_bolig vb

order by vb.geom_5973 <->  st_centroid(j.geom)
limit 6623
) qry;


