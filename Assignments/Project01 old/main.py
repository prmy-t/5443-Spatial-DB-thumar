from fastapi import Request, Response
import psycopg2
import psycopg2.extras
import os
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#cors
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]


app = FastAPI(middleware=middleware)

# origins = [
#         "*"
#     ]
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins="*",
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
# )

#SQL_Queries
sql_dict = {
    "create_table_sql": """
        DROP TABLE IF EXISTS airport;
        CREATE TABLE public.airports
        (
            id smallint,
            name character varying(100),
            city character varying(35),
            country character varying(35),
            "3-code" character varying(3),
            "4-code" character varying(4), 
            geom geometry,
            lat numeric(12,9),
            lon numeric(12,9),
            elevation smallint,
            gmt character varying(5),
            tz_short character varying(3), 
            timezone character varying(30), 
            type character varying(7)
        )
    """,
    'copy_csv_sql': """
    copy airports(id, name, city, country, "3-code", "4-code", lat, lon, elevation, gmt, tz_short, timezone, type) 
    from '/Users/prmy/Documents/5443-Spatial-DB-thumar/Assignments/Project01/airports.csv'
    with delimiter ',' csv header;
    """,
    'update_geom_sql':"""
    UPDATE airports SET geom = ST_SetSRID(ST_MakePoint(lon,lat), 4326);
    """
}

#Connection
conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="project1",
        user="postgres",
        password="221702"
    )
conn.autocommit = True
cur = conn.cursor()

#Functions...
def load_data(sql, cur):
    fire_api(sql['create_table_sql'], cur, False)
    fire_api(sql['copy_csv_sql'], cur, False)
    fire_api(sql['update_geom_sql'], cur, False)
    
def fire_api(sql, cur,fetch):
    cur.execute(sql)
    res = cur.fetchall() if fetch else 0
    return res

#Load_the_data


## API
#Home
@app.get("/")
def home(res:Response):
    
    return '''This is home'''

#Find_all
@app.get("/find-all")
def findAll(request:Request):
    sql = "SELECT * FROM airports"
    return fire_api(sql, cur, True)

#Find_by_airport_code
@app.get("/find/{code}")
def findByCode(request:Request, res:Response):
    code = request.url.path.strip('/').split('/')[1].upper()
    sql = """SELECT * FROM airports WHERE "3-code"='{0}'""".format(code)
    res = fire_api(sql, cur, True)
    return res

#Find_closest_point
@app.get("/find-closest/")
def findClosest(lat, lon):
    sql = "SELECT A.geom,ST_Distance (A.geom, ST_SetSRID(ST_Point ({0}, {1}) ,4326)) as distance, name, city, country,lat, lon FROM airports as A WHERE ST_Distance (A.geom, ST_SetSRID(ST_Point ({0}, {1}), 4326)) < 1000 order by distance LIMIT 1".format(lon,lat)
    return fire_api(sql, cur, True)

if __name__ == "__main__":
    load_data(sql_dict,cur)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)