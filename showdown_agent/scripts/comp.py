import asyncio
import importlib
import os
import sys
from typing import List, Dict
import poke_env as pke
from poke_env import AccountConfiguration
from poke_env.player.player import Player
from tabulate import tabulate

# === Your existing helper functions ===
def rank_players_by_victories(results_dict, top_k=10):
    victory_scores = {}
    for player, opponents in results_dict.items():
        victories = [
            1 if (score is not None and score > 0.5) else 0
            for opp, score in opponents.items()
            if opp != player
        ]
        if victories:
            victory_scores[player] = sum(victories) / len(victories)
        else:
            victory_scores[player] = 0.0
    return sorted(victory_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

def gather_players():
    import importlib.util

    players = []
    replay_dir = os.path.join(os.path.dirname(__file__), "replays")
    os.makedirs(replay_dir, exist_ok=True)

    # Only use htho884.py from the players folder
    player_file = os.path.join(os.path.dirname(__file__), "players", "htho884.py")
    module_name = "htho884"
    spec = importlib.util.spec_from_file_location(module_name, player_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    if hasattr(module, "CustomAgent"):
        player_name = module_name
        agent_class = getattr(module, "CustomAgent")
        agent_replay_dir = os.path.join(replay_dir, player_name)
        os.makedirs(agent_replay_dir, exist_ok=True)
        account_config = AccountConfiguration(player_name, None)
        player = agent_class(
            account_configuration=account_config,
            battle_format="gen9ubers",
        )
        player._save_replays = agent_replay_dir
        players.append(player)
    return players
def gather_bots():
    bot_folders = os.path.join(os.path.dirname(__file__), "bots")
    bot_teams_folders = os.path.join(bot_folders, "teams")
    generic_bots = []
    bot_teams = {}

    for team_file in os.listdir(bot_teams_folders):
        if team_file.endswith(".txt"):
            with open(os.path.join(bot_teams_folders, team_file), "r", encoding="utf-8") as file:
                bot_teams[team_file[:-4]] = file.read()

    for module_name in os.listdir(bot_folders):
        if module_name.endswith(".py"):
            module_path = f"{bot_folders}/{module_name}"
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            for team_name, team in bot_teams.items():
                if hasattr(module, "CustomAgent"):
                    agent_class = getattr(module, "CustomAgent")
                    config_name = f"{module_name[:-3]}-{team_name}"
                    account_config = AccountConfiguration(config_name, None)
                    generic_bots.append(
                        agent_class(
                            team=team,
                            account_configuration=account_config,
                            battle_format="gen9ubers",
                        )
                    )
    return generic_bots

async def cross_evaluate(agents: List[Player]):
    return await pke.cross_evaluate(agents, n_challenges=3)

def evaluate_against_bots(players: List[Player]):
    cross_eval_results = asyncio.run(cross_evaluate(players))
    top_players = rank_players_by_victories(cross_eval_results, top_k=len(cross_eval_results))
    return top_players

# === NEW: Multiple runs to compute average ranking ===
def main():
    generic_bots = gather_bots()
    players = gather_players()

    run_count = 20
    rank_totals: Dict[str, int] = {player.username: 0 for player in players}

    for run in range(1, run_count + 1):
        print(f"\n=== Run {run}/{run_count} ===")
        for player in players:
            agents = [player] + generic_bots
            rankings = evaluate_against_bots(agents)

            for rank, (agent, winrate) in enumerate(rankings, start=1):
                if agent == player.username:
                    rank_totals[player.username] += rank
                    print(f"{player.username} ranked {rank} this run (Win rate {winrate:.2f})")

    # Compute average rank and percentage
    print("\n=== Average Rankings over", run_count, "runs ===")
    for player in players:
        avg_rank = rank_totals[player.username] / run_count
        total_players = len(generic_bots) + 1
        avg_percentage = (1 - ((avg_rank - 1) / (total_players - 1))) * 100
        print(f"{player.username}: Avg Rank {avg_rank:.2f} ({avg_percentage:.2f}%)")

if __name__ == "__main__":
    main()
