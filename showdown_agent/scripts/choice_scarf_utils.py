#!/usr/bin/env python3
"""
Utility functions for detecting Choice items in Pokémon battles.
These functions can be easily imported and used in existing player scripts.
"""

from typing import Optional, Union, Any
from poke_env.battle import AbstractBattle


def has_choice_scarf(pokemon: Any) -> bool:
    """
    Check if a Pokémon has a Choice Scarf.
    
    Args:
        pokemon: The Pokémon object to check
        
    Returns:
        bool: True if the Pokémon has Choice Scarf, False otherwise
    """
    item = getattr(pokemon, 'item', None)
    return item == 'choicescarf' if item else False


def has_choice_item(pokemon: Any) -> bool:
    """
    Check if a Pokémon has any Choice item (Scarf, Band, or Specs).
    
    Args:
        pokemon: The Pokémon object to check
        
    Returns:
        bool: True if the Pokémon has any Choice item, False otherwise
    """
    item = getattr(pokemon, 'item', None)
    if not item:
        return False
    
    choice_items = ['choicescarf', 'choiceband', 'choicespecs']
    return item in choice_items


def get_choice_item_type(pokemon: Any) -> Optional[str]:
    """
    Get the type of Choice item a Pokémon has, if any.
    
    Args:
        pokemon: The Pokémon object to check
        
    Returns:
        Optional[str]: The type of Choice item ('choicescarf', 'choiceband', 'choicespecs') 
                     or None if no Choice item
    """
    item = getattr(pokemon, 'item', None)
    if not item:
        return None
    
    choice_items = ['choicescarf', 'choiceband', 'choicespecs']
    return item if item in choice_items else None


def is_choice_locked(pokemon: Any) -> bool:
    """
    Check if a Pokémon is choice-locked (has a Choice item).
    This is an alias for has_choice_item() for clarity.
    
    Args:
        pokemon: The Pokémon object to check
        
    Returns:
        bool: True if the Pokémon is choice-locked, False otherwise
    """
    return has_choice_item(pokemon)


def check_battle_choice_items(battle: AbstractBattle) -> dict:
    """
    Check Choice items for both active Pokémon in a battle.
    
    Args:
        battle: The battle object to check
        
    Returns:
        dict: Dictionary containing Choice item information for both Pokémon
    """
    me = battle.active_pokemon
    opp = battle.opponent_active_pokemon
    
    result = {
        'my_pokemon': {
            'species': me.species,
            'item': getattr(me, 'item', None),
            'has_choice_scarf': has_choice_scarf(me),
            'has_choice_item': has_choice_item(me),
            'choice_item_type': get_choice_item_type(me)
        },
        'opponent_pokemon': {
            'species': opp.species if opp else None,
            'item': getattr(opp, 'item', None) if opp else None,
            'has_choice_scarf': has_choice_scarf(opp) if opp else False,
            'has_choice_item': has_choice_item(opp) if opp else False,
            'choice_item_type': get_choice_item_type(opp) if opp else None
        }
    }
    
    return result


def print_choice_item_info(battle: AbstractBattle, turn: int = None) -> None:
    """
    Print detailed information about Choice items in the current battle state.
    
    Args:
        battle: The battle object to check
        turn: Optional turn number to display
    """
    info = check_battle_choice_items(battle)
    
    turn_str = f"Turn {turn}" if turn is not None else "Current"
    print(f"\n=== CHOICE ITEM INFO - {turn_str} ===")
    
    # My Pokémon info
    my_info = info['my_pokemon']
    print(f"My Pokémon: {my_info['species']}")
    print(f"  Item: {my_info['item'] or 'No item'}")
    print(f"  Choice Scarf: {'YES' if my_info['has_choice_scarf'] else 'NO'}")
    print(f"  Choice Item: {'YES' if my_info['has_choice_item'] else 'NO'}")
    if my_info['choice_item_type']:
        print(f"  Choice Type: {my_info['choice_item_type']}")
    
    # Opponent Pokémon info
    opp_info = info['opponent_pokemon']
    if opp_info['species']:
        print(f"\nOpponent Pokémon: {opp_info['species']}")
        print(f"  Item: {opp_info['item'] or 'No item'}")
        print(f"  Choice Scarf: {'YES' if opp_info['has_choice_scarf'] else 'NO'}")
        print(f"  Choice Item: {'YES' if opp_info['has_choice_item'] else 'NO'}")
        if opp_info['choice_item_type']:
            print(f"  Choice Type: {opp_info['choice_item_type']}")
    else:
        print(f"\nOpponent Pokémon: None")


# Example usage functions
def example_usage():
    """Show examples of how to use these utility functions."""
    print("=== CHOICE SCARF UTILITY FUNCTIONS ===")
    print("\nAvailable functions:")
    print("1. has_choice_scarf(pokemon) - Check if Pokémon has Choice Scarf")
    print("2. has_choice_item(pokemon) - Check if Pokémon has any Choice item")
    print("3. get_choice_item_type(pokemon) - Get the type of Choice item")
    print("4. is_choice_locked(pokemon) - Check if Pokémon is choice-locked")
    print("5. check_battle_choice_items(battle) - Get Choice item info for both Pokémon")
    print("6. print_choice_item_info(battle, turn) - Print detailed Choice item info")
    
    print("\nExample integration in your choose_move method:")
    print("""
    def choose_move(self, battle: AbstractBattle):
        me = battle.active_pokemon
        
        # Check if I have Choice Scarf
        if has_choice_scarf(me):
            print("I have Choice Scarf!")
            # Your Choice Scarf logic here
        
        # Check if I'm choice-locked
        if is_choice_locked(me):
            print("I'm choice-locked!")
            # Your choice-locked logic here
        
        # Get opponent's Choice item info
        opp = battle.opponent_active_pokemon
        if has_choice_item(opp):
            choice_type = get_choice_item_type(opp)
            print(f"Opponent has {choice_type}!")
        
        # Or use the comprehensive check
        choice_info = check_battle_choice_items(battle)
        if choice_info['my_pokemon']['has_choice_scarf']:
            print("I have Choice Scarf!")
    """)


if __name__ == "__main__":
    example_usage()
