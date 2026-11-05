import random


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
    "Guardian": {
        "health": 170,
        "power": 55,
        "defense": 85,
        "skills": ["Attack", "Protect", "Hardening Aura"],
        "weapon": "War Hammer",
    },
    "Ranger": {
        "health": 115,
        "power": 90,
        "defense": 35,
        "skills": ["Attack", "Grenade", "PickPocket"],
        "weapon": "Longbow",
    },
    "Alchemist": {
        "health": 105,
        "power": 65,
        "defense": 45,
        "skills": ["Attack", "Heal", "Debuff"],
        "weapon": "Alchemy Kit",
    },
}

ranks = ["Bronze", "Silver", "Platinum", "Diamond", "Elite", "Divine", "Master Rank"]
fake_player_names = ["Nova", "Mira", "Kade", "Orion", "Vex", "Sable", "Rook", "Astra"]

bosses = [
    {
        "name": "Iron Colossus",
        "health": 300,
        "power": 55,
        "defense": 15,
        "armor_piercing": 15,
    },
    {
        "name": "Elder Dragon",
        "health": 380,
        "power": 65,
        "defense": 20,
        "armor_piercing": 20,
    },
    {
        "name": "Void Champion",
        "health": 340,
        "power": 70,
        "defense": 18,
        "armor_piercing": 20,
    },
]


def register():
    return input("What is your username? ").strip()


def role_selection(username):
    while True:
        print("Available roles:")
        for role in role_data:
            print(f"- {role}")

        role_select = input(
            f"Hello, {username}. Select a role from the list above: "
        ).strip()
        if role_select not in role_data:
            print("Invalid role selected. Please try again.")
            continue

        confirm = input(f"Select {role_select}? Y / N: ").strip().upper()
        if confirm == "Y":
            print("Role selected!")
            return role_select


def damage_enemy(player, enemy, multiplier=1):
    power = player["power"] + player.get("combat_power_bonus", 0)
    damage = max(1, int(power * multiplier) - enemy["defense"])
    enemy["health"] = max(0, enemy["health"] - damage)
    print(f"You deal {damage} damage. {enemy['name']} has {enemy['health']} health left.")


def attack(player, enemy=None):
    if enemy is None:
        print(f"You attack with your {player['weapon']}.")
        return
    damage_enemy(player, enemy)


def guard(player, amount, skill_name):
    player["guard"] = player.get("guard", 0) + amount
    print(f"{skill_name} raises your defense for the next enemy attack.")


def protect(player, enemy=None):
    if enemy is None:
        player["defense"] += 10
        print(f"You protect yourself. Defense is now {player['defense']}.")
    else:
        guard(player, 10, "Protect")


def upgrade(player, enemy=None):
    if enemy is None:
        player["power"] += 10
        print(f"Your equipment is upgraded. Power is now {player['power']}.")
    else:
        player["combat_power_bonus"] += 10
        print("Your power increases for this fight.")


def heal(player, enemy=None):
    player["health"] = min(player["max_health"], player["health"] + 30)
    print(f"You heal. Health is now {player['health']}/{player['max_health']}.")


def buff(player, enemy=None):
    if enemy is None:
        player["power"] += 10
        print(f"You gain a power buff. Power is now {player['power']}.")
    else:
        player["combat_power_bonus"] += 10
        print("Your power increases for this fight.")


def debuff(player, enemy=None):
    if enemy is None:
        print("Debuff can only be used while fighting an enemy.")
    else:
        enemy["power"] = max(1, enemy["power"] - 10)
        print(f"You weaken {enemy['name']}. Its power is now {enemy['power']}.")


def pickpocket(player, enemy=None):
    if enemy is None:
        print("PickPocket can only be used while fighting an enemy.")
    else:
        stolen_gems = random.randint(20, 40)
        player["loot_bonus"] += stolen_gems
        print(f"You steal supplies worth {stolen_gems} bonus gems if you win.")


def cover(player, enemy=None):
    if enemy is None:
        player["defense"] += 15
        print(f"You take cover. Defense is now {player['defense']}.")
    else:
        guard(player, 15, "Cover")


def grenade(player, enemy=None):
    if enemy is None:
        print(f"You prepare a grenade with {int(player['power'] * 1.5)} damage.")
    else:
        damage_enemy(player, enemy, 1.5)


