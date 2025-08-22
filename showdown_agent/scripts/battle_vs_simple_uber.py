import asyncio
import importlib.util
import os
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


# === Load the simple bot specifically ===
def load_simple_bot():
    bot_folder = "bots"
    team_folder = os.path.join(bot_folder, "teams")

    # Use the uber team for the simple bot
    team_file = os.path.join(team_folder, "uber.txt")
    with open(team_file, "r", encoding="utf-8") as f:
        team = f.read()

    # Load the simple bot specifically
    simple_bot_path = os.path.join(bot_folder, "simple.py")
    spec = importlib.util.spec_from_file_location("simple_bot", simple_bot_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "CustomAgent"):
        raise RuntimeError("CustomAgent class not found in simple.py")

    bot_class = getattr(module, "CustomAgent")

    return bot_class(
        team=team,
        account_configuration=AccountConfiguration("simple-uber", None),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers"
    )


# === Main async logic ===
async def main():
    print("Loading htho884 agent...")
    htho_agent = load_htho884()
    
    print("Loading simple-uber bot...")
    simple_bot = load_simple_bot()

    print("Starting battle: htho884 vs simple-uber...")
    # Challenge simple bot to a single battle
    await htho_agent.battle_against(simple_bot, n_battles=1)

    print(f"Battle complete!")
    print(f"htho884 wins: {htho_agent.n_won_battles}")
    print(f"simple-uber wins: {simple_bot.n_won_battles}")

    # Print replay URL if saved
    if hasattr(htho_agent, '_replays') and htho_agent._replays:
        print(f"Replay saved to: {htho_agent._replays[-1]}")

if __name__ == "__main__":
    asyncio.run(main())
