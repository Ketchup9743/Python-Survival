import time

def register():
    global username
    username = input("What is your username?")
    
role_data = {
    "Engineer": {
        "health": 100,
        "power": 50,
        "defense": 30,
        "skills": ["Attack", "Protect", "Upgrade"],
        "weapon": "Pocket Knife",
    },
    "Medic": {
        "health": 125,
        "power": 60,
        "defense": 20,
        "skills": ["Heal", "Attack", "Buff"],
        "weapon": "Scalpel",
    },
    "Support": {
        "health": 110,
        "power": 20,
        "defense": 80,
        "skills": ["Attack", "Buff", "Debuff"],
        "weapon": "Sword",
    },
    "Miner": {
        "health": 100,
        "power": 80,
        "defense": 40,
        "skills": ["Attack", "PickPocket", "Cover"],
        "weapon": "Pickaxe",
    },
    "Soldier": {
        "health": 150,
        "power": 70,
        "defense": 70,
        "skills": ["Attack", "Grenade", "Cover"],
        "weapon": "Rifle",
    },
    "Divine Caster": {
        "health": 80,
        "power": 150,
        "defense": 60,
        "skills": ["Divine Beam", "Healing Light", "Hardening Aura"],
        "weapon": "Divine Staff",
    },
}
def skills():
    skill_use = input("Select one of your skills")
def role_selection():
    for role in role_data:
        print(role)

    role_select = input(f"Hello! {username}, please select your role from the list above:")
    if role_select == "Engineer":
        role_data["Engineer"] = True
        confirm = input("Are you sure you want to select Engineer as your role? Y / N")
        if confirm == "Y":
            print("Role Selected!")
        elif confirm == "N":
            role_selection()

    elif role_select == "Medic":
        role_data["Medic"] = True
        confirm = input("Are you sure you want to select Medic as your role? Y / N")
        if confirm == "Y":
            print("Role Selected!")
        elif confirm == "N":
            role_selection()

    elif role_select == "Support":
        role_data["Support"] = True
        confirm = input("Are you sure you want to select Support as your role? Y / N")
        if confirm == "Y":
            print("Role Selected!")
        elif confirm == "N":
            role_selection()

    elif role_select == "Miner":
        role_data["Miner"] = True
        confirm = input("Are you sure you want to select Miner as your role? Y / N")
        if confirm == "Y":
            print("Role Selected!")
        elif confirm == "N":
            role_selection()

    elif role_select == "Soldier":  
        role_data["Soldier"] = True
        confirm = input("Are you sure you want to select Soldier as your role? Y / N")
        if confirm == "Y":
            print("Role Selected!")
        elif confirm == "N":
            role_selection()

    else:
        print("Invalid role selected. Please try again.")
        return register()
register()
role_selection()
def tutorial():
    print("Welcome to the tutorial!")

play_tutorial = input("Would you like to play the tutorial? Y / N")
if play_tutorial = "Y":
    tutorial()
else:
    pass
