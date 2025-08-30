import asyncio
import importlib.util
import os
import sys

from poke_env.player import Player
from poke_env import AccountConfiguration, LocalhostServerConfiguration


# === Load htho884 agent from players/htho884.py ===
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


# === Load second agent from players/second.py ===
def load_second():
    module_path = os.path.join("players", "second.py")
    spec = importlib.util.spec_from_file_location("second", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["second"] = module
    spec.loader.exec_module(module)

    if hasattr(module, "CustomAgent"):
        player_class = getattr(module, "CustomAgent")
        return player_class(
            account_configuration=AccountConfiguration("second", None),
            server_configuration=LocalhostServerConfiguration,
            battle_format="gen9ubers"
        )
    else:
        raise ImportError("CustomAgent class not found in second.py")


# === Main async logic ===
async def main():
    print("Loading htho884 agent...")
    htho_agent = load_htho884()
    
    print("Loading second agent...")
    second_agent = load_second()

    print("Starting battle: htho884 vs second")
    print("=" * 50)
    
    # Start the battle
    await htho_agent.battle_against(second_agent, n_battles=1)

    print("=" * 50)
    print(f"Battle complete!")
    print(f"htho884 wins: {htho_agent.n_won_battles}")
    print(f"second wins: {second_agent.n_won_battles}")
    print(f"Total battles: {htho_agent.n_battles}")

    # Print replay URL if saved
    if hasattr(htho_agent, '_replays') and htho_agent._replays:
        print(f"Replay saved to: {htho_agent._replays[-1]}")


if __name__ == "__main__":
    asyncio.run(main())





