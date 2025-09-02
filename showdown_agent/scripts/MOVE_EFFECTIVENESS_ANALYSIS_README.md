# Move Effectiveness Analysis Methods

This document describes the new move effectiveness analysis methods added to the `htho884.py` player agent.

## Overview

The agent now includes comprehensive methods to analyze how effective each available move is against the current opponent Pokémon. This analysis takes into account:

- **Type effectiveness**: How well the move type matches against opponent types
- **STAB bonus**: Same Type Attack Bonus when the move type matches your Pokémon's type
- **Ability immunities**: Special abilities that make moves completely ineffective
- **Base power**: The raw power of the move
- **Estimated damage**: Calculated damage percentage against the opponent
- **KO potential**: Whether the move can potentially knock out the opponent

## Available Methods

### 1. `get_move_effectiveness_analysis(battle, opponent=None)`

Returns a detailed dictionary containing comprehensive analysis of all available moves.

**Parameters:**
- `battle`: The current battle object
- `opponent`: Optional specific opponent to analyze against (defaults to active opponent)

**Returns:**
A dictionary with the following structure:
```python
{
    'opponent': {
        'species': 'opponent_name',
        'types': [type1, type2],
        'ability': 'ability_name',
        'current_hp': 0.75  # as fraction
    },
    'my_pokemon': {
        'species': 'my_pokemon_name',
        'types': [type1, type2]
    },
    'moves': {
        'move_name': {
            'type': move_type,
            'base_power': 80,
            'raw_effectiveness': 2.0,
            'stab_bonus': 1.5,
            'total_effectiveness': 3.0,
            'effectiveness_category': '2x SUPER EFFECTIVE',
            'is_immune': False,
            'estimated_damage': 0.45,
            'pp': 15,
            'disabled': False,
            'can_ko': False
        }
    }
}
```

### 2. `print_move_effectiveness_analysis(battle, opponent=None)`

Prints a formatted, human-readable analysis to the console.

**Example Output:**
```
============================================================
MOVE EFFECTIVENESS ANALYSIS
============================================================
Your Pokemon: Flutter Mane (Ghost, Fairy)
Opponent: Kingambit (Dark, Steel)
Opponent Ability: Defiant
Opponent HP: 100.0%
============================================================

MOONBLAST
  Type: Fairy
  Base Power: 95
  Effectiveness: SUPER EFFECTIVE
  Raw Multiplier: 2.0x
  STAB Bonus: 1.5x
  Total Multiplier: 3.0x
  Estimated Damage: 67.5%
  KO Potential: NO
  PP: 15

SHADOW BALL
  Type: Ghost
  Base Power: 80
  Effectiveness: NEUTRAL
  Raw Multiplier: 1.0x
  STAB Bonus: 1.5x
  Total Multiplier: 1.5x
  Estimated Damage: 30.0%
  KO Potential: NO
  PP: 15
```

### 3. `get_effectiveness_summary(battle, opponent=None)`

Returns a quick summary with counts and best moves by effectiveness category.

**Returns:**
```python
{
    'opponent': 'opponent_name',
    'opponent_types': [type1, type2],
    'total_moves': 4,
    'categories': {
        '2x SUPER EFFECTIVE': ['Moonblast'],
        'SUPER EFFECTIVE': ['Mystical Fire'],
        'NEUTRAL': ['Shadow Ball', 'Power Gem']
    },
    'best_moves': {
        '2x SUPER EFFECTIVE': [
            {'name': 'Moonblast', 'base_power': 95, 'effectiveness': 2.0, 'estimated_damage': 0.675}
        ],
        'SUPER EFFECTIVE': [
            {'name': 'Mystical Fire', 'base_power': 75, 'effectiveness': 1.5, 'estimated_damage': 0.45}
        ]
    }
}
```

## Effectiveness Categories

Moves are categorized based on their raw type effectiveness multiplier:

- **4x SUPER EFFECTIVE**: Raw multiplier ≥ 4.0 (e.g., Ground vs Fire/Steel)
- **2x SUPER EFFECTIVE**: Raw multiplier ≥ 2.0 (e.g., Fighting vs Normal)
- **SUPER EFFECTIVE**: Raw multiplier > 1.0 (e.g., Water vs Fire)
- **NEUTRAL**: Raw multiplier = 1.0 (e.g., Normal vs Normal)
- **RESISTED**: Raw multiplier > 0.0 and < 1.0 (e.g., Fire vs Water)
- **IMMUNE**: Raw multiplier = 0.0 or ability-based immunity (e.g., Ground vs Flying)
- **NO EFFECT**: Raw multiplier = 0.0 (e.g., Normal vs Ghost)

## Automatic Integration

The effectiveness analysis is automatically called during battle when the agent is making move decisions. You'll see the analysis printed to the console before each move selection, providing real-time information about move effectiveness.

## Usage Examples

### During Battle (Automatic)
The analysis runs automatically, but you can also call it manually:

```python
# Get detailed analysis
analysis = agent.get_move_effectiveness_analysis(battle)

# Print formatted analysis
agent.print_move_effectiveness_analysis(battle)

# Get quick summary
summary = agent.get_effectiveness_summary(battle)
```

### Manual Analysis
```python
# Analyze against a specific opponent
specific_opponent = battle.opponent_team[0]
analysis = agent.get_move_effectiveness_analysis(battle, specific_opponent)
```

## Benefits

1. **Strategic Decision Making**: Clear understanding of which moves are most effective
2. **KO Potential Assessment**: Know which moves can potentially knock out the opponent
3. **Type Advantage Recognition**: Identify 4x and 2x effective moves quickly
4. **STAB Optimization**: See when STAB bonuses enhance move effectiveness
5. **Immunity Detection**: Avoid using moves that won't work due to abilities or typing

## Technical Details

- **Damage Estimation**: Uses the existing `estimate_damage_frac` method
- **Type Effectiveness**: Leverages the comprehensive `TYPE_EFFECTIVENESS` matrix
- **Ability Immunities**: Checks for common immunity abilities like Levitate, Flash Fire, etc.
- **STAB Calculation**: Automatically applies 1.5x multiplier for same-type moves
- **Performance**: Analysis is computed efficiently and only when needed

## Future Enhancements

Potential improvements could include:
- Weather effects on move effectiveness
- Terrain effects
- Item-based effectiveness modifiers
- Status condition considerations
- Priority move analysis
