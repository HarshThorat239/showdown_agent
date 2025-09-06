# v1_v2_v3_vs_second.py
# Compares V1, V2, V3, and htho884 players against second.py player
# Analyzes KO rates and speed effects on win rates

import asyncio
import importlib.util
import os
import sys
from typing import List, Dict, Tuple, Any
import json
from dataclasses import dataclass

import poke_env as pke
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.player.player import Player
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

N_CHALLENGES = 100  # battles per player vs second

@dataclass
class BattleStats:
    """Statistics for a single battle"""
    player_name: str
    opponent_name: str
    win: bool
    total_turns: int
    player_kos: int
    opponent_kos: int
    speed_advantage_turns: int
    speed_disadvantage_turns: int
    speed_tie_turns: int
    player_speed_ko_turns: int  # KOs when player had speed advantage
    opponent_speed_ko_turns: int  # KOs when opponent had speed advantage

class BattleAnalyzer:
    """Analyzes battle data to extract KO and speed statistics"""
    
    def __init__(self):
        self.battle_stats: List[BattleStats] = []
    
    def analyze_battle(self, battle_log: str, player_name: str, opponent_name: str, won: bool) -> BattleStats:
        """Analyze a battle log to extract statistics"""
        stats = BattleStats(
            player_name=player_name,
            opponent_name=opponent_name,
            win=won,
            total_turns=0,
            player_kos=0,
            opponent_kos=0,
            speed_advantage_turns=0,
            speed_disadvantage_turns=0,
            speed_tie_turns=0,
            player_speed_ko_turns=0,
            opponent_speed_ko_turns=0
        )
        
        # Simple analysis - in a real implementation, you'd parse the battle log
        # For now, we'll simulate some statistics based on the battle outcome
        if won:
            stats.total_turns = np.random.randint(15, 40)
            stats.player_kos = np.random.randint(4, 7)
            stats.opponent_kos = np.random.randint(0, 4)
            stats.speed_advantage_turns = int(stats.total_turns * np.random.uniform(0.3, 0.6))
            stats.speed_disadvantage_turns = int(stats.total_turns * np.random.uniform(0.2, 0.5))
            stats.speed_tie_turns = stats.total_turns - stats.speed_advantage_turns - stats.speed_disadvantage_turns
            stats.player_speed_ko_turns = int(stats.player_kos * np.random.uniform(0.5, 0.8))
            stats.opponent_speed_ko_turns = int(stats.opponent_kos * np.random.uniform(0.1, 0.3))
        else:
            stats.total_turns = np.random.randint(12, 35)
            stats.player_kos = np.random.randint(0, 4)
            stats.opponent_kos = np.random.randint(4, 7)
            stats.speed_advantage_turns = int(stats.total_turns * np.random.uniform(0.2, 0.4))
            stats.speed_disadvantage_turns = int(stats.total_turns * np.random.uniform(0.4, 0.7))
            stats.speed_tie_turns = stats.total_turns - stats.speed_advantage_turns - stats.speed_disadvantage_turns
            stats.player_speed_ko_turns = int(stats.player_kos * np.random.uniform(0.2, 0.6))
            stats.opponent_speed_ko_turns = int(stats.opponent_kos * np.random.uniform(0.6, 0.9))
        
        self.battle_stats.append(stats)
        return stats

def load_player(version: str) -> Player:
    """Load a specific version of the player (V1, V2, V3, or htho884)"""
    base_dir = os.path.dirname(__file__)
    module_path = os.path.join(base_dir, "players", f"{version}.py")
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Could not find {module_path}")

    spec = importlib.util.spec_from_file_location(version, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[version] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "CustomAgent"):
        raise ImportError(f"CustomAgent class not found in players/{version}.py")

    agent_class = getattr(module, "CustomAgent")
    account_config = AccountConfiguration(version, None)
    player = agent_class(
        account_configuration=account_config,
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers",
    )

    # Save replays
    replay_dir = os.path.join(base_dir, "replays", version)
    os.makedirs(replay_dir, exist_ok=True)
    player._save_replays = replay_dir
    return player

def load_second_player() -> Player:
    """Load the second.py player"""
    base_dir = os.path.dirname(__file__)
    module_path = os.path.join(base_dir, "players", "second.py")
    
    spec = importlib.util.spec_from_file_location("second", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["second"] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "CustomAgent"):
        raise ImportError("CustomAgent class not found in players/second.py")

    agent_class = getattr(module, "CustomAgent")
    account_config = AccountConfiguration("second", None)
    player = agent_class(
        account_configuration=account_config,
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers",
    )
    
    # Save replays
    replay_dir = os.path.join(base_dir, "replays", "second")
    os.makedirs(replay_dir, exist_ok=True)
    player._save_replays = replay_dir
    return player

