from poke_env.battle.pokemon_type import PokemonType

# Copy the type effectiveness matrix from htho884.py
TYPE_EFFECTIVENESS = {
    PokemonType.NORMAL:  {PokemonType.ROCK: 0.5, PokemonType.GHOST: 0.0, PokemonType.STEEL: 0.5},
    PokemonType.FIRE:    {PokemonType.FIRE: 0.5, PokemonType.WATER: 0.5, PokemonType.GRASS: 2.0, PokemonType.ICE: 2.0, PokemonType.BUG: 2.0, PokemonType.ROCK: 0.5, PokemonType.DRAGON: 0.5, PokemonType.STEEL: 2.0},
    PokemonType.WATER:   {PokemonType.FIRE: 2.0, PokemonType.WATER: 0.5, PokemonType.GRASS: 0.5, PokemonType.GROUND: 2.0, PokemonType.ROCK: 2.0, PokemonType.DRAGON: 0.5},
    PokemonType.ELECTRIC:{PokemonType.WATER: 2.0, PokemonType.ELECTRIC: 0.5, PokemonType.GRASS: 0.5, PokemonType.GROUND: 0.0, PokemonType.FLYING: 2.0, PokemonType.DRAGON: 0.5},
    PokemonType.GRASS:   {PokemonType.FIRE: 0.5, PokemonType.WATER: 2.0, PokemonType.GRASS: 0.5, PokemonType.POISON: 0.5, PokemonType.GROUND: 2.0, PokemonType.FLYING: 0.5, PokemonType.BUG: 0.5, PokemonType.ROCK: 2.0, PokemonType.DRAGON: 0.5, PokemonType.STEEL: 0.5},
    PokemonType.ICE:     {PokemonType.FIRE: 0.5, PokemonType.WATER: 0.5, PokemonType.GRASS: 2.0, PokemonType.ICE: 0.5, PokemonType.GROUND: 2.0, PokemonType.FLYING: 2.0, PokemonType.DRAGON: 2.0, PokemonType.STEEL: 0.5},
    PokemonType.FIGHTING:{PokemonType.NORMAL: 2.0, PokemonType.ICE: 2.0, PokemonType.ROCK: 2.0, PokemonType.DARK: 2.0, PokemonType.STEEL: 2.0, PokemonType.POISON: 0.5, PokemonType.FLYING: 0.5, PokemonType.PSYCHIC: 0.5, PokemonType.BUG: 0.5, PokemonType.GHOST: 0.0, PokemonType.FAIRY: 0.5},
    PokemonType.POISON:  {PokemonType.GRASS: 2.0, PokemonType.FAIRY: 2.0, PokemonType.POISON: 0.5, PokemonType.GROUND: 0.5, PokemonType.ROCK: 0.5, PokemonType.GHOST: 0.5, PokemonType.STEEL: 0.0},
    PokemonType.GROUND:  {PokemonType.FIRE: 2.0, PokemonType.ELECTRIC: 2.0, PokemonType.POISON: 2.0, PokemonType.ROCK: 2.0, PokemonType.STEEL: 2.0, PokemonType.GRASS: 0.5, PokemonType.BUG: 0.5, PokemonType.FLYING: 0.0},
    PokemonType.FLYING:  {PokemonType.GRASS: 2.0, PokemonType.FIGHTING: 2.0, PokemonType.BUG: 2.0, PokemonType.ELECTRIC: 0.5, PokemonType.ROCK: 0.5, PokemonType.STEEL: 0.5},
    PokemonType.PSYCHIC: {PokemonType.FIGHTING: 2.0, PokemonType.POISON: 2.0, PokemonType.PSYCHIC: 0.5, PokemonType.STEEL: 0.5, PokemonType.DARK: 0.0},
    PokemonType.BUG:     {PokemonType.GRASS: 2.0, PokemonType.PSYCHIC: 2.0, PokemonType.DARK: 2.0, PokemonType.FIRE: 0.5, PokemonType.FIGHTING: 0.5, PokemonType.POISON: 0.5, PokemonType.FLYING: 0.5, PokemonType.GHOST: 0.5, PokemonType.STEEL: 0.5, PokemonType.FAIRY: 0.5},
    PokemonType.ROCK:    {PokemonType.FIRE: 2.0, PokemonType.ICE: 2.0, PokemonType.FLYING: 2.0, PokemonType.BUG: 2.0, PokemonType.FIGHTING: 0.5, PokemonType.GROUND: 0.5, PokemonType.STEEL: 0.5},
    PokemonType.GHOST:   {PokemonType.PSYCHIC: 2.0, PokemonType.GHOST: 2.0, PokemonType.NORMAL: 0.0, PokemonType.DARK: 0.5},
    PokemonType.DRAGON:  {PokemonType.DRAGON: 2.0, PokemonType.STEEL: 0.5, PokemonType.FAIRY: 0.0},
    PokemonType.DARK:    {PokemonType.PSYCHIC: 2.0, PokemonType.GHOST: 2.0, PokemonType.FIGHTING: 0.5, PokemonType.DARK: 0.5, PokemonType.FAIRY: 0.5},
    PokemonType.STEEL:   {PokemonType.ICE: 2.0, PokemonType.ROCK: 2.0, PokemonType.FAIRY: 2.0, PokemonType.FIRE: 0.5, PokemonType.WATER: 0.5, PokemonType.ELECTRIC: 0.5, PokemonType.STEEL: 0.5},
    PokemonType.FAIRY:   {PokemonType.FIGHTING: 2.0, PokemonType.DRAGON: 2.0, PokemonType.DARK: 2.0, PokemonType.FIRE: 0.5, PokemonType.POISON: 0.5, PokemonType.STEEL: 0.5},
}

