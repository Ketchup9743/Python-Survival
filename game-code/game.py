import json
import os
import random
import sys
import time


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
fake_player_names = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6", "Player 7", "Player 8"]
SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savegame.json")

enemy_archetypes = [
    {
        "name": "Cave Brute",
        "health": 150,
        "power": 30,
        "defense": 5,
        "damage_resistance": 0,
        "status_resistance": 0,
        "special": "heavy",
    },
    {
        "name": "Venom Stalker",
        "health": 105,
        "power": 25,
        "defense": 8,
        "damage_resistance": 5,
        "status_resistance": 0,
        "special": "poison",
    },
    {
        "name": "Stone Sentinel",
        "health": 180,
        "power": 20,
        "defense": 15,
        "damage_resistance": 25,
        "status_resistance": 50,
        "special": "guard",
    },
    {
        "name": "Storm Wisp",
        "health": 90,
        "power": 32,
        "defense": 4,
        "damage_resistance": 0,
        "status_resistance": 0,
        "special": "stun",
    },
]

quest_data = {
    "win_3": {
        "name": "Arena Regular",
        "description": "Win 3 fights",
        "target": 3,
        "stat": "wins",
        "reward": 150,
    },
    "hunt_2": {
        "name": "Monster Tracker",
        "description": "Win 2 hunts",
        "target": 2,
        "stat": "hunts",
        "reward": 200,
    },
    "use_10_skills": {
        "name": "Practice Makes Perfect",
        "description": "Use 10 skills in combat",
        "target": 10,
        "stat": "skill_uses",
        "reward": 150,
    },
    "boss_1": {
        "name": "Big Game",
        "description": "Defeat a boss",
        "target": 1,
        "stat": "boss_wins",
        "reward": 300,
    },
}

bosses = [
    {
        "name": "Iron Colossus",
        "health": 300,
        "power": 55,
        "defense": 15,
        "armor_piercing": 15,
        "special": "heavy",
    },
    {
        "name": "Elder Dragon",
        "health": 380,
        "power": 65,
        "defense": 20,
        "armor_piercing": 20,
        "special": "poison",
    },
    {
        "name": "Void Champion",
        "health": 340,
        "power": 70,
        "defense": 18,
        "armor_piercing": 20,
        "special": "stun",
    },
]

pets = {
    "ember fox": {
        "cost": 600,
        "description": "+10% damage",
        "damage_bonus": 10,
    },
    "iron tortoise": {
        "cost": 600,
        "description": "+8 defense",
        "defense_bonus": 8,
    },
    "healing hare": {
        "cost": 650,
        "description": "+25 max health",
        "health_bonus": 25,
    },
    "scholar owl": {
        "cost": 750,
        "description": "+15% XP",
        "xp_bonus": 15,
    },
    "lucky raccoon": {
        "cost": 750,
        "description": "+15% gems",
        "gem_bonus": 15,
    },
}

achievement_data = {
    "first_win": {"name": "First Victory", "description": "Win your first fight", "reward": 100},
    "ten_wins": {"name": "Veteran Fighter", "description": "Win 10 fights", "reward": 400},
    "boss_slayer": {"name": "Boss Slayer", "description": "Defeat a boss", "reward": 500},
    "level_five": {"name": "Rising Hero", "description": "Reach level 5", "reward": 300},
}


def terminal_animation_enabled():
    return sys.stdout.isatty() and os.environ.get("TERM") != "dumb"


def render_pixel_title():
    print()
    print("  +--------------------------------------+")
    print("  |  ____        _   _                   |")
    print("  | |  _ \\ _   _| |_| |__   ___  _ __   |")
    print("  | | |_) | | | | __| '_ \\ / _ \\| '_ \\  |")
    print("  | |  __/| |_| | |_| | | | (_) | | | | |")
    print("  | |_|    \\__, |\\__|_| |_|\\___/|_| |_| |")
    print("  |        |___/       SURVIVAL v1.0     |")
    print("  +--------------------------------------+")
    print("  ........................................")
    if terminal_animation_enabled():
        for frame in ("[    ]", "[.   ]", "[..  ]", "[... ]"):
            print(f"       BOOT {frame}", end="\r", flush=True)
            time.sleep(0.06)
        print(" " * 24, end="\r", flush=True)
        for frame in ("....................", "::::::::::::::::::::"):
            print(f"       SIGNAL {frame}", end="\r", flush=True)
            time.sleep(0.04)
        print(" " * 32, end="\r", flush=True)
    print()


