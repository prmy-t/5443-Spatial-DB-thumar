import os
import geojson
import json
import psycopg2
import requests
from time import sleep


# Database configuration
conn = psycopg2.connect("dbname=project3 user=postgres password=221702")
conn.autocommit = True
cur = conn.cursor()

# DATA
firing_point = "ST_Centroid(reg.geom)"

# --x--x--x--x--x-- New Functions --x--x--x--x--x--
def get_area():
    sql = """select area, center::point from regions"""
    cur.execute(sql)
    data = cur.fetchone()
    return {"area" : data[0],"center" : data[1]}

def get_Bbox():
    sql = """select bbox::polygon from regions;"""
    cur.execute(sql)
    data = cur.fetchone()
    return data[0]

def generate_batteries():
    cur.execute("""
    CREATE TABLE if not exists enve(id serial, geom geometry);

    CREATE TABLE if not exists batteries(location geometry);

    INSERT INTO enve(geom)
    select distinct (st_dumpPoints(st_envelope(geom))).geom from regions; 

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 1),((select geom from enve where id = 2))));

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 2),((select geom from enve where id = 3))));

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 3),((select geom from enve where id = 4))));

    INSERT INTO batteries
    select st_centroid(st_makeline((select geom from enve where id = 4),((select geom from enve where id = 1))));

    INSERT INTO batteries
    select center from regions;  

    select location::point from batteries;
    """)

    data = cur.fetchall()
    return data

def save_sweep_to_table(i):
    with open("latest_missiles.json") as file:
        gj = geojson.load(file)
        for feature in gj['features']:
            geom = (json.dumps(feature['geometry']))
            m_id = feature["id"]
            missile_type = feature['properties']['missile_type']
            bearing = feature['properties']['bearing']
            altitude = feature['properties']['altitude']
            currentTime = feature['properties']['current_time']
            cur.execute('INSERT INTO sweep%s (m_id, missile_type, geom, bearing, altitude, currentTime) VALUES (%s, %s, ST_setSRID(ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s))),4326), %s, %s, %s);', (i,m_id, missile_type, geom, bearing, altitude, currentTime))

def create_sweep_tables():
    sql = """
        CREATE TABLE if not exists sweep1(m_id int, missile_type text, geom geometry, bearing double precision, altitude double precision, currentTime time);
        CREATE TABLE if not exists sweep2(m_id int, missile_type text, geom geometry, bearing double precision, altitude double precision, currentTime time);
        TRUNCATE TABLE sweep1, sweep2;
    """
    cur.execute(sql)
    return "created"

def get_sweep():
    i = 1
    create_sweep_tables()
    sleep(1)
    while(i<3):
        sweep = requests.get(f"http://missilecommand.live:8080/RADAR_SWEEP").json()

        if sweep:
            truncate_table('latest_missiles')
            sweep_obj = json.dumps(sweep)
            #CREATE: JSON file of the necessary data...
            createJson('latest_missiles', sweep_obj)
            #SAVE: JSON files to Postgres table...
            save_to_postgres('latest_missiles')
            save_sweep_to_table(i)
        i += 1
        sleep(1)
    generate_missile_info()
    return predict_landing()

def generate_missile_info():
    sql = """
        CREATE TABLE if not exists 
        missile_info(
            m_id int, 
            missile_type text, 
            last_geom geometry, 
            speed double precision, 
            last_bearing double precision,
            last_altitude double precision, 
            drop_rate double precision,
            currenttime time);
        TRUNCATE TABLE missile_info;

        INSERT INTO missile_info
        select 
        one.m_id,
        one.missile_type,
        two.geom,
        ST_Distance(one.geom, two.geom, false),
        two.bearing,
        two.altitude,
        (one.altitude - two.altitude),
        two.currenttime
        from sweep1 one, sweep2 two
        where one.m_id = two.m_id;
    """
    cur.execute(sql)

    return "missile info saved."

def predict_landing():
    sql = """
        CREATE TABLE if not exists prediction(landing_time time, landing_location geometry, hitting_region text); TRUNCATE TABLE prediction;

        INSERT INTO prediction(landing_time, landing_location)
        select
        currenttime + ((last_altitude - drop_rate)* interval '1 second'),
        ST_Project(last_geom::geography, speed* (last_altitude / drop_rate), radians(last_bearing))::geometry as landing_geom
        from missile_info;

        UPDATE prediction 
        SET hitting_region = (select ST_intersects(reg.geom, landing_location) from regions reg);

    """
    cur.execute(sql)

    return "prediction is ready."