def type_multiplier(atk_type, def_types):
    mult = 1.0
    inner = TYPE_EFFECTIVENESS.get(atk_type, {})
    for i in def_types:
        if i is None:
            continue
        mult *= inner.get(i, 1.0)
    return mult

# Test Flutter Mane moves vs Kingambit
flutter_mane_moves = [
    ("Moonblast", PokemonType.FAIRY),
    ("Shadow Ball", PokemonType.GHOST),
    ("Mystical Fire", PokemonType.FIRE),
    ("Power Gem", PokemonType.ROCK)
]

kingambit_types = [PokemonType.DARK, PokemonType.STEEL]

print("=== FLUTTER MANE vs KINGAMBIT EFFECTIVENESS TEST ===")
print(f"Kingambit types: {kingambit_types}")
print()

for move_name, move_type in flutter_mane_moves:
    effectiveness = type_multiplier(move_type, kingambit_types)
    
    # Calculate individual type effectiveness
    dark_eff = TYPE_EFFECTIVENESS.get(move_type, {}).get(PokemonType.DARK, 1.0)
    steel_eff = TYPE_EFFECTIVENESS.get(move_type, {}).get(PokemonType.STEEL, 1.0)
    
    print(f"{move_name} ({move_type}):")
    print(f"  vs Dark: {dark_eff}x")
    print(f"  vs Steel: {steel_eff}x")
    print(f"  Total: {effectiveness}x")
    
    if effectiveness > 1.0:
        print(f"  *** SUPER EFFECTIVE ***")
    elif effectiveness == 1.0:
        print(f"  *** NEUTRAL ***")
    else:
        print(f"  *** RESISTED ***")
    print()

# Test the move selection logic
print("=== MOVE SELECTION LOGIC TEST ===")
moves = []
super_effective_moves = []
neutral_moves = []
resisted_moves = []

for move_name, move_type in flutter_mane_moves:
    raw_mult = type_multiplier(move_type, kingambit_types)
    
    # Simulate damage calculation (simplified)
    dmg = raw_mult * 0.3  # Simplified damage estimate
    
    moves.append((move_name, dmg, raw_mult))
    
    if raw_mult > 1.0:
        super_effective_moves.append((move_name, dmg, raw_mult))
        print(f"DEBUG: {move_name} categorized as SUPER EFFECTIVE")
    elif abs(raw_mult - 1.0) < 1e-9:
        neutral_moves.append((move_name, dmg, raw_mult))
        print(f"DEBUG: {move_name} categorized as NEUTRAL")
    else:
        resisted_moves.append((move_name, dmg, raw_mult))
        print(f"DEBUG: {move_name} categorized as RESISTED")

print(f"\nFound {len(super_effective_moves)} super effective, {len(neutral_moves)} neutral, {len(resisted_moves)} resisted moves")

if super_effective_moves:
    # Sort by effectiveness first, then by damage within same effectiveness
    best_se_move = max(super_effective_moves, key=lambda x: (x[2], x[1]))  # (effectiveness, damage)
    print(f"Selected SUPER EFFECTIVE move: {best_se_move[0]} (damage: {best_se_move[1]:.3f}, effectiveness: {best_se_move[2]})")
else:
    print("No super effective moves found!")
