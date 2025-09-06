# tournament.py
# Tournament script for V1, V2, V3, and htho884.py players - Round Robin Competition

import asyncio
import importlib.util
import os
import sys
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import poke_env as pke
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.player.player import Player
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

N_CHALLENGES = 50  # battles per matchup (reduced for faster tournament)

@dataclass
class PlayerStats:
    """Track individual player statistics in the tournament."""
    name: str
    wins: int = 0
    losses: int = 0
    draws: int = 0
    total_battles: int = 0
    win_rate: float = 0.0
    
    @property
    def points(self) -> int:
        """Calculate tournament points (3 for win, 1 for draw, 0 for loss)."""
        return self.wins * 3 + self.draws * 1
    
    @property
    def win_percentage(self) -> float:
        """Calculate win percentage."""
        if self.total_battles == 0:
            return 0.0
        return (self.wins / self.total_battles) * 100

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
    account_config = AccountConfiguration(f"{player_name}_tournament", None)
    player = agent_class(
        account_configuration=account_config,
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen9ubers",
    )

    # Save replays
    replay_dir = os.path.join(base_dir, "replays", f"tournament_{player_name}")
    os.makedirs(replay_dir, exist_ok=True)
    player._save_replays = replay_dir
    
    return player

async def evaluate_matchup(player1: Player, player2: Player, n_challenges: int) -> Tuple[float, float]:
    """Evaluate a matchup between two players and return their win rates."""
    print(f"🎮 {player1.username} vs {player2.username} ({n_challenges} battles each)...")
    
    res = await pke.cross_evaluate([player1, player2], n_challenges=n_challenges)

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

    player1_key = _resolve_key(res, player1)
    player2_key = _resolve_key(res[player1_key], player2)
    
    player1_wr = res[player1_key][player2_key]
    player2_wr = res[player2_key][player1_key]
    
    print(f"  => {player1.username}: {player1_wr * 100:.1f}% | {player2.username}: {player2_wr * 100:.1f}%")
    return player1_wr, player2_wr

async def run_round_robin_tournament(player_names: List[str], n_challenges: int) -> Dict[str, PlayerStats]:
    """Run a round-robin tournament between all players."""
    print("🏆 Starting Round-Robin Tournament")
    print("="*60)
    
    # Load all players
    players = {}
    for name in player_names:
        try:
            players[name] = load_player(name)
        except Exception as e:
            print(f"❌ Error loading {name}: {e}")
            return {}
    
    # Initialize player statistics
    player_stats = {name: PlayerStats(name) for name in player_names}
    
    # Run round-robin matches
    total_matches = len(player_names) * (len(player_names) - 1) // 2
    current_match = 0
    
    for i, player1_name in enumerate(player_names):
        for j, player2_name in enumerate(player_names):
            if i < j:  # Avoid duplicate matches and self-matches
                current_match += 1
                print(f"\n📊 Match {current_match}/{total_matches}")
                
                player1 = players[player1_name]
                player2 = players[player2_name]
                
                # Run the matchup
                wr1, wr2 = await evaluate_matchup(player1, player2, n_challenges)
                
                # Update statistics
                stats1 = player_stats[player1_name]
                stats2 = player_stats[player2_name]
                
                # Calculate wins/losses/draws for this matchup
                battles_per_player = n_challenges
                wins1 = int(wr1 * battles_per_player)
                wins2 = int(wr2 * battles_per_player)
                draws = battles_per_player - wins1 - wins2
                
                # Update player1 stats
                stats1.wins += wins1
                stats1.losses += wins2
                stats1.draws += draws
                stats1.total_battles += battles_per_player
                
                # Update player2 stats
                stats2.wins += wins2
                stats2.losses += wins1
                stats2.draws += draws
                stats2.total_battles += battles_per_player
    
    # Calculate final win rates
    for stats in player_stats.values():
        stats.win_rate = stats.win_percentage
    
    return player_stats

def calculate_rankings(player_stats: Dict[str, PlayerStats]) -> List[Tuple[str, PlayerStats]]:
    """Calculate tournament rankings based on points, then win rate."""
    # Sort by points (descending), then by win rate (descending)
    rankings = sorted(
        player_stats.items(),
        key=lambda x: (x[1].points, x[1].win_rate),
        reverse=True
    )
    return rankings