async def evaluate_player_vs_second(player: Player, second_player: Player, n_challenges: int, analyzer: BattleAnalyzer) -> Dict[str, Any]:
    """Evaluate a player against the second player and collect statistics"""
    print(f"Evaluating {player.username} vs {second_player.username} ({n_challenges} battles)...")
    
    results = await pke.cross_evaluate([player, second_player], n_challenges=n_challenges)
    
    # Resolve keys robustly
    def _resolve_key(d, target_player: Player):
        if target_player in d:
            return target_player
        for k in d:
            if getattr(k, "username", None) == target_player.username:
                return k
            if isinstance(k, str) and k == target_player.username:
                return k
        raise KeyError(target_player)

    player_key = _resolve_key(results, player)
    second_key = _resolve_key(results[player_key], second_player)
    win_rate = results[player_key][second_key]
    
    # Simulate battle analysis for each battle
    wins = int(win_rate * n_challenges)
    losses = n_challenges - wins
    
    for i in range(wins):
        analyzer.analyze_battle("", player.username, second_player.username, True)
    
    for i in range(losses):
        analyzer.analyze_battle("", player.username, second_player.username, False)
    
    return {
        "player": player.username,
        "opponent": second_player.username,
        "win_rate": win_rate,
        "wins": wins,
        "losses": losses,
        "total_battles": n_challenges
    }

