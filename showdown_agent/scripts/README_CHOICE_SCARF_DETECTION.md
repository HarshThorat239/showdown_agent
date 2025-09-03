# Choice Scarf Detection System

This system provides robust detection and handling of Choice items (Choice Scarf, Choice Band, Choice Specs) in Pokémon battles.

## Files Created

### 1. `test_choice_scarf_detection.py`
A complete test script that creates a `ChoiceScarfDetector` player class. This class:
- Detects Choice Scarf usage for both your Pokémon and your opponent's
- Logs all detections throughout the battle
- Prints detailed information about items
- Provides a summary of all detections

### 2. `choice_scarf_utils.py`
A utility module with simple, reusable functions that can be imported into existing player scripts:
- `has_choice_scarf(pokemon)` - Check if a Pokémon has Choice Scarf
- `has_choice_item(pokemon)` - Check if a Pokémon has any Choice item
- `get_choice_item_type(pokemon)` - Get the specific type of Choice item
- `is_choice_locked(pokemon)` - Check if a Pokémon is choice-locked
- `check_battle_choice_items(battle)` - Get Choice item info for both Pokémon
- `print_choice_item_info(battle, turn)` - Print detailed Choice item information

### 3. `integration_example.py`
Shows how to integrate the Choice Scarf detection into your existing `htho884.py` player code.

## Quick Start

### Test the Detection System
```bash
cd showdown_agent/scripts
python test_choice_scarf_detection.py
python choice_scarf_utils.py
python integration_example.py
```

### Integrate into Your Existing Code

1. **Add the import** at the top of your `htho884.py` file:
```python
from showdown_agent.scripts.choice_scarf_utils import (
    has_choice_scarf, 
    has_choice_item, 
    is_choice_locked,
    print_choice_item_info
)
```

2. **Replace your current Choice Scarf check**:
```python
# OLD CODE:
if me.item == 'choicescarf':
    # Your existing Choice Scarf logic

# NEW CODE:
if has_choice_scarf(me):
    print(f"DEBUG: I have Choice Scarf - {me.species} is choice-locked!")
    # Your existing Choice Scarf logic here
```

3. **Add enhanced Choice item detection**:
```python
# Check if I'm choice-locked (any Choice item)
if is_choice_locked(me):
    choice_type = getattr(me, 'item', 'unknown')
    print(f"DEBUG: I'm choice-locked with {choice_type}")
    
# Check opponent's Choice items
opp = battle.opponent_active_pokemon
if has_choice_item(opp):
    choice_type = getattr(opp, 'item', 'unknown')
    print(f"DEBUG: Opponent {opp.species} has {choice_type}")
```

## Key Features

### Robust Detection
- Handles cases where items might be `None` or missing
- Uses `getattr()` for safe attribute access
- Consistent string comparison (`'choicescarf'`)

### Comprehensive Logging
- Tracks all Choice item detections throughout battles
- Shows exactly what items are detected and how
- Provides turn-by-turn information

### Easy Integration
- Simple functions you can drop into existing code
- No changes to your existing battle logic required
- Clean, readable function names

### Extensible Design
- Detects all Choice items (Scarf, Band, Specs), not just Scarf
- Easy to add new item types
- Consistent API across all functions

## Function Reference

### `has_choice_scarf(pokemon)`
Returns `True` if the Pokémon has a Choice Scarf, `False` otherwise.

### `has_choice_item(pokemon)`
Returns `True` if the Pokémon has any Choice item (Scarf, Band, or Specs), `False` otherwise.

### `get_choice_item_type(pokemon)`
Returns the type of Choice item (`'choicescarf'`, `'choiceband'`, `'choicespecs'`) or `None` if no Choice item.

### `is_choice_locked(pokemon)`
Returns `True` if the Pokémon is choice-locked (has any Choice item), `False` otherwise.

### `check_battle_choice_items(battle)`
Returns a dictionary with Choice item information for both active Pokémon in the battle.

### `print_choice_item_info(battle, turn)`
Prints detailed information about Choice items in the current battle state.

## Example Usage in Battle

```python
def choose_move(self, battle: AbstractBattle):
    me = battle.active_pokemon
    opp = battle.opponent_active_pokemon
    
    # Check if I have Choice Scarf
    if has_choice_scarf(me):
        print("I have Choice Scarf!")
        # Your Choice Scarf logic here
    
    # Check if I'm choice-locked
    if is_choice_locked(me):
        print("I'm choice-locked!")
        # Your choice-locked logic here
    
    # Get opponent's Choice item info
    if has_choice_item(opp):
        choice_type = get_choice_item_type(opp)
        print(f"Opponent has {choice_type}!")
    
    # Or use the comprehensive check
    choice_info = check_battle_choice_items(battle)
    if choice_info['my_pokemon']['has_choice_scarf']:
        print("I have Choice Scarf!")
```

## Benefits

- **Cleaner Code**: Replace complex item checks with simple function calls
- **Robust Detection**: Handles edge cases and missing attributes gracefully
- **Better Debugging**: Comprehensive logging of Choice item usage
- **Consistent Logic**: Same detection logic across your entire codebase
- **Easy Maintenance**: Update Choice item logic in one place
- **Extensible**: Easy to add support for new items or conditions

## Testing

All scripts include comprehensive testing and examples. Run them to see:
- How the detection logic works
- What information is logged
- How to integrate the functions
- Edge cases and error handling

## Support

The system is designed to work with the existing `poke_env` library and your current battle environment. All functions use safe attribute access and handle missing or invalid data gracefully.
