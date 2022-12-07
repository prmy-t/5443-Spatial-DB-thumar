from pick import pick
from api import *
from data import data

title = ""
options = []


def main_menu():
    title = "Please choose your Action: "
    options = []
    for ele in data:
        options.append(ele["item"])
    options.append("Exit")
    selected = pick(options, title, "👉🏻")
    return selected[0]

def register_menu():
    title = "You have already registered."
    options = ["Go back"]
    selected = pick(options, title, "👉🏻")
    return selected[0]

def start_menu():
    title = "Success: "+ start() + f"\n -> {data[1]['description']}"
    options = ["Go back"]
    selected = pick(options, title, "👉🏻")
    return selected[0]

def generate_fleet_menu():
    title = "Success: "+ generate_fleet() + f"\n -> {data[2]['description']}"
    options = ["Go back"]
    selected = pick(options, title, "👉🏻")
    return selected[0]

def battle_location_menu():
    title = "Success: "+ get_battle_location() + f"\n -> {data[3]['description']}"
    options = ["Go back"]
    selected = pick(options, title, "👉🏻")
    return selected[0]

def steam_to_battle_menu():
    title = "Success: "+ steam_to_battle() + f"\n -> {data[3]['description']}"
    options = ["Go back"]
    selected = pick(options, title, "👉🏻")
    return selected[0]


while True:
    selected = main_menu()

    if selected == "Register":
        selected = register_menu()
    elif selected == "Go back":
        selected = main_menu()
    elif selected == "Start":
        selected = start_menu()
    elif selected == "Generate Fleet":
        selected = generate_fleet_menu()
    elif selected == "Get Battle Location":
        selected = battle_location_menu()
    elif selected == "Steam To Battle":
        selected = battle_location_menu()
    elif selected == "Exit":
        break