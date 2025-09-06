# node pokemon-showdown start --no-security

import argparse
import asyncio
import importlib.util
import os
import sys
from typing import List, Dict, Optional, Tuple

import poke_env as pke
from poke_env import AccountConfiguration
from poke_env.player.player import Player
from tabulate import tabulate


# ------------------------------- ranking utils -------------------------------

def rank_players_by_victories(results_dict: Dict[str, Dict[str, float]], top_k=10):
    victory_scores = {}
    for player, opponents in results_dict.items():
        victories = [
            1 if (score is not None and score > 0.5) else 0
            for opp, score in opponents.items()
            if opp != player
        ]
        victory_scores[player] = (sum(victories) / len(victories)) if victories else 0.0
    return sorted(victory_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]


# ------------------------------- loading utils -------------------------------

def _unique_username(base: str, existing: set) -> str:
    name = base
    i = 2
    while name in existing:
        name = f"{base}-{i}"
        i += 1
    existing.add(name)
    return name


def _load_module_from_path(path: str):
    """Load a module from an arbitrary filesystem path. Raises to caller."""
    path = os.path.abspath(path)
    mod_name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)  # may raise (we catch where we call)
    return module


def _instantiate_customagent(module, username: str, team: Optional[str] = None) -> Player:
    if not hasattr(module, "CustomAgent"):
        raise RuntimeError(f"Module {module} has no CustomAgent class")
    cls = getattr(module, "CustomAgent")
    acc = AccountConfiguration(username, None)
    if team is None:
        return cls(account_configuration=acc, battle_format="gen9ubers")
    return cls(team=team, account_configuration=acc, battle_format="gen9ubers")


# -------------------------------- gatherers ----------------------------------

