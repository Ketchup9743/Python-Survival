import time
import json

def register():
    username = input("What is your username?")
    roles = {
        "Engineer": False,
        "Medic": False,
        "Support": False,
        "Miner": False,
        "Soldier": False
    }

    for role in roles:
        print(role)
    role_select = input(f"Hello! {username}, please select your role from the list above:")
    
    if role_select == "Engineer":
        roles["Engineer"] = True
    elif role_select == "Medic":
        roles["Medic"] = True
    elif role_select == "Support":
        roles["Support"] = True
    elif role_select == "Miner":
        roles["Miner"] = True
    elif role_select == "Soldier":  
        roles["Soldier"] = True
    else:
        print("Invalid role selected. Please try again.")
        return register()
register()

def tutorial():
    play_tutorial = ("Would you like to play the tutorial? Y / N")
    if play_tutorial =  Y:
        pass
    elif play_tutorial = N:
        pass
    else:
        return tutorial()
tutorial()