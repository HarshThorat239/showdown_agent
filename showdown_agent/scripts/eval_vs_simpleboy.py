# eval_vs_simpleboy.py
# Evaluation script for V1, V2, V3, and htho884.py players against simpleboy.py

import asyncio
import importlib.util
import os
import sys
from typing import List, Dict, Tuple
import poke_env as pke
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.player.player import Player
import matplotlib.pyplot as plt
import numpy as np

N_CHALLENGES = 100  # battles per player

def load_player(player_name: str) -> Player:
    """Load a player from the players directory."""
    base_dir = os.path.dirname(__file__)
    module_path = os.path.join(base_dir, "players", f"{player_name}.py")
    
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Could not find {module_path}")

    spec = importlib.util.spec_from_file_location(player_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[player_name] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "CustomAgent"):
        raise ImportError(f"CustomAgent class not found in players/{player_name}.py")

    agent_class = getattr(module, "CustomAgent")
    account_config = AccountConfiguration(f"{player_name}_player", None)
    player = agent_class(
        account_configuration=account_config,
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers",
    )

    # Save replays
    replay_dir = os.path.join(base_dir, "replays", f"{player_name}_vs_simpleboy")
    os.makedirs(replay_dir, exist_ok=True)
    player._save_replays = replay_dir
    
    return player

def load_simpleboy() -> Player:
    """Load the simpleboy player."""
    base_dir = os.path.dirname(__file__)
    module_path = os.path.join(base_dir, "players", "second.py")
    
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Could not find {module_path}")

    spec = importlib.util.spec_from_file_location("simpleboy", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["simpleboy"] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "CustomAgent"):
        raise ImportError("CustomAgent class not found in players/simpleboy.py")

    agent_class = getattr(module, "CustomAgent")
    account_config = AccountConfiguration("simpleboy_player", None)
    player = agent_class(
        account_configuration=account_config,
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers",
    )

    # Save replays
    replay_dir = os.path.join(base_dir, "replays", "simpleboy_as_opponent")
    os.makedirs(replay_dir, exist_ok=True)
    player._save_replays = replay_dir
    
    return player

async def evaluate_player_vs_simpleboy(player: Player, simpleboy: Player, n_challenges: int) -> float:
    """Evaluate a single player against simpleboy and return win rate."""
    print(f"Evaluating {player.username} vs {simpleboy.username} ({n_challenges} battles)...")
    
    res = await pke.cross_evaluate([player, simpleboy], n_challenges=n_challenges)

    # Resolve keys robustly (Player or username)
    def _resolve_key(d, target_player: Player):
        if target_player in d:
            return target_player
        for k in d:
            if getattr(k, "username", None) == target_player.username:
                return k
            if isinstance(k, str) and k == target_player.username:
                return k
        raise KeyError(target_player)

    player_key = _resolve_key(res, player)
    simpleboy_key = _resolve_key(res[player_key], simpleboy)
    win_rate = res[player_key][simpleboy_key]
    
    print(f"  => {player.username} win rate: {win_rate * 100:.1f}%")
    return win_rate

async def evaluate_all_players_vs_simpleboy(player_names: List[str], n_challenges: int) -> Dict[str, float]:
    """Evaluate all players against simpleboy."""
    results = {}
    simpleboy = load_simpleboy()
    
    for player_name in player_names:
        try:
            player = load_player(player_name)
            win_rate = await evaluate_player_vs_simpleboy(player, simpleboy, n_challenges)
            results[player_name] = win_rate
        except Exception as e:
            print(f"Error loading {player_name}: {e}")
            results[player_name] = 0.0
    
    return results

