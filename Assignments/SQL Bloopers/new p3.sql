select currenttime + ((last_altitude - drop_rate)* interval '1 second') from sweep1, missile_info;
select * from sweep2;
select * from missile_info order by m_id;
drop table missile_info;
select * from prediction;
select * from regions;
select 
one.m_id,
one.missile_type,
ST_Distance(one.geom, two.geom, false) as speed,
two.altitude as last_altitude,
one.altitude - two.altitude as drop_rate
from sweep1 one, sweep2 two
where one.m_id = two.m_id;

SELECT now()::time, now()::TIME + ((last_altitude - drop_rate)* interval '1 second'), (last_altitude - drop_rate) from missile_info;

select
        last_altitude - drop_rate as landing_in_sec,
        ST_Project(last_geom::geography, (last_altitude / drop_rate) * speed, radians(last_bearing))::geometry as landing_geom
        from missile_info;