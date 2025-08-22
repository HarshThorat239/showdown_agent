#!/usr/bin/env python3
# fight_simple_uber.py
#
# Play as a human (in the browser) against a simple Gen 9 Ubers bot on the real
# Pokémon Showdown server.
#
# Requirements:
#   - poke-env installed
#   - A bot class in bots/<file>.py (defaults provided below)
#
# Usage examples:
#   Accept mode (you challenge the bot from the browser):
#       python fight_simple_uber.py --human-username myhuman \
#           --format gen9ubers --mode accept
#
#   Challenge mode (the bot challenges your human account):
#       python fight_simple_uber.py --human-username myhuman \
#           --format gen9ubers --mode challenge
#
# Notes:
#   - Your *human* team is set in the browser (Build Team → import/paste).
#   - To point at a specific bot implementation, use --bot-module and --bot-class.
#     By default this script looks for: bots/simple.py:CustomAgent
#   - If you want the bot to use a specific team file, pass: --bot-team path/to/team.txt
#   - By default, the bot uses a guest account to avoid authentication issues
#   - If you want to use a specific username, provide --bot-token with an auth token

import argparse
import asyncio
import importlib.util
import os
import sys
import random
import string

from poke_env import AccountConfiguration, ShowdownServerConfiguration
from poke_env.player.player import Player


def generate_random_username(prefix="Bot"):
    """Generate a random username to avoid conflicts."""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}_{random_suffix}"


def load_class_from_file(module_path: str, class_name: str):
    """Dynamically load a class from a Python file."""
    module_path = os.path.abspath(module_path)
    spec = importlib.util.spec_from_file_location("bot_module", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["bot_module"] = module
    spec.loader.exec_module(module)
    if not hasattr(module, class_name):
        raise AttributeError(f"{class_name} not found in {module_path}")
    return getattr(module, class_name)


async def run_battle(
    bot_module: str,
    bot_class: str,
    bot_username: str | None,
    bot_token: str | None,
    human_username: str,
    battle_format: str,
    mode: str,
    bot_team: str | None,
):
    # Load the bot class
    BotClass = load_class_from_file(bot_module, bot_class)

    # Optional: read bot team from a text file
    team_str = None
    if bot_team:
        with open(bot_team, "r", encoding="utf-8") as f:
            team_str = f.read()

    # Instantiate the bot
    init_kwargs = {
        "account_configuration": AccountConfiguration(bot_username, bot_token),
        "server_configuration": ShowdownServerConfiguration,
        "battle_format": battle_format,
    }
    if team_str is not None:
        init_kwargs["team"] = team_str

    bot: Player = BotClass(**init_kwargs)

    print(f"Bot '{bot.username}' is online on Pokémon Showdown server (format: {battle_format}).")
    if team_str:
        print(f"Bot is using team from: {bot_team}")
    else:
        print("Bot has no explicit team set (will use its internal default, if any).")

    # Either wait for your challenge, or send one to you
    if mode == "accept":
        print(
            f"Waiting for a challenge from '{human_username}'... "
            f"(Go to https://play.pokemonshowdown.com, log in as '{human_username}', "
            f"select your team, and challenge '{bot.username}' in {battle_format})"
        )
        await bot.accept_challenges(human_username, n_challenges=1)
    else:
        print(
            f"Sending a challenge to '{human_username}'... "
            f"(Accept it in your browser with your chosen team)"
        )
        await bot.send_challenges(human_username, n_challenges=1, to_wait=True)

    # Wait until all battles conclude, then clean up
    await bot._detailed_teardown()
    print("Battle finished. Bot logged out.")


def main():
    parser = argparse.ArgumentParser(
        description="Fight a simple Gen 9 Ubers bot via the real Pokémon Showdown server."
    )
    parser.add_argument(
        "--bot-module",
        default="bots/simple.py",
        help="Path to the bot file (default: bots/simple.py)",
    )
    parser.add_argument(
        "--bot-class",
        default="CustomAgent",
        help='Bot class name in the module (default: "CustomAgent")',
    )
    parser.add_argument(
        "--bot-username",
        help="Showdown username for the bot account. If not provided, uses a guest account.",
    )
    parser.add_argument(
        "--bot-token",
        help="Authentication token for the bot account (required if using --bot-username)",
    )
    parser.add_argument(
        "--human-username",
        required=True,
        help="Your human username (used in the browser)",
    )
    parser.add_argument(
        "--format",
        default="gen9ubers",
        help="Battle format (default: gen9ubers)",
    )
    parser.add_argument(
        "--mode",
        choices=["accept", "challenge"],
        default="accept",
        help="accept = bot waits for your challenge; challenge = bot challenges you",
    )
    parser.add_argument(
        "--bot-team",
        default="bots/teams/uber.txt",
        help="Optional path to a team file for the bot. Default: bots/teams/uber.txt",
    )

    args = parser.parse_args()

    # Handle bot username and token
    bot_username = args.bot_username
    bot_token = args.bot_token
    
    # If username is provided but no token, warn the user
    if bot_username and not bot_token:
        print("Warning: You provided a bot username but no authentication token.")
        print("This will likely cause authentication errors.")
        print("Either provide --bot-token or remove --bot-username to use a guest account.")
        print("Continuing anyway...")

    asyncio.run(
        run_battle(
            bot_module=args.bot_module,
            bot_class=args.bot_class,
            bot_username=bot_username,
            bot_token=bot_token,
            human_username=args.human_username,
            battle_format=args.format,
            mode=args.mode,
            bot_team=args.bot_team,
        )
    )


if __name__ == "__main__":
    main()