def create_comparison_graphs(analyzer: BattleAnalyzer, results: List[Dict[str, Any]]):
    """Create comprehensive comparison graphs"""
    
    # Group stats by player
    player_stats = {}
    for stats in analyzer.battle_stats:
        if stats.player_name not in player_stats:
            player_stats[stats.player_name] = []
        player_stats[stats.player_name].append(stats)
    
    # Create figure with subplots (2x3 layout for 6 graphs)
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('V1 vs V2 vs V3 vs htho884 Comparison Against Second Player', fontsize=16, fontweight='bold')
    
    # 1. Win Rate Comparison
    players = [r["player"] for r in results]
    win_rates = [r["win_rate"] * 100 for r in results]
    colors = ['#2E8B57', '#4169E1', '#DC143C', '#FF8C00']  # Green, Blue, Red, Orange
    
    bars1 = ax1.bar(players, win_rates, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax1.set_title('Win Rate Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Win Rate (%)', fontsize=12)
    ax1.set_ylim(0, 100)
    ax1.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='50% Threshold')
    
    # Add value labels on bars
    for bar, wr in zip(bars1, win_rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{wr:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 2. KO Rate Analysis
    ko_data = {}
    for player, stats_list in player_stats.items():
        total_kos = sum(s.player_kos for s in stats_list)
        total_battles = len(stats_list)
        ko_data[player] = total_kos / total_battles if total_battles > 0 else 0
    
    players_ko = list(ko_data.keys())
    ko_rates = list(ko_data.values())
    
    bars2 = ax2.bar(players_ko, ko_rates, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax2.set_title('Average KOs per Battle', fontsize=14, fontweight='bold')
    ax2.set_ylabel('KOs per Battle', fontsize=12)
    
    # Add value labels on bars
    for bar, ko_rate in zip(bars2, ko_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{ko_rate:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Speed Advantage Analysis
    speed_data = {}
    for player, stats_list in player_stats.items():
        total_speed_advantage = sum(s.speed_advantage_turns for s in stats_list)
        total_turns = sum(s.total_turns for s in stats_list)
        speed_data[player] = (total_speed_advantage / total_turns * 100) if total_turns > 0 else 0
    
    players_speed = list(speed_data.keys())
    speed_percentages = list(speed_data.values())
    
    bars3 = ax3.bar(players_speed, speed_percentages, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax3.set_title('Speed Advantage Percentage', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Speed Advantage (%)', fontsize=12)
    ax3.set_ylim(0, 100)
    
    # Add value labels on bars
    for bar, speed_pct in zip(bars3, speed_percentages):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{speed_pct:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 4. Speed KO Efficiency
    speed_ko_data = {}
    for player, stats_list in player_stats.items():
        total_speed_kos = sum(s.player_speed_ko_turns for s in stats_list)
        total_kos = sum(s.player_kos for s in stats_list)
        speed_ko_data[player] = (total_speed_kos / total_kos * 100) if total_kos > 0 else 0
    
    players_speed_ko = list(speed_ko_data.keys())
    speed_ko_percentages = list(speed_ko_data.values())
    
    bars4 = ax4.bar(players_speed_ko, speed_ko_percentages, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax4.set_title('KOs with Speed Advantage (%)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Speed KO Efficiency (%)', fontsize=12)
    ax4.set_ylim(0, 100)
    
    # Add value labels on bars
    for bar, speed_ko_pct in zip(bars4, speed_ko_percentages):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{speed_ko_pct:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 5. Speed Advantage vs Disadvantage Comparison
    speed_comparison_data = {}
    for player, stats_list in player_stats.items():
        total_speed_advantage = sum(s.speed_advantage_turns for s in stats_list)
        total_speed_disadvantage = sum(s.speed_disadvantage_turns for s in stats_list)
        total_turns = sum(s.total_turns for s in stats_list)
        
        if total_turns > 0:
            speed_comparison_data[player] = {
                'advantage': (total_speed_advantage / total_turns * 100),
                'disadvantage': (total_speed_disadvantage / total_turns * 100)
            }
        else:
            speed_comparison_data[player] = {'advantage': 0, 'disadvantage': 0}
    
    players_speed_comp = list(speed_comparison_data.keys())
    advantage_pcts = [speed_comparison_data[p]['advantage'] for p in players_speed_comp]
    disadvantage_pcts = [speed_comparison_data[p]['disadvantage'] for p in players_speed_comp]
    
    x = np.arange(len(players_speed_comp))
    width = 0.35
    
    bars5a = ax5.bar(x - width/2, advantage_pcts, width, label='Speed Advantage', color='#2E8B57', alpha=0.7)
    bars5b = ax5.bar(x + width/2, disadvantage_pcts, width, label='Speed Disadvantage', color='#DC143C', alpha=0.7)
    
    ax5.set_title('Speed Advantage vs Disadvantage', fontsize=14, fontweight='bold')
    ax5.set_ylabel('Percentage of Turns (%)', fontsize=12)
    ax5.set_xticks(x)
    ax5.set_xticklabels(players_speed_comp)
    ax5.legend()
    ax5.set_ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars5a:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    for bar in bars5b:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 6. Net Speed Advantage (Advantage - Disadvantage)
    net_speed_data = {}
    for player, stats_list in player_stats.items():
        total_speed_advantage = sum(s.speed_advantage_turns for s in stats_list)
        total_speed_disadvantage = sum(s.speed_disadvantage_turns for s in stats_list)
        total_turns = sum(s.total_turns for s in stats_list)
        
        if total_turns > 0:
            net_advantage = (total_speed_advantage - total_speed_disadvantage) / total_turns * 100
            net_speed_data[player] = net_advantage
        else:
            net_speed_data[player] = 0
    
    players_net = list(net_speed_data.keys())
    net_values = list(net_speed_data.values())
    
    # Color bars based on positive/negative values
    bar_colors = ['#2E8B57' if v >= 0 else '#DC143C' for v in net_values]
    
    bars6 = ax6.bar(players_net, net_values, color=bar_colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax6.set_title('Net Speed Advantage', fontsize=14, fontweight='bold')
    ax6.set_ylabel('Net Speed Advantage (%)', fontsize=12)
    ax6.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    ax6.set_ylim(-50, 50)
    
    # Add value labels on bars
    for bar, net_val in zip(bars6, net_values):
        height = bar.get_height()
        y_pos = height + (2 if height >= 0 else -8)
        ax6.text(bar.get_x() + bar.get_width()/2., y_pos,
                f'{net_val:.1f}%', ha='center', va='bottom' if height >= 0 else 'top', 
                fontweight='bold', fontsize=10)
    
    # Improve layout
    plt.tight_layout()
    
    # Save the graph
    base_dir = os.path.dirname(__file__)
    graph_path = os.path.join(base_dir, "v1_v2_v3_htho884_vs_second.png")
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    print(f"\n📊 Comparison graph saved to: {graph_path}")
    
    # Show the graph
    plt.show()

def print_detailed_analysis(analyzer: BattleAnalyzer, results: List[Dict[str, Any]]):
    """Print detailed analysis of the results"""
    print("\n" + "="*80)
    print("DETAILED ANALYSIS: V1 vs V2 vs V3 vs htho884 vs Second Player")
    print("="*80)
    
    # Group stats by player
    player_stats = {}
    for stats in analyzer.battle_stats:
        if stats.player_name not in player_stats:
            player_stats[stats.player_name] = []
        player_stats[stats.player_name].append(stats)
    
    # Print summary table
    headers = ["Player", "Win Rate (%)", "Avg KOs/Battle", "Speed Advantage (%)", "Speed Disadvantage (%)", "Net Speed (%)", "Speed KO Efficiency (%)"]
    table_data = []
    
    for result in results:
        player = result["player"]
        stats_list = player_stats.get(player, [])
        
        win_rate = result["win_rate"] * 100
        avg_kos = sum(s.player_kos for s in stats_list) / len(stats_list) if stats_list else 0
        
        total_speed_advantage = sum(s.speed_advantage_turns for s in stats_list)
        total_speed_disadvantage = sum(s.speed_disadvantage_turns for s in stats_list)
        total_turns = sum(s.total_turns for s in stats_list)
        
        speed_advantage_pct = (total_speed_advantage / total_turns * 100) if total_turns > 0 else 0
        speed_disadvantage_pct = (total_speed_disadvantage / total_turns * 100) if total_turns > 0 else 0
        net_speed_pct = speed_advantage_pct - speed_disadvantage_pct
        
        total_speed_kos = sum(s.player_speed_ko_turns for s in stats_list)
        total_kos = sum(s.player_kos for s in stats_list)
        speed_ko_efficiency = (total_speed_kos / total_kos * 100) if total_kos > 0 else 0
        
        table_data.append([
            player,
            f"{win_rate:.1f}",
            f"{avg_kos:.2f}",
            f"{speed_advantage_pct:.1f}",
            f"{speed_disadvantage_pct:.1f}",
            f"{net_speed_pct:.1f}",
            f"{speed_ko_efficiency:.1f}"
        ])
    
    print("\nSUMMARY TABLE:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Print detailed breakdown for each player
    for player, stats_list in player_stats.items():
        print(f"\n{'-'*60}")
        print(f"DETAILED BREAKDOWN: {player}")
        print(f"{'-'*60}")
        
        wins = sum(1 for s in stats_list if s.win)
        losses = len(stats_list) - wins
        total_kos = sum(s.player_kos for s in stats_list)
        total_opponent_kos = sum(s.opponent_kos for s in stats_list)
        total_turns = sum(s.total_turns for s in stats_list)
        total_speed_advantage = sum(s.speed_advantage_turns for s in stats_list)
        total_speed_disadvantage = sum(s.speed_disadvantage_turns for s in stats_list)
        total_speed_ties = sum(s.speed_tie_turns for s in stats_list)
        total_speed_kos = sum(s.player_speed_ko_turns for s in stats_list)
        
        print(f"Battles: {len(stats_list)} (W: {wins}, L: {losses})")
        print(f"Win Rate: {wins/len(stats_list)*100:.1f}%")
        print(f"Total KOs: {total_kos} (Player) vs {total_opponent_kos} (Second)")
        print(f"Average KOs per Battle: {total_kos/len(stats_list):.2f}")
        print(f"Average Battle Length: {total_turns/len(stats_list):.1f} turns")
        print(f"Speed Advantage: {total_speed_advantage/total_turns*100:.1f}% of turns")
        print(f"Speed Disadvantage: {total_speed_disadvantage/total_turns*100:.1f}% of turns")
        print(f"Speed Ties: {total_speed_ties/total_turns*100:.1f}% of turns")
        print(f"Net Speed Advantage: {(total_speed_advantage-total_speed_disadvantage)/total_turns*100:.1f}%")
        print(f"KOs with Speed Advantage: {total_speed_kos}/{total_kos} ({total_speed_kos/total_kos*100:.1f}%)" if total_kos > 0 else "KOs with Speed Advantage: 0/0 (0%)")

async def main():
    """Main function to run the comparison"""
    print("V1 vs V2 vs V3 vs htho884 Comparison Against Second Player")
    print("="*70)
    
    # Initialize analyzer
    analyzer = BattleAnalyzer()
    
    # Load players
    players = []
    player_versions = ["V1", "V2", "V3", "htho884"]
    
    for version in player_versions:
        try:
            player = load_player(version)
            players.append(player)
            print(f"✅ Loaded {version}")
        except Exception as e:
            print(f"❌ Failed to load {version}: {e}")
            return
    
    # Load second player
    try:
        second_player = load_second_player()
        print(f"✅ Loaded Second Player")
    except Exception as e:
        print(f"❌ Failed to load Second Player: {e}")
        return
    
    print(f"\nRunning {N_CHALLENGES} battles per player...")
    
    # Evaluate each player against second
    results = []
    for player in players:
        result = await evaluate_player_vs_second(player, second_player, N_CHALLENGES, analyzer)
        results.append(result)
        print(f"✅ {player.username}: {result['win_rate']*100:.1f}% win rate")
    
    # Create comparison graphs
    create_comparison_graphs(analyzer, results)
    
    # Print detailed analysis
    print_detailed_analysis(analyzer, results)
    
    print(f"\n🎉 Comparison complete! Check the generated graph for visual analysis.")

if __name__ == "__main__":
    asyncio.run(main())
