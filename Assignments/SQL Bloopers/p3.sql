SELECT geom, ST_AsText(ST_Intersection( ST_SetSRID(ST_Point(-157.898158, 21.360301),4326) ::geometry, geom)) from us_mil limit 5;
select * from temp;
alter table temp rename column st_astext to points;
create table temp as (SELECT ST_AsText(geom) FROM public.us_mil as points limit 5 );

SELECT ST_AsText(ST_Intersection(points, geom)) from us_mil limit 5;


SELECT ST_AsText(ST_GeneratePoints(geom, 2, 4326))
FROM (
    SELECT ST_Buffer(
        ST_GeomFromText(
        'POLYGON((50 50,150 150,150 50,50 50))'),
        10, 'endcap=round join=round') AS geom
) AS s;

SELECT ST_AsGeoJSON(ST_GeneratePoints(geom, 1, 1999))
FROM (
SELECT ST_Buffer(
	ST_GeomFromText('LineString(-129.7844079 54.3457868, -129.7844079 19.7433195)'),
  1, 'endcap=round join=round')  As geom ) as s;
  
( -129.7844079 54.3457868, -61.9513812 54.3457868,-61.9513812 19.7433195,-129.7844079 19.7433195, -129.7844079 54.3457868)

--points on the top
SELECT ST_AsText((dp).geom) As wkt_geom 
FROM (
    SELECT ST_DumpPoints(
        ST_Segmentize(
            ST_GeomFromText('LINESTRING(-129.7844079 54.3457868, -61.9513812 54.3457868)',28992), 
            3
        )
   ) AS dp
) AS foo;

--points on the bottom
SELECT ST_x((dp).geom) AS x,ST_y((dp).geom) As y
FROM (
    SELECT ST_DumpPoints(
        ST_Segmentize(
            ST_GeomFromText('LINESTRING(-61.9513812 19.7433195,-129.7844079 19.7433195)',28992), 
            65
        )
   ) AS dp
) AS foo;


SELECT ST_AsGeoJSON(J.*) FROM (SELECT ST_GeneratePoints(geom, 12, 1996) 
FROM (
SELECT ST_Buffer(
	ST_GeomFromText('LINESTRING(-129.7844079 19.7433195,-61.9513812 19.7433195 , -61.9513812 54.3457868,-129.7844079 54.3457868)'),
  1, 'endcap=round join=round')  As geom ) as s )as J;
  
  
  
SELECT ST_AsText(ST_PointN(ST_GeomFromText('LineString(-129.7844079 19.7433195,-61.9513812 19.7433195)'), 1));
  
  
  
 SELECT ST_AsGeoJSON(J.*) FROM (SELECT ST_GeneratePoints(geom, 1, 1996) 
FROM (
SELECT ST_Buffer(
	ST_GeomFromText('LINESTRING(-129.7844079 19.7433195,-61.9513812 19.7433195 , -61.9513812 54.3457868,-129.7844079 54.3457868)'),
  1, 'endcap=round join=round')  As geom ) as s )as J;