def save_game(player):
    save_data = {
        key: value
        for key, value in player.items()
        if key not in {
            "guard", "combat_power_bonus", "loot_bonus", "location", "statuses",
        }
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as save_file:
            json.dump(save_data, save_file, indent=2)
    except OSError as error:
        print(f"Save failed: {error}")
        return
    print(f"Game saved to {SAVE_FILE}.")


def load_game(player):
    try:
        with open(SAVE_FILE, encoding="utf-8") as save_file:
            saved_player = json.load(save_file)
    except FileNotFoundError:
        print("No save file found. Use /save to create one.")
        return
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load save: {error}")
        return

    if (
        not isinstance(saved_player, dict)
        or not isinstance(saved_player.get("role"), str)
        or saved_player["role"] not in role_data
    ):
        print("Save file is invalid: missing a valid character role.")
        return
    if not isinstance(saved_player.get("skills"), list) or not all(
        isinstance(skill, str) and skill in skill_functions
        for skill in saved_player["skills"]
    ):
        print("Save file is invalid: character skills are not recognized.")
        return
    if not isinstance(saved_player.get("weapon"), str):
        print("Save file is invalid: character weapon is missing.")
        return
    integer_fields = (
        "health", "max_health", "power", "defense", "base_health", "base_power",
        "base_defense", "gems", "prestige",
        "level", "xp", "skill_points", "rank_points",
    )
    if any(
        not isinstance(saved_player.get(field), int)
        or isinstance(saved_player.get(field), bool)
        or saved_player[field] < 0
        for field in integer_fields
    ):
        print("Save file is invalid: character stats must be non-negative integers.")
        return
    if any(saved_player[field] < 1 for field in ("level", "max_health", "base_health")):
        print("Save file is invalid: level and health values must be positive.")
        return
    if not isinstance(saved_player.get("pets"), list) or any(
        not isinstance(pet, str) or pet not in pets
        for pet in saved_player["pets"]
    ):
        print("Save file is invalid: pet data is not recognized.")
        return
    active_pet = saved_player.get("active_pet")
    if active_pet is not None and (
        not isinstance(active_pet, str) or active_pet not in saved_player["pets"]
    ):
        print("Save file is invalid: active pet is not owned.")
        return
    if not isinstance(saved_player.get("upgrades"), dict) or any(
        not isinstance(saved_player["upgrades"].get(stat), int)
        or isinstance(saved_player["upgrades"].get(stat), bool)
        or saved_player["upgrades"][stat] < 0
        for stat in ("health", "power", "defense")
    ):
        print("Save file is invalid: upgrade data is incomplete.")
        return
    stats = saved_player.get("combat_stats", {})
    if not isinstance(stats, dict) or any(
        not isinstance(stats.get(key, 0), int)
        or isinstance(stats.get(key, 0), bool)
        or stats.get(key, 0) < 0
        for key in ("wins", "hunts", "boss_wins", "skill_uses")
    ):
        print("Save file is invalid: combat progress is malformed.")
        return
    for field, valid_ids in (
        ("claimed_quests", quest_data),
        ("achievements", achievement_data),
    ):
        if not isinstance(saved_player.get(field, []), list) or any(
            not isinstance(item, str) or item not in valid_ids
            for item in saved_player.get(field, [])
        ):
            print(f"Save file is invalid: {field.replace('_', ' ')} data is malformed.")
            return

    player.clear()
    player.update(saved_player)
    player.setdefault("username", "")
    player.setdefault("skill_points", 0)
    player.setdefault(
        "combat_stats",
        {"wins": 0, "hunts": 0, "boss_wins": 0, "skill_uses": 0},
    )
    player.setdefault("claimed_quests", [])
    player.setdefault("achievements", [])
    player["combat_stats"] = {
        "wins": 0,
        "hunts": 0,
        "boss_wins": 0,
        "skill_uses": 0,
        **player["combat_stats"],
    }
    player["name"] = player["username"] or player["role"]
    player["health"] = min(player["health"], effective_max_health(player))
    player["location"] = "home"
    print(f"Loaded character: {player.get('username') or player['role']}.")


def health_bar(current, maximum, width=20):
    maximum = max(1, maximum)
    filled = max(0, min(width, int(width * current / maximum)))
    return "#" * filled + "-" * (width - filled)


def render_pixel_status(player, enemy):
    print(
        f"  YOU   {health_bar(player['health'], effective_max_health(player))} "
        f"{player['health']}/{effective_max_health(player)}"
    )
    print(
        f"  FOE   {health_bar(enemy['health'], enemy.get('max_health', enemy['health']))} "
        f"{enemy['health']}/{enemy.get('max_health', enemy['health'])}"
    )


def render_pixel_battle(player, enemy):
    enemy_art = {
        "Cave Brute": "[O]",
        "Venom Stalker": "<v>",
        "Stone Sentinel": "[#]",
        "Storm Wisp": "(*)",
        "Iron Colossus": "[###]",
        "Elder Dragon": "<==>",
        "Void Champion": "{X}",
    }
    enemy_name = enemy["name"]
    if enemy_name.startswith("Level "):
        enemy_name = enemy_name.split(" ", 2)[-1]
    foe = enemy_art.get(enemy_name, "[XXX]")
    print("  +--------------------------------------+")
    print("  |             BATTLE SCREEN            |")
    print(f"  |       [O]                 {foe:>7}      |")
    print("  |       /|\\                  /|\\       |")
    print("  |       / \\                  / \\       |")
    print("  +--------------------------------------+")
    render_pixel_status(player, enemy)


def animate_impact():
    if not terminal_animation_enabled():
        return
    for frame in ("  *", " ** ", "*****"):
        print(f"       HIT {frame}", end="\r", flush=True)
        time.sleep(0.04)
    print(" " * 20, end="\r", flush=True)


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
    pet = pets.get(player.get("active_pet"), {})
    resistance = max(0, min(90, enemy.get("damage_resistance", 0)))
    damage = max(
        1,
        (
            int(power * multiplier) * (100 + pet.get("damage_bonus", 0)) // 100
            - enemy["defense"]
        )
        * (100 - resistance)
        // 100
        - enemy.get("guard", 0),
    )
    enemy["guard"] = 0
    enemy["health"] = max(0, enemy["health"] - damage)
    print(f"You deal {damage} damage. {enemy['name']} has {enemy['health']} health left.")


def apply_status(target, name, turns, damage=0):
    status_resistance = max(0, min(90, target.get("status_resistance", 0)))
    if status_resistance and damage:
        damage = max(1, damage * (100 - status_resistance) // 100)
    if status_resistance and turns > 1:
        turns = max(1, turns * (100 - status_resistance) // 100)
    statuses = target.setdefault("statuses", {})
    current = statuses.get(name, {"turns": 0, "damage": 0})
    statuses[name] = {
        "turns": max(current["turns"], turns),
        "damage": max(current["damage"], damage),
    }
    print(f"{target['name']} is affected by {name} for {statuses[name]['turns']} turns.")


def tick_statuses(target):
    statuses = target.setdefault("statuses", {})
    stunned = "stun" in statuses
    for name, effect in list(statuses.items()):
        if effect["damage"]:
            target["health"] = max(0, target["health"] - effect["damage"])
            print(
                f"{target['name']} takes {effect['damage']} {name} damage "
                f"({target['health']} health left)."
            )
        effect["turns"] -= 1
        if effect["turns"] <= 0:
            del statuses[name]
    return stunned


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
        print("Protect can only be used while fighting an enemy.")
    else:
        guard(player, 10, "Protect")


def upgrade(player, enemy=None):
    if enemy is None:
        print("Upgrade can only be used while fighting an enemy.")
    else:
        boost_combat_power(player)


def heal(player, enemy=None):
    max_health = effective_max_health(player)
    player["health"] = min(max_health, player["health"] + 30)
    print(f"You heal. Health is now {player['health']}/{max_health}.")


def buff(player, enemy=None):
    if enemy is None:
        print("Buff can only be used while fighting an enemy.")
    else:
        boost_combat_power(player)


def boost_combat_power(player, amount=10):
    bonus_limit = max(10, player["power"] // 2)
    current_bonus = player.get("combat_power_bonus", 0)
    player["combat_power_bonus"] = min(current_bonus + amount, bonus_limit)
    if player["combat_power_bonus"] == current_bonus:
        print("Your power boost is already at its limit for this fight.")
    else:
        print("Your power increases for this fight.")


def debuff(player, enemy=None):
    if enemy is None:
        print("Debuff can only be used while fighting an enemy.")
    else:
        enemy["power"] = max(1, enemy["power"] - 10)
        print(f"You weaken {enemy['name']}. Its power is now {enemy['power']}.")
        apply_status(enemy, "poison", 3, 5)


def pickpocket(player, enemy=None):
    steal_gems(player, enemy, 40)


def steal_gems(player, enemy, max_loot_bonus):
    if enemy is None:
        print("PickPocket can only be used while fighting an enemy.")
    else:
        available_bonus = max_loot_bonus - player.get("loot_bonus", 0)
        if available_bonus <= 0:
            print("You have already stolen the maximum bonus gems for this fight.")
            return
        stolen_gems = min(random.randint(20, 40), available_bonus)
        player["loot_bonus"] = player.get("loot_bonus", 0) + stolen_gems
        print(f"You steal supplies worth {stolen_gems} bonus gems if you win.")


def cover(player, enemy=None):
    if enemy is None:
        print("Cover can only be used while fighting an enemy.")
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
    max_health = effective_max_health(player)
    player["health"] = min(max_health, player["health"] + 40)
    print(f"Healing Light restores health to {player['health']}/{max_health}.")


def hardening_aura(player, enemy=None):
    if enemy is None:
        print("Hardening Aura can only be used while fighting an enemy.")
    else:
        guard(player, 20, "Hardening Aura")


def power_strike(player, enemy=None):
    if enemy is None:
        print(f"Power Strike would deal {int(player['power'] * 1.5)} damage.")
    else:
        damage_enemy(player, enemy, 1.5)
        enemy["power"] = max(1, enemy["power"] - 5)
        print(f"Power Strike staggers {enemy['name']}, reducing its power by 5.")


def aegis_guard(player, enemy=None):
    if enemy is None:
        print("Aegis Guard can only be used while fighting an enemy.")
    else:
        guard(player, 20, "Aegis Guard")
        enemy["power"] = max(1, enemy["power"] - 5)
        print(f"Aegis Guard weakens {enemy['name']} by 5 power.")


def masterwork(player, enemy=None):
    if enemy is None:
        print("Masterwork can only be used while fighting an enemy.")
    else:
        boost_combat_power(player, 20)
        guard(player, 5, "Masterwork")


def greater_heal(player, enemy=None):
    max_health = effective_max_health(player)
    player["health"] = min(max_health, player["health"] + 50)
    print(f"Greater Heal restores health to {player['health']}/{max_health}.")
    if enemy is not None:
        guard(player, 10, "Greater Heal")


def battle_focus(player, enemy=None):
    if enemy is None:
        print("Battle Focus can only be used while fighting an enemy.")
    else:
        boost_combat_power(player, 20)
        guard(player, 10, "Battle Focus")


def crippling_blow(player, enemy=None):
    if enemy is None:
        print("Crippling Blow can only be used while fighting an enemy.")
    else:
        enemy["power"] = max(1, enemy["power"] - 20)
        print(f"You cripple {enemy['name']}. Its power is now {enemy['power']}.")


def plunder(player, enemy=None):
    steal_gems(player, enemy, 60)


def reinforced_cover(player, enemy=None):
    if enemy is None:
        print("Reinforced Cover can only be used while fighting an enemy.")
    else:
        guard(player, 25, "Reinforced Cover")
        enemy["power"] = max(1, enemy["power"] - 5)
        print(f"Reinforced Cover weakens {enemy['name']} by 5 power.")


def cluster_bomb(player, enemy=None):
    if enemy is None:
        print(f"Cluster Bomb would deal {int(player['power'] * 2)} damage.")
    else:
        damage_enemy(player, enemy, 2)
        enemy["power"] = max(1, enemy["power"] - 5)
        print(f"The blast weakens {enemy['name']} by 5 power.")
        apply_status(enemy, "burn", 2, 8)


def celestial_nova(player, enemy=None):
    if enemy is None:
        print(f"Celestial Nova would deal {int(player['power'] * 2.5)} damage.")
    else:
        damage_enemy(player, enemy, 2.5)
        enemy["power"] = max(1, enemy["power"] - 10)
        print(f"Celestial Nova weakens {enemy['name']} by 10 power.")


def divine_renewal(player, enemy=None):
    max_health = effective_max_health(player)
    player["health"] = min(max_health, player["health"] + 65)
    print(f"Divine Renewal restores health to {player['health']}/{max_health}.")
    if enemy is not None:
        guard(player, 10, "Divine Renewal")


def iron_aegis(player, enemy=None):
    if enemy is None:
        print("Iron Aegis can only be used while fighting an enemy.")
    else:
        guard(player, 30, "Iron Aegis")
        enemy["power"] = max(1, enemy["power"] - 10)
        print(f"Iron Aegis weakens {enemy['name']} by 10 power.")


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

skill_upgrades = {
    "Attack": ("Power Strike", "Deal 50% more damage and stagger the enemy."),
    "Protect": ("Aegis Guard", "Gain 20 guard and weaken the enemy by 5 power."),
    "Upgrade": ("Masterwork", "Gain a larger power boost and 5 guard."),
    "Heal": ("Greater Heal", "Restore 50 health and gain 10 guard."),
    "Buff": ("Battle Focus", "Gain a larger power boost and 10 guard."),
    "Debuff": ("Crippling Blow", "Reduce enemy power by 20 instead of 10."),
    "PickPocket": ("Plunder", "Steal up to 60 bonus gems instead of 40."),
    "Cover": ("Reinforced Cover", "Gain 25 guard and weaken the enemy by 5 power."),
    "Grenade": ("Cluster Bomb", "Deal double damage and weaken the enemy."),
    "Divine Beam": ("Celestial Nova", "Deal 2.5x damage and weaken the enemy."),
    "Healing Light": ("Divine Renewal", "Restore 65 health and gain 10 guard."),
    "Hardening Aura": ("Iron Aegis", "Gain 30 guard and weaken the enemy by 10 power."),
}

skill_functions.update(
    {
        "Power Strike": power_strike,
        "Aegis Guard": aegis_guard,
        "Masterwork": masterwork,
        "Greater Heal": greater_heal,
        "Battle Focus": battle_focus,
        "Crippling Blow": crippling_blow,
        "Plunder": plunder,
        "Reinforced Cover": reinforced_cover,
        "Cluster Bomb": cluster_bomb,
        "Celestial Nova": celestial_nova,
        "Divine Renewal": divine_renewal,
        "Iron Aegis": iron_aegis,
    }
)


def show_skills(player):
    print(f"\nRole: {player['role']}")
    level = player.get("level", 1)
    xp = player.get("xp", 0)
    max_health = effective_max_health(player)
    print(
        f"Level: {level} | XP: {xp}/{100 * level} | "
        f"Rank: {ranks[min(player.get('rank_points', 0) // 3, len(ranks) - 1)]} | "
        f"Skill points: {player.get('skill_points', 0)}"
    )
    print(
        f"Stats: Health {player['health']}/{max_health} | "
        f"Power {player['power']} | Defense {player['defense']} | "
        f"Weapon {player['weapon']}"
    )
    print("Skills: " + ", ".join(player["skills"]))
    active_pet = player.get("active_pet")
    if active_pet:
        print(f"Active pet: {active_pet.title()} ({pets[active_pet]['description']})")


def train(player, instruction=None):
    skill_points = player.get("skill_points", 0)
    if skill_points < 1:
        print("You need a skill point to train. Gain one each time you level up.")
        return

    if instruction is None:
        print(f"You have {skill_points} skill point(s).")
        print("Upgrade options:")
        for skill in player["skills"]:
            if skill in skill_upgrades:
                upgraded_skill, description = skill_upgrades[skill]
                print(f"- upgrade {skill} -> {upgraded_skill}: {description}")
        available_skills = [
            skill for skill in skill_upgrades if skill not in player["skills"]
        ]
        print("Skills available to learn: " + ", ".join(available_skills))
        print("Use: upgrade <skill> | replace <old skill> with <new skill> | cancel")
        instruction = input("Choose your training: ").strip()

    instruction = instruction.strip()
    if instruction.casefold() in {"", "cancel"}:
        print("Training cancelled.")
        return

    if instruction.casefold().startswith("upgrade "):
        skill_name = instruction[len("upgrade "):].strip()
        current_skill = next(
            (
                skill for skill in player["skills"]
                if skill.casefold() == skill_name.casefold()
            ),
            None,
        )
        if current_skill is None:
            print("You can only upgrade a skill you currently know.")
            return
        if current_skill not in skill_upgrades:
            print(f"{current_skill} has no further upgrade.")
            return
        upgraded_skill, _ = skill_upgrades[current_skill]
        skill_index = player["skills"].index(current_skill)
        player["skills"][skill_index] = upgraded_skill
        player["skill_points"] = skill_points - 1
        print(f"{current_skill} upgraded to {upgraded_skill}.")
        return

    action, separator, replacement = instruction.partition(" ")
    with_index = replacement.casefold().find(" with ")
    if action.casefold() != "replace" or not separator or with_index < 0:
        print("Use: upgrade <skill> or replace <old skill> with <new skill>.")
        return

    old_name = replacement[:with_index]
    new_name = replacement[with_index + len(" with "):]
    old_skill = next(
        (
            skill for skill in player["skills"]
            if skill.casefold() == old_name.strip().casefold()
        ),
        None,
    )
    new_skill = next(
        (
            skill for skill in skill_upgrades
            if skill.casefold() == new_name.strip().casefold()
        ),
        None,
    )
    if old_skill is None:
        print("You can only replace a skill you currently know.")
        return
    if new_skill is None:
        print("That skill is not available to learn. Check /train for the skill list.")
        return
    if new_skill in player["skills"]:
        print(f"You already know {new_skill}.")
        return

    skill_index = player["skills"].index(old_skill)
    player["skills"][skill_index] = new_skill
    player["skill_points"] = skill_points - 1
    print(f"{old_skill} replaced with {new_skill}.")


def use_skill(player, skill_name):
    if skill_name not in player["skills"]:
        print(f"Your {player['role']} role cannot use {skill_name}.")
        return
    skill_functions[skill_name](player)


def ensure_progression_data(player):
    player["combat_stats"] = {
        "wins": 0,
        "hunts": 0,
        "boss_wins": 0,
        "skill_uses": 0,
        **player.get("combat_stats", {}),
    }
    player.setdefault("claimed_quests", [])
    player.setdefault("achievements", [])


def update_progression_rewards(player):
    ensure_progression_data(player)
    stats = player["combat_stats"]
    for quest_id, quest in quest_data.items():
        if quest_id in player["claimed_quests"] or stats.get(quest["stat"], 0) < quest["target"]:
            continue
        player["claimed_quests"].append(quest_id)
        player["gems"] += quest["reward"]
        print(f"Quest complete: {quest['name']}! +{quest['reward']} gems.")

    achievements = {
        "first_win": stats["wins"] >= 1,
        "ten_wins": stats["wins"] >= 10,
        "boss_slayer": stats["boss_wins"] >= 1,
        "level_five": player["level"] >= 5,
    }
    for achievement_id, unlocked in achievements.items():
        if not unlocked or achievement_id in player["achievements"]:
            continue
        achievement = achievement_data[achievement_id]
        player["achievements"].append(achievement_id)
        player["gems"] += achievement["reward"]
        print(
            f"Achievement unlocked: {achievement['name']}! "
            f"+{achievement['reward']} gems."
        )


def show_quests(player):
    ensure_progression_data(player)
    stats = player["combat_stats"]
    print("\nQuests:")
    for quest_id, quest in quest_data.items():
        progress = min(stats.get(quest["stat"], 0), quest["target"])
        status = "CLAIMED" if quest_id in player["claimed_quests"] else "IN PROGRESS"
        print(
            f"- {quest['name']}: {quest['description']} "
            f"[{progress}/{quest['target']}] {status} (+{quest['reward']} gems)"
        )
    print("\nAchievements:")
    for achievement_id, achievement in achievement_data.items():
        status = "UNLOCKED" if achievement_id in player["achievements"] else "LOCKED"
        print(
            f"- {achievement['name']}: {achievement['description']} "
            f"[{status}] (+{achievement['reward']} gems)"
        )


def show_help():
    print("\nCommands:")
    print("/help - Show this command list")
    print("/tutorial - Play through the tutorial")
    print("/skills - Show your role, stats, and available skills")
    print("/train - Spend skill points to replace or upgrade a skill")
    print("/home - Return home and restore your health")
    print("/arena - Fight a random ranked opponent for XP and gems")
    print("/ranked - Check your rank and fight a fake ranked player")
    print("/boss - Fight a powerful boss for 500-800 gems on victory")
    print("/hunt - Fight a monster with a special ability for rewards")
    print("/quests - Check quest and achievement progress")
    print("/save - Save your character; /load - Load your saved character")
    print("/gem - Check your current gems")
    print("/shop - Show upgrades and their prices")
    print("/shop health|power|defense - Buy a stat upgrade")
    print("/shop pet <name> - Buy a pet; /pet <name> equips an owned pet")
    print("/pets - List pets, effects, and ownership")
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
    print("Pets:")
    for name, pet in pets.items():
        status = " (owned)" if name in player["pets"] else ""
        print(f"{name}: {pet['cost']} gems ({pet['description']}){status}")
    print(
        "Buy with /shop health, /shop power, /shop defense, /shop prestige, "
        "or /shop pet <name>."
    )


def effective_max_health(player):
    pet = pets.get(player.get("active_pet"), {})
    return player["max_health"] + pet.get("health_bonus", 0)


def show_pets(player):
    active_pet = player.get("active_pet")
    print("\nPets:")
    for name, pet in pets.items():
        if name in player["pets"]:
            status = " (equipped)" if name == active_pet else " (owned)"
        else:
            status = f" ({pet['cost']} gems)"
        print(f"- {name.title()}: {pet['description']}{status}")
    print("Buy pets with /shop pet <name>; equip an owned pet with /pet <name>.")
    print("Use /pet off to unequip your pet.")


def equip_pet(player, pet_name):
    if pet_name == "off":
        player["active_pet"] = None
        player["health"] = min(player["health"], effective_max_health(player))
        print("Your pet is unequipped.")
        return
    if pet_name not in pets:
        print("Unknown pet. Type /pets to see the available pets.")
        return
    if pet_name not in player["pets"]:
        print(f"You don't own the {pet_name.title()}. Buy it with /shop pet {pet_name}.")
        return

    player["active_pet"] = pet_name
    player["health"] = min(player["health"], effective_max_health(player))
    print(f"{pet_name.title()} is now your active pet: {pets[pet_name]['description']}.")


def shop(player, item=None):
    if item is None:
        show_shop(player)
        return

    if item.startswith("pet "):
        pet_name = item[4:].strip()
        if pet_name not in pets:
            print("Unknown pet. Type /pets to see the available pets.")
            return
        if pet_name in player["pets"]:
            print(f"You already own the {pet_name.title()}.")
            return
        cost = pets[pet_name]["cost"]
        if player["gems"] < cost:
            print(f"You need {cost} gems to buy the {pet_name.title()}.")
            return
        player["gems"] -= cost
        player["pets"].append(pet_name)
        print(f"You adopted the {pet_name.title()}! Equip it with /pet {pet_name}.")
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
    player["health"] = effective_max_health(player)
    print(f"You are home. Health restored to {player['health']}/{effective_max_health(player)}.")


def rank_for_points(rank_points):
    rank_index = min(rank_points // 3, len(ranks) - 1)
    return ranks[rank_index]


def xp_to_next_level(level):
    return level * 100


def award_experience(player, amount):
    pet = pets.get(player.get("active_pet"), {})
    amount = amount * (100 + pet.get("xp_bonus", 0)) // 100
    player["xp"] += amount
    print(f"You earned {amount} XP.")
    while player["xp"] >= xp_to_next_level(player["level"]):
        player["xp"] -= xp_to_next_level(player["level"])
        player["level"] += 1
        player["skill_points"] = player.get("skill_points", 0) + 1
        player["max_health"] += 10
        player["health"] += 10
        player["power"] += 5
        player["defense"] += 3
        print(
            f"Level up! You are now level {player['level']}: "
            "+10 max health, +5 power, +3 defense, +1 skill point."
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
        "damage_resistance": 0,
        "status_resistance": 0,
        "special": random.choice(["heavy", "poison", "guard", "stun"]),
    }


def make_hunt_enemy(player):
    enemy = random.choice(enemy_archetypes).copy()
    level_bonus = max(0, player["level"] - 1)
    enemy["health"] += level_bonus * 12
    enemy["power"] += level_bonus * 2
    enemy["name"] = f"Level {player['level']} {enemy['name']}"
    return enemy


def enemy_attack(player, enemy, turn):
    special = enemy.get("special")
    if special == "heavy" and turn % 3 == 0:
        print(f"{enemy['name']} winds up a heavy blow!")
    elif special == "poison" and turn % 3 == 0:
        apply_status(player, "poison", 3, 5)
    elif special == "stun" and turn % 4 == 0:
        apply_status(player, "stun", 1)
    elif special == "guard" and turn % 3 == 0:
        enemy["guard"] = 20
        print(f"{enemy['name']} braces behind its stone armor.")

    pet = pets.get(player.get("active_pet"), {})
    effective_defense = max(
        0,
        player["defense"]
        + pet.get("defense_bonus", 0)
        - enemy.get("armor_piercing", 0),
    )
    power = enemy["power"] * 3 // 2 if special == "heavy" and turn % 3 == 0 else enemy["power"]
    damage = max(1, power - effective_defense - player.get("guard", 0))
    player["health"] = max(0, player["health"] - damage)
    player["guard"] = 0
    print(
        f"{enemy['name']} hits you for {damage}. "
        f"Your health is {player['health']}/{effective_max_health(player)}."
    )


def update_boss_phase(enemy):
    if not enemy.get("is_boss") or enemy["health"] <= 0:
        return
    health_ratio = enemy["health"] / max(1, enemy["max_health"])
    phase = 3 if health_ratio <= 0.25 else 2 if health_ratio <= 0.5 else 1
    if phase <= enemy.get("phase", 1):
        return
    enemy["phase"] = phase
    enemy["power"] += 12 if phase == 2 else 15
    enemy["defense"] += 5 if phase == 2 else 3
    if phase == 3:
        enemy["special"] = "heavy"
    print(
        f"\n{enemy['name']} enters phase {phase}! "
        f"It grows stronger (Power {enemy['power']}, Defense {enemy['defense']})."
    )


def fight_opponent(
    player, opponents, reward_range, location, xp_reward, ranked=False
):
    enemy = random.choice(opponents).copy()
    enemy["max_health"] = enemy["health"]
    enemy["statuses"] = {}
    enemy["guard"] = 0
    enemy.setdefault("damage_resistance", 0)
    enemy.setdefault("status_resistance", 0)
    enemy.setdefault("special", None)
    enemy["is_boss"] = location == "boss arena"
    enemy["phase"] = 1
    player["location"] = location
    player["guard"] = 0
    player["combat_power_bonus"] = 0
    player["loot_bonus"] = 0
    player["statuses"] = {}
    player.setdefault("name", player.get("username") or player["role"])
    ensure_progression_data(player)
    turn = 0
    opponent_details = ""
    if "rank" in enemy:
        opponent_details = f", Level {enemy['level']}, {enemy['rank']}"
    print(
        f"\n{location.title()} opponent: {enemy['name']}{opponent_details} "
        f"(Health {enemy['health']}, Power {enemy['power']}, Defense {enemy['defense']})"
    )
    render_pixel_battle(player, enemy)

    while player["health"] > 0 and enemy["health"] > 0:
        player_stunned = "stun" in player.get("statuses", {})
        action = None
        if not player_stunned:
            action = input(
                f"Choose a skill ({', '.join(player['skills'])}) or /run: "
            ).strip()
            if action.lower() == "/run":
                print("You left the fight without a reward.")
                break
            if action.lower() == "/skills":
                show_skills(player)
                continue
            if action not in player["skills"]:
                print("That skill is not available to your role. Type /skills to see your skills.")
                continue

        player_stunned = tick_statuses(player)
        tick_statuses(enemy)
        update_boss_phase(enemy)
        if player["health"] <= 0 or enemy["health"] <= 0:
            break

        if player_stunned:
            print("You are stunned and lose your turn!")
        else:
            assert action is not None
            enemy_health_before = enemy["health"]
            skill_functions[action](player, enemy)
            player["combat_stats"]["skill_uses"] += 1
            update_progression_rewards(player)
            update_boss_phase(enemy)
            if enemy["health"] < enemy_health_before:
                animate_impact()
            if enemy["health"] <= 0:
                render_pixel_status(player, enemy)
                break

        turn += 1
        enemy_attack(player, enemy, turn)
        render_pixel_status(player, enemy)

    if enemy["health"] <= 0:
        pet = pets.get(player.get("active_pet"), {})
        reward = (
            (random.randint(*reward_range) + player["loot_bonus"])
            * (100 + pet.get("gem_bonus", 0))
            // 100
        )
        player["gems"] += reward
        print(f"You defeated {enemy['name']} and earned {reward} gems!")
        award_experience(player, xp_reward)
        player["combat_stats"]["wins"] += 1
        if location == "monster hunt":
            player["combat_stats"]["hunts"] += 1
        if enemy["is_boss"]:
            player["combat_stats"]["boss_wins"] += 1
        update_progression_rewards(player)
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
    player["statuses"] = {}


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
        player, bosses, (500, 800), "boss arena", xp_reward=200
    )


def hunt(player):
    enemy = make_hunt_enemy(player)
    fight_opponent(
        player, [enemy], (90, 180), "monster hunt", xp_reward=60
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
        elif command_name == "/train":
            train(player, argument)
        elif command_name == "/home":
            go_home(player)
        elif command_name == "/arena":
            arena(player)
        elif command_name == "/ranked":
            show_ranked_and_fight(player)
        elif command_name == "/boss":
            boss_fight(player)
        elif command_name == "/hunt":
            hunt(player)
        elif command_name == "/quests":
            show_quests(player)
        elif command_name == "/save":
            save_game(player)
        elif command_name == "/load":
            load_game(player)
        elif command_name == "/gem":
            print(f"You have {player['gems']} gems.")
        elif command_name == "/pets":
            show_pets(player)
        elif command_name == "/pet":
            equip_pet(player, argument or "")
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
    print("Each level also gives 1 skill point. Use /train to upgrade or replace a skill.")
    print("Pets give one passive bonus at a time; buy them in the shop and equip with /pet.")
    print("Use /hunt for monsters, /quests for goals, and /save or /load to keep progress.")
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
        "username": username,
        "name": username or selected_role,
        "role": selected_role,
        "health": role["health"],
        "max_health": role["health"],
        "power": role["power"],
        "defense": role["defense"],
        "skills": role["skills"].copy(),
        "weapon": role["weapon"],
        "base_health": role["health"],
        "base_power": role["power"],
        "base_defense": role["defense"],
        "gems": 0,
        "prestige": 0,
        "level": 1,
        "xp": 0,
        "skill_points": 0,
        "rank_points": 0,
        "upgrades": {"health": 0, "power": 0, "defense": 0},
        "pets": [],
        "active_pet": None,
        "combat_stats": {"wins": 0, "hunts": 0, "boss_wins": 0, "skill_uses": 0},
        "claimed_quests": [],
        "achievements": [],
        "location": "home",
    }

    render_pixel_title()
    play_tutorial = input("Would you like to play the tutorial? Y / N: ").strip().upper()
    if play_tutorial == "Y":
        tutorial(player)
    game_loop(player)


if __name__ == "__main__":
    main()