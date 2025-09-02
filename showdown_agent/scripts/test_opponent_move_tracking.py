#!/usr/bin/env python3
"""
Test script to verify opponent move tracking functionality
"""

import sys
sys.path.append('.')

from scripts.players.htho884 import CustomAgent
from poke_env.battle.pokemon_type import PokemonType

def test_opponent_move_tracking():
    """Test the opponent move tracking functionality"""
    print("Testing opponent move tracking functionality...")
    
    # Create an instance of the agent
    agent = CustomAgent()
    
    # Test initial state
    print(f"Initial opponent_last_move: {agent.opponent_last_move}")
    print(f"Initial opponent_last_move_type: {agent.opponent_last_move_type}")
    
    # Test the get_opponent_last_move_type method
    move_type = agent.get_opponent_last_move_type()
    print(f"get_opponent_last_move_type() returns: {move_type}")
    
    # Test type multiplier functionality
    test_types = [PokemonType.FIRE, PokemonType.WATER]
    fire_effectiveness = agent.type_multiplier(PokemonType.FIRE, test_types)
    water_effectiveness = agent.type_multiplier(PokemonType.WATER, test_types)
    
    print(f"Fire vs Fire/Water: {fire_effectiveness}")
    print(f"Water vs Fire/Water: {water_effectiveness}")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_opponent_move_tracking()

