# expert_main_vs_bots.py
# Runs only players/htho884.py vs every bot; prints W/L/D per opponent.

import asyncio
import importlib.util
import os
import sys
from typing import List, Dict, Tuple

import poke_env as pke
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.player.player import Player
from tabulate import tabulate

N_CHALLENGES = 10  # battles per opponent

def load_htho884() -> Player:
    base_dir = os.path.dirname(__file__)
    module_path = os.path.join(base_dir, "players", "htho884.py")
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Could not find {module_path}")

    spec = importlib.util.spec_from_file_location("htho884", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["htho884"] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "CustomAgent"):
        raise ImportError("CustomAgent class not found in players/htho884.py")

    agent_class = getattr(module, "CustomAgent")
    account_config = AccountConfiguration("htho884", None)
    player = agent_class(
        account_configuration=account_config,
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers",
    )

    # Save replays
    replay_dir = os.path.join(base_dir, "replays", "htho884")
    os.makedirs(replay_dir, exist_ok=True)
    player._save_replays = replay_dir
    return player

def gather_bots() -> List[Player]:
    base_dir = os.path.dirname(__file__)
    bot_dir = os.path.join(base_dir, "bots")
    team_dir = os.path.join(bot_dir, "teams")

    # Load teams
    bot_teams: Dict[str, str] = {}
    if os.path.isdir(team_dir):
        for team_file in os.listdir(team_dir):
            if team_file.endswith(".txt"):
                with open(os.path.join(team_dir, team_file), "r", encoding="utf-8") as f:
                    bot_teams[team_file[:-4]] = f.read()

    generic_bots: List[Player] = []

    for module_name in os.listdir(bot_dir):
        if not module_name.endswith(".py"):
            continue
        module_path = os.path.join(bot_dir, module_name)

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        if not hasattr(module, "CustomAgent"):
            continue

        agent_class = getattr(module, "CustomAgent")

        # If there are no teams, still instantiate once with no team
        if not bot_teams:
            config_name = f"{module_name[:-3]}"
            account_config = AccountConfiguration(config_name, None)
            generic_bots.append(
                agent_class(
                    account_configuration=account_config,
                    server_configuration=LocalhostServerConfiguration,
                    battle_format="gen9ubers",
                )
            )
            continue

        # Otherwise, instantiate once per team
        for team_name, team in bot_teams.items():
            config_name = f"{module_name[:-3]}-{team_name}"
            account_config = AccountConfiguration(config_name, None)
            generic_bots.append(
                agent_class(
                    team=team,
                    account_configuration=account_config,
                    server_configuration=LocalhostServerConfiguration,
                    battle_format="gen9ubers",
                )
            )

    return generic_bots

async def cross_evaluate(agents: List[Player]):
    # Optional: wrap with a timeout so it doesn’t hang silently forever
    return await asyncio.wait_for(
        pke.cross_evaluate(agents, n_challenges=N_CHALLENGES),
        timeout=600,  # 10 minutes; increase if your machine is slow
    )

async def quick_smoke_test(me: Player, one_bot: Player):
    # Single quick match so you can see immediate output
    print(f"Smoke test: {me.username} vs {one_bot.username}")
    res = await pke.cross_evaluate([me, one_bot], n_challenges=1)
    # Results dict can be keyed by Player instances or by usernames depending on library version
    def _resolve_key(d, player: Player):
        if player in d:
            return player
        for k in d:
            # Key may be a Player-like object
            if getattr(k, "username", None) == player.username:
                return k
            # Or it may be a plain username string
            if isinstance(k, str) and k == player.username:
                return k
        raise KeyError(player)

    me_key = _resolve_key(res, me)
    bot_key = _resolve_key(res[me_key], one_bot)
    wr = res[me_key][bot_key]
    print(f"  => wr={wr * 100:.1f}% (100%=win, 0%=loss, 50%=draw)")

async def evaluate_vs_all(me: Player, bots: List[Player], n_challenges: int) -> Dict[Player, float]:
    """Evaluate only `me` vs each bot; return map opponent -> winrate."""
    results: Dict[Player, float] = {}
    for bot in bots:
        res = await pke.cross_evaluate([me, bot], n_challenges=n_challenges)

        # Resolve keys robustly (Player or username)
        def _resolve_key(d, player: Player):
            if player in d:
                return player
            for k in d:
                if getattr(k, "username", None) == player.username:
                    return k
                if isinstance(k, str) and k == player.username:
                    return k
            raise KeyError(player)

        me_key = _resolve_key(res, me)
        bot_key = _resolve_key(res[me_key], bot)
        results[bot] = res[me_key][bot_key]
    return results

def main():
    # 1) Make sure the server is running:
    #    node pokemon-showdown start --no-security
    print("Checking setup…")
    me = load_htho884()
    bots = gather_bots()

    if not bots:
        print("No bots found in bots/ or bots/teams/.")
        return

    print(f"Evaluating {me.username} vs {len(bots)} bot(s). Battles/opponent: {N_CHALLENGES}")

    # Quick smoke test vs first bot for instant feedback
    asyncio.run(quick_smoke_test(me, bots[0]))

    # Only evaluate ME vs each bot (no bot-vs-bot matches)
    print("Running evaluation: me vs each bot…")
    wr_against_all = asyncio.run(evaluate_vs_all(me, bots, N_CHALLENGES))
    print("Done.\n")

    username_by_agent = {me: me.username, **{b: b.username for b in bots}}

    # Pretty table of my winrates vs each bot
    headers = ["Opponent", "Winrate (%)"]
    table = [[username_by_agent[b], wr_against_all[b] * 100] for b in bots]
    print("Winrates vs each opponent:")
    print(tabulate(table, headers=headers, floatfmt=".1f"))

    # My results grouped
    my_row = wr_against_all
    wins: List[Tuple[str, float]] = []
    losses: List[Tuple[str, float]] = []
    draws: List[Tuple[str, float]] = []

    for opp, wr in my_row.items():
        if wr > 0.5:
            wins.append((username_by_agent[opp], wr))
        elif wr < 0.5:
            losses.append((username_by_agent[opp], wr))
        else:
            draws.append((username_by_agent[opp], wr))

    wins.sort(key=lambda x: x[1], reverse=True)
    losses.sort(key=lambda x: x[1])
    draws.sort(key=lambda x: x[0])

    print("\n================== RESULTS FOR htho884 ==================")
    print(f"Total opponents: {len(bots)}  |  Battles per opponent: {N_CHALLENGES}\n")

    def block(title: str, items: List[Tuple[str, float]]):
        print(title)
        if not items:
            print("  (none)")
        else:
            for name, wr in items:
                print(f"  - {name}: winrate {wr * 100:.1f}%")
        print()

    block("✅ Wins (wr > 0.50):", wins)
    block("❌ Losses (wr < 0.50):", losses)
    block("➖ Draws (wr = 0.50):", draws)

if __name__ == "__main__":
    main()
