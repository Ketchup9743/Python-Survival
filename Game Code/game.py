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
    def role_selection():
        for role in roles:
            print(role)

        role_select = input(f"Hello! {username}, please select your role from the list above:")
        if role_select == "Engineer":
            roles["Engineer"] = True
            confirm = input("Are you sure you want to select Engineer as your role? Y / N")
            if confirm = "Y":
                print("Role Selected!")
            elif confirm = "N":
                role_selection()

        elif role_select == "Medic":
            roles["Medic"] = True
            confirm = input("Are you sure you want to select Medic as your role? Y / N")
            if confirm = "Y":
                print("Role Selected!")
            elif confirm = "N":
                role_selection()

        elif role_select == "Support":
            roles["Support"] = True
            confirm = input("Are you sure you want to select Support as your role? Y / N")
            if confirm = "Y":
                print("Role Selected!")
            elif confirm = "N":
                role_selection()

        elif role_select == "Miner":
            roles["Miner"] = True
            confirm = input("Are you sure you want to select Miner as your role? Y / N")
            if confirm = "Y":
                print("Role Selected!")
            elif confirm = "N":
                role_selection()

        elif role_select == "Soldier":  
            roles["Soldier"] = True
            confirm = input("Are you sure you want to select Soldier as your role? Y / N")
            if confirm = "Y":
                print("Role Selected!")
            elif confirm = "N":
                role_selection()

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