#!/usr/bin/env python3
# fight_my_agent.py
#
# Play as a human (in the browser) against your CustomAgent on a local Showdown server.
# Requirements:
#   - Local server running: `node pokemon-showdown start --no-security`
#   - Your CustomAgent in players/<file>.py with class "CustomAgent"
#   - poke-env installed
#
# Usage examples:
#   Accept mode (you challenge the agent from the browser):
#       python fight_my_agent.py --agent-module players/htho884.py \
#           --agent-class CustomAgent --agent-username htho884 \
#           --human-username myhuman --format gen9ubers --mode accept
#
#   Challenge mode (agent challenges your human account):
#       python fight_my_agent.py --agent-module players/htho884.py \
#           --agent-class CustomAgent --agent-username htho884 \
#           --human-username myhuman --format gen9ubers --mode challenge
#
# Notes:
#   - Your *human* team is set in the browser (Build Team → import/paste).
#   - By default the agent uses its own internal team logic. If you want the agent
#     to use a specific team file, add: --agent-team path/to/team.txt

import argparse
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


async def run_battle(
    agent_module: str,
    agent_class: str,
    agent_username: str,
    human_username: str,
    battle_format: str,
    mode: str,
    agent_team: str | None,
):
    # Load your CustomAgent class
    AgentClass = load_class_from_file(agent_module, agent_class)

    # Read agent team if provided
    team_str = None
    if agent_team:
        with open(agent_team, "r", encoding="utf-8") as f:
            team_str = f.read()

    # Instantiate the agent
    init_kwargs = {
    "account_configuration": AccountConfiguration(agent_username, None),
    "server_configuration": LocalhostServerConfiguration,
    "battle_format": battle_format,
}
    if team_str is not None:  # only include if you actually provided a team file
        init_kwargs["team"] = team_str

    agent: Player = AgentClass(**init_kwargs)

    # Helpful printouts
    print(f"Agent '{agent.username}' is online on local server (format: {battle_format}).")
    if team_str:
        print(f"Agent is using team from: {agent_team}")
    else:
        print("Agent has no explicit team set (will use its internal default, if any).")

    # Either wait for your challenge, or send one to you
    if mode == "accept":
        print(
            f"Waiting for a challenge from '{human_username}'... "
            f"(Open http://localhost:8000, log in as '{human_username}', "
            f"select your team, and challenge '{agent.username}' in {battle_format})"
        )
        await agent.accept_challenges(human_username, n_challenges=1)
    else:
        print(
            f"Sending a challenge to '{human_username}'... "
            f"(Accept it in your browser with your chosen team)"
        )
        await agent.send_challenges(human_username, n_challenges=1, to_wait=True)

    # Wait until all battles conclude, then clean up
    await agent._detailed_teardown()
    print("Battle finished. Agent logged out.")


def main():
    parser = argparse.ArgumentParser(description="Fight your agent with your own team via local Showdown.")
    parser.add_argument("--agent-module", required=True, help="Path to your agent file, e.g. players/simpleboy.py")
    parser.add_argument("--agent-class", default="CustomAgent", help="Agent class name (default: CustomAgent)")
    parser.add_argument("--agent-username", required=True, help="Showdown username for the agent (bot) account")
    parser.add_argument("--human-username", required=True, help="Your human username (used in browser)")
    parser.add_argument("--format", default="gen9ubers", help="Battle format, e.g. gen9ubers")
    parser.add_argument(
        "--mode",
        choices=["accept", "challenge"],
        default="accept",
        help="accept = agent waits for your challenge; challenge = agent challenges you",
    )
    parser.add_argument(
        "--agent-team",
        default=None,
        help="Optional path to a team file for the agent. If omitted, agent uses its internal default.",
    )

    args = parser.parse_args()

    asyncio.run(
        run_battle(
            agent_module=args.agent_module,
            agent_class=args.agent_class,
            agent_username=args.agent_username,
            human_username=args.human_username,
            battle_format=args.format,
            mode=args.mode,
            agent_team=args.agent_team,
        )
    )


if __name__ == "__main__":
    main()
