from time import sleep
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import json
import requests
from datetime import datetime, timedelta

from functions import *

"""
           _____ _____   _____ _   _ ______ ____
     /\   |  __ \_   _| |_   _| \ | |  ____/ __ \
    /  \  | |__) || |     | | |  \| | |__ | |  | |
   / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
  / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
 /_/    \_\_|   |_____| |_____|_| \_|_|    \____/
The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
"""
# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.

app = FastAPI(
    title="🚀Missile Command🚀",
    version="0.0.1",
    terms_of_service="🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

"""
  ___   _ _____ _
 |   \ /_\_   _/_\
 | |) / _ \| |/ _ \
 |___/_/ \_\_/_/ \_\
"""
#storing team_id, after receiving from server.
global_team_id = 0
# to save the missile data for solution.
firing_point = ""
nearest_missile = {};
isTurnedOn = True


"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/
"""

@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/REGISTER")
def region():
    res = requests.get("http://missilecommand.live:8080/REGISTER").json()
    
    #error handling
    if not res:
        return {'error':"no response"}

    #Classifying received data
    team_id = res['id']
    region_obj = json.dumps(res['region'])
    cities_obj = json.dumps(res['cities'])
    
    #Creating JSON files of the Region and Cities...
    createJson('regions', region_obj)
    createJson('cities', cities_obj)

    #Creating tables in Postgres...
    dropTables()
    createTables()

    #Saving JSON files to Postgres table...
    save_to_postgres('cities')
    save_to_postgres('regions')
    createBuffer('cities', 'geom', 'geometry')

    res = f"""Team Id: {team_id}.\
    Received Region.\
    Received Cities."""
    return res
    
@app.get("/calculate_area")
def calculate_area():
    return get_area()

@app.get("/show_bounding_box")
def get_bounding_box():
    return get_Bbox()

@app.get("/create_batteries")
def create_batteries():
    return generate_batteries()

@app.get("/START")
def missileInfo(team_id):
    global_team_id = team_id
    starting = requests.get(f"http://missilecommand.live:8080/START/{team_id}").json()
    return starting[0]

@app.get("/determine_hits")
def determine_hits():
    return get_sweep()

@app.get("/radar_sweep")
def radar_sweep():

    sql_find_hits = "SELECT ci.buffer, mi.missile_type, mi.geom FROM missiles mi, cities ci WHERE ST_Intersects(mi.geom, ci.buffer);"
    
    while(True):
        print('Getting sweep...')
        sweep = requests.get(f"http://missilecommand.live:8080/RADAR_SWEEP").json()

        if sweep:
            truncate_table('latest_missiles')
            sweep_obj = json.dumps(sweep)
            #CREATE: JSON file of the necessary data...
            createJson('latest_missiles', sweep_obj)
            #SAVE: JSON files to Postgres table...
            save_to_postgres('latest_missiles')
            
            #PRINT: NUM of missiles flying...
            missiles_count = len(sweep['features'])
            print(missiles_count, ' Missiles are flying...')


            #A. Plan of solution
            #determine target missile.
            target_missile = get_nearest_missile_from_attacking_point()
            if(target_missile == 0):
                print("No missiles in firing area.")
            else:
                print({"targeted_missile":target_missile})
                # Checking if the Missile has traveled.
                if hasTraveled(target_missile):
                    #DECODE: missile Speed, latest altitude & bearing.
                    target_missile_info = decode_missile(target_missile)
                    # print(target_missile)
                    #PROJECTION: 
                    projection_info = projectPoint(target_missile_info)

                    #POSTING_SOLUTION
                    print("searching solution...")
                    now = datetime.now()

                    missile_speed = target_missile_info["speed"]
                    center_to_projection_dist = projection_info["distance_from_center"]
                    sec = int(center_to_projection_dist/missile_speed)
                    fired_time = now.strftime("%m/%d/%Y %H:%M:%S")
                    expected_hit_time = now + timedelta(seconds=sec)
                    expected_hit_time = expected_hit_time.strftime("%m/%d/%Y %H:%M:%S")

                    requests.post("http://missilecommand.live:8080/FIRE_SOLUTION", json = {
                        "team_id": global_team_id,
                        "target_missile_id": target_missile_info["m_id"],
                        "missile_type": target_missile_info["missile_type"],
                        "fired_time": fired_time,
                        "firedfrom_lat": projection_info["firedFrom_lat"],
                        "firedfrom_lon": projection_info["firedFrom_lon"],
                        "aim_lat": projection_info["aim_lat"],
                        "aim_lon": projection_info["aim_lon"],
                        "expected_hit_time": expected_hit_time,
                        "target_alt": projection_info["target_alt"]
                    })
                    print("solution Implemented...")

            #B. Checking for hits
            check_hits()
            sleep(1)
            print("\n")
        else:
            print('Attack finished !')

@app.get("/create_shp_file/")
def create_shp_file(tableName):
    return to_shp_file(tableName, tableName)

@app.get("/RESET_Game")
def reset():
    reset = requests.get("http://missilecommand.live:8080/RESET").json()
    return reset['Finished'] 

if __name__ == "__main__":
    uvicorn.run("test_api:app", host="127.0.0.1", port=3000, log_level="debug", reload=True)