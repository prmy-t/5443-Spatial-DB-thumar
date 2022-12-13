-- find hits--
select st_intersection(mi.geom, ci.geom) from missiles mi,cities ci where st_intersects(mi.geom, ci.geom);

-- Getting distance from latest missiles to firing point --
select 
l_mi.m_id,
l_mi.missile_type,
st_distance(ST_Centroid(reg.geom), l_mi.geom, false) as distance  
from latest_missiles l_mi, regions reg
order by distance DESC
limit 1;

-- Getting missile speed and altitude-difference. -- 
select st_distance(a.geom, b.geom, false) as speed, a.altitude as last_altitude, (a.altitude - b.altitude) as alt_difference, b.bearing as last_bearing
from (select * from missiles mi where missile_type = 'Patriot' and m_id = 14 order by currenttime DESC OFFSET 0 limit 1) as a,
(select * from missiles mi where missile_type = 'Patriot' and m_id = 14 order by currenttime DESC OFFSET 1 limit 1) as b;

-- helper query --
select st_asText(geom), * from missiles where missile_type = 'Harpoon' order by currenttime DESC limit 2;
--x--x--x--x--x--x--x--x--x--


-- projecting a point of missile after 4 seconds. -- 
drop table temp;
create table temp(region_center geometry, closest_point geometry, projection geometry, pro_altitude int, bearing int);
INSERT INTO temp
select 
st_setSRID(ST_Centroid(reg.geom), 4326),
st_closestpoint(st_makeLine(st_setsrid(mi.geom,4326), st_project(mi.geom, (41506.5579)*4, radians(2.0130162))::geometry), st_setSRID(ST_Centroid(reg.geom), 4326))::geometry,
st_makeLine(st_setsrid(mi.geom,4326), st_project(mi.geom, (41506.5579)*4, radians(2.0130162))::geometry),
altitude- (4*127.360999),
bearing
from missiles mi, regions reg
where missile_type = 'Patriot'and m_id = 14 
order by currenttime DESC 
limit 1;

SELECT * from t_regions;
create table t_regions(center geography);
insert into t_regions select region_center::geography from temp;
create table t_closest(closest_point geometry);
insert into t_closest select closest_point from temp;
create table t_projection(line geometry);
insert into t_projection select projection from temp;

select * from projection;
select st_srid(center) from regions;
select st_distance(st_closestPoint(pro.projected_line, reg.center), reg.center, false) from regions reg, projection pro;

select * from projection;

select 
        l_mi.m_id,
        l_mi.missile_type,
        st_distance(ST_Centroid(reg.geom), l_mi.geom, false) as distance  
        from latest_missiles l_mi, regions reg
        order by distance DESC
        limit 1;
		
		
select 
pro.projected_altitude as target_alt,
st_x(st_asText(pro.closest_point_from_center)) as aim_lon,
st_y(st_asText(pro.closest_point_from_center)) as aim_lat,
pro.distance_to_center as distance,
st_x(st_asText(reg.center)) as firedFrom_lon,
st_y(st_asText(reg.center)) as firedFrom_lat
from regions reg, projection pro;

select distinct center::point from regions;
select 
        l_mi.m_id,
        l_mi.missile_type,
        st_distance(ST_Centroid(reg.geom), l_mi.geom, false) as distance  
        from latest_missiles l_mi, regions reg
        order by distance
        limit 1;
drop table enve;
drop table batteries;
create table enve(id serial, geom geometry);
select id, geom:: point from enve;
select * from batteries;
select * from regions;
select st_centroid(st_makeline((select geom from enve where id = 1),((select geom from enve where id = 2))));
INSERT INTO enve(geom)
select distinct (st_dumpPoints(st_envelope(geom))).geom from regions; 



--from code --

 CREATE TABLE enve(id serial, geom geometry);

    CREATE TABLE batteries(location geometry);

    INSERT INTO enve(geom)
    select distinct (st_dumpPoints(st_envelope(geom))).geom from regions; 

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 1),((select geom from enve where id = 2))));

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 2),((select geom from enve where id = 3))));

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 3),((select geom from enve where id = 4))));

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 4),((select geom from enve where id = 1))));

    INSERT INTO batteries
    select center from regions;  