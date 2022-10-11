-- Table: public.missiles_position

-- DROP TABLE IF EXISTS public.missiles_position;

CREATE TABLE IF NOT EXISTS public.missiles_position
(
    name text COLLATE pg_catalog."default",
    starts geometry,
    ends geometry,
    time_stamp time without time zone
)

--Generate points on the top and bottom of bbox.

SELECT ST_x((ST_Dump(ST_GeneratePoints(geom, ${num_of_missiles * 2}, 1996))).geom)as x,
       ST_y((ST_Dump(ST_GeneratePoints(geom, ${num_of_missiles * 2}, 1996))).geom) as y
       FROM (
       	SELECT ST_Buffer(ST_GeomFromText('SRID=4326;LINESTRING(-129.784 19.743,-61.951 19.743, -61.951 54.345,-129.784 54.345)'),8, 'endcap=round join=round') As geom
       ) as s;
	   
	   
-- Inserting missiles data from generated points.

INSERT INTO missiles_position
VALUES(
	'${generate_name()}', 
    ST_SetSRID(ST_MakePoint(${data[i].x}, ${data[i].y}, 500), 4326),
    ST_SetSRID(ST_MakePoint(${data[data.length / 2 + i].x}, ${data[data.length / 2 + i].y},500), 4326),
    current_time
)
	   