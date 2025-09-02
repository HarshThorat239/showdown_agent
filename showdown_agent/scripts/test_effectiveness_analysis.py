#!/usr/bin/env python3
"""
Test script for the new move effectiveness analysis methods.
This script demonstrates how to use the effectiveness analysis functionality.
"""

from players.htho884 import CustomAgent

def test_effectiveness_analysis():
    """
    Test the effectiveness analysis methods with a mock battle scenario.
    """
    print("Testing Move Effectiveness Analysis Methods")
    print("=" * 50)
    
    # Create an instance of the agent
    agent = CustomAgent()
    
    print("\nAvailable methods:")
    print("1. get_move_effectiveness_analysis(battle, opponent=None)")
    print("   - Returns detailed analysis dictionary")
    print("2. print_move_effectiveness_analysis(battle, opponent=None)")
    print("   - Prints formatted analysis to console")
    print("3. get_effectiveness_summary(battle, opponent=None)")
    print("   - Returns quick summary with counts and best moves")
    
    print("\nUsage examples:")
    print("- agent.get_move_effectiveness_analysis(battle)")
    print("- agent.print_move_effectiveness_analysis(battle)")
    print("- agent.get_effectiveness_summary(battle)")
    
    print("\nThe analysis includes:")
    print("- Move type and base power")
    print("- Raw effectiveness multiplier")
    print("- STAB bonus (if applicable)")
    print("- Total effectiveness (including STAB)")
    print("- Effectiveness category (4x, 2x, super effective, neutral, resisted, immune)")
    print("- Estimated damage percentage")
    print("- KO potential")
    print("- PP and disabled status")
    
    print("\nEffectiveness categories:")
    print("- 4x SUPER EFFECTIVE: Raw multiplier >= 4.0")
    print("- 2x SUPER EFFECTIVE: Raw multiplier >= 2.0")
    print("- SUPER EFFECTIVE: Raw multiplier > 1.0")
    print("- NEUTRAL: Raw multiplier = 1.0")
    print("- RESISTED: Raw multiplier > 0.0 and < 1.0")
    print("- IMMUNE: Raw multiplier = 0.0 or ability-based immunity")
    print("- NO EFFECT: Raw multiplier = 0.0")
    
    print("\nNote: These methods are automatically called during battle")
    print("when the agent is making move decisions, providing real-time")
    print("analysis of move effectiveness against the current opponent.")

if __name__ == "__main__":
    test_effectiveness_analysis()