#--x--x--x--x--x--x--x--x--x OLD FUNCTIONS --x--x--x--x--x--x--x--x--

# INITIAL PART STARTS --x--x--x--x--x--x--
def createJson(filename, file_object):
        with open(filename+".json","w") as outfile:
            outfile.write(file_object)

def dropTables():
    cur.execute("DROP TABLE IF EXISTS regions, batteries, enve, cities, missiles, latest_missiles, missile_hits, projection")
    return 'Tables are dropped...'

def truncate_table(table_name):
    cur.execute(f"TRUNCATE {table_name};")

def createTables():  
    cur.execute("CREATE TABLE cities(id int, geom geometry, latitude double precision, longitude double precision);")
    cur.execute("CREATE TABLE regions(gid int, cid int, geom geometry, area int, center geometry,bbox geometry, prev_size text, reduced_size text);")
    cur.execute("CREATE TABLE missiles(m_id int, missile_type text, geom geometry, bearing double precision, altitude double precision, currentTime time);")
    cur.execute("CREATE TABLE latest_missiles(m_id int, missile_type text, geom geometry, bearing double precision, altitude double precision, currentTime time);")
    cur.execute("CREATE TABLE missile_hits(m_id int, missile_type text, geom geometry, city_id int);")
    cur.execute("CREATE TABLE if not exists projection(projected_line geometry, projected_altitude int , bearing int, closest_point_from_center geometry, distance_to_center int);")
    return 'Tables are created...'

