#!/usr/bin/env python3
"""
Integration example showing how to use the Choice Scarf utilities
in your existing htho884.py player code.
"""

# Example of how to integrate the Choice Scarf detection into your existing code

def example_integration():
    """Show how to integrate Choice Scarf detection into your existing choose_move method."""
    
    print("=== INTEGRATION EXAMPLE ===")
    print("\nHere's how to integrate Choice Scarf detection into your htho884.py file:")
    
    print("\n1. Add this import at the top of your file:")
    print("""
    from showdown_agent.scripts.choice_scarf_utils import (
        has_choice_scarf, 
        has_choice_item, 
        is_choice_locked,
        print_choice_item_info
    )
    """)
    
    print("\n2. Replace your current Choice Scarf check:")
    print("""
    # OLD CODE:
    if me.item == 'choicescarf':
        # Your existing Choice Scarf logic
    """)
    
    print("\n3. With this cleaner version:")
    print("""
    # NEW CODE:
    if has_choice_scarf(me):
        print(f"DEBUG: I have Choice Scarf - {me.species} is choice-locked!")
        # Your existing Choice Scarf logic here
        
        # Enhanced logic for choice-locked Pokémon
        if not super_effective_moves and not neutral_moves and resisted_moves:
            # All available moves are resisted (no neutral or super effective)
            best_switch = None
            if hasattr(self, "pick_counter_switch"):
                best_switch = self.pick_counter_switch(battle)
            else:
                try:
                    from showdown_agent.scripts.players.second import pick_counter_switch
                    best_switch = pick_counter_switch(battle)
                except Exception:
                    best_switch = None
            if best_switch:
                print(f"DEBUG: All moves resisted/immune, swapping to {getattr(best_switch, 'species', str(best_switch))}")
                return self.create_order(best_switch)
    """)
    
    print("\n4. Add additional Choice item detection:")
    print("""
    # Check if I'm choice-locked (any Choice item)
    if is_choice_locked(me):
        choice_type = getattr(me, 'item', 'unknown')
        print(f"DEBUG: I'm choice-locked with {choice_type}")
        
        # Add your choice-locked logic here
        # For example, prioritize moves that won't get resisted
    
    # Check opponent's Choice items
    opp = battle.opponent_active_pokemon
    if has_choice_item(opp):
        choice_type = getattr(opp, 'item', 'unknown')
        print(f"DEBUG: Opponent {opp.species} has {choice_type}")
        
        # Add your opponent choice item logic here
        # For example, predict their next move based on their choice lock
    """)
    
    print("\n5. Optional: Add detailed Choice item logging:")
    print("""
    # Add this at the start of your choose_move method for debugging
    if hasattr(self, 'debug_choice_items') and self.debug_choice_items:
        print_choice_item_info(battle, len(battle.turns))
    """)
    
    print("\n6. Complete integration example:")
    print("""
    def choose_move(self, battle: AbstractBattle):
        opp = battle.opponent_active_pokemon
        me = battle.active_pokemon
        
        # Debug Choice items if enabled
        if hasattr(self, 'debug_choice_items') and self.debug_choice_items:
            print_choice_item_info(battle, len(battle.turns))
        
        # Your existing move evaluation logic...
        moves = []
        super_effective_moves = []
        neutral_moves = []
        resisted_moves = []
        
        # ... (your existing move evaluation code)
        
        # Enhanced Choice Scarf logic
        if has_choice_scarf(me):
            print(f"DEBUG: *** CHOICE SCARF DETECTED: {me.species} ***")
            
            # If all moves are resisted, consider switching
            if not super_effective_moves and not neutral_moves and resisted_moves:
                print("DEBUG: All moves resisted with Choice Scarf - considering switch")
                # Your switching logic here
                
        # Check for any Choice item
        if is_choice_locked(me):
            choice_type = getattr(me, 'item', 'unknown')
            print(f"DEBUG: *** CHOICE LOCKED: {me.species} with {choice_type} ***")
            
            # Your choice-locked logic here
            
        # Check opponent's Choice items
        if has_choice_item(opp):
            choice_type = getattr(opp, 'item', 'unknown')
            print(f"DEBUG: *** OPPONENT CHOICE ITEM: {opp.species} with {choice_type} ***")
            
            # Your opponent choice item logic here
        
        # Continue with your existing move selection logic...
    """)
    
    print("\n=== BENEFITS OF THIS INTEGRATION ===")
    print("✓ Cleaner, more readable code")
    print("✓ Robust item detection (handles None values)")
    print("✓ Easy to extend for other Choice items")
    print("✓ Consistent detection across your codebase")
    print("✓ Better debugging and logging")
    print("✓ Reusable utility functions")


if __name__ == "__main__":
    example_integration()
