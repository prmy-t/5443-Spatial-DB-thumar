import time
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


def create_Bbox(UpperLeft, lowerRight, section, width, height):
    ulLon = UpperLeft["lon"]
    ulLat = UpperLeft["lat"]
    lrLon = lowerRight["lon"]
    lrLat = lowerRight["lat"]
    sql = f"""DROP TABLE if exists Bbox; 
            create table Bbox(box geometry, section text, center geometry, width int, height int);
            INSERT INTO Bbox(box, section, width, height)
            select 
            ST_MakeEnvelope({ulLon}, {ulLat}, {lrLon}, {lrLat}, 4326)::geometry,
            '{section}',
            {width},
            {height}
            ;
            UPDATE Bbox set center = ST_SetSRID(ST_Centroid(box),4326);
    """
    cur.execute(sql)
    return "Bbox created."

def save_ships_to_postgres(ships):
    create_ships_tables()

    for ship in ships:

        #SHIP_Table
        ship_id = ship["id"]
        identifier = ship["identifier"]
        category = ship["category"]
        shipClass = ship["shipClass"]
        length = ship["length"]
        width = ship["width"]
        speed = ship["speed"]
        turn_radius = ship["turn_radius"]

        cur.execute('INSERT INTO ships(ship_id, identifier, category,shipClass,length,width, speed,turn_radius) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', (ship_id, identifier, category, shipClass, length, width, speed, turn_radius))

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

        #SHIP_ARMOR
        ship_id = ship["id"]
        hull = ship["armor"]["hull"]
        deck = ship["armor"]["deck"]

        cur.execute('INSERT INTO ship_armors VALUES(%s, %s, %s)',(ship_id, hull, deck))

    return "Fleet has been generated."


##Supporting Functions...

def create_ships_tables():
    sql_create_ship_table = """
    create table if not exists 
    ships(
        table_id SERIAL,
        bearing smallint,
        ship_id smallint,
        identifier text,
        category text,
        shipClass text,
        length smallint,
        width smallint,
        torpedoLaunchers smallint,
        speed smallint,
        turn_radius smallint,
        location geometry
    ); 
    TRUNCATE TABLE ships;ALTER SEQUENCE ships_table_id_seq RESTART with 1; 
        """
    sql_create_armaments_table = """
        create table if not exists 
        ship_armaments(
            ship_id smallint,
            gun_name text,
            gun_info text,
            ammo_type text[],
            ammo text[],
            gun_rof smallint,
            gun_propellant smallint,
            POS smallint
        ); 
        TRUNCATE TABLE ship_armaments;
    """
    sql_create_armor_table = """
    create table if not exists 
    ship_armors(
        ship_id smallint,
        hull smallint,
        deck smallint
    ); 
    TRUNCATE TABLE ship_armors;
    """

    cur.execute(sql_create_ship_table)
    cur.execute(sql_create_armaments_table)
    cur.execute(sql_create_armor_table)

    return "table has been created"


def generate_point(section):
    
    # cur.execute("select section from bbox;")
    # section = cur.fetchone()[0]

    index = cardinalList.index(section)
    
    cur.execute("select count(*) from ships;")
    ship_count = cur.fetchall()[0][0]
    direction = cardinalList[index % 16]
    min_degree = cardinalMin[index % 16]
    max_degree = cardinalMax[index % 16]

    cur.execute(f"""CREATE TABLE if not exists region(geom geometry, center geometry, p1 geometry, p2 geometry, p3 geometry);
    TRUNCATE TABLE region;
    INSERT INTO region(p1, p2, p3)
    SELECT 
    center,
    ST_Intersection( ST_MakeLine(center, ST_Project(center::geography, 100000, radians({min_degree}))::geometry), ST_Boundary(box)) ,
    ST_Intersection(ST_MakeLine(center, ST_Project(center::geography, 100000, radians({max_degree}))::geometry), ST_Boundary(box))
    from Bbox;
    UPDATE region set geom = ST_MakePolygon(ST_MakeLine(ARRAY[p1, p2, p3, p1]));
    UPDATE region set center = ST_SetSRID(ST_Centroid(geom),4326);
    """)
    generate_ship_location(ship_count, index)

def generate_ship_location(ship_count, sector_index):
    ship_deployed = 0
    oppositeBearing = float(cardinalDegree[(sector_index + 8) % 16])
    cur.execute("create table if not exists temp_points(id SERIAL, point geometry, bearing smallint); Truncate table temp_points;ALTER SEQUENCE temp_points_id_seq RESTART with 1;")
    sql_insert = "INSERT INTO temp_points(point, bearing)"
    
    if ship_deployed <= 0:
        sql_make_center = f"""{sql_insert} select center,{oppositeBearing} from region;"""
        cur.execute(sql_make_center)
        ship_deployed += 1
    
    outer_loop = math.ceil(ship_count/8)
    for i in range(outer_loop):
        # for j in range(4):
        
        sql_make_plus = f"""
        {sql_insert} select ST_Project(center, {(i+1)*222}, radians(90))::geometry, {oppositeBearing} from region;
        {sql_insert} select ST_Project(center, {(i+1)*222}, radians(270))::geometry, {oppositeBearing} from region;
        {sql_insert} select ST_Project(center, {(i+1)*111}, radians(180))::geometry, {oppositeBearing} from region;
        {sql_insert} select ST_Project(center, {(i+1)*111}, radians(0))::geometry, {oppositeBearing} from region;
        """
        cur.execute(sql_make_plus)
        cur.execute("select st_astext(point) from temp_points order by id offset 1 limit 2;")

        plus = cur.fetchall()
        for point in plus:
            p = list(point)[0]
            sql_make_minus = f"""
            {sql_insert} select ST_Project('{p}'::geography, {(i+1)*111}, radians(180))::geometry, {oppositeBearing} from region;
            {sql_insert} select ST_Project('{p}'::geography, {(i+1)*111}, radians(0))::geometry, {oppositeBearing} from region;
            """
            cur.execute(sql_make_minus)
    
    sql_assign_location = """update ships set location = tp.point, bearing = tp.bearing from temp_points tp where tp.id = table_id;"""
    cur.execute(sql_assign_location)
    return "Location generated."

def changeSpeedDirection(ship_id, speed, bearing):
    sql = f"""
     UPDATE ships
     SET speed = {speed}, bearing = {bearing}
     WHERE ship_id = {ship_id}
    """

    cur.execute(sql)

    return "speed and direction has been changed"

def changeFleetDirection(bearing):
    sql = f"""UPDATE ships SET bearing = {bearing}"""
    cur.execute(sql)

    return "Fleet direction has been changed"

def move_guns(ship_id, gun_id, pos):
    sql = f"""
        UPDATE gun_armaments
        SET pos = {pos}
        WHERE ship_id = {ship_id};
    """
    cur.execute(sql)
    return "moved"
    
def show_final_product():
    cur.execute("""
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
    """)
    data = cur.fetchall()
    arr = []
    ts = int(time.time())
    for i in data:
        i[0]["location"]["timeStamp"] = ts
        arr.append(i[0])

    final_product = json.dumps(arr)

    with open("final_product.json", "w") as file:
        file.write(final_product)

    return final_product