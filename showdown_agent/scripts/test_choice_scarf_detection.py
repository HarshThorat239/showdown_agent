#!/usr/bin/env python3
"""
Test script to detect if a Pokémon is using a Choice Scarf.
This script demonstrates how to access and check the item of the active Pokémon.
"""

import asyncio
from poke_env.player import Player
from poke_env.battle import AbstractBattle


class ChoiceScarfDetector(Player):
    """A simple player that detects and reports Choice Scarf usage."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choice_scarf_detections = []
    
    def choose_move(self, battle: AbstractBattle):
        """Detect Choice Scarf usage and log it."""
        me = battle.active_pokemon
        opp = battle.opponent_active_pokemon
        
        # Check if our active Pokémon has Choice Scarf
        my_item = getattr(me, 'item', None)
        my_has_scarf = my_item == 'choicescarf' if my_item else False
        
        # Check if opponent's active Pokémon has Choice Scarf
        opp_item = getattr(opp, 'item', None)
        opp_has_scarf = opp_item == 'choicescarf' if opp_item else False
        
        # Log the detection
        detection_info = {
            'turn': len(battle.turns),
            'my_pokemon': me.species,
            'my_item': my_item,
            'my_has_scarf': my_has_scarf,
            'opp_pokemon': opp.species if opp else 'None',
            'opp_item': opp_item,
            'opp_has_scarf': opp_has_scarf,
            'battle_id': getattr(battle, 'battle_tag', 'Unknown')
        }
        
        self.choice_scarf_detections.append(detection_info)
        
        # Print detection results
        print(f"\n=== CHOICE SCARF DETECTION - Turn {detection_info['turn']} ===")
        print(f"My Pokémon: {detection_info['my_pokemon']}")
        print(f"My Item: {detection_info['my_item']}")
        print(f"I have Choice Scarf: {'YES' if detection_info['my_has_scarf'] else 'NO'}")
        print(f"Opponent Pokémon: {detection_info['opp_pokemon']}")
        print(f"Opponent Item: {detection_info['opp_item']}")
        print(f"Opponent has Choice Scarf: {'YES' if detection_info['opp_has_scarf'] else 'NO'}")
        
        # Additional item information
        if my_item:
            print(f"\nMy item details:")
            print(f"  - Item ID: {my_item}")
            print(f"  - Item type: {type(my_item)}")
            print(f"  - Is Choice Scarf: {my_has_scarf}")
            print(f"  - Item comparison: 'choicescarf' == '{my_item}' -> {my_has_scarf}")
        
        if opp_item:
            print(f"\nOpponent item details:")
            print(f"  - Item ID: {opp_item}")
            print(f"  - Item type: {type(opp_item)}")
            print(f"  - Is Choice Scarf: {opp_has_scarf}")
            print(f"  - Item comparison: 'choicescarf' == '{opp_item}' -> {opp_has_scarf}")
        
        # Check for other Choice items
        choice_items = ['choicescarf', 'choiceband', 'choicespecs']
        if my_item in choice_items:
            print(f"\n*** I have a Choice item: {my_item} ***")
        if opp_item in choice_items:
            print(f"\n*** Opponent has a Choice item: {opp_item} ***")
        
        # Make a simple move choice (just use the first available move)
        if battle.available_moves:
            return self.create_order(battle.available_moves[0])
        else:
            # If no moves available, switch to first available Pokémon
            if battle.available_switches:
                return self.create_order(battle.available_switches[0])
            else:
                # Struggle if nothing else available
                return self.create_order("struggle")
    
    def get_summary(self):
        """Get a summary of all Choice Scarf detections."""
        if not self.choice_scarf_detections:
            return "No Choice Scarf detections recorded."
        
        summary = f"\n=== CHOICE SCARF DETECTION SUMMARY ===\n"
        summary += f"Total detections: {len(self.choice_scarf_detections)}\n\n"
        
        for detection in self.choice_scarf_detections:
            summary += f"Turn {detection['turn']}:\n"
            summary += f"  My {detection['my_pokemon']}: {'Choice Scarf' if detection['my_has_scarf'] else detection['my_item'] or 'No item'}\n"
            summary += f"  Opponent {detection['opp_pokemon']}: {'Choice Scarf' if detection['opp_has_scarf'] else detection['opp_item'] or 'No item'}\n\n"
        
        return summary


def test_choice_scarf_detection():
    """Test the Choice Scarf detection functionality."""
    print("Testing Choice Scarf detection...")
    
    # Create a detector instance
    detector = ChoiceScarfDetector()
    
    # Simulate some test scenarios
    print("\n1. Testing item comparison logic:")
    test_items = ['choicescarf', 'choiceband', 'choicespecs', 'lifeorb', 'expertbelt', None]
    
    for item in test_items:
        is_scarf = item == 'choicescarf' if item else False
        print(f"  Item: {item} -> Is Choice Scarf: {is_scarf}")
    
    print("\n2. Testing Choice item detection:")
    choice_items = ['choicescarf', 'choiceband', 'choicespecs']
    for item in test_items:
        if item in choice_items:
            print(f"  {item} is a Choice item")
        else:
            print(f"  {item} is NOT a Choice item")
    
    print("\n3. Testing string comparison edge cases:")
    edge_cases = ['ChoiceScarf', 'CHOICESCARF', 'choice_scarf', 'choice scarf', '']
    for case in edge_cases:
        is_scarf = case == 'choicescarf'
        print(f"  '{case}' == 'choicescarf' -> {is_scarf}")
    
    return detector


if __name__ == "__main__":
    # Run the test
    detector = test_choice_scarf_detection()
    
    print("\n" + "="*50)
    print("Choice Scarf Detection Test Complete!")
    print("="*50)
    print("\nTo use this in a real battle:")
    print("1. Import this class into your main script")
    print("2. Create an instance of ChoiceScarfDetector")
    print("3. Use it in your battle environment")
    print("\nThe detector will automatically log all Choice Scarf detections")
    print("and provide detailed information about items during battles.")
