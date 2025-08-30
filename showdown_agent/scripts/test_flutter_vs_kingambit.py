#!/usr/bin/env python3
"""
Test script specifically for Flutter Mane vs Kingambit move selection.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from players.htho884 import CustomAgent
from poke_env.battle.pokemon_type import PokemonType
from poke_env.battle import AbstractBattle
from poke_env.player import Player

def test_flutter_vs_kingambit():
    """
    Test Flutter Mane's move selection against Kingambit.
    """
    print("=== TESTING FLUTTER MANE vs KINGAMBIT (FIXED LOGIC) ===")
    
    # Create an instance of the agent
    agent = CustomAgent()
    
    # Mock battle setup
    class MockBattle:
        def __init__(self):
            self.weather = None
            self.terrain = None
            self.opponent_active_pokemon = MockPokemon(["dark", "steel"])  # Kingambit
            self.active_pokemon = MockPokemon(["ghost", "fairy"])  # Flutter Mane
            self.available_moves = []
            self.available_switches = []
            self.team = []
            self.side_conditions = {}
    
    class MockMove:
        def __init__(self, name, move_type, base_power=80):
            self.name = name
            self.type = move_type
            self.base_power = base_power
            self.pp = 16
            self.disabled = False
    
    class MockPokemon:
        def __init__(self, types, species="unknown"):
            self.types = [getattr(PokemonType, t.upper()) for t in types]
            self.ability = None
            self.species = species
            self.current_hp_fraction = 1.0
            self.base_stats = {'spe': 135}  # Flutter Mane speed
    
    # Create mock battle
    battle = MockBattle()
    battle.opponent_active_pokemon.species = "kingambit"
    battle.active_pokemon.species = "fluttermane"
    
    # Test with Kingambit at different HP levels
    test_hp_levels = [1.0, 0.8, 0.6, 0.4, 0.2]
    
    for hp_level in test_hp_levels:
        print(f"\n=== TESTING WITH KINGAMBIT AT {hp_level:.1%} HP ===")
        
        # Set Kingambit's HP
        battle.opponent_active_pokemon.current_hp_fraction = hp_level
        battle.opponent_active_pokemon.base_stats = {'spe': 50}  # Kingambit is slower than Flutter Mane
        
        # Create Flutter Mane's moves
        moonblast = MockMove("moonblast", PokemonType.FAIRY, 95)
        shadow_ball = MockMove("shadowball", PokemonType.GHOST, 80)
        mystical_fire = MockMove("mysticalfire", PokemonType.FIRE, 75)
        power_gem = MockMove("powergem", PokemonType.ROCK, 80)
        
        battle.available_moves = [moonblast, shadow_ball, mystical_fire, power_gem]
        
        # Simulate the move selection process
        opp = battle.opponent_active_pokemon
        me = battle.active_pokemon
        opp_types = opp.types
        my_types = me.types
        opp_hp = opp.current_hp_fraction or 1.0
        
        moves = []
        super_effective_moves = []
        neutral_moves = []
        resisted_moves = []
        
        for mv in battle.available_moves:
            move_type = getattr(mv, 'type', None)
            if move_type is None:
                move_type = getattr(mv, 'type_id', None)
            if move_type is None:
                continue
                
            move_name = getattr(mv, 'name', getattr(mv, 'display_name', 'Unknown'))
            
            raw_mult = agent.type_multiplier(move_type, opp_types)
            if raw_mult == 0.0:
                continue
            
            # Check for ability-based immunities
            opp_ability = getattr(opp, 'ability', None)
            if agent.is_move_immune(move_type, opp_ability):
                continue
                
            dmg = agent.estimate_damage_frac(mv, my_types, opp_types)
            moves.append((mv, dmg, raw_mult))
            
            # Categorize moves by effectiveness
            if raw_mult > 1.0:
                super_effective_moves.append((mv, dmg, raw_mult))
            elif abs(raw_mult - 1.0) < 1e-9:
                neutral_moves.append((mv, dmg, raw_mult))
            else:
                resisted_moves.append((mv, dmg, raw_mult))
        
        print(f"Kingambit HP: {opp_hp:.3f}")
        print(f"Speed comparison: {me.base_stats.get('spe', 0)} vs {opp.base_stats.get('spe', 0)}")
        
        # Test the FIXED guaranteed KO logic
        if super_effective_moves and me.base_stats['spe'] > opp.base_stats['spe']:
            print(f"*** CHECKING FOR GUARANTEED KO (FIXED LOGIC) ***")
            
            # First, check if any super effective moves can KO
            print("Checking super effective moves first:")
            for m, dmg, mult in sorted(super_effective_moves, key=lambda x: (x[2], x[1]), reverse=True):
                move_name = getattr(m, 'name', getattr(m, 'display_name', 'Unknown'))
                ko_threshold = opp_hp + 0.1
                print(f"  {move_name}: damage={dmg:.3f}, effectiveness={mult}, KO threshold={ko_threshold:.3f}")
                if dmg >= ko_threshold:
                    print(f"  *** SELECTED SUPER EFFECTIVE KO MOVE: {move_name} ***")
                    break
            else:
                # If no super effective moves can KO, then check neutral moves
                print("No super effective moves can KO, checking neutral moves:")
                for m, dmg, mult in sorted(moves, key=lambda x: x[1], reverse=True):
                    move_name = getattr(m, 'name', getattr(m, 'display_name', 'Unknown'))
                    ko_threshold = opp_hp + 0.1
                    print(f"  {move_name}: damage={dmg:.3f}, effectiveness={mult}, KO threshold={ko_threshold:.3f}")
                    if dmg >= ko_threshold and mult >= 1.0:
                        print(f"  *** SELECTED NEUTRAL KO MOVE: {move_name} ***")
                        break
        else:
            print("Guaranteed KO check not triggered")
        
        # Test super effective move selection
        if super_effective_moves:
            best_se_move = max(super_effective_moves, key=lambda x: (x[2], x[1]))
            move_name = getattr(best_se_move[0], 'name', getattr(best_se_move[0], 'display_name', 'Unknown'))
            print(f"Best super effective move: {move_name} (damage: {best_se_move[1]:.3f}, effectiveness: {best_se_move[2]})")
        else:
            print("No super effective moves found!")

if __name__ == "__main__":
    test_flutter_vs_kingambit()
