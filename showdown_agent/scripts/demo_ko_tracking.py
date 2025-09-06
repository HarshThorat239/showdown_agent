#!/usr/bin/env python3
"""
Demo script showing the new KO rating and Pokemon survivability tracking features.
This script demonstrates the enhanced evaluation capabilities.
"""

import os
import sys
from eval import BattleTracker, PokemonStats, display_pokemon_stats, create_pokemon_performance_graph

def demo_battle_tracker():
    """Demonstrate the battle tracking functionality with sample data."""
    print("🎯 DEMONSTRATING KO RATING AND POKEMON SURVIVABILITY TRACKING")
    print("=" * 70)
    
    # Create a tracker
    tracker = BattleTracker()
    
    # Simulate some battle data
    print("📊 Simulating battle data...")
    
    # Add some sample Pokemon statistics
    sample_pokemon = [
        ("Ribombee", 5, 2, 20, 45, 0.0, 0.0, 8, 3),
        ("Eternatus", 8, 1, 25, 60, 0.0, 0.0, 12, 2),
        ("Koraidon", 12, 3, 30, 75, 0.0, 0.0, 15, 5),
        ("Ho-Oh", 6, 4, 22, 50, 0.0, 0.0, 10, 4),
        ("Zacian-Crowned", 15, 2, 28, 80, 0.0, 0.0, 18, 3),
        ("Kyogre", 10, 5, 26, 65, 0.0, 0.0, 14, 6)
    ]
    
    for species, kos_dealt, kos_taken, battles, turns, dmg_dealt, dmg_taken, switches_in, switches_out in sample_pokemon:
        stats = PokemonStats(species)
        stats.kos_dealt = kos_dealt
        stats.kos_taken = kos_taken
        stats.battles_participated = battles
        stats.turns_survived = turns
        stats.total_damage_dealt = dmg_dealt
        stats.total_damage_taken = dmg_taken
        stats.switches_in = switches_in
        stats.switches_out = switches_out
        tracker.pokemon_stats[species] = stats
    
    print("✅ Sample data loaded!")
    print(f"   Total Pokemon tracked: {len(tracker.pokemon_stats)}")
    print(f"   Total battles simulated: {sum(stats.battles_participated for stats in tracker.pokemon_stats.values())}")
    
    # Display the statistics
    display_pokemon_stats(tracker)
    
    # Save to file
    tracker.save_stats_to_file("demo_pokemon_stats.txt")
    
    # Create performance graph
    print("\n📊 Creating performance visualization...")
    create_pokemon_performance_graph(tracker)
    
    print("\n🎉 Demo completed! Check the generated files:")
    print("   - demo_pokemon_stats.txt (detailed statistics)")
    print("   - pokemon_performance.png (visualization)")

def explain_metrics():
    """Explain what each metric means."""
    print("\n📚 METRIC EXPLANATIONS")
    print("=" * 50)
    
    explanations = {
        "KO Rating": "Measures net KO performance: (KOs dealt - KOs taken) / battles participated. Positive values indicate the Pokemon is getting more KOs than it's taking.",
        "Survivability Rating": "Average turns survived per battle. Higher values indicate the Pokemon stays alive longer in battles.",
        "Damage Efficiency": "Ratio of damage dealt to damage taken. Values > 1.0 indicate the Pokemon is dealing more damage than it receives.",
        "KOs Dealt": "Total number of opponent Pokemon this Pokemon has knocked out.",
        "KOs Taken": "Total number of times this Pokemon has been knocked out.",
        "Battles Participated": "Number of battles this Pokemon has been used in.",
        "Turns Survived": "Total number of turns this Pokemon has been active across all battles."
    }
    
    for metric, explanation in explanations.items():
        print(f"• {metric}: {explanation}")
    
    print(f"\n💡 INTERPRETATION TIPS:")
    print(f"   - High KO Rating + High Survivability = Excellent Pokemon")
    print(f"   - High KO Rating + Low Survivability = Glass cannon")
    print(f"   - Low KO Rating + High Survivability = Defensive wall")
    print(f"   - Low KO Rating + Low Survivability = Needs improvement")

if __name__ == "__main__":
    print("🚀 Pokemon Showdown Agent - KO Rating & Survivability Demo")
    print("=" * 60)
    
    # Run the demo
    demo_battle_tracker()
    
    # Explain the metrics
    explain_metrics()
    
    print(f"\n✨ To use this in real battles, run: python eval.py")
    print(f"   The enhanced eval.py now includes all these tracking features!")

