#!/usr/bin/env python3
"""
Test script to demonstrate the move memory system for the Pokémon Showdown agent.
This script shows how to manually record opponent moves and use the memory system.
"""

from players.htho884 import CustomAgent

def test_move_memory():
    """Test the move memory functionality"""
    
    # Create an agent instance
    agent = CustomAgent()
    
    print("=== Testing Move Memory System ===\n")
    
    # Test 1: Record some moves manually
    print("1. Recording opponent moves...")
    agent.record_opponent_move("kingambit", "kowtowcleave")
    agent.record_opponent_move("kingambit", "suckerpunch")
    agent.record_opponent_move("kingambit", "ironhead")
    agent.record_opponent_move("kingambit", "kowtowcleave")  # Used twice
    
    agent.record_opponent_move("fluttermane", "moonblast")
    agent.record_opponent_move("fluttermane", "shadowball")
    agent.record_opponent_move("fluttermane", "mysticalfire")
    
    print()
    
    # Test 2: Check what moves we know
    print("2. Checking known moves...")
    kingambit_moves = agent.get_opponent_moves("kingambit")
    print(f"Kingambit moves: {kingambit_moves}")
    
    fluttermane_moves = agent.get_opponent_moves("fluttermane")
    print(f"Flutter Mane moves: {fluttermane_moves}")
    
    # Test 3: Get most used moves
    print("\n3. Most used moves...")
    kingambit_top = agent.get_most_used_moves("kingambit", top_n=2)
    print(f"Kingambit top moves: {kingambit_top}")
    
    # Test 4: Check specific move usage
    print("\n4. Specific move usage...")
    kowtow_count = agent.get_move_usage_count("kingambit", "kowtowcleave")
    print(f"Kingambit used Kowtow Cleave {kowtow_count} times")
    
    # Test 5: Check if we've seen a move
    print("\n5. Checking if we've seen moves...")
    has_suckerpunch = agent.has_seen_move("kingambit", "suckerpunch")
    has_thunderbolt = agent.has_seen_move("kingambit", "thunderbolt")
    print(f"Have we seen Kingambit use Sucker Punch? {has_suckerpunch}")
    print(f"Have we seen Kingambit use Thunderbolt? {has_thunderbolt}")
    
    # Test 6: Print memory summary
    print("\n6. Memory summary...")
    agent.print_move_memory_summary()
    
    # Test 7: Save and reload memory
    print("\n7. Testing save/load functionality...")
    agent.save_move_memory("test_memory.txt")
    
    # Create a new agent to test loading
    new_agent = CustomAgent()
    new_agent.load_move_memory("test_memory.txt")
    
    print("After loading memory:")
    new_agent.print_move_memory_summary()
    
    print("\n=== Move Memory Test Complete ===")

if __name__ == "__main__":
    test_move_memory()
