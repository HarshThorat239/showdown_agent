#!/usr/bin/env python3
"""
Test that Eternatus uses Recover when below 40% HP and Recover is available.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from players.htho884 import CustomAgent
from poke_env.battle.pokemon_type import PokemonType


def test_eternatus_recover_usage():
    class TestAgent(CustomAgent):
        def create_order(self, order):
            return order

    class MockMove:
        def __init__(self, name, move_type=None, base_power=0):
            self.name = name
            self.type = move_type
            self.base_power = base_power

    class MockPokemon:
        def __init__(self, species, types):
            self.species = species
            self.types = [getattr(PokemonType, t.upper()) for t in types]
            self.current_hp_fraction = 0.35
            self.base_stats = {'spe': 130}
            self.ability = None

    class MockOpponentPokemon:
        def __init__(self, species, types):
            self.species = species
            self.types = [getattr(PokemonType, t.upper()) for t in types]
            self.current_hp_fraction = 1.0
            self.base_stats = {'spe': 90}
            self.ability = None

    class MockBattle:
        def __init__(self):
            self.active_pokemon = MockPokemon('Eternatus', ['poison', 'dragon'])
            self.opponent_active_pokemon = MockOpponentPokemon('zacian', ['fairy', 'steel'])
            self.available_moves = []
            self.available_switches = []
            self.team = []
            self.side_conditions = {}
            self.opponent_side_conditions = {}
            self.weather = None

    agent = TestAgent()
    battle = MockBattle()

    # Include Recover among other moves; order should not matter
    recover = MockMove('Recover')
    dynacannon = MockMove('Dynamax Cannon', PokemonType.DRAGON, 100)
    sludge_bomb = MockMove('Sludge Bomb', PokemonType.POISON, 90)
    fire_blast = MockMove('Fire Blast', PokemonType.FIRE, 110)
    battle.available_moves = [dynacannon, sludge_bomb, recover, fire_blast]

    chosen = agent.choose_move(battle)
    assert getattr(chosen, 'name', '').lower() == 'recover', 'Agent did not choose Recover when below 40% HP'
    print('PASS: Eternatus chose Recover when below 40% HP and Recover was available')


if __name__ == '__main__':
    test_eternatus_recover_usage()

