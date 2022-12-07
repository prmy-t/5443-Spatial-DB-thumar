data = [
  {
    "item": "Register",
    "description": "Call this once ever.",
    "params": {
      "hash_key": "string",
      "fleet_name": "string"
    },
    "cmd": "gameStart",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy'",
        "explanation": "see description "
      }
    ],
    "returns": "{'success':True/False}"
  },
  {
    "item": "Start",
    "description": "Places you on the player queue to allow you to take a turn.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int"
    },
    "cmd": "gameStart",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy'",
        "explanation": "see description "
      }
    ],
    "returns": "{'success':True/False}"
  },
  {
    "item": "Generate Fleet",
    "description": "Creates a new fleet for current game instance.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int"
    },
    "cmd": "generateFleet",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy'",
        "explanation": "see description "
      }
    ],
    "returns": "{Large json file with all of your fleet data.}"
  },
  {
    
    "item": "Get Battle Location",
    "description": "Sends back the bounding box and cardinal location in the bbox for you to move/position your fleet.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int"
    },
    "cmd": "battleLocation",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy'}",
        "explanation": "see description "
      }
    ],
    "returns": {
      "bbox": {
        "UpperLeft": "{'lon':dd.ffffffff,'lat':dd.ffffffff}",
        "LowerRight": "{'lon':dd.ffffffff,'lat':dd.ffffffff}"
      },
      "CardinalLocation": "SSE"
    }
  },
  {
    "item": "Steam To Battle",
    "description": "Place your fleet at its pseudo random location in the game board.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int",
      "ship_id": "list[int]",
      "location": "list[tuples(float,float)]",
      "bearing": "list[float]"
    },
    "cmd": "positionFleet",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [1,2,3,...,N],'location': [(lon1,lat1),(lon2,lat2),(lon3,lat3),...(lonN,latN)],'bearing':[bearing1,bearing2,bearing3,...,bearingN]}",
        "explanation": "Places all your fleets ships at specified locations. "
      }
    ],
    "returns": "{'success':True/False}"
  },
  {
    "item": "Ships Speed",
    "description": "Sets the speed for one or more ships.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int",
      "ship_id": "list[int]",
      "speed": "list[float]"
    },
    "cmd": "shipsSpeed",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [],'speed': [21]}",
        "explanation": "Set the speed of all ships in the fleet to 21km per hour"
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [16],'speed': [21]}",
        "explanation": "Set the speed of ship with id 16 to 21km per hour"
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [16,19,23,24],'speed': [18,18,21,21]}",
        "explanation": "Set the speed of ship with id 16 to 18km, ship with id 19 to 18km ship 23 to 21km and so on"
      }
    ],
    "returns": "{'success':True/False}"
  },
  {
    "item": "Move Ships",
    "description": "Starts moving one or more ships in the fleet in direction each ship is facing.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int",
      "ship_id": "list[int]",
      "distance": "list[float]"
    },
    "cmd": "moveShips",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [],'distance': [20000]}",
        "explanation": "Move all ships in the fleet 20000 meters at each ships current heading."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [16],'distance': [1000]}",
        "explanation": "Move the ship with id 16 1000 meters at its current heading."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [16,19,23,24],'distance': [3000,2000,1500,20000]}",
        "explanation": "Move the ship with id 16 3000 meters in its current heading, ship with id 19 2000m at its heading, ship with id 23 1500 meters ... and so on."
      }
    ],
    "returns": "{'success':True/False}"
  },
  {
    "item": "Turn Ships",
    "description": "Starts turning one or more ships in the fleet giving each listed a new heading.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int",
      "ship_id": "list[int]",
      "heading": "list[float]"
    },
    "cmd": "turnShips",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [],'heading': [277]}",
        "explanation": "Turn all ships to the new heading of 277 degrees."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [16],'heading': [188]}",
        "explanation": "Turn the ship with id 16 to a new heading of 188 degrees."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id': [16,19,23],'heading': [180,90,270]}",
        "explanation": "Turn ship with id 16 to 180 degrees, ship with id 19 to 90 degrees meters, and ship with id 23 to a new heading of 270 degrees."
      }
    ],
    "returns": "{'success':True/False}"
  },
  {
    "item": "Move Guns",
    "description": "Starts turning one or more ships guns toward a particular bearing and elevation. The bearing is in relation to the ship.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int",
      "ship_id": "list[int]",
      "gun_id": "list[float]",
      "b_e": "list[(float,float)]"
    },
    "cmd": "moveGuns",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy','ship_id':[],'gun_id':[],'b_e': [(90,25)]}",
        "explanation": "Turn all ships guns in your fleet to starboard (90 degrees) and at an elevation of 25 degrees."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id':[23],'gun_id':[1,2,3,4],'b_e': [(90,25),(90,25),(270,15),(270,15)]}",
        "explanation": "Turn guns 1 and 2 on ship 23 to starboard (90 degrees) with elevation 25 degrees and guns 3,4 to port (270 degrees) and at an elevation of 15 degrees."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id':[23,24,25],'gun_id':[[1,2,3,4],[1,2,3,4],[1,2,3,4]],'b_e': [[(90,25),(90,25),(270,15),(270,15)],[(90,25),(90,25),(270,15),(270,15)],[(90,25),(90,25),(270,15),(270,15)],[(90,25),(90,25),(270,15),(270,15)]]}",
        "explanation": "I'm not sure how I feel about this big command.'"
      }
    ],
    "returns": "{'success':True/False}"
  },
  {
    "item": "Fire Guns",
    "description": "Starts turning one or more ships guns toward a particular bearing and elevation. The bearing is in relation to the ship.",
    "params": {
      "hash_key": "string",
      "fleet_id": "int",
      "ship_id": "list[int]",
      "gun_id": "list[float]"
    },
    "cmd": "fireGuns",
    "examples": [
      {
        "command": "{'fleet_id': 'us_navy','ship_id':[],'gun_id':[]}",
        "explanation": "Fire every gun in your fleet at its current bearing and elevation."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id':[23],'gun_id':[]}",
        "explanation": "Fire all the guns on ship 23 at their current bearing and elevation."
      },
      {
        "command": "{'fleet_id': 'us_navy','ship_id':[23,24],'gun_id':[[1,3,5],[2,4]]}",
        "explanation": "Fire guns 1,3,5 on ship 23 and fire guns 2,4 on ship 24 at their current bearing and elevation."
      }
    ],
    "returns": "{'success':True/False}"
  }
]
