#!/usr/bin/env python3
"""
Test script for the find_effective_moves function.
This demonstrates how to use the new effective moves analysis functionality.
"""

from showdown_agent.scripts.players.htho884 import CustomAgent
from poke_env.battle.pokemon_type import PokemonType
from poke_env.battle import AbstractBattle
from poke_env.player import Player

def test_effective_moves():
    """
    Test the find_effective_moves function with various scenarios.
    """
    # Create an instance of the agent
    agent = CustomAgent()
    
    # Example 1: Fire move in Sunny Day weather
    print("=== EXAMPLE 1: Fire move in Sunny Day ===")
    
    # Mock battle with Sunny Day weather
    class MockBattle:
        def __init__(self):
            self.weather = {'name': 'sun'}  # Weather is a dict with 'name' key
            self.terrain = None
            self.opponent_active_pokemon = MockPokemon(["grass", "poison"])
    
    class MockMove:
        def __init__(self, name, move_type, base_power=80):
            self.name = name
            self.type = move_type
            self.base_power = base_power
    
    class MockPokemon:
        def __init__(self, types):
            self.types = [getattr(PokemonType, t.upper()) for t in types]
            self.ability = None
    
    # Create mock battle and moves
    battle = MockBattle()
    fire_move = MockMove("Flamethrower", PokemonType.FIRE, 90)
    water_move = MockMove("Surf", PokemonType.WATER, 90)
    grass_move = MockMove("Energy Ball", PokemonType.GRASS, 90)
    
    moves = [fire_move, water_move, grass_move]
    opp_types = [PokemonType.GRASS, PokemonType.POISON]  # Victreebel-like
    my_types = [PokemonType.FIRE]  # Charizard-like
    
    # Test the function
    effective_moves = agent.find_effective_moves(battle, moves, opp_types, my_types)
    
    # Print results
    agent.print_effective_moves_debug(effective_moves)
    
    # Get best move
    best_move = agent.get_best_effective_move(effective_moves)
    if best_move:
        move, damage, effectiveness, boost = best_move
        print(f"\nBEST MOVE: {move.name}")
        print(f"Damage: {damage:.3f}")
        print(f"Effectiveness: {effectiveness:.2f}x")
        print(f"Boosts: {boost}")
    
    print("\n" + "="*50)
    
    # Example 2: Electric move in Electric Terrain
    print("=== EXAMPLE 2: Electric move in Electric Terrain ===")
    
    battle.weather = None
    battle.terrain = {'name': 'electric'}  # Terrain is a dict with 'name' key
    battle.opponent_active_pokemon = MockPokemon(["water", "flying"])  # Gyarados-like
    
    electric_move = MockMove("Thunderbolt", PokemonType.ELECTRIC, 90)
    normal_move = MockMove("Hyper Beam", PokemonType.NORMAL, 150)
    
    moves = [electric_move, normal_move]
    opp_types = [PokemonType.WATER, PokemonType.FLYING]
    my_types = [PokemonType.ELECTRIC]  # Jolteon-like
    
    effective_moves = agent.find_effective_moves(battle, moves, opp_types, my_types)
    agent.print_effective_moves_debug(effective_moves)
    
    best_move = agent.get_best_effective_move(effective_moves)
    if best_move:
        move, damage, effectiveness, boost = best_move
        print(f"\nBEST MOVE: {move.name}")
        print(f"Damage: {damage:.3f}")
        print(f"Effectiveness: {effectiveness:.2f}x")
        print(f"Boosts: {boost}")
    
    print("\n" + "="*50)
    
    # Example 3: Water move in Rain
    print("=== EXAMPLE 3: Water move in Rain ===")
    
    battle.weather = {'name': 'rain'}  # Weather is a dict with 'name' key
    battle.terrain = None
    battle.opponent_active_pokemon = MockPokemon(["fire"])  # Arcanine-like
    
    water_move = MockMove("Hydro Pump", PokemonType.WATER, 110)
    fire_move = MockMove("Fire Blast", PokemonType.FIRE, 110)
    
    moves = [water_move, fire_move]
    opp_types = [PokemonType.FIRE]
    my_types = [PokemonType.WATER]  # Blastoise-like
    
    effective_moves = agent.find_effective_moves(battle, moves, opp_types, my_types)
    agent.print_effective_moves_debug(effective_moves)
    
    best_move = agent.get_best_effective_move(effective_moves)
    if best_move:
        move, damage, effectiveness, boost = best_move
        print(f"\nBEST MOVE: {move.name}")
        print(f"Damage: {damage:.3f}")
        print(f"Effectiveness: {effectiveness:.2f}x")
        print(f"Boosts: {boost}")

def test_immunity_scenarios():
    """
    Test immunity scenarios (like Ground moves vs Levitate).
    """
    print("\n" + "="*50)
    print("=== EXAMPLE 4: Immunity Scenarios ===")
    
    agent = CustomAgent()
    
    class MockBattle:
        def __init__(self):
            self.weather = None
            self.terrain = None
            self.opponent_active_pokemon = MockPokemon(["ghost", "flying"], "levitate")
    
    class MockMove:
        def __init__(self, name, move_type, base_power=80):
            self.name = name
            self.type = move_type
            self.base_power = base_power
    
    class MockPokemon:
        def __init__(self, types, ability=None):
            self.types = [getattr(PokemonType, t.upper()) for t in types]
            self.ability = ability
    
    battle = MockBattle()
    ground_move = MockMove("Earthquake", PokemonType.GROUND, 100)
    normal_move = MockMove("Hyper Beam", PokemonType.NORMAL, 150)
    
    moves = [ground_move, normal_move]
    opp_types = [PokemonType.GHOST, PokemonType.FLYING]  # Gengar-like with Levitate
    my_types = [PokemonType.GROUND]  # Garchomp-like
    
    effective_moves = agent.find_effective_moves(battle, moves, opp_types, my_types)
    agent.print_effective_moves_debug(effective_moves)
    
    best_move = agent.get_best_effective_move(effective_moves)
    if best_move:
        move, damage, effectiveness, boost = best_move
        print(f"\nBEST MOVE: {move.name}")
        print(f"Damage: {damage:.3f}")
        print(f"Effectiveness: {effectiveness:.2f}x")
        print(f"Boosts: {boost}")

if __name__ == "__main__":
    test_effective_moves()
    test_immunity_scenarios()
    print("\n=== TESTING COMPLETE ===")
