select * from bbox;
select * from ships;
select * from ship_armors;
select * from ship_armaments;
select * from region;
select * from temp_points;
select st_y(st_astext(point)) as lat, st_x(st_astext(point)) as lon from temp_points;

UPDATE region set geom = ST_MakePolygon(ST_MakeLine(ARRAY[p1, p2, p3, p1]));

select st_astext(point) from temp_points order by ship_id offset 1 limit 2;

select 
	json_build_object(
		'ship_id',ship_id,
		'bearing',bearing,
		'location',json_build_object(
			'coords',json_build_object(
				'lon', st_x(st_asText(location)),
				'lat', st_y(st_asText(location))
			)
		),
		'speed', speed,
		'hitpoints', 500
	)
from ships;

SELECT 
    center,
    ST_Intersection( ST_MakeLine(center, ST_Project(center::geography, 100000, radians(326.25))::geometry), ST_Boundary(box)) ,
    ST_Intersection(ST_MakeLine(center, ST_Project(center::geography, 100000, radians(303.75))::geometry), ST_Boundary(box))
from Bbox;