def gather_players():
    base_dir = os.path.dirname(__file__)
    replay_dir = os.path.join(base_dir, "replays")
    os.makedirs(replay_dir, exist_ok=True)

    players: List[Player] = []
    failed: List[Tuple[str, str]] = []

    def load_agents_from(subdir: str, prefix: str):
        folder = os.path.join(base_dir, subdir)
        if not os.path.isdir(folder):
            return

        for filename in os.listdir(folder):
            if not filename.endswith(".py"):
                continue
            file_path = os.path.join(folder, filename)

            # Create a unique module name so players/ and opps/ can't collide
            modname = f"{prefix}_{filename[:-3]}"
            spec = importlib.util.spec_from_file_location(modname, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[modname] = module
            try:
                spec.loader.exec_module(module)  # type: ignore
            except ModuleNotFoundError as e:
                print(f"[warn] Skipping {subdir}/{filename}: missing dependency -> {e}")
                failed.append((filename, str(e)))
                continue
            except Exception as e:
                print(f"[warn] Skipping {subdir}/{filename}: import error -> {e}")
                failed.append((filename, str(e)))
                continue

            if hasattr(module, "CustomAgent"):
                cls = getattr(module, "CustomAgent")
                username = f"{prefix}-{filename[:-3]}"
                acc = AccountConfiguration(username, None)
                try:
                    agent = cls(account_configuration=acc, battle_format="gen9ubers")
                except Exception as e:
                    print(f"[warn] Skipping {subdir}/{filename}: init error -> {e}")
                    failed.append((filename, str(e)))
                    continue

                agent_replay_dir = os.path.join(replay_dir, username)
                os.makedirs(agent_replay_dir, exist_ok=True)
                agent._save_replays = agent_replay_dir

                players.append(agent)

    # Load your own agents in players/, then friends in opps/
    load_agents_from("players", "p")
    load_agents_from("opps", "opp")

    return players


def gather_bots(only: Optional[set] = None) -> List[Player]:
    """
    Load generic bots and their teams.
    If `only` is provided, include only config names like 'simple-uber', 'max_damage-uber'.
    """
    bot_folders = os.path.join(os.path.dirname(__file__), "bots")
    bot_teams_folders = os.path.join(bot_folders, "teams")

    generic_bots: List[Player] = []
    bot_teams: Dict[str, str] = {}

    if os.path.isdir(bot_teams_folders):
        for team_file in os.listdir(bot_teams_folders):
            if team_file.endswith(".txt"):
                with open(os.path.join(bot_teams_folders, team_file), "r", encoding="utf-8") as f:
                    bot_teams[team_file[:-4]] = f.read()

    used_names: set = set()

    if os.path.isdir(bot_folders):
        for module_name in os.listdir(bot_folders):
            if not module_name.endswith(".py"):
                continue
            module_path = os.path.join(bot_folders, module_name)
            try:
                module = _load_module_from_path(module_path)
            except Exception as e:
                print(f"[warn] Skipping bot {module_name}: import error -> {e}")
                continue

            if not hasattr(module, "CustomAgent"):
                continue
            cls = getattr(module, "CustomAgent")

            for team_name, team in bot_teams.items():
                config_name = f"{module_name[:-3]}-{team_name}"  # e.g. simple-uber
                if only and config_name not in only:
                    continue
                username = _unique_username(config_name, used_names)
                acc = AccountConfiguration(username, None)
                try:
                    bot = cls(team=team, account_configuration=acc, battle_format="gen9ubers")
                except Exception as e:
                    print(f"[warn] Skipping bot {config_name}: init error -> {e}")
                    continue
                generic_bots.append(bot)

    return generic_bots


# ------------------------------- evaluation ----------------------------------

async def cross_evaluate_agents(agents: List[Player], n: int):
    return await pke.cross_evaluate(agents, n_challenges=n)


def evaluate_against_bots(agents: List[Player], n: int) -> List[Tuple[str, float]]:
    print(f"{len(agents)} are competing in this challenge")
    print("Running Cross Evaluations...")
    results = asyncio.run(cross_evaluate_agents(agents, n))
    print("Evaluations Complete")

    # Pretty matrix
    table = [["-"] + [p.username for p in agents]]
    for p_1, row in results.items():
        table.append([p_1] + [row[p_2] for p_2 in row])
    print(tabulate(table[1:], headers=table[0], floatfmt=".2f"))

    print("Rankings")
    top_players = rank_players_by_victories(results, top_k=len(results))
    return top_players


def assign_marks(rank: int) -> float:
    modifier = 1.0 if rank > 10 else 0.5
    top_marks = 10.0 if rank < 10 else 5.0
    mod_rank = rank % 10
    marks = top_marks - (mod_rank - 1) * modifier
    return 0.0 if marks < 0 else marks


# ------------------------ NEW: “vs-mine” head-to-head ------------------------

async def _amain_vs_mine(mine: Player, opponents: List[Player], n: int) -> List[Tuple[str, int, int, int, float]]:
    """
    Sequentially pit `mine` vs each opponent only, for `n` battles.
    Returns list of (opp_username, my_wins, opp_wins, total, my_wr).
    """
    rows: List[Tuple[str, int, int, int, float]] = []
    for opp in opponents:
        if opp.username == mine.username:
            continue
        # reset counters for a clean head-to-head
        mine.reset_battles()
        opp.reset_battles()
        print(f"==> {mine.username} vs {opp.username} (n={n})")
        await mine.battle_against(opp, n_battles=n)
        my_w, op_w = mine.n_won_battles, opp.n_won_battles
        tot = max(1, my_w + op_w)
        rows.append((opp.username, my_w, op_w, tot, my_w / tot))
    return rows


def evaluate_vs_mine(players: List[Player], mine_username: str, n: int,
                     include_bots: List[Player]) -> List[Tuple[str, int, int, int, float]]:
    look = {p.username: p for p in players}
    if mine_username not in look:
        raise SystemExit(f"--mine '{mine_username}' not found. Loaded: {sorted(look)}")

    mine = look[mine_username]
    # Opponents = everyone else (players + bots)
    opponents = [p for p in players if p.username != mine_username] + list(include_bots)

    rows = asyncio.run(_amain_vs_mine(mine, opponents, n=n))

    # Pretty print
    print("\n=== Head-to-head (ONLY vs mine) ===")
    header = ["Opponent", "My Wins", "Opp Wins", "Total", "My WR"]
    printable = [[u, w, l, t, f"{wr:.2f}"] for (u, w, l, t, wr) in rows]
    printable.sort(key=lambda r: float(r[-1]), reverse=True)
    print(tabulate(printable, headers=header))

    # Save CSV
    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "vs_mine.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for u, w, l, t, wr in rows:
            f.write(f"{u},{w},{l},{t},{wr:.4f}\n")
    print(f"\nSaved head-to-head CSV to {csv_path}")

    # Quick “as good as mine” hints
    borderline = [(u, wr) for (u, _, __, ___, wr) in rows if 0.45 <= wr <= 0.55]
    if borderline:
        print("\nOpponents roughly as good as yours (0.45–0.55):")
        for u, wr in sorted(borderline, key=lambda x: x[1], reverse=True):
            print(f"  {u}: {wr:.2f}")

    return rows


# ----------------------------------- main ------------------------------------

def parse_args():
    ap = argparse.ArgumentParser(description="Evaluate agents vs generic bots (and classmates).")
    ap.add_argument("--n", type=int, default=3, help="Challenges per pairing (default: 3)")
    ap.add_argument("--add", nargs="*", default=[], help="Extra agent file paths to include (friends/classmates)")
    ap.add_argument("--bots", type=str, default="", help="Comma list of bot config names to include. "
                    "Use 'none' to disable (default: all).")
    ap.add_argument("--only", type=str, default="", help="Comma list of agent usernames to keep (filters players only)")
    ap.add_argument("--head2head", action="store_true", help="Run each of your agents head-to-head vs all others only")
    ap.add_argument("--duel", type=str, default="", help="Run ONLY a vs b, comma-separated usernames (e.g. p-lsiv157,opp-T)")
    # NEW:
    ap.add_argument("--vs-mine", action="store_true", help="Run ONLY <mine> vs everyone else (no opp-vs-opp).")
    ap.add_argument("--mine", type=str, default="", help="Username of your agent in players/ (e.g. p-my_agent).")
    return ap.parse_args()


def main():
    args = parse_args()

    # -------------- bots --------------
    if args.bots and args.bots.strip().lower() in {"none", "off", "0"}:
        generic_bots: List[Player] = []
    else:
        bot_only = set(filter(None, (s.strip() for s in args.bots.split(",")))) if args.bots else None
        generic_bots = gather_bots(only=bot_only)

    # -------------- players --------------
    players = gather_players()

    # Load extra agent files passed via --add (if any)
    for extra_path in args.add:
        try:
            mod = _load_module_from_path(extra_path)
        except Exception as e:
            print(f"[warn] --add {extra_path}: import error -> {e}")
            continue
        username = f"extra-{os.path.splitext(os.path.basename(extra_path))[0]}"
        try:
            agent = _instantiate_customagent(mod, username=username)
        except Exception as e:
            print(f"[warn] --add {extra_path}: init error -> {e}")
            continue
        # Give it a replay folder like others
        base_dir = os.path.dirname(__file__)
        replay_dir = os.path.join(base_dir, "replays", username)
        os.makedirs(replay_dir, exist_ok=True)
        agent._save_replays = replay_dir
        players.append(agent)

    # Optional filter by username
    if args.only:
        keep = {s.strip() for s in args.only.split(",") if s.strip()}
        players = [p for p in players if p.username in keep]

    # -------------- DUEL mode --------------
    if args.duel:
        a, b = [s.strip() for s in args.duel.split(",")]
        look = {p.username: p for p in players}
        missing = [u for u in (a, b) if u not in look]
        if missing:
            raise SystemExit(f"Could not find {missing}. Loaded players: {sorted(look)}")

        agents = [look[a], look[b]]
        print(f"Running duel: {a} vs {b} (n={args.n})")
        results = asyncio.run(cross_evaluate_agents(agents, n=args.n))

        table = [["-"] + [p.username for p in agents]]
        for p_1, row in results.items():
            table.append([p_1] + [row[p_2] for p_2 in row])
        print(tabulate(table[1:], headers=table[0], floatfmt=".2f"))

        wr_a = results[a][b]; wr_b = results[b][a]
        print(f"\nHead-to-head winrates: {a}: {wr_a:.2f}  |  {b}: {wr_b:.2f}")
        return  # stop after duel

    # -------------- VS-MINE mode --------------
    if args.vs_mine:
        if not args.mine:
            # If exactly one 'p-*' is loaded, assume it's mine; else require --mine
            p_users = [p.username for p in players if p.username.startswith("p-")]
            if len(p_users) == 1:
                args.mine = p_users[0]
                print(f"[info] --mine not provided; assuming {args.mine}")
            else:
                raise SystemExit("Use --mine <username> (e.g., p-my_agent) to select your agent.")
        evaluate_vs_mine(players, mine_username=args.mine, n=args.n, include_bots=generic_bots)
        return

    # -------------- original evaluation path --------------
    results_file = os.path.join(os.path.dirname(__file__), "results", "marking_results.txt")
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    with open(results_file, "w", encoding="utf-8") as f:
        pass

    for player in players:
        print(f"Evaluating player: {player.username}")
        if args.head2head:
            opponents = [player]
            opponents.extend([p for p in players if p.username != player.username])
            opponents.extend(generic_bots)  # may be empty if --bots none
            rankings = evaluate_against_bots(opponents, n=args.n)
        else:
            agents = [player] + generic_bots
            rankings = evaluate_against_bots(agents, n=args.n)

        player_rank = len(rankings) + 1
        player_mark = 0.0
        print("Rank. Player - Win Rate - Mark")
        for rank, (agent, winrate) in enumerate(rankings, 1):
            mark = assign_marks(rank)
            print(f"{rank}. {agent} - {winrate:.2f} - {mark}")
            if agent == player.username:
                player_rank = rank
                player_mark = mark

        print(f"{player.username} ranked #{player_rank} with a mark of {player_mark}\n")
        with open(results_file, "a", encoding="utf-8") as f:
            f.write(f"{player.username} #{player_rank} {player_mark}\n")


if __name__ == "__main__":
    main()