from fastapi import Request
import psycopg2
import psycopg2.extras
import os
from fastapi import FastAPI

app = FastAPI()
DATABASE_URL = 'postgresql://postgres:221702@localhost:5432/project1'

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="project1",
    user="postgres",
    password="221702"
)

cur = conn.cursor()

@app.get("/find-all")
def home(request:Request):
    sql = "SELECT * FROM airports"
    cur.execute(sql)
    data = cur.fetchall()
    return data;

@app.get("/find/{city}")
def home(request:Request):
    city = request.url.path.strip('/').split('/')[1].capitalize()
    sql = "SELECT * FROM airports WHERE city='{0}'".format(city)
    cur.execute(sql)
    data = cur.fetchall()
    return data;

@app.get("/find-closest/")
def home(lat, lon):
    sql = "SELECT A.geom,ST_Distance (A.geom, ST_SetSRID(ST_Point ({0}, {1}) ,4326)) as dist, name, city, country FROM airports as A WHERE ST_Distance (A.geom, ST_SetSRID(ST_Point ({0}, {1}), 4326)) < 1000 order by dist LIMIT 1".format(lon,lat)
    cur.execute(sql)
    data = cur.fetchall()
    return data





# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

