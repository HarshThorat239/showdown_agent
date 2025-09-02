#!/usr/bin/env python3
"""
Test script to demonstrate enhanced defensive calculations.
This script shows how the new system analyzes opponent's specific damaging moves
rather than just their Pokémon types for more precise defensive advantage assessment.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from poke_env.environment.pokemon_type import PokemonType
from showdown_agent.scripts.players.htho884 import CustomAgent

def test_enhanced_defensive_calculations():
    """Test the enhanced defensive calculations with example scenarios."""
    
    # Create an instance of the enhanced agent
    agent = CustomAgent()
    
    print("=== Enhanced Defensive Calculations Test ===\n")
    
    # Test 1: Analyze opponent's damaging moves
    print("Test 1: Analyzing opponent's damaging moves")
    print("-" * 50)
    
    # Simulate a battle scenario (this would normally come from the battle object)
    # For demonstration, we'll create mock data
    
    # Example: Opponent has a Kingambit with known moves
    mock_opponent_moves = {
        'kowtowcleave': {
            'type': PokemonType.DARK,
            'base_power': 85
        },
        'ironhead': {
            'type': PokemonType.STEEL,
            'base_power': 80
        },
        'suckerpunch': {
            'type': PokemonType.DARK,
            'base_power': 70
        },
        'swordsdance': {
            'type': PokemonType.NORMAL,
            'base_power': 0  # Status move
        }
    }
    
    print("Opponent moves analysis:")
    for move_name, move_data in mock_opponent_moves.items():
        if move_data['base_power'] > 0:
            print(f"  - {move_name}: {move_data['type']} type, {move_data['base_power']} BP")
        else:
            print(f"  - {move_name}: Status move")
    
    # Test 2: Calculate defensive risk for different Pokémon
    print("\nTest 2: Defensive risk calculations")
    print("-" * 50)
    
    # Example candidate Pokémon types
    test_candidates = [
        ("Flutter Mane", [PokemonType.GHOST, PokemonType.FAIRY]),
        ("Iron Moth", [PokemonType.FIRE, PokemonType.POISON]),
        ("Koraidon", [PokemonType.FIGHTING, PokemonType.DRAGON]),
        ("Zacian-Crowned", [PokemonType.FAIRY, PokemonType.STEEL])
    ]
    
    opponent_types = [PokemonType.DARK, PokemonType.STEEL]  # Kingambit types
    
    print("Defensive risk analysis vs Kingambit (Dark/Steel):")
    print()
    
    for candidate_name, candidate_types in test_candidates:
        print(f"{candidate_name} ({candidate_types}):")
        
        # Calculate type-based defensive risk (old method)
        type_based_risk = agent.calculate_defensive_risk_vs_types(
            type('MockPokemon', (), {'types': candidate_types})(), 
            opponent_types
        )
        
        # Calculate move-based defensive risk (new method)
        mock_analysis = {
            'damaging_moves': [
                {
                    'name': 'kowtowcleave',
                    'type': PokemonType.DARK,
                    'base_power': 85,
                    'usage_preference': 0.4  # 40% usage
                },
                {
                    'name': 'ironhead',
                    'type': PokemonType.STEEL,
                    'base_power': 80,
                    'usage_preference': 0.3  # 30% usage
                },
                {
                    'name': 'suckerpunch',
                    'type': PokemonType.DARK,
                    'base_power': 70,
                    'usage_preference': 0.2  # 20% usage
                }
            ]
        }
        
        move_based_risk, move_risks = agent.calculate_defensive_risk_vs_moves(
            type('MockPokemon', (), {'types': candidate_types})(),
            mock_analysis,
            type('MockBattle', (), {'opponent_active_pokemon': type('MockOpponent', (), {'types': opponent_types})})()
        )
        
        print(f"  Type-based risk: {type_based_risk:.2f}")
        print(f"  Move-based risk: {move_based_risk:.2f}")
        
        # Show detailed move risks
        print("  Move-specific risks:")
        for move_name, risk_info in move_risks.items():
            if risk_info['effectiveness'] > 1.0:
                print(f"    - {move_name}: {risk_info['effectiveness']:.1f}x effective, risk: {risk_info['risk']:.2f}")
            else:
                print(f"    - {move_name}: {risk_info['effectiveness']:.1f}x effective, risk: {risk_info['risk']:.2f}")
        print()
    
    # Test 3: Show the improvement in decision making
    print("Test 3: Decision making improvement")
    print("-" * 50)
    
    print("Benefits of move-based defensive calculations:")
    print("1. More precise risk assessment based on actual moves")
    print("2. Considers move usage patterns and preferences")
    print("3. Accounts for STAB bonuses on opponent moves")
    print("4. Provides detailed breakdown of vulnerabilities")
    print("5. Better switch-in decisions based on specific threats")
    print()
    
    print("Example scenario:")
    print("- Flutter Mane vs Kingambit")
    print("- Type-based: Only considers Dark/Steel vs Ghost/Fairy")
    print("- Move-based: Considers Kowtow Cleave (Dark) and Iron Head (Steel) specifically")
    print("- Result: More accurate assessment of actual threat level")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_enhanced_defensive_calculations()

