

-- Creating table: missiles_position 
create table if not exists missiles_position(name text, starts geometry, ends geometry, altitude smallint, time_stamp time); 


--Generate points on the top and bottom of bbox.
SELECT ST_x((ST_Dump(
                  ST_GeneratePoints(geom, 20, 1996)
                  )).geom)as x,
              ST_y((ST_Dump(
                  ST_GeneratePoints(geom, 20, 1996)
                  )).geom) as y
FROM (
SELECT ST_Buffer(
	ST_GeomFromText('SRID=4326;LINESTRING(-129.784 19.743,-61.951 19.743, -61.951 54.345,-129.784 54.345)'),
	3,
	'endcap=round join=round')  As geom 
) as it;


-- Inserting missiles data from generated points.
insert into missiles_position
	values(
    	'${generate_name()}', 
        ST_SetSRID(ST_MakePoint(${data[i].x}, ${data[i].y}),4326),
        ST_SetSRID(ST_MakePoint(${data[data.length / 2 + i].x}, ${data[data.length / 2 + i].y}),4326),Math.floor(Math.random() * (12000 - 10000) + 10000)},
       	current_time
    );