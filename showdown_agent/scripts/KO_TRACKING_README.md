# KO Rating and Pokemon Survivability Tracking

## Overview

The evaluation script (`eval.py`) has been enhanced with comprehensive KO rating and Pokemon survivability tracking capabilities. This allows you to analyze individual Pokemon performance beyond just win/loss records.

## New Features

### 1. KO Rating System
- **Definition**: `(KOs dealt - KOs taken) / battles participated`
- **Interpretation**: 
  - Positive values: Pokemon gets more KOs than it takes
  - Negative values: Pokemon gets KO'd more often than it KOs opponents
  - Zero: Even KO performance

### 2. Survivability Rating
- **Definition**: `turns survived / battles participated`
- **Interpretation**: Average number of turns a Pokemon stays alive per battle
- **Higher values**: More durable Pokemon that stay in battle longer

### 3. Additional Metrics
- **Damage Efficiency**: Ratio of damage dealt to damage taken
- **Battle Participation**: Number of battles each Pokemon was used in
- **Total KOs**: Separate tracking of KOs dealt and KOs taken
- **Turn Tracking**: Total turns survived across all battles

## Usage

### Running Enhanced Evaluation
```bash
python eval.py
```

The script now automatically tracks and displays:
1. Traditional win/loss statistics
2. **NEW**: Detailed Pokemon performance analysis
3. **NEW**: KO ratings and survivability metrics
4. **NEW**: Visual graphs for Pokemon performance
5. **NEW**: Saved statistics file for later analysis

### Output Files Generated
- `winrate_graph.png`: Win rates against each opponent
- `pokemon_performance.png`: KO ratings and survivability visualizations
- `pokemon_performance_stats.txt`: Detailed text statistics

## Sample Output

### Pokemon Performance Table
```
┌─────────────────┬────────────┬──────────────┬───────────┬───────────┬─────────┬───────────────┬──────────────────┐
│ Pokemon         │ KO Rating  │ Survivability│ KOs Dealt │ KOs Taken │ Battles │ Turns Survived│ Damage Efficiency│
├─────────────────┼────────────┼──────────────┼───────────┼───────────┼─────────┼───────────────┼──────────────────┤
│ Zacian-Crowned  │ 0.46       │ 2.9          │ 15        │ 2         │ 28      │ 80            │ ∞                │
│ Koraidon        │ 0.30       │ 2.5          │ 12        │ 3         │ 30      │ 75            │ ∞                │
│ Eternatus       │ 0.28       │ 2.4          │ 8         │ 1         │ 25      │ 60            │ ∞                │
│ Kyogre          │ 0.19       │ 2.5          │ 10        │ 5         │ 26      │ 65            │ ∞                │
│ Ribombee        │ 0.15       │ 2.3          │ 5         │ 2         │ 20      │ 45            │ ∞                │
│ Ho-Oh           │ 0.09       │ 2.3          │ 6         │ 4         │ 22      │ 50            │ ∞                │
└─────────────────┴────────────┴──────────────┴───────────┴───────────┴─────────┴───────────────┴──────────────────┘
```

### Summary Statistics
```
📊 SUMMARY STATISTICS:
   Total Pokemon Analyzed: 6
   Average KO Rating: 0.25
   Average Survivability: 2.5 turns/battle
   Total KOs Dealt: 56
   Total KOs Taken: 17
   KO Ratio: 56/17 (3.29)

🏆 TOP PERFORMERS:
   Best KO Rating: Zacian-Crowned (0.46)
   Best Survivability: Zacian-Crowned (2.9 turns/battle)
   Worst KO Rating: Ho-Oh (0.09)
```

## Technical Implementation

### Core Classes

#### `PokemonStats`
Tracks individual Pokemon performance with properties:
- `ko_rating`: Calculated KO performance metric
- `survivability_rating`: Average turns survived per battle
- `damage_efficiency`: Damage dealt/taken ratio

#### `BattleTracker`
Monitors battle events and updates Pokemon statistics:
- Tracks turn-by-turn Pokemon activity
- Detects KO events
- Calculates participation metrics
- Generates summary statistics

#### `TrackingPlayer`
Wrapper around the original player that adds tracking capabilities:
- Delegates moves to original player
- Tracks battle state changes
- Updates statistics in real-time

### Key Methods

- `track_turn()`: Records Pokemon activity each turn
- `check_for_kos()`: Detects when Pokemon are knocked out
- `get_summary_stats()`: Returns formatted statistics
- `save_stats_to_file()`: Exports data for analysis

## Interpretation Guide

### Pokemon Performance Types

1. **Excellent Pokemon** (High KO Rating + High Survivability)
   - Example: Zacian-Crowned with 0.46 KO rating, 2.9 survivability
   - These are your best performers

2. **Glass Cannons** (High KO Rating + Low Survivability)
   - Deal lots of damage but get KO'd quickly
   - May need better positioning or support

3. **Defensive Walls** (Low KO Rating + High Survivability)
   - Stay alive long but don't get many KOs
   - Good for stalling or support roles

4. **Needs Improvement** (Low KO Rating + Low Survivability)
   - Poor performance across the board
   - Consider team changes or strategy adjustments

### Strategic Insights

- **Team Balance**: Look for a mix of high KO rating and high survivability Pokemon
- **Weak Links**: Identify Pokemon with consistently poor performance
- **Usage Patterns**: Check if high-performing Pokemon are being used enough
- **Meta Adaptation**: Adjust team composition based on performance data

## Demo Script

Run `demo_ko_tracking.py` to see the tracking system in action with sample data:

```bash
python demo_ko_tracking.py
```

This demonstrates all the new features without requiring actual battles.

## Future Enhancements

Potential improvements for the tracking system:
- Move effectiveness tracking
- Type advantage/disadvantage analysis
- Item usage statistics
- Weather/terrain impact analysis
- Opponent-specific performance metrics

