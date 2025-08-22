#!/usr/bin/env python3
# challenge_simple_uber.py
#
# Make your htho884 bot challenge the simple-uber bot on a local Showdown server.
# Requirements:
#   - Local server running: `node pokemon-showdown start --no-security`
#   - Your CustomAgent in players/htho884.py with class "CustomAgent"
#   - Simple bot in bots/simple.py with class "CustomAgent"
#   - poke-env installed
#
# Usage:
#   python challenge_simple_uber.py

import asyncio
import importlib.util
import os
import sys

from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.player.player import Player


def load_class_from_file(module_path: str, class_name: str):
    """Dynamically load a class from a Python file."""
    module_path = os.path.abspath(module_path)
    spec = importlib.util.spec_from_file_location("user_agent_module", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["user_agent_module"] = module
    spec.loader.exec_module(module)
    if not hasattr(module, class_name):
        raise AttributeError(f"{class_name} not found in {module_path}")
    return getattr(module, class_name)


async def run_bot_vs_bot_battle():
    print("Loading htho884 agent...")
    # Load your CustomAgent class
    HthoAgentClass = load_class_from_file("players/htho884.py", "CustomAgent")
    
    print("Loading simple-uber bot...")
    # Load the simple bot class
    SimpleBotClass = load_class_from_file("bots/simple.py", "CustomAgent")
    
    # Read the uber team for the simple bot
    team_file = "bots/teams/uber.txt"
    with open(team_file, "r", encoding="utf-8") as f:
        simple_bot_team = f.read()
    
    print("Initializing agents...")
    # Instantiate your agent (htho884)
    htho_agent: Player = HthoAgentClass(
        account_configuration=AccountConfiguration("htho884", None),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers"
    )
    
    # Instantiate the simple bot
    simple_bot: Player = SimpleBotClass(
        team=simple_bot_team,
        account_configuration=AccountConfiguration("simple-uber", None),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers"
    )
    
    print(f"htho884 agent '{htho_agent.username}' is online.")
    print(f"simple-uber bot '{simple_bot.username}' is online.")
    print("Starting battle: htho884 vs simple-uber...")
    
    # Make htho884 challenge simple-uber
    await htho_agent.send_challenges("simple-uber", n_challenges=1, to_wait=True)
    
    # Wait until all battles conclude, then clean up
    await htho_agent._detailed_teardown()
    await simple_bot._detailed_teardown()
    
    print("Battle finished!")
    print(f"htho884 wins: {htho_agent.n_won_battles}")
    print(f"simple-uber wins: {simple_bot.n_won_battles}")
    
    # Print replay URL if saved
    if hasattr(htho_agent, '_replays') and htho_agent._replays:
        print(f"Replay saved to: {htho_agent._replays[-1]}")


def main():
    print("=== htho884 vs simple-uber Battle ===")
    print("Make sure you have a local Showdown server running:")
    print("  node pokemon-showdown start --no-security")
    print()
    
    asyncio.run(run_bot_vs_bot_battle())


if __name__ == "__main__":
    main()
