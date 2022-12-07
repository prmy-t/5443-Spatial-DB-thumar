import random
import json
import psycopg2
import math
from psycopg2.extras import Json

conn = psycopg2.connect("dbname=bettleship user=postgres password=221702")
conn.autocommit = True
cur = conn.cursor()

#DATA
cardinalList = ["N","NNE","NE","ENE","E","ESE","SE","SSE", "S","SSW","SW","WSW","W","WNW","NW","NNW"]
cardinalDegree = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
cardinalMax = [348.75, 11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25]
cardinalMin = [11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75]


def create_Bbox():
    upper_lon,upper_lat = [-4.660732777703032, 44.54346587896811]
    lower_lon,lower_lat = [-4.657947669987465, 44.54306084373429]
    print(upper_lat)
    print(lower_lat)
    
    sql = f"""DROP TABLE if exists Bbox; 
            create table Bbox(box geometry, center geometry);
            INSERT INTO Bbox(box)
            select ST_MakeEnvelope({upper_lon}, {lower_lat}, {lower_lon}, {upper_lat}, 4326)::geometry;
            UPDATE Bbox set center = ST_SetSRID(ST_Centroid(box),4326);
    """
    cur.execute(sql)
    cur.execute("""select ship_id, st_y(st_astext(location)), st_x(st_astext(location)) from ships;""")
    data = cur.fetchall()[0]
    return "Bbox created."

def save_to_postgres(filename):
    create_tables()

    with open("ships.json") as file:
        json_file = json.load(file)
        for ship in json_file:
            
            # SHIPS TABLE
            ship_id = ship["id"]
            category = ship["category"]
            shipClass = ship["shipClass"]
            length = ship["length"]
            width = ship["width"]
            speed = ship["speed"]
            turn_radius = ship["turn_radius"]
            location = ship["location"]


            #SHIP_ARMOR
            ship_id = ship["id"]
            hull = ship["armor"]["hull"]
            deck = ship["armor"]["deck"]

            #SHIP_armament
            for armament in ship["armament"]:
                gun_name = armament["gun"]["name"],
                gun_info = armament["gun"]["info"],
                ammo_type = armament["gun"]["ammoType"],
                
                ammo = armament["gun"]["ammo"],
                gun_rof = armament["gun"]["rof"],
                gun_propellant = armament["gun"]["propellant"]
                pos = armament["pos"]
                cur.execute('INSERT INTO ship_armaments VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', (ship_id, gun_name, gun_info, [json.dumps(ammo_type)], [json.dumps(ammo)], gun_rof, gun_propellant, pos))

            cur.execute('INSERT INTO ships(ship_id,category,shipClass,length,width,speed,turn_radius,location) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', 
            (ship_id, category, shipClass, length, width, speed, turn_radius, location))

            cur.execute('INSERT INTO ship_armors VALUES(%s, %s, %s)',(ship_id, hull, deck))
        
    return "Data has been saved"

##Supporting Functions...

def create_tables():
    sql_create_ship_table = """
    create table if not exists ships(
        table_id SERIAL,
        ship_id smallint,
        category text,
        shipClass text,
        length smallint,
        width smallint,
        speed smallint,
        turn_radius smallint,
        location geometry); TRUNCATE TABLE ships;ALTER SEQUENCE ships_table_id_seq RESTART with 1; 
        """
    sql_create_armaments_table = """
        create table if not exists ship_armaments(
        ship_id smallint,
        gun_name text,
        gun_info text,
        ammo_type text[],
        ammo text[],
        gun_rof smallint,
        gun_propellant smallint,
        POS smallint
        ); TRUNCATE TABLE ship_armaments;
    """
    sql_create_armor_table = """
    create table if not exists ship_armors(
        ship_id smallint,
        hull smallint,
        deck smallint); TRUNCATE TABLE ship_armors;
        """

    cur.execute(sql_create_ship_table)
    cur.execute(sql_create_armaments_table)
    cur.execute(sql_create_armor_table)

    return "table has been created"

def generate_point(sector):
    random_degree = random.uniform(0, 360)
    degrees = int(float(random_degree))
    index = int((random_degree + 11.25) / 22.5)
    direction = cardinalList[index % 16]
    min_degree = cardinalMin[index % 16]
    max_degree = cardinalMax[index % 16]

    print({"random_degree":random_degree,"direction":direction,"min_degree":min_degree,"max_degree":max_degree})
    cur.execute(f"""CREATE TABLE if not exists region(geom geometry, center geometry, p1 geometry, p2 geometry, p3 geometry);
    TRUNCATE TABLE region;
    INSERT INTO region(p1, p2, p3)
    SELECT 
    center,
    ST_Intersection( ST_MakeLine(center, ST_Project(center::geography, 500, radians({min_degree}))::geometry), ST_Boundary(box)) ,
    ST_Intersection(ST_MakeLine(center, ST_Project(center::geography, 500, radians({max_degree}))::geometry), ST_Boundary(box))
    from Bbox;
    UPDATE region set geom = ST_MakePolygon(ST_MakeLine(ARRAY[p1, p2, p3, p1]));
    UPDATE region set center = ST_SetSRID(ST_Centroid(geom),4326)
    """)
    generate_ship_location(26)
    return "success"

def generate_ship_location(ship_count):
    ship_deployed = 0
    cur.execute("create table if not exists temp_points(id SERIAL, point geometry); Truncate table temp_points;ALTER SEQUENCE temp_points_id_seq RESTART with 1;")
    sql_insert = "INSERT INTO temp_points(point)"
    
    if ship_deployed <= 0:
        sql_make_center = f"""{sql_insert} select center from region;"""
        cur.execute(sql_make_center)
        ship_deployed += 1
    
    outer_loop = math.ceil(ship_count/8)
    for i in range(outer_loop):
        print(i)
        # for j in range(4):
        
        sql_make_plus = f"""
        {sql_insert} select ST_Project(center, {(i+1)*222}, radians(90))::geometry from region;
        {sql_insert} select ST_Project(center, {(i+1)*222}, radians(270))::geometry from region;
        {sql_insert} select ST_Project(center, {(i+1)*111}, radians(180))::geometry from region;
        {sql_insert} select ST_Project(center, {(i+1)*111}, radians(0))::geometry from region;
        """
        cur.execute(sql_make_plus)
        cur.execute("select st_astext(point) from temp_points order by id offset 1 limit 2;")

        plus = cur.fetchall()
        for point in plus:
            p = list(point)[0]
            print(p)
            sql_make_minus = f"""
            {sql_insert} select ST_Project('{p}'::geography, {(i+1)*111}, radians(180))::geometry from region;
            {sql_insert} select ST_Project('{p}'::geography, {(i+1)*111}, radians(0))::geometry from region;
            """
            cur.execute(sql_make_minus)