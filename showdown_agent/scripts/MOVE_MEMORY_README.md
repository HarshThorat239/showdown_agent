# Move Memory System for Pokémon Showdown Agent

This document explains how to use the move memory system that has been added to the `htho884.py` agent.

## Overview

The move memory system allows the agent to remember which moves opponent Pokémon have used across multiple battles. This information is used to make better strategic decisions during battles.

## Features

### 1. Persistent Memory
- Tracks moves used by each opponent Pokémon species
- Memory persists across different battles and sessions
- Automatically saves to `move_memory.txt` file

### 2. Strategic Decision Making
- Uses known opponent moves to inform switching decisions
- Prioritizes moves that can KO threatening opponents
- Considers move patterns when evaluating risk

### 3. Easy Integration
- Automatically loads existing memory when agent starts
- Simple API for manually recording moves
- Debug output shows what moves are known

## How to Use

### Basic Usage

The move memory system is automatically active when you use the `CustomAgent` class. It will:

1. Load existing move memory from `move_memory.txt` (if it exists)
2. Track moves during battles
3. Use this information to make better decisions
4. Save memory periodically

### Manual Move Recording

You can manually record opponent moves using the `record_opponent_move` method:

```python
from players.htho884 import CustomAgent

agent = CustomAgent()

# Record that Kingambit used Kowtow Cleave
agent.record_opponent_move("kingambit", "kowtowcleave")

# Record that Flutter Mane used Moonblast
agent.record_opponent_move("fluttermane", "moonblast")
```

### Checking Known Moves

You can check what moves are known for a specific Pokémon:

```python
# Get all known moves for Kingambit
moves = agent.get_opponent_moves("kingambit")
print(moves)  # {'kowtowcleave': 2, 'suckerpunch': 1, 'ironhead': 1}

# Get the most frequently used moves
top_moves = agent.get_most_used_moves("kingambit", top_n=3)
print(top_moves)  # ['kowtowcleave', 'ironhead', 'suckerpunch']

# Check if a specific move has been seen
has_move = agent.has_seen_move("kingambit", "thunderbolt")
print(has_move)  # False
```

### Memory Management

```python
# Save memory to a specific file
agent.save_move_memory("my_memory.txt")

# Load memory from a specific file
agent.load_move_memory("my_memory.txt")

# Print a summary of all recorded moves
agent.print_move_memory_summary()
```

## Integration with Battle System

The move memory system integrates with the battle decision-making process:

1. **Switch Evaluation**: When considering switches, the agent looks at known opponent moves to assess risk
2. **Move Selection**: When choosing moves, the agent considers if the opponent has threatening moves
3. **KO Prioritization**: If the opponent has shown threatening moves, the agent prioritizes moves that can KO quickly

## Debug Output

The system provides debug output to show what it's thinking:

```
DEBUG: Known moves for kingambit: {'kowtowcleave': 2, 'suckerpunch': 1}
DEBUG: Most used moves by kingambit: ['kowtowcleave', 'suckerpunch']
DEBUG: Opponent has threatening moves: ['kowtowcleave']
DEBUG: *** PRIORITIZING KO MOVE: sacredsword vs threatening opponent ***
```

## File Format

The move memory is saved in a simple CSV format:

```
kingambit,kowtowcleave,2
kingambit,suckerpunch,1
fluttermane,moonblast,1
```

Each line contains: `species,move_name,usage_count`

## Testing

Run the test script to see the system in action:

```bash
python test_move_memory.py
```

This will demonstrate all the features of the move memory system.

## Advanced Usage

### Custom Integration

You can integrate move tracking into your own battle analysis:

```python
# After observing an opponent move in battle
if opponent_used_move:
    agent.record_opponent_move(opponent_species, move_name)

# When making decisions
known_moves = agent.get_opponent_moves(current_opponent)
if "thunderbolt" in known_moves:
    # Opponent has shown Thunderbolt, be careful with Water types
    pass
```

### Memory Persistence

The memory system automatically:
- Loads memory when the agent is created
- Saves memory every 10 turns during battles
- Preserves data across different battle sessions

## Limitations

1. **Manual Recording**: Currently requires manual recording of moves (could be automated with battle log parsing)
2. **Simple Analysis**: Uses basic keyword matching for move threat assessment
3. **No Context**: Doesn't track when moves were used (just frequency)

## Future Improvements

Potential enhancements:
- Automatic move detection from battle logs
- More sophisticated threat analysis
- Context-aware move tracking (situation when used)
- Machine learning integration for pattern recognition
