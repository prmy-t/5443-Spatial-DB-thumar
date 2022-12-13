drop table ser;
create table if not exists ser(id SERIAL, x_start float(7),y_start float(7),x_end float(7),y_end float(7));

truncate ser;
UPDATE ser
set x_start = q.the_x, y_start = q.the_y
from (SELECT ST_x((dp).geom) As the_x, ST_y((dp).geom) As the_y 
    	FROM (
    		SELECT ST_DumpPoints(
        		ST_Segmentize(
            		ST_GeomFromText('LINESTRING(-129.7844079 54.3457868, -61.9513812 54.3457868)',28992), 
            		33.833 
        			)
   			) AS dp
		) AS o offset 1 limit 2)As q
where id = 1;
		
	
insert into ser(x_end, y_end) 
	SELECT ST_x((dp).geom) As x,ST_y((dp).geom) As y 
    FROM (
    	SELECT ST_DumpPoints(
        		ST_Segmentize(
            		ST_GeomFromText('LINESTRING(-129.7844079 54.3457868, -61.9513812 54.3457868)',28992), 
            		15.833 
        			)
   		) AS dp
	) AS foo  offset 1 limit 4;


-- Advance update

update ser as s set
    x_start = q.the_x,
	y_start = q.the_y
from (
	SELECT 
	floor(random() * 4 + 1) as s_id,
	ST_x((dp).geom) As x,
	ST_y((dp).geom) As y 
    FROM (
    	SELECT ST_DumpPoints(
        		ST_Segmentize(
            		ST_GeomFromText('LINESTRING(-129.7844079 19.7433195, -61.9513812 19.7433195)',28992), 
            		15.833 
        			)
   		) AS dp
	) AS foo  offset 1 limit 4

	
) as q(s_id, the_x, the_y) 
where s.id != q.s_id;



do $$
begin
for r in 1..10 loop
insert into ser values(floor(random()*(10-1+1))+1);
end loop;
end;
$$;

select * from ser;