# Effective Moves Analysis Guide

This guide explains how to use the new `find_effective_moves` function and related helper functions to analyze move effectiveness including type advantages, STAB bonuses, weather boosts, and terrain effects.

## Overview

The `find_effective_moves` function provides comprehensive analysis of move effectiveness by considering:

1. **Type Effectiveness**: Base type advantages/disadvantages
2. **STAB (Same Type Attack Bonus)**: 1.5x multiplier when move type matches Pokemon type
3. **Weather Boosts**: Environmental conditions that affect move power
4. **Terrain Effects**: Field effects that boost or reduce move power
5. **Ability Immunities**: Abilities that make moves completely ineffective

## Function Reference

### `find_effective_moves(battle, moves, opp_types, my_types)`

**Parameters:**
- `battle`: The current battle state object
- `moves`: List of available moves
- `opp_types`: List of opponent's Pokemon types
- `my_types`: List of your Pokemon's types

**Returns:**
Dictionary with categorized moves by effectiveness:
```python
{
    'x6': [],      # 6x effective (STAB + weather + type advantage)
    'x4': [],      # 4x effective (STAB + type advantage or weather + type advantage)
    'x3': [],      # 3x effective (STAB + weather boost)
    'x2': [],      # 2x effective (type advantage or STAB)
    'x1.5': [],    # 1.5x effective (STAB only)
    'x1': [],      # 1x effective (neutral)
    'x0.5': [],    # 0.5x effective (resisted)
    'x0.25': [],   # 0.25x effective (double resisted)
    'x0': []       # 0x effective (immune)
}
```

Each move entry contains: `(move_object, damage, effectiveness, boost_description)`

### `get_best_effective_move(effective_moves, min_effectiveness=1.0)`

**Parameters:**
- `effective_moves`: Dictionary from `find_effective_moves`
- `min_effectiveness`: Minimum effectiveness to consider (default 1.0)

**Returns:**
Best move tuple or None if no suitable moves found.

### `print_effective_moves_debug(effective_moves)`

**Parameters:**
- `effective_moves`: Dictionary from `find_effective_moves`

**Returns:**
None (prints debug information to console)

## Usage Examples

### Basic Usage

```python
from showdown_agent.scripts.players.htho884 import CustomAgent

# Create agent instance
agent = CustomAgent()

# Get effective moves analysis
effective_moves = agent.find_effective_moves(battle, available_moves, opponent_types, my_types)

# Get the best move
best_move = agent.get_best_effective_move(effective_moves)
if best_move:
    move, damage, effectiveness, boost = best_move
    print(f"Best move: {move.name} ({effectiveness:.2f}x effective)")
```

### Advanced Usage with Custom Thresholds

```python
# Only consider moves with at least 2x effectiveness
best_move = agent.get_best_effective_move(effective_moves, min_effectiveness=2.0)

# Print detailed analysis
agent.print_effective_moves_debug(effective_moves)
```

## Environmental Effects

### Weather Boosts

| Weather | Affected Types | Effect |
|---------|----------------|---------|
| Sunny Day | Fire | +50% damage |
| Sunny Day | Water | -50% damage |
| Rain | Water | +50% damage |
| Rain | Fire | -50% damage |

### Terrain Boosts

| Terrain | Affected Types | Effect |
|---------|----------------|---------|
| Electric Terrain | Electric | +30% damage |
| Grassy Terrain | Grass | +30% damage |
| Psychic Terrain | Psychic | +30% damage |
| Misty Terrain | Dragon | -50% damage |

## Ability Immunities

The function automatically detects and handles ability-based immunities:

| Ability | Immune to |
|---------|-----------|
| Levitate | Ground |
| Flash Fire | Fire |
| Water Absorb | Water |
| Dry Skin | Water |
| Sap Sipper | Grass |
| Lightning Rod | Electric |
| Storm Drain | Water |

## Integration with Existing Code

You can integrate this function into your existing move selection logic:

```python
def choose_move(self, battle):
    # ... existing code ...
    
    # Use the new effective moves analysis
    effective_moves = self.find_effective_moves(battle, battle.available_moves, opp_types, my_types)
    
    # Get best move with minimum 1.5x effectiveness
    best_move = self.get_best_effective_move(effective_moves, min_effectiveness=1.5)
    
    if best_move:
        move, damage, effectiveness, boost = best_move
        print(f"Using {move.name} ({effectiveness:.2f}x effective, {boost})")
        return self.create_order(move)
    
    # Fallback to existing logic
    # ... rest of existing code ...
```

## Testing

Run the test script to see examples in action:

```bash
python showdown_agent/scripts/test_effective_moves.py
```

This will demonstrate various scenarios including:
- Fire moves in Sunny Day
- Electric moves in Electric Terrain
- Water moves in Rain
- Immunity scenarios

## Performance Considerations

- The function processes all moves in a single pass
- Type effectiveness calculations are cached in the existing `TYPE_EFFECTIVENESS` matrix
- Weather and terrain checks are minimal string comparisons
- The function is designed to be called once per turn and cached if needed

## Common Use Cases

1. **Priority Move Selection**: Find the highest effectiveness moves first
2. **Weather Teams**: Optimize move selection based on current weather
3. **Terrain Teams**: Leverage terrain effects for maximum damage
4. **Type Coverage**: Ensure you have moves that hit effectively
5. **Immunity Detection**: Avoid using moves that won't work due to abilities