def print_tournament_results(player_stats: Dict[str, PlayerStats], rankings: List[Tuple[str, PlayerStats]]):
    """Print detailed tournament results."""
    print("\n" + "="*80)
    print("🏆 TOURNAMENT RESULTS - FINAL STANDINGS")
    print("="*80)
    
    # Create results table
    headers = ["Rank", "Player", "Points", "Wins", "Losses", "Draws", "Win Rate", "Total Battles"]
    table_data = []
    
    for rank, (player_name, stats) in enumerate(rankings, 1):
        table_data.append([
            rank,
            player_name,
            stats.points,
            stats.wins,
            stats.losses,
            stats.draws,
            f"{stats.win_rate:.1f}%",
            stats.total_battles
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Print winner announcement
    winner_name, winner_stats = rankings[0]
    print(f"\n🥇 TOURNAMENT CHAMPION: {winner_name}")
    print(f"   Points: {winner_stats.points}")
    print(f"   Win Rate: {winner_stats.win_rate:.1f}%")
    print(f"   Record: {winner_stats.wins}-{winner_stats.losses}-{winner_stats.draws}")
    
    # Print podium
    if len(rankings) >= 3:
        print(f"\n🏆 PODIUM:")
        print(f"   🥇 1st: {rankings[0][0]} ({rankings[0][1].points} pts)")
        print(f"   🥈 2nd: {rankings[1][0]} ({rankings[1][1].points} pts)")
        print(f"   🥉 3rd: {rankings[2][0]} ({rankings[2][1].points} pts)")

def create_tournament_graph(player_stats: Dict[str, PlayerStats], rankings: List[Tuple[str, PlayerStats]]):
    """Create visualizations for tournament results."""
    if not player_stats:
        print("No tournament data to display.")
        return
    
    # Extract data for plotting
    player_names = [name for name, _ in rankings]
    win_rates = [stats.win_rate for _, stats in rankings]
    points = [stats.points for _, stats in rankings]
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Win Rate bar chart
    colors_wr = ['#FFD700' if i == 0 else '#C0C0C0' if i == 1 else '#CD7F32' if i == 2 else '#2E8B57' for i in range(len(win_rates))]
    bars1 = ax1.bar(player_names, win_rates, color=colors_wr, alpha=0.8)
    ax1.set_title('Tournament Win Rates', fontsize=14, fontweight='bold', pad=20)
    ax1.set_ylabel('Win Rate (%)', fontsize=12)
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, wr in zip(bars1, win_rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{wr:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Points bar chart
    colors_pts = ['#FFD700' if i == 0 else '#C0C0C0' if i == 1 else '#CD7F32' if i == 2 else '#4169E1' for i in range(len(points))]
    bars2 = ax2.bar(player_names, points, color=colors_pts, alpha=0.8)
    ax2.set_title('Tournament Points', fontsize=14, fontweight='bold', pad=20)
    ax2.set_ylabel('Points', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, pts in zip(bars2, points):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{pts}', ha='center', va='bottom', fontweight='bold')
    
    # Rotate x-axis labels for better readability
    for ax in [ax1, ax2]:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save the graph
    base_dir = os.path.dirname(__file__)
    graph_path = os.path.join(base_dir, "tournament_results.png")
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')
    print(f"\n📊 Tournament results graph saved to: {graph_path}")
    
    plt.show()

def print_matchup_summary(player_stats: Dict[str, PlayerStats]):
    """Print a summary of all matchups."""
    print("\n" + "="*60)
    print("📊 MATCHUP SUMMARY")
    print("="*60)
    
    player_names = list(player_stats.keys())
    print(f"{'Player':<12}", end="")
    for name in player_names:
        print(f"{name:>8}", end="")
    print()
    print("-" * (12 + 8 * len(player_names)))
    
    for player1 in player_names:
        print(f"{player1:<12}", end="")
        for player2 in player_names:
            if player1 == player2:
                print(f"{'--':>8}", end="")
            else:
                # This is a simplified view - in a real implementation you'd track individual matchup results
                print(f"{'vs':>8}", end="")
        print()

async def main():
    """Main tournament function."""
    print("🏆 POKEMON SHOWDOWN TOURNAMENT")
    print("Competitors: V1, V2, V3, htho884")
    print(f"Format: Round-Robin | Battles per matchup: {N_CHALLENGES}")
    print("="*60)
    
    # Players to compete
    player_names = ["V1", "V2", "V3", "htho884"]
    
    # Check if all player files exist
    missing_players = []
    for player_name in player_names:
        base_dir = os.path.dirname(__file__)
        player_path = os.path.join(base_dir, "players", f"{player_name}.py")
        if not os.path.exists(player_path):
            missing_players.append(player_name)
    
    if missing_players:
        print(f"❌ Missing player files: {missing_players}")
        print("Available players:")
        players_dir = os.path.join(base_dir, "players")
        if os.path.exists(players_dir):
            for file in os.listdir(players_dir):
                if file.endswith(".py") and file != "__init__.py":
                    print(f"  - {file[:-3]}")
        return
    
    # Run tournament
    print("🎮 Starting tournament...")
    player_stats = await run_round_robin_tournament(player_names, N_CHALLENGES)
    
    if not player_stats:
        print("❌ Tournament failed to complete.")
        return
    
    # Calculate rankings
    rankings = calculate_rankings(player_stats)
    
    # Display results
    print_tournament_results(player_stats, rankings)
    
    # Create tournament graph
    print("\n📊 Generating tournament visualization...")
    create_tournament_graph(player_stats, rankings)
    
    # Print matchup summary
    print_matchup_summary(player_stats)
    
    print("\n✅ Tournament complete!")
    print(f"🏆 Champion: {rankings[0][0]}")

if __name__ == "__main__":
    asyncio.run(main())