def divine_beam(player, enemy=None):
    if enemy is None:
        print(f"Divine Beam would deal {player['power'] * 2} damage.")
    else:
        damage_enemy(player, enemy, 2)


def healing_light(player, enemy=None):
    player["health"] = min(player["max_health"], player["health"] + 40)
    print(f"Healing Light restores health to {player['health']}/{player['max_health']}.")


def hardening_aura(player, enemy=None):
    if enemy is None:
        player["defense"] += 20
        print(f"Hardening Aura raises defense to {player['defense']}.")
    else:
        guard(player, 20, "Hardening Aura")


skill_functions = {
    "Attack": attack,
    "Protect": protect,
    "Upgrade": upgrade,
    "Heal": heal,
    "Buff": buff,
    "Debuff": debuff,
    "PickPocket": pickpocket,
    "Cover": cover,
    "Grenade": grenade,
    "Divine Beam": divine_beam,
    "Healing Light": healing_light,
    "Hardening Aura": hardening_aura,
}


def show_skills(player):
    print(f"\nRole: {player['role']}")
    level = player.get("level", 1)
    xp = player.get("xp", 0)
    print(
        f"Level: {level} | XP: {xp}/{100 * level} | "
        f"Rank: {ranks[min(player.get('rank_points', 0) // 3, len(ranks) - 1)]}"
    )
    print(
        f"Stats: Health {player['health']}/{player['max_health']} | "
        f"Power {player['power']} | Defense {player['defense']} | "
        f"Weapon {player['weapon']}"
    )
    print("Skills: " + ", ".join(player["skills"]))


def use_skill(player, skill_name):
    if skill_name not in player["skills"]:
        print(f"Your {player['role']} role cannot use {skill_name}.")
        return
    skill_functions[skill_name](player)


def show_help():
    print("\nCommands:")
    print("/help - Show this command list")
    print("/tutorial - Play through the tutorial")
    print("/skills - Show your role, stats, and available skills")
    print("/home - Return home and restore your health")
    print("/arena - Fight a random ranked opponent for XP and gems")
    print("/ranked - Check your rank and fight a fake ranked player")
    print("/boss - Fight a powerful boss for 1200-2000 gems on victory")
    print("/gem - Check your current gems")
    print("/shop - Show upgrades and their prices")
    print("/shop health|power|defense - Buy a stat upgrade")
    print("/shop prestige - Prestige for 10000 gems and a permanent stat bonus")
    print("Type a skill name to use it; /quit exits the game.")


def upgrade_cost(player, stat):
    return 250 + player["upgrades"][stat] * 200


def show_shop(player):
    upgrades = player["upgrades"]
    print("\nShop:")
    print(f"health: {upgrade_cost(player, 'health')} gems (+20 max health)")
    print(f"power: {upgrade_cost(player, 'power')} gems (+5 power)")
    print(f"defense: {upgrade_cost(player, 'defense')} gems (+5 defense)")
    print("prestige: 10000 gems (resets upgrades, adds permanent stat bonuses)")
    print("Buy with /shop health, /shop power, /shop defense, or /shop prestige.")


def shop(player, item=None):
    if item is None:
        show_shop(player)
        return

    if item in player["upgrades"]:
        cost = upgrade_cost(player, item)
        if player["gems"] < cost:
            print(f"You need {cost} gems to upgrade {item}.")
            return

        player["gems"] -= cost
        player["upgrades"][item] += 1
        if item == "health":
            player["max_health"] += 20
            player["health"] += 20
        else:
            player[item] += 5
        print(f"Upgraded {item}. You have {player['gems']} gems left.")
        show_skills(player)
        return

    if item == "prestige":
        cost = 10000
        if player["gems"] < cost:
            print(f"You need {cost} gems to prestige.")
            return

        player["gems"] -= cost
        player["prestige"] += 1
        player["upgrades"] = {"health": 0, "power": 0, "defense": 0}
        level_bonus = player.get("level", 1) - 1
        player["max_health"] = (
            player["base_health"] + 10 * player["prestige"] + 10 * level_bonus
        )
        player["health"] = player["max_health"]
        player["power"] = (
            player["base_power"] + 5 * player["prestige"] + 5 * level_bonus
        )
        player["defense"] = (
            player["base_defense"] + 5 * player["prestige"] + 3 * level_bonus
        )
        print(f"Prestige {player['prestige']} achieved! Your stats have been reset and boosted.")
        show_skills(player)
        return

    print("Unknown shop item. Type /shop to see what's available.")


