import contextlib
import http.cookies
import http.server
import io
import json
import os
import random
import secrets
import sys
import urllib.parse

import game


HTML_PAGE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Python Survival - Browser Edition</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #25223a;
      --paper: #fff5dc;
      --panel: #f9e9c5;
      --pink: #ee8b9b;
      --blue: #86c8d6;
      --green: #91bd78;
      --dark-green: #567b59;
      --gold: #f1c96a;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--ink);
      color: var(--ink);
      font: 15px "Courier New", monospace;
      image-rendering: pixelated;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 14px max(16px, calc((100vw - 1200px) / 2));
      color: var(--paper);
    }
    header h1 { margin: 0; color: var(--gold); font-size: clamp(20px, 4vw, 30px); }
    #player-status { text-align: right; font-size: 13px; }
    main { width: min(1200px, calc(100% - 24px)); margin: 0 auto 24px; }
    .layout { display: grid; grid-template-columns: minmax(0, 1fr) 270px; gap: 12px; }
    .frame { border: 5px solid var(--paper); box-shadow: 0 5px 0 #11101c; }
    #scene {
      display: block;
      width: 100%;
      aspect-ratio: 16 / 9;
      min-height: 300px;
      background: #a9d8e6;
      image-rendering: pixelated;
    }
    #menu { padding: 12px; background: var(--panel); border: 4px solid var(--gold); }
    #menu h2 { margin: 0 0 10px; font-size: 16px; }
    #actions { display: grid; gap: 7px; }
    button {
      min-height: 38px;
      padding: 8px;
      border: 3px solid var(--ink);
      border-radius: 0;
      background: #fffdf5;
      color: var(--ink);
      font: bold 12px "Courier New", monospace;
      text-align: left;
      cursor: pointer;
      box-shadow: 0 3px 0 #aaa18e;
    }
    button:hover, button:focus-visible { background: var(--pink); outline: 2px solid white; }
    #log {
      height: 150px;
      overflow-y: auto;
      margin-top: 12px;
      padding: 10px;
      border: 4px solid var(--paper);
      background: #fffdf5;
      white-space: pre-wrap;
      line-height: 1.5;
    }
    #command-form {
      display: flex;
      gap: 8px;
      margin-top: 12px;
      padding: 10px;
      border: 4px solid var(--gold);
      background: var(--panel);
    }
    #command {
      flex: 1;
      min-width: 0;
      padding: 10px;
      border: 3px solid var(--ink);
      border-radius: 0;
      font: 15px "Courier New", monospace;
    }
    #command-form button { min-width: 100px; background: var(--gold); text-align: center; }
    #hint { color: #5e596b; font-size: 12px; margin: 8px 2px; }
    @media (max-width: 760px) {
      header { align-items: flex-start; flex-direction: column; }
      #player-status { text-align: left; }
      .layout { grid-template-columns: 1fr; }
      #menu { order: -1; }
      #actions { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      #scene { min-height: 250px; }
      #log { height: 125px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>PYTHON SURVIVAL</h1>
    <div id="player-status">A pixel adventure</div>
  </header>
  <main>
    <div class="layout">
      <section>
        <canvas id="scene" class="frame" width="960" height="540" aria-label="Pixel game scene"></canvas>
      </section>
      <aside id="menu" class="frame">
        <h2 id="menu-title">ACTION MENU</h2>
        <div id="actions"></div>
      </aside>
    </div>
    <div id="log" role="log" aria-live="polite">Welcome, adventurer. Start a journey or load your saved character.</div>
    <form id="command-form">
      <input id="command" autocomplete="off" placeholder="Type a command (try /help)" aria-label="Game command">
      <button type="submit">SEND</button>
    </form>
    <p id="hint">Examples: /new Alex | Ranger, /hunt, /shop, /save, /load. During battle, enter a skill name.</p>
  </main>
  <script>
    const canvas = document.querySelector("#scene");
    const ctx = canvas.getContext("2d");
    const actions = document.querySelector("#actions");
    const logElement = document.querySelector("#log");
    const commandInput = document.querySelector("#command");
    let state = null;
    let requestBusy = false;

    function pixelRect(x, y, width, height, color) {
      ctx.fillStyle = color;
      ctx.fillRect(x, y, width, height);
    }

    function drawScene() {
      if (!state) return;
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);
      pixelRect(0, 0, width, height, "#a9d8e6");
      pixelRect(0, 355, width, 185, "#94c27d");
      pixelRect(0, 412, width, 128, "#6d9c67");
      pixelRect(770, 42, 75, 75, "#f3ce75");
      for (const [x, y] of [[55, 274], [190, 325], [702, 270], [850, 330]]) {
        pixelRect(x + 24, y + 34, 38, 112, "#578663");
        pixelRect(x, y + 8, 88, 62, "#739f71");
        pixelRect(x + 22, y - 18, 46, 72, "#8bb27c");
      }

      if (state.mode !== "battle" || !state.enemy) {
        drawHouse();
        drawHero(200, 425);
        text("SUNMEADOW VILLAGE", 480, 62, 25, "#25223a");
        text("A quiet place to prepare for adventure", 480, 94, 15, "#25223a");
        return;
      }

      drawHero(210, 425);
      drawEnemy(684, 425, state.enemy.name);
      text(state.enemy.name.toUpperCase(), 480, 55, 24, "#25223a");
      if (state.enemy.is_boss) text("PHASE " + state.enemy.phase, 480, 84, 15, "#25223a");
      drawBars();
    }

    function text(value, x, y, size, color) {
      ctx.fillStyle = color;
      ctx.font = "bold " + size + "px Courier New";
      ctx.textAlign = "center";
      ctx.fillText(value, x, y);
    }

    function drawHouse() {
      pixelRect(390, 285, 170, 134, "#f4d18c");
      ctx.fillStyle = "#d77d79";
      ctx.strokeStyle = "#25223a";
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(372, 290); ctx.lineTo(475, 215); ctx.lineTo(578, 290);
      ctx.closePath(); ctx.fill(); ctx.stroke();
      pixelRect(448, 345, 48, 74, "#8b6254");
      pixelRect(516, 310, 27, 30, "#86c8d6");
    }

    function drawHero(x, ground) {
      pixelRect(x, ground - 58, 38, 38, "#f1c96a");
      pixelRect(x + 4, ground - 86, 30, 30, "#f0bd96");
      pixelRect(x + 2, ground - 94, 34, 9, "#57465d");
      pixelRect(x + 7, ground - 20, 11, 24, "#4d5267");
      pixelRect(x + 24, ground - 20, 11, 24, "#4d5267");
      pixelRect(x + 25, ground - 76, 4, 4, "#25223a");
    }

    function drawEnemy(x, ground, name) {
      const colors = {
        "Cave Brute": "#a57868", "Venom Stalker": "#8f9b68",
        "Stone Sentinel": "#898d9d", "Storm Wisp": "#9b8cb9",
        "Iron Colossus": "#888a8c", "Elder Dragon": "#bd7869",
        "Void Champion": "#665e80"
      };
      const plainName = name.replace(/^Level \d+ /, "");
      const color = colors[plainName] || "#bc847d";
      pixelRect(x, ground - 83, 106, 83, color);
      pixelRect(x + 6, ground - 104, 94, 36, color);
      pixelRect(x + 20, ground - 92, 9, 9, "#fffdf5");
      pixelRect(x + 76, ground - 92, 9, 9, "#fffdf5");
      pixelRect(x + 32, ground - 66, 51, 6, "#25223a");
      pixelRect(x + 12, ground, 23, 12, "#25223a");
      pixelRect(x + 72, ground, 23, 12, "#25223a");
    }

    function drawBars() {
      const playerMax = state.player.max_health + ((state.player.active_pet === "healing hare") ? 25 : 0);
      const enemyMax = state.enemy.max_health || state.enemy.health;
      drawBar(32, 465, "YOU", state.player.health, playerMax);
      drawBar(530, 465, "FOE", state.enemy.health, enemyMax);
    }

    function drawBar(x, y, label, current, maximum) {
      pixelRect(x, y, 398, 54, "#fff5dc");
      ctx.strokeStyle = "#25223a"; ctx.lineWidth = 4; ctx.strokeRect(x, y, 398, 54);
      ctx.textAlign = "left"; ctx.fillStyle = "#25223a";
      ctx.font = "bold 15px Courier New"; ctx.fillText(label, x + 12, y + 21);
      pixelRect(x + 74, y + 10, 300, 14, "#d6cdb9");
      pixelRect(x + 74, y + 10, 300 * Math.max(0, current) / Math.max(1, maximum), 14, "#77a86d");
      ctx.font = "13px Courier New"; ctx.fillText(current + " / " + maximum, x + 74, y + 43);
    }

    function appendLog(message) {
      if (!message) return;
      logElement.textContent += "\n" + message.trim();
      logElement.scrollTop = logElement.scrollHeight;
    }

    function drawActions(items) {
      actions.replaceChildren();
      for (const item of items) {
        const button = document.createElement("button");
        button.textContent = item.label;
        button.addEventListener("click", () => sendCommand(item.command));
        actions.append(button);
      }
    }

    async function refresh() {
      const response = await fetch("/api/state");
      state = await response.json();
      logElement.textContent = state.log.join("\n");
      logElement.scrollTop = logElement.scrollHeight;
      document.querySelector("#player-status").textContent = state.player
        ? `${state.player.name} | LV ${state.player.level} | GEMS ${state.player.gems} | HP ${state.player.health}/${state.max_health}`
        : "A pixel adventure";
      document.querySelector("#menu-title").textContent = state.mode === "battle" ? "CHOOSE A MOVE" : "ACTION MENU";
      drawActions(state.actions);
      drawScene();
    }

    async function sendCommand(command) {
      if (requestBusy || !command) return;
      requestBusy = true;
      try {
        const response = await fetch("/api/command", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({command})
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || "Request failed");
        await refresh();
      } catch (error) {
        appendLog("Error: " + error.message);
      } finally {
        requestBusy = false;
        commandInput.focus();
      }
    }

    document.querySelector("#command-form").addEventListener("submit", event => {
      event.preventDefault();
      const command = commandInput.value.trim();
      commandInput.value = "";
      sendCommand(command);
    });

    refresh().catch(error => appendLog("Could not connect to game server: " + error.message));
  </script>
