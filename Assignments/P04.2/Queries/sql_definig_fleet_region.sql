CREATE TABLE if not exists region(geom geometry, center geometry, p1 geometry, p2 geometry, p3 geometry);
    TRUNCATE TABLE region;
    INSERT INTO region(p1, p2, p3)
    SELECT 
    center,
    ST_Intersection( ST_MakeLine(center, ST_Project(center::geography, 100000, radians({min_degree}))::geometry), ST_Boundary(box)) ,
    ST_Intersection(ST_MakeLine(center, ST_Project(center::geography, 100000, radians({max_degree}))::geometry), ST_Boundary(box))
    from Bbox;
    UPDATE region set geom = ST_MakePolygon(ST_MakeLine(ARRAY[p1, p2, p3, p1]));
    UPDATE region set center = ST_SetSRID(ST_Centroid(geom),4326);