def go_home(player):
    player["location"] = "home"
    player["health"] = player["max_health"]
    print(f"You are home. Health restored to {player['health']}/{player['max_health']}.")


def rank_for_points(rank_points):
    rank_index = min(rank_points // 3, len(ranks) - 1)
    return ranks[rank_index]


def xp_to_next_level(level):
    return level * 100


def award_experience(player, amount):
    player["xp"] += amount
    print(f"You earned {amount} XP.")
    while player["xp"] >= xp_to_next_level(player["level"]):
        player["xp"] -= xp_to_next_level(player["level"])
        player["level"] += 1
        player["max_health"] += 10
        player["health"] += 10
        player["power"] += 5
        player["defense"] += 3
        print(
            f"Level up! You are now level {player['level']}: "
            "+10 max health, +5 power, +3 defense."
        )


def make_ranked_opponent(player):
    player_rank_index = min(player["rank_points"] // 3, len(ranks) - 1)
    opponent_rank_index = max(
        0,
        min(
            len(ranks) - 1,
            player_rank_index + random.choice([-1, 0, 0, 1]),
        ),
    )
    opponent_level = max(1, player["level"] + random.randint(-1, 1))
    level_difference = opponent_level - player["level"]
    rank_difference = opponent_rank_index - player_rank_index
    opponent_role = random.choice(list(role_data))
    return {
        "name": f"{random.choice(fake_player_names)} the {opponent_role}",
        "rank": ranks[opponent_rank_index],
        "level": opponent_level,
        "health": max(
            1,
            player["max_health"]
            + level_difference * 10
            + rank_difference * 15
            + random.randint(-5, 5),
        ),
        "power": max(
            1,
            player["power"]
            + level_difference * 4
            + rank_difference * 6
            + random.randint(-4, 4),
        ),
        "defense": max(
            0,
            player["defense"]
            + level_difference * 2
            + rank_difference * 3
            + random.randint(-3, 3),
        ),
    }


def fight_opponent(
    player, opponents, reward_range, location, xp_reward, ranked=False
):
    enemy = random.choice(opponents).copy()
    enemy["max_health"] = enemy["health"]
    player["location"] = location
    player["guard"] = 0
    player["combat_power_bonus"] = 0
    player["loot_bonus"] = 0
    escaped = False
    opponent_details = ""
    if "rank" in enemy:
        opponent_details = f", Level {enemy['level']}, {enemy['rank']}"
    print(
        f"\n{location.title()} opponent: {enemy['name']}{opponent_details} "
        f"(Health {enemy['health']}, Power {enemy['power']}, Defense {enemy['defense']})"
    )

    while player["health"] > 0 and enemy["health"] > 0:
        action = input(
            f"Choose a skill ({', '.join(player['skills'])}) or /run: "
        ).strip()
        if action.lower() == "/run":
            print("You left the fight without a reward.")
            escaped = True
            break
        if action.lower() == "/skills":
            show_skills(player)
            continue
        if action not in player["skills"]:
            print("That skill is not available to your role. Type /skills to see your skills.")
            continue

        skill_functions[action](player, enemy)
        if enemy["health"] <= 0:
            break

        effective_defense = max(
            0, player["defense"] - enemy.get("armor_piercing", 0)
        )
        damage = max(1, enemy["power"] - effective_defense - player["guard"])
        player["health"] = max(0, player["health"] - damage)
        player["guard"] = 0
        print(
            f"{enemy['name']} hits you for {damage}. "
            f"Your health is {player['health']}/{player['max_health']}."
        )

    if enemy["health"] <= 0:
        reward = random.randint(*reward_range) + player["loot_bonus"]
        player["gems"] += reward
        print(f"You defeated {enemy['name']} and earned {reward} gems!")
        award_experience(player, xp_reward)
        if ranked:
            old_rank = rank_for_points(player["rank_points"])
            player["rank_points"] += 1
            new_rank = rank_for_points(player["rank_points"])
            if new_rank != old_rank:
                print(f"Rank promotion! You are now {new_rank}.")
            else:
                print(
                    f"Rank progress: {player['rank_points'] % 3}/3 wins toward the next rank."
                )
    elif player["health"] <= 0:
        player["health"] = 1
        print("You were defeated and returned home with 1 health. No gems awarded.")
        if ranked:
            old_rank = rank_for_points(player["rank_points"])
            player["rank_points"] = max(0, player["rank_points"] - 1)
            new_rank = rank_for_points(player["rank_points"])
            if new_rank != old_rank:
                print(f"Rank dropped to {new_rank}.")
            else:
                print("You lost 1 rank point.")

    player["location"] = "home"
    player["guard"] = 0
    player["combat_power_bonus"] = 0
    player["loot_bonus"] = 0


def arena(player):
    ranked_fight(player)


def ranked_fight(player):
    opponent = make_ranked_opponent(player)
    rank_index = min(player["rank_points"] // 3, len(ranks) - 1)
    reward_range = (80 + rank_index * 30, 160 + rank_index * 40)
    fight_opponent(
        player,
        [opponent],
        reward_range,
        "ranked arena",
        xp_reward=80,
        ranked=True,
    )


def show_ranked_and_fight(player):
    print(
        f"Your rank is {rank_for_points(player['rank_points'])} "
        f"({player['rank_points']} rank points)."
    )
    print("Ranks: " + " -> ".join(ranks))
    ranked_fight(player)


def boss_fight(player):
    fight_opponent(
        player, bosses, (1200, 2000), "boss arena", xp_reward=200
    )


def game_loop(player):
    print("Type /help to see commands, or /quit to exit.")
    while True:
        command = input("What do you want to do? ").strip()
        command_parts = command.split(maxsplit=1)
        command_name = command_parts[0].lower() if command_parts else ""
        argument = command_parts[1].lower() if len(command_parts) > 1 else None

        if command_name == "/quit":
            print("Goodbye!")
            return
        if command_name == "/help":
            show_help()
        elif command_name == "/tutorial":
            tutorial(player)
        elif command_name == "/skills":
            show_skills(player)
        elif command_name == "/home":
            go_home(player)
        elif command_name == "/arena":
            arena(player)
        elif command_name == "/ranked":
            show_ranked_and_fight(player)
        elif command_name == "/boss":
            boss_fight(player)
        elif command_name == "/gem":
            print(f"You have {player['gems']} gems.")
        elif command_name == "/shop":
            shop(player, argument)
        elif command_name.startswith("/"):
            print("Unknown command. Type /help to see the command list.")
        else:
            use_skill(player, command.strip())


def tutorial(player):
    print("\nWelcome to the tutorial!")
    print("Your role determines which skills you can use in a fight.")
    show_skills(player)
    print("In ranked fights, choose a skill each turn. Your opponent attacks after your turn.")
    print("Wins give gems and XP. Leveling up raises your health, power, and defense.")
    print("Win ranked fights to climb through the ranks; losses can lower your rank points.")
    print("Practice one of your skills on a harmless training dummy, or type /skip.")

    practice_player = player.copy()
    practice_player["guard"] = 0
    practice_player["combat_power_bonus"] = 0
    practice_player["loot_bonus"] = 0
    dummy = {"name": "Training Dummy", "health": 100, "power": 0, "defense": 0}

    while True:
        action = input(f"Choose one of your skills ({', '.join(player['skills'])}): ").strip()
        if action.lower() == "/skip":
            break
        if action not in player["skills"]:
            print("That skill is not available to your role. Try one from the list.")
            continue
        skill_functions[action](practice_player, dummy)
        break

    print("\nUseful commands:")
    print("/arena and /ranked fight fake ranked players; /boss fights a powerful enemy.")
    print("/gem checks your balance; /shop lists upgrades; /home restores your health.")
    print("Use /help at any time to see every command.")


def main():
    username = register()
    selected_role = role_selection(username)
    role = role_data[selected_role]
    player = {
        "role": selected_role,
        "health": role["health"],
        "max_health": role["health"],
        "power": role["power"],
        "defense": role["defense"],
        "skills": role["skills"],
        "weapon": role["weapon"],
        "base_health": role["health"],
        "base_power": role["power"],
        "base_defense": role["defense"],
        "gems": 0,
        "prestige": 0,
        "level": 1,
        "xp": 0,
        "rank_points": 0,
        "upgrades": {"health": 0, "power": 0, "defense": 0},
        "location": "home",
    }

    play_tutorial = input("Would you like to play the tutorial? Y / N: ").strip().upper()
    if play_tutorial == "Y":
        tutorial(player)
    game_loop(player)


if __name__ == "__main__":
    main()