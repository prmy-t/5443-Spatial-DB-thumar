from time import sleep
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import random
import requests

from functions import *


app = FastAPI(
    title="🚀Missile Command🚀",
    version="0.0.1",
    terms_of_service="🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

# At the start generate game_id & fleet_id
@app.get("/start")
def start():
    global game_id, fleet_id
    game_id = random.randint(0,9)
    fleet_id = random.randint(11,20)

    return f"Game_id: {game_id}, Fleet_id: {fleet_id}"

# generate fleet & will save it to the postgres
@app.get("/Generate_fleet")
def generate_fleet():
    fleet = requests.get("https://battleshipgame.fun:8080/generate_fleet/?fleetName=noobmaster69&hash=217323467714198537483354125622023591364").json()
    
    return save_ships_to_postgres(fleet)

# will generate random location on the given section and assign it to the ships.
@app.get("/get_battle_location")
def get_battle_location():
    location = requests.get(f"""https://battleshipgame.fun:8080/get_battle_location/?hash=217323467714198537483354125622023591364&game_id={game_id}""").json()
    bbox = location["bbox"]
    # return location
    create_Bbox(bbox["UpperLeft"],bbox["LowerRight"], location["section"], location["width"],location["height"])
    generate_point(location["section"])
    return "Location assigned to ships."

# Post the ship data to the server 
@app.get("/steam_to_battle")
def steam_to_battle():
    final_product = show_final_product()
    res = requests.post("https://battleshipgame.fun:8080/steam_to_battle?hash=217323467714198537483354125622023591364", data= final_product).json()
    return res

# Create a bounding box from given coordinates.
@app.get("/Specify_Bbox")
def specify_Bbox():
    """ Give the input of coordinates in the formate of: lon, lat"""
    return create_Bbox()


@app.get("/Radar_Sweep")
def radar_sweep():
    """ Gets the radar sweep from server."""
    save_ships_to_postgres('ships')
    return 'sweep received, data saved to postgres'

@app.get("/moveGuns")
def moveGuns(ship_id,gun_id,gun_position):
    move_guns(ship_id,gun_id,gun_position)

@app.get("/change_fleet_direction")
def change_fleet_direction(bearing):
    changeFleetDirection(bearing)

@app.get("change_speed_direction")
def change_speed_direction(ship_id, speed, bearing):
    changeSpeedDirection(ship_id, speed, bearing)


@app.get("/generate-final-product")
def final_product():
    return show_final_product()
    

if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=8000, log_level="debug", reload=True)