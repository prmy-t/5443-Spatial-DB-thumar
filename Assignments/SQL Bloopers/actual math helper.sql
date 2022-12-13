select geom::geography from latest_missiles;
select st_astext(st_project(geom, 1000000, radians(2.45))) from latest_missiles;
select geom::geography from cities;
select * from missiles where m_id = 1 order by currenttime DESC;
select mi.m_id, mi.missile_type, st_intersection(mi.geom, ci.buffer) as intersection, ci.id as city_id from latest_missiles mi, cities ci where st_intersects(mi.geom, ci.buffer) = 'true';


-- Getting distance from latest missiles to firing point --

select 
l_mi.m_id,
l_mi.missile_type,
st_distance(ST_Centroid(reg.geom), l_mi.geom, false) as distance  
from latest_missiles l_mi, regions reg
order by distance DESC
limit 1;

select * from missiles where missile_type = 'Javelin' and m_id = 1 order by currenttime DESC limit 2

-- Sort missile by distance from Firing point ASC --
select st_distance(mi.geom, )

-- Get missile info --
select
st_distance(a.geom, b.geom, false) as speed,
(b.altitude - a.altitude) as alt_difference,
b.bearing as last_bearing
from 
(select * from missiles mi where missile_type = 'Javelin' and m_id = 1 order by currenttime DESC OFFSET 0 limit 1) as a,
(select * from missiles mi where missile_type = 'Javelin' and m_id = 1 order by currenttime DESC OFFSET 1 limit 1) as b;
-- Varifying the output --
select
st_distance(mi1.geom, mi2.geom, false) as speed,
(mi1.altitude - mi2.altitude) as alt_difference,
mi2.bearing as last_bearing
from missiles mi1 INNER join missiles mi2
on mi1.m_id = mi2.m_id where mi1.missile_type = 'Javelin' and mi1.m_id = 1 order by mi1.currenttime limit 2; 