def createBuffer(table, column, datatype):
    cur.execute(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS buffer {datatype};")
    cur.execute(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS base_area {datatype};")
    cur.execute(f"UPDATE {table} SET buffer= ST_setSRID(ST_Buffer({column}, 0.25), 4326);")
    cur.execute(f"UPDATE {table} SET base_area= ST_setSRID(ST_Buffer({column}, 0.1), 4326);")
    return f"Buffer created on table {table}"

def save_to_postgres(filename):
    with open(filename+'.json') as file:
        gj = geojson.load(file)
        for feature in gj['features']:
            geom = (json.dumps(feature['geometry']))
            if filename == 'cities':
                id = feature['properties']['id']
                latitude = feature['properties']['latitude']
                longitude = feature['properties']['longitude']
                cur.execute('INSERT INTO cities (id, geom, latitude, longitude) VALUES (%s, ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s))), %s, %s)', (id, geom ,latitude, longitude))
                print('Inserted data into cities table...')
            if filename == 'regions':
                gid = feature['properties']['gid']
                cid = feature['properties']['cid']
                prev_size = feature['properties']['prev_size']
                reduced_size = feature['properties']['reduced_size']
                cur.execute('INSERT INTO regions (gid, cid, geom, area, center, bbox, prev_size, reduced_size) VALUES (%s, %s, ST_SetSRID(ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s))),4326), ST_area(ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s))))* 0.3048,ST_SetSRID(ST_Centroid(ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s)))), 4326), ST_envelope((ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s))))) , %s, %s)', (gid, cid, geom, geom , geom, geom, prev_size, reduced_size))
                print('Inserted data into regions table...')

            if filename == 'latest_missiles':
                m_id = feature["id"]
                missile_type = feature['properties']['missile_type']
                bearing = feature['properties']['bearing']
                altitude = feature['properties']['altitude']
                currentTime = feature['properties']['current_time']
                cur.execute('INSERT INTO latest_missiles (m_id, missile_type, geom, bearing, altitude, currentTime) VALUES (%s, %s, ST_setSRID(ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s))),4326), %s, %s, %s);', (m_id, missile_type, geom, bearing, altitude, currentTime))
                cur.execute('INSERT INTO missiles (m_id, missile_type, geom, bearing, altitude, currentTime) VALUES (%s, %s, ST_setSRID(ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON(%s))),4326), %s, %s, %s);', (m_id, missile_type, geom, bearing, altitude, currentTime))
                

def saveHitsToPostgres(sql):
    cur.execute("TRUNCATE TABLE missile_hits; INSERT INTO missile_hits " + sql)

# INITIAL PART ENDS --x--x--x--x--x--x--

# --x--x---x--x---x---x---x--x---x--x---x--x--x-x

# CALCULATION PART STARTS --x--x--x--x--x--x--

# DATA
response = {"m_id":0, "missile_type":"","speed":0, "last_altitude":0,"alt_difference":0, "bearing":0, "distance":0}

def check_hits():
    sql="""INSERT INTO missile_hits
        select mi.m_id, mi.missile_type, st_intersection(mi.geom, ci.buffer) as intersection, ci.id as city_id from latest_missiles mi, cities ci where st_intersects(mi.geom, ci.buffer) = 'true';select * from missile_hits;
    """
    cur.execute(sql)
    data = cur.fetchall()
    print("-->-->-->Hits: ",len(data), " <--<--<--")

def get_nearest_missile_from_attacking_point():
    sql = """
        select 
        l_mi.m_id,
        l_mi.missile_type,
        st_distance(ST_Centroid(reg.geom), l_mi.geom, false) as distance  
        from latest_missiles l_mi, regions reg
        order by distance
        limit 1;
    """
    cur.execute(sql)
    data = cur.fetchone()
    
    response["m_id"] = data[0]
    response["missile_type"] = data[1]
    response["distance"] = data[2]
    print("Distance: ",response["distance"])
    if(response["distance"] <= (1000*1000)):
        return response
    else:
        return 0

def hasTraveled(missile):
    sql = f"""
        select * from missiles where missile_type = '{missile["missile_type"]}' and m_id = {missile["m_id"]} order by currenttime DESC limit 2;
    """
    cur.execute(sql)
    res = cur.fetchall()
    if len(res) > 1:
        return True
    else:
        return False

def decode_missile(missile):
    sql = f"""
    select st_distance(a.geom, b.geom, false) as speed,a.altitude as last_altitude, (a.altitude - b.altitude) as alt_difference, b.bearing as last_bearing
    from (select * from missiles mi where missile_type = '{missile["missile_type"]}' and m_id = {missile["m_id"]} order by currenttime DESC OFFSET 0 limit 1) as a,
    (select * from missiles mi where missile_type = '{missile["missile_type"]}' and m_id = {missile["m_id"]} order by currenttime DESC OFFSET 1 limit 1) as b;
    """
    cur.execute(sql)
    data = cur.fetchone()

    response["speed"] = data[0]
    response["last_altitude"] = data[1]
    response["alt_difference"] = data[2]
    response["bearing"] = data[3]

    return response

def lengthOfTable(table):
    cur.execute(f"Select COUNT(*) as count from {table}")
    table_count = cur.fetchone()
    return table_count[0] 

def projectPoint(missile):
    sql = f"""
    TRUNCATE TABLE projection;
        INSERT INTO projection(projected_line, projected_altitude, bearing)
        select 
        st_makeLine(geom, st_project(geom, ({missile["speed"]})*4, radians(2.0130162))::geometry),
        {missile["last_altitude"]} - (4*{missile["alt_difference"]}),
        {missile["bearing"]}
        from missiles mi 
        where missile_type = '{missile['missile_type']}'and m_id = {missile['m_id']} 
        order by currenttime DESC 
        limit 1;
        UPDATE projection SET closest_point_from_center = (SELECT st_closestPoint(pro.projected_line, reg.center) from regions reg, projection pro);
        UPDATE projection SET distance_to_center = (SELECT st_distance(st_closestPoint(pro.projected_line, reg.center), reg.center, false) from regions reg, projection pro);
        select 
        pro.projected_altitude,
        st_x(st_asText(pro.closest_point_from_center)),
        st_y(st_asText(pro.closest_point_from_center)),
        pro.distance_to_center,
        st_x(st_asText(reg.center)),
        st_y(st_asText(reg.center))
        from regions reg, projection pro;
    """
    cur.execute(sql)
    data = cur.fetchone()    
    projection_info = {
        "target_alt": data[0],
        "aim_lon":data[1],
        "aim_lat":data[2], 
        "distance_from_center":data[3],
        "firedFrom_lon":data[4],
        "firedFrom_lat":data[5]
    }

    return projection_info

def to_shp_file(table, file):
    os.system(f"""pgsql2shp  -u "postgres" -h "localhost" -P "221702" -f "shp_files/{file}" "project3" public.{table}""")
    return f"file has been saved with name: {file}"
