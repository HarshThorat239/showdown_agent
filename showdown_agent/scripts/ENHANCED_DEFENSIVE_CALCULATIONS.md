# Enhanced Defensive Calculations

## Overview

The enhanced defensive calculations system analyzes the opponent's specific damaging moves rather than just their Pokémon types for more precise defensive advantage assessment. This provides significantly better decision-making for switches and defensive positioning.

## Key Improvements

### 1. Move-Based Analysis vs Type-Based Analysis

**Before (Type-Based):**
- Only considered opponent's Pokémon types
- Used generic type effectiveness calculations
- Could not account for specific move coverage

**After (Move-Based):**
- Analyzes opponent's actual damaging moves
- Considers base power, type effectiveness, and STAB bonuses
- Provides detailed breakdown of specific threats

### 2. New Methods Added

#### `analyze_opponent_damaging_moves(battle)`
- Extracts opponent's known damaging moves
- Analyzes move coverage by type
- Tracks move usage preferences over time

#### `calculate_defensive_risk_vs_moves(candidate_mon, opponent_moves_analysis, battle)`
- Calculates defensive risk based on opponent's specific moves
- Considers STAB bonuses for opponent moves
- Weights risk by move usage preferences
- Returns detailed breakdown of move-specific risks

#### `calculate_defensive_risk_vs_types(candidate_mon, opp_types)`
- Fallback method using traditional type-based calculations
- Used when opponent move information is unavailable

#### `track_opponent_move_usage(battle, move_used)`
- Tracks opponent move usage patterns
- Builds historical data for better predictions

#### `get_opponent_move_preferences(opp_species)`
- Returns move usage preferences based on historical data
- Helps weight risk calculations by likelihood of move usage

### 3. Enhanced Switch Decision Logic

The `pick_best_switch()` method now:
- Uses move-based defensive risk when opponent moves are known
- Falls back to type-based calculations when move data is unavailable
- Provides detailed debugging output showing move-specific risks
- Considers both offensive advantage and defensive safety

### 4. Improved Current Pokémon Evaluation

The main decision logic now:
- Calculates current Pokémon's defensive risk using opponent's specific moves
- Provides detailed breakdown of vulnerabilities
- Helps determine if staying in is safe or switching is necessary

## Example Scenario

### Flutter Mane vs Kingambit

**Type-Based Analysis:**
- Flutter Mane (Ghost/Fairy) vs Kingambit (Dark/Steel)
- Dark is super-effective vs Ghost (2x)
- Steel is neutral vs Fairy (1x)
- Overall risk: 2x (Dark type advantage)

**Move-Based Analysis:**
- Kowtow Cleave (Dark, 85 BP): 2x effective, STAB bonus = 1.5x, usage = 40%
- Iron Head (Steel, 80 BP): 1x effective, STAB bonus = 1.5x, usage = 30%
- Sucker Punch (Dark, 70 BP): 2x effective, STAB bonus = 1.5x, usage = 20%
- Weighted risk calculation considering actual move usage and base power

## Benefits

1. **More Accurate Risk Assessment**: Considers actual moves rather than theoretical type advantages
2. **Better Switch Decisions**: Identifies specific threats and vulnerabilities
3. **Usage Pattern Learning**: Tracks opponent move preferences over time
4. **Detailed Debugging**: Provides comprehensive breakdown of risk factors
5. **Fallback Compatibility**: Maintains functionality when move data is unavailable

## Implementation Details

### Risk Calculation Formula

```
Move Risk = Type Effectiveness × STAB Bonus × (Base Power / 100) × (1 + Usage Preference)
Total Risk = Average(Move Risks) × Super-Effective Penalty
```

### Super-Effective Penalty

When opponent has super-effective coverage:
```
Total Risk *= (1.0 + Super-Effective Count × 0.5)
```

### Usage Preference Weighting

Moves with higher historical usage get weighted more heavily in risk calculations, reflecting the opponent's likely behavior patterns.

## Testing

Run the test script to see the enhanced calculations in action:

```bash
python showdown_agent/scripts/test_enhanced_defensive_calculations.py
```

This will demonstrate the difference between type-based and move-based defensive risk calculations with real examples.

## Future Enhancements

1. **Move Memory Integration**: Connect with existing move memory systems
2. **Prediction Models**: Use machine learning to predict opponent moves
3. **Team Analysis**: Consider opponent's full team when calculating switch risks
4. **Item and Ability Effects**: Include held items and abilities in calculations
5. **Weather and Field Effects**: Account for environmental factors

