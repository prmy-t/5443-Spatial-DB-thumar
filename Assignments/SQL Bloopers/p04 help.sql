select ST_AsGeoJSON(ST_Intersection(
	'POLYGON((-95.932617188 38.891032826,
			-100.810546875 37.160316547,
	-97.448730469 30.069093964,
	-87.01171875 31.503629306,
	-85.561523438 36.844460741,
	-95.932617188 38.891032826
			))'::geometry,
			'LINESTRING(-57.440049946
            52.401384266,-132.196677996
            21.491262426)'::geometry));
	

SELECT ST_Distance('SRID=4326;POINT(-57.440049946 52.401384266)'::geometry,
 					'SRID=4326;POINT(-91.994529192 38.113913155)'::geometry);
					
SELECT degrees( ST_Angle('POINT(-57.440049946 52.401384266)', 'POINT(-132.196677996 21.491262426)') );

SELECT ST_AsText(ST_Project('POINT(-91.994529192 38.113913155)'::geography, 100000, radians(45.0)));

	
	
	
	
	
select ST_AsGeojson(starts) from missiles_position;


select 
	ST_AsText(
		ST_Intersection(
			ST_SetSRID(area, 4326), ST_SetSRID(ST_MakeLine(starts::geometry, ends::geometry),4326)
			)
		), st_asgeojson(area), st_asgeojson(starts), st_asgeojson(ends)
from mil_base 
CROSS JOIN
(select * from missiles_position order by time_stamp DESC limit 50) a;




