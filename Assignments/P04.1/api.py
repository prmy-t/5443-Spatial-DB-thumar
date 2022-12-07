from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

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


@app.get("/Specify_Bbox")
def specify_Bbox():
    """ Give the input of coordinates in the formate of: lon, lat"""
    return create_Bbox()

@app.get("/Radar_Sweep")
def radar_sweep():
    """ Gets the radar sweep from server."""
    save_to_postgres('ships')
    return 'sweep received, data saved to postgres'

@app.get("/Generate_Location")
def generate_location():
    """Select from Sector:  
        N,NNE,NE,
        ENE,E,ESE,
        SE,SSE,S,
        SSW,SW,
        WSW,W,WNW,
        NW,NNW
        """
    return generate_point("N")

    

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)