def create_winrate_graph(results: Dict[str, float]):
    """Create a bar graph showing win rates of each player against simpleboy."""
    if not results:
        print("No results to display.")
        return
    
    # Extract data for plotting
    player_names = list(results.keys())
    win_rates = [results[name] * 100 for name in player_names]  # Convert to percentage
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    colors = ['#2E8B57' if wr >= 50 else '#DC143C' for wr in win_rates]
    bars = plt.bar(player_names, win_rates, color=colors, alpha=0.7)
    
    # Customize the plot
    plt.title('Player Win Rates vs Simpleboy', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Players', fontsize=12)
    plt.ylabel('Win Rate (%)', fontsize=12)
    plt.ylim(0, 100)
    
    # Add horizontal line at 50% for reference
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.7, label='50% (Even)')
    
    # Add value labels on top of bars
    for bar, wr in zip(bars, win_rates):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{wr:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3)
    
    # Add legend
    plt.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the graph
    base_dir = os.path.dirname(__file__)
    graph_path = os.path.join(base_dir, "winrate_vs_simpleboy.png")
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    print(f"\n📊 Win rate graph saved to: {graph_path}")
    
    # Show the graph
    plt.show()
    
    # Print summary statistics
    avg_winrate = np.mean(win_rates)
    best_player = player_names[np.argmax(win_rates)]
    worst_player = player_names[np.argmin(win_rates)]
    
    print(f"\n📈 Summary Statistics:")
    print(f"   Average Win Rate: {avg_winrate:.1f}%")
    print(f"   Best Performance: {best_player} ({max(win_rates):.1f}%)")
    print(f"   Worst Performance: {worst_player} ({min(win_rates):.1f}%)")
    print(f"   Total Players: {len(player_names)}")
    print(f"   Battles per Player: {N_CHALLENGES}")

def print_results_table(results: Dict[str, float]):
    """Print a formatted table of results."""
    print("\n" + "="*60)
    print("EVALUATION RESULTS: Players vs Simpleboy")
    print("="*60)
    
    # Sort by win rate (descending)
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Player':<15} {'Win Rate':<10} {'Battles':<10} {'Status'}")
    print("-" * 60)
    
    for player_name, win_rate in sorted_results:
        status = "✅ Win" if win_rate > 0.5 else "❌ Loss" if win_rate < 0.5 else "➖ Draw"
        print(f"{player_name:<15} {win_rate*100:>7.1f}%   {N_CHALLENGES:<10} {status}")
    
    print("-" * 60)
    print(f"Total battles per player: {N_CHALLENGES}")
    print(f"Total players evaluated: {len(results)}")

async def main():
    """Main evaluation function."""
    print("🚀 Starting evaluation: V1, V2, V3, and htho884 vs Simpleboy")
    print(f"📊 Battles per player: {N_CHALLENGES}")
    print("="*60)
    
    # Players to evaluate
    player_names = ["V1", "V2", "V3", "htho884"]
    
    # Check if all player files exist
    missing_players = []
    for player_name in player_names:
        base_dir = os.path.dirname(__file__)
        player_path = os.path.join(base_dir, "players", f"{player_name}.py")
        if not os.path.exists(player_path):
            missing_players.append(player_name)
    
    # Check if simpleboy exists
    base_dir = os.path.dirname(__file__)
    simpleboy_path = os.path.join(base_dir, "players", "simpleboy.py")
    if not os.path.exists(simpleboy_path):
        print(f"❌ Missing simpleboy.py file at {simpleboy_path}")
        return
    
    if missing_players:
        print(f"❌ Missing player files: {missing_players}")
        print("Available players:")
        players_dir = os.path.join(base_dir, "players")
        if os.path.exists(players_dir):
            for file in os.listdir(players_dir):
                if file.endswith(".py") and file != "__init__.py":
                    print(f"  - {file[:-3]}")
        return
    
    # Run evaluation
    print("🎮 Starting battles...")
    results = await evaluate_all_players_vs_simpleboy(player_names, N_CHALLENGES)
    
    # Display results
    print_results_table(results)
    
    # Create win rate graph
    print("\n📊 Generating win rate graph...")
    create_winrate_graph(results)
    
    print("\n✅ Evaluation complete!")

if __name__ == "__main__":
    asyncio.run(main())