</body>
</html>"""


def new_player(username, selected_role):
    role = game.role_data[selected_role]
    return {
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


class BrowserGame:
    def __init__(self):
        self.player = None
        self.enemy = None
        self.fight = None
        self.turn = 0
        self.screen = "home"
        self.log = ["Welcome, adventurer. Start a journey or load your saved character."]

    def _capture(self, callback, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            callback(*args)
        message = output.getvalue().strip()
        if message:
            self.log.append(message)

    def _append(self, message):
        if message:
            self.log.append(message)

    def state(self):
        player = self.player
        if player is None:
            return {
                "mode": "start",
                "player": None,
                "enemy": None,
                "max_health": 0,
                "log": self.log[-30:],
                "actions": [
                    {"label": "NEW ADVENTURE", "command": "/new Hero | Engineer"},
                    {"label": "LOAD SAVED GAME", "command": "/load"},
                ],
            }

        if self.enemy is not None:
            action_list = [
                {"label": skill.upper(), "command": skill}
                for skill in player["skills"]
            ]
            action_list.append({"label": "RUN AWAY", "command": "/run"})
            enemy = {
                key: self.enemy.get(key)
                for key in ("name", "health", "max_health", "is_boss", "phase", "statuses")
            }
            mode = "battle"
        elif self.screen == "shop":
            action_list = [
                {
                    "label": f"BUY {stat.upper()} ({game.upgrade_cost(player, stat)}g)",
                    "command": f"/shop {stat}",
                }
                for stat in ("health", "power", "defense")
            ]
            action_list.extend(
                {
                    "label": f"{pet_name.title()} ({pet['cost']}g)",
                    "command": f"/shop pet {pet_name}",
                }
                for pet_name, pet in game.pets.items()
                if pet_name not in player["pets"]
            )
            action_list.extend(
                [
                    {"label": "PRESTIGE (10000g)", "command": "/shop prestige"},
                    {"label": "BACK TO VILLAGE", "command": "/home"},
                ]
            )
            enemy = None
            mode = "shop"
        elif self.screen == "training":
            action_list = []
            available_skills = [
                skill for skill in game.skill_upgrades if skill not in player["skills"]
            ]
            for skill in player["skills"]:
                if skill in game.skill_upgrades:
                    upgraded, _ = game.skill_upgrades[skill]
                    action_list.append(
                        {
                            "label": f"UPGRADE {skill} -> {upgraded}",
                            "command": f"/train upgrade {skill}",
                        }
                    )
                action_list.extend(
                    {
                        "label": f"{skill} -> {new_skill}",
                        "command": f"/train replace {skill} with {new_skill}",
                    }
                    for new_skill in available_skills
                )
            action_list.append({"label": "BACK TO VILLAGE", "command": "/home"})
            enemy = None
            mode = "training"
        elif self.screen == "pets":
            action_list = [
                {
                    "label": f"EQUIP {pet.title()}",
                    "command": f"/pet {pet}",
                }
                for pet in player["pets"]
            ]
            action_list.extend(
                [
                    {"label": "UNEQUIP PET", "command": "/pet off"},
                    {"label": "BACK TO VILLAGE", "command": "/home"},
                ]
            )
            enemy = None
            mode = "pets"
        elif self.screen in {"quests", "skills"}:
            action_list = [{"label": "BACK TO VILLAGE", "command": "/home"}]
            enemy = None
            mode = self.screen
        else:
            enemy = None
            action_list = [
                {"label": label, "command": command}
                for label, command in (
                    ("RANKED ARENA", "/arena"),
                    ("MONSTER HUNT", "/hunt"),
                    ("BOSS BATTLE", "/boss"),
                    ("SHOP", "/shop"),
                    ("TRAIN SKILLS", "/train"),
                    ("PETS", "/pets"),
                    ("QUESTS & ACHIEVEMENTS", "/quests"),
                    ("REST / HEAL", "/home"),
                    ("SAVE GAME", "/save"),
                )
            ]
            mode = "home"
        return {
            "mode": mode,
            "player": {
                key: player.get(key)
                for key in (
                    "name", "role", "health", "max_health", "power", "defense",
                    "gems", "level", "xp", "skill_points", "rank_points", "skills",
                    "pets", "active_pet", "statuses",
                )
            },
            "enemy": enemy,
            "max_health": game.effective_max_health(player),
            "log": self.log[-30:],
            "actions": action_list,
        }

    def _start_fight(self, enemy, location, reward_range, xp_reward, ranked=False):
        self.enemy = enemy.copy()
        self.enemy["max_health"] = enemy["health"]
        self.enemy["statuses"] = {}
        self.enemy["guard"] = 0
        self.enemy.setdefault("damage_resistance", 0)
        self.enemy.setdefault("status_resistance", 0)
        self.enemy.setdefault("special", None)
        self.enemy["is_boss"] = location == "boss arena"
        self.enemy["phase"] = 1
        self.screen = "battle"
        self.fight = {
            "location": location,
            "reward": reward_range,
            "xp": xp_reward,
            "ranked": ranked,
        }
        self.player["location"] = location
        self.player["guard"] = 0
        self.player["combat_power_bonus"] = 0
        self.player["loot_bonus"] = 0
        self.player["statuses"] = {}
        game.ensure_progression_data(self.player)
        self.turn = 0
        self._append(
            f"{self.enemy['name']} appears! "
            f"Health {self.enemy['health']}, power {self.enemy['power']}."
        )

    def _start_ranked(self):
        rank_index = min(self.player["rank_points"] // 3, len(game.ranks) - 1)
        reward = (80 + rank_index * 30, 160 + rank_index * 40)
        self._start_fight(
            game.make_ranked_opponent(self.player),
            "ranked arena",
            reward,
            80,
            ranked=True,
        )

    def _start_hunt(self):
        self._start_fight(game.make_hunt_enemy(self.player), "monster hunt", (90, 180), 60)

    def _start_boss(self):
        self._start_fight(random.choice(game.bosses), "boss arena", (500, 800), 200)

    def _finish_fight(self, victory):
        player = self.player
        enemy = self.enemy
        fight = self.fight
        if victory:
            pet = game.pets.get(player.get("active_pet"), {})
            base_reward = random.randint(*fight["reward"]) + player.get("loot_bonus", 0)
            reward = base_reward * (100 + pet.get("gem_bonus", 0)) // 100
            player["gems"] += reward
            self._append(f"Victory! You earned {reward} gems.")
            self._capture(game.award_experience, player, fight["xp"])
            stats = player["combat_stats"]
            stats["wins"] += 1
            if fight["location"] == "monster hunt":
                stats["hunts"] += 1
            if enemy["is_boss"]:
                stats["boss_wins"] += 1
            self._capture(game.update_progression_rewards, player)
            if fight["ranked"]:
                old_rank = game.rank_for_points(player["rank_points"])
                player["rank_points"] += 1
                new_rank = game.rank_for_points(player["rank_points"])
                self._append(f"Rank: {new_rank} ({player['rank_points']} points).")
                if new_rank != old_rank:
                    self._append(f"Promotion! You reached {new_rank}.")
        else:
            player["health"] = 1
            self._append("Defeat! You return with 1 health and no battle rewards.")
            if fight["ranked"]:
                player["rank_points"] = max(0, player["rank_points"] - 1)

        player["location"] = "home"
        player["guard"] = 0
        player["combat_power_bonus"] = 0
        player["loot_bonus"] = 0
        player["statuses"] = {}
        self.enemy = None
        self.fight = None
        self.screen = "home"

    def _player_action(self, action):
        player = self.player
        enemy = self.enemy
        if action == "/run":
            player["location"] = "home"
            player["statuses"] = {}
            player["guard"] = 0
            player["combat_power_bonus"] = 0
            player["loot_bonus"] = 0
            self.enemy = None
            self.fight = None
            self.screen = "home"
            self._append("You retreated safely. No battle rewards were earned.")
            return
        if action not in player["skills"]:
            self._append("Choose one of your listed skills or use /run.")
            return

        stunned = "stun" in player.get("statuses", {})
        self._capture(game.tick_statuses, player)
        self._capture(game.tick_statuses, enemy)
        self._capture(game.update_boss_phase, enemy)
        if player["health"] <= 0:
            self._finish_fight(False)
            return
        if enemy["health"] <= 0:
            self._finish_fight(True)
            return

        if stunned:
            self._append("You are stunned and lose your turn!")
        else:
            self._capture(game.skill_functions[action], player, enemy)
            player["combat_stats"]["skill_uses"] += 1
            self._capture(game.update_progression_rewards, player)
            self._capture(game.update_boss_phase, enemy)
            if enemy["health"] <= 0:
                self._finish_fight(True)
                return

        self.turn += 1
        self._capture(game.enemy_attack, player, enemy, self.turn)
        if player["health"] <= 0:
            self._finish_fight(False)

    def command(self, command):
        command = command.strip()
        if not command:
            return
        self._append(f"> {command}")
        if self.enemy is not None:
            if command.startswith("/"):
                self._player_action(command.lower())
            else:
                self._player_action(command)
            return

        if command.startswith("/new"):
            details = command[len("/new"):].strip()
            username, separator, selected_role = details.partition("|")
            selected_role = selected_role.strip()
            if not separator or selected_role not in game.role_data:
                self._append("Use /new <name> | <role>. Roles: " + ", ".join(game.role_data))
                return
            self.player = new_player(username.strip(), selected_role)
            self.screen = "home"
            self._append(f"Welcome, {self.player['name']} the {selected_role}!")
            return

        command_parts = command.split(maxsplit=1)
        command_name = command_parts[0].lower()
        argument = command_parts[1] if len(command_parts) > 1 else None
        if command_name == "/help":
            self._append(
                "Commands: /new Name | Role, /load, /save, /arena, /hunt, /boss, "
                "/home, /skills, /train, /shop, /pets, /pet NAME, /quests, /gem."
            )
        elif command_name == "/load":
            loaded = self.player.copy() if self.player else {}
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                game.load_game(loaded)
            message = output.getvalue().strip()
            if "Loaded character:" in message:
                self.player = loaded
                self.screen = "home"
            self._append(message)
        elif self.player is None:
            self._append("Start with /new <name> | <role>, or use /load.")
        elif command_name == "/save":
            self._capture(game.save_game, self.player)
        elif command_name == "/arena":
            self._start_ranked()
        elif command_name == "/ranked":
            self._append(
                f"Rank: {game.rank_for_points(self.player['rank_points'])} "
                f"({self.player['rank_points']} points)."
            )
            self._start_ranked()
        elif command_name == "/hunt":
            self._start_hunt()
        elif command_name == "/boss":
            self._start_boss()
        elif command_name == "/home":
            self.player["location"] = "home"
            self.player["health"] = game.effective_max_health(self.player)
            self.enemy = None
            self.fight = None
            self.screen = "home"
            self._append("You rest at home and recover all health.")
        elif command_name == "/skills":
            self._capture(game.show_skills, self.player)
            self.screen = "skills"
        elif command_name == "/train":
            if not argument:
                self._append(
                    "Training: /train upgrade Attack or "
                    "/train replace Attack with Heal. Skill points: "
                    f"{self.player.get('skill_points', 0)}."
                )
                self.screen = "training"
            else:
                self._capture(game.train, self.player, argument)
                self.screen = "training"
        elif command_name == "/shop":
            if argument:
                self._capture(game.shop, self.player, argument.lower())
            else:
                self._append("Shop: /shop health, /shop power, /shop defense, /shop prestige, /shop pet ember fox.")
            self.screen = "shop"
        elif command_name == "/pets":
            self._capture(game.show_pets, self.player)
            self.screen = "pets"
        elif command_name == "/pet":
            self._capture(game.equip_pet, self.player, (argument or "").lower())
        elif command_name == "/quests":
            self._capture(game.show_quests, self.player)
            self.screen = "quests"
        elif command_name == "/back":
            self.screen = "home"
        elif command_name == "/gem":
            self._append(f"You have {self.player['gems']} gems.")
        else:
            self._append("Unknown command. Type /help to see commands.")


sessions = {}


class GameRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "PythonSurvival/1.0"

    def _session(self):
        cookies = http.cookies.SimpleCookie(self.headers.get("Cookie", ""))
        morsel = cookies.get("session")
        session_id = morsel.value if morsel else ""
        if session_id not in sessions:
            session_id = secrets.token_urlsafe(24)
            sessions[session_id] = BrowserGame()
            return session_id, sessions[session_id], True
        return session_id, sessions[session_id], False

    def _send_json(self, payload, status=200, session_id=None, is_new=False):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if is_new and session_id:
            self.send_header(
                "Set-Cookie",
                f"session={session_id}; HttpOnly; SameSite=Strict; Path=/",
            )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        session_id, session, is_new = self._session()
        parsed_path = urllib.parse.urlsplit(self.path).path
        if parsed_path == "/":
            body = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            if is_new:
                self.send_header(
                    "Set-Cookie",
                    f"session={session_id}; HttpOnly; SameSite=Strict; Path=/",
                )
            self.end_headers()
            self.wfile.write(body)
        elif parsed_path == "/api/state":
            self._send_json(session.state(), session_id=session_id, is_new=is_new)
        else:
            self._send_json(
                {"error": "Not found"},
                404,
                session_id=session_id,
                is_new=is_new,
            )

    def do_POST(self):
        session_id, session, is_new = self._session()
        if urllib.parse.urlsplit(self.path).path != "/api/command":
            self._send_json(
                {"error": "Not found"},
                404,
                session_id=session_id,
                is_new=is_new,
            )
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json({"error": "Invalid content length"}, 400, session_id, is_new)
            return
        if content_length < 0 or content_length > 4096:
            self._send_json({"error": "Request is too large"}, 413, session_id, is_new)
            return
        try:
            payload = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(
                {"error": "Request must contain valid JSON"},
                400,
                session_id,
                is_new,
            )
            return
        command = payload.get("command") if isinstance(payload, dict) else None
        if not isinstance(command, str) or len(command) > 160:
            self._send_json(
                {"error": "Command must be text under 160 characters"},
                400,
                session_id,
                is_new,
            )
            return
        try:
            session.command(command)
        except (KeyError, TypeError, ValueError) as error:
            self._send_json(
                {"error": f"Command failed: {error}"},
                400,
                session_id,
                is_new,
            )
            return
        self._send_json(
            session.state(),
            session_id=session_id,
            is_new=is_new,
        )

    def log_message(self, format_string, *args):
        sys.stderr.write(
            f"{self.address_string()} - {format_string % args}\n"
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run Python Survival in a browser.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = http.server.ThreadingHTTPServer((args.host, args.port), GameRequestHandler)
    print(f"Python Survival browser game listening on http://{args.host}:{args.port}")
    print("Forward this port in Codespaces and open its browser preview.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping browser game.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
