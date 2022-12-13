

SELECT ST_x((ST_Dump(ST_GeneratePoints(geom, 20, 1996))).geom) as x,ST_y((ST_Dump(ST_GeneratePoints(geom, 20, 1996))).geom) as y
FROM (
SELECT ST_Buffer(
	ST_GeomFromText('LINESTRING(-129.7844079 19.7433195,-61.9513812 19.7433195 , -61.9513812 54.3457868,-129.7844079 54.3457868)'),
  1, 'endcap=round join=round')  As geom ) as s;
  

SELECT 
    ST_LineInterpolatePoints('LINESTRING(-121.81640624999999 54.36775852406841,-86.396484375 19.72534224805787)', 0.01)
	

select * from missiles;
drop table missiles;

create table missiles(name text, starts point, ends point, altitude smallint, speed smallint, blast_redius smallint, time_stemp time)

insert into missiles(name, starts,ends) 
                values(
                  'nam', 
                  Point(2,4),
                  Point(3,7)
				)
					