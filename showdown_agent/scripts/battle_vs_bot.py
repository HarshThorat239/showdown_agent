import asyncio
import importlib.util
import os
import random
import sys

from poke_env.player import Player
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.teambuilder import Teambuilder


# === Load your CustomAgent from players/htho884.py ===
def load_htho884():
    module_path = os.path.join("players", "htho884.py")
    spec = importlib.util.spec_from_file_location("htho884", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["htho884"] = module
    spec.loader.exec_module(module)

    if hasattr(module, "CustomAgent"):
        player_class = getattr(module, "CustomAgent")
        return player_class(
            account_configuration=AccountConfiguration("htho884", None),
            server_configuration=LocalhostServerConfiguration,
            battle_format="gen9ubers"
        )
    else:
        raise ImportError("CustomAgent class not found in htho884.py")


# === Load a random bot from bots/ ===
def load_random_bot():
    bot_folder = "bots"
    team_folder = os.path.join(bot_folder, "teams")

    team_files = [f for f in os.listdir(team_folder) if f.endswith(".txt")]
    chosen_team_file = random.choice(team_files)
    with open(os.path.join(team_folder, chosen_team_file), "r", encoding="utf-8") as f:
        team = f.read()

    # Filter only bot scripts that contain a CustomAgent class
    valid_bots = []
    for bot_file in os.listdir(bot_folder):
        if not bot_file.endswith(".py"):
            continue
        spec = importlib.util.spec_from_file_location("bot_module", os.path.join(bot_folder, bot_file))
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            if hasattr(module, "CustomAgent"):
                valid_bots.append((bot_file, module))
        except Exception:
            continue

    if not valid_bots:
        raise RuntimeError("No valid bots with CustomAgent found.")

    chosen_file, chosen_module = random.choice(valid_bots)
    bot_class = getattr(chosen_module, "CustomAgent")

    return bot_class(
        team=team,
        account_configuration=AccountConfiguration("random-bot", None),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers"
    )



# === Main async logic ===
async def main():
    htho_agent = load_htho884()
    bot_agent = load_random_bot()

    # Challenge bot to a single battle
    await htho_agent.battle_against(bot_agent, n_battles=1)

    print(f"Battle complete. Result: {htho_agent.n_won_battles} win(s) out of 1")

    # # Print replay URL if saved
    # if htho_agent._replays:
    #     print(f"Replay saved to: {htho_agent._replays[-1]}")

if __name__ == "__main__":
    asyncio.run(main())
