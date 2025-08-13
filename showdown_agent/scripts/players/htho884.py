from poke_env.battle import AbstractBattle, side_condition, pokemon_type, move
from poke_env.player import Player
from poke_env.battle.pokemon_type import PokemonType
import poke_env.battle as battle




team = """
Palafin @ Choice Scarf  
Ability: Zero to Hero  
Tera Type: Water  
EVs: 4 HP / 252 Atk / 252 Spe  
Adamant Nature  
- Flip Turn  
- Ice Punch  
- Aqua Tail  
- Close Combat  

Flutter Mane @ Life Orb  
Ability: Protosynthesis  
Tera Type: Fire  
EVs: 4 Def / 252 SpA / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Moonblast  
- Shadow Ball  
- Mystical Fire  
- Power Gem 

Arceus-Fairy @ Pixie Plate  
Ability: Multitype  
Tera Type: Fairy  
EVs: 132 Def / 132 SpA / 244 Spe  
Timid Nature  
IVs: 0 Atk  
- Judgment  
- Flamethrower  
- Psychic  
- Aura Sphere  

Dialga-Origin @ Adamant Crystal  
Ability: Pressure  
Tera Type: Stellar  
EVs: 252 Def / 4 SpA / 252 SpD  
Relaxed Nature  
IVs: 0 Atk  
- Flash Cannon  
- Roar of Time  
- Flamethrower  
- Thunderbolt  

Zacian-Crowned @ Rusted Sword  
Ability: Intrepid Sword  
Tera Type: Fairy  
EVs: 140 HP / 252 Atk / 116 Spe  
Jolly Nature  
- Sacred Sword  
- Behemoth Blade  
- Play Rough  
- Ice Fang  

Hoopa-Unbound  
Ability: Magician  
Tera Type: Fighting  
EVs: 140 Atk / 116 SpA / 252 Spe  
Naughty Nature  
- Hyperspace Fury  
- Phantom Force  
- Drain Punch  
- Future Sight    
"""
    # === FULL TYPE EFFECTIVENESS MATRIX ===
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


class CustomAgent(Player):
    def __init__(self, *args, **kwargs):
        global team
        if "team" not in globals():
            team = ""
        super().__init__(team=team, *args, **kwargs)

        # Palafin state
        self.palafin_seen_once = False        # first time base Palafin has appeared
        self.palafin_pivot_done = False       # once we Flip Turn, don't force it again

    def team_preview(self, battle: AbstractBattle) -> int:
        return 0

    # ---------- TYPE HELPERS ----------
    def type_multiplier(self, atk_type, def_types):
        mult = 1.0
        inner = TYPE_EFFECTIVENESS.get(atk_type, {})
        for t in def_types:
            if t is None:
                continue
            mult *= inner.get(t, 1.0)
        return mult

    def estimated_effectiveness(self, move_type, opp_types, my_types):
        eff = self.type_multiplier(move_type, opp_types)
        if move_type in my_types:
            eff *= 1.5
        return eff

    def estimate_damage_frac(self, mv, my_types, opp_types):
        bp = getattr(mv, "base_power", 0) or 0
        if bp <= 0:
            return 0.0
        
        # Get move type - handle both direct type and type_id
        move_type = getattr(mv, 'type', None)
        if move_type is None:
            move_type = getattr(mv, 'type_id', None)
        
        if move_type is None:
            return 0.0
            
        eff = self.estimated_effectiveness(move_type, opp_types, my_types)
        return max(0.0, min((bp / 100.0) * eff, 1.0))

    def opponent_has_advantage(self, my_types, opp_types, thresh=1.0):
        return any(self.type_multiplier(otype, my_types) > thresh for otype in opp_types)

    def pick_best_switch(self, battle, opp_types):
        best_mon, best_score = None, float("-inf")
        for mon in battle.available_switches:
            worst_incoming = max(self.type_multiplier(otype, mon.types) for otype in opp_types)
            best_offense   = max(1.5 * self.type_multiplier(ct, opp_types) for ct in mon.types)
            score = best_offense / (worst_incoming + 1e-6)
            if score > best_score:
                best_score, best_mon = score, mon
        return best_mon

    def _is_flip_turn(self, mv) -> bool:
        # robust check by id and name
        mid = (getattr(mv, "id", "") or "").lower()
        if mid == "flipturn":
            return True
        mname = (getattr(mv, "name", "") or getattr(mv, "display_name", "") or "").lower().replace(" ", "")
        return mname == "flipturn"

    # ---------- POLICY ----------
    def choose_move(self, battle: AbstractBattle):
        opp = battle.opponent_active_pokemon
        me  = battle.active_pokemon
        opp_types = opp.types
        my_types  = me.types
        opp_hp    = opp.current_hp_fraction or 1.0

        # If forced to switch (e.g., after a pivot), pick best counter
        if not battle.available_moves and battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types)
            if counter:
                return self.create_order(counter)
            return self.create_order(list(battle.available_switches)[0])

        # --- PALAFIN (base form): always Flip Turn on first appearance ---
        species = (getattr(me, "species", "") or getattr(me, "name", "")).lower()
        is_palafin_base = ("palafin" in species) and ("hero" not in species)
        if is_palafin_base and not self.palafin_pivot_done:
            for mv in battle.available_moves:
                if self._is_flip_turn(mv):
                    self.palafin_seen_once = True
                    self.palafin_pivot_done = True
                    return self.create_order(mv)
            # If Flip Turn isn't usable (disabled/PP), fall through to normal logic

        # --- NEW PRIORITY-BASED MOVE SELECTION ---
        moves = []
        super_effective_moves = []
        neutral_moves = []
        resisted_moves = []
        
        for mv in battle.available_moves:
            # Optional: avoid re-using Flip Turn after the initial pivot
            if self.palafin_pivot_done and self._is_flip_turn(mv):
                continue
            if not mv.base_power or mv.base_power <= 0:
                continue
            
            # Get move type - handle both direct type and type_id
            move_type = getattr(mv, 'type', None)
            if move_type is None:
                move_type = getattr(mv, 'type_id', None)
            
            if move_type is None:
                continue
                
            raw_mult = self.type_multiplier(move_type, opp_types)
            if raw_mult == 0.0:
                continue
            dmg = self.estimate_damage_frac(mv, my_types, opp_types)
            moves.append((mv, dmg, raw_mult))
            
            # Debug output for troubleshooting
            move_name = getattr(mv, 'name', getattr(mv, 'display_name', 'Unknown'))
            print(f"DEBUG: Move {move_name} (type: {move_type}) vs {opp_types} = {raw_mult}x effectiveness")
            
            # Categorize moves by effectiveness
            if raw_mult > 1.0:
                super_effective_moves.append((mv, dmg, raw_mult))
                print(f"DEBUG: {move_name} categorized as SUPER EFFECTIVE")
            elif abs(raw_mult - 1.0) < 1e-9:
                neutral_moves.append((mv, dmg, raw_mult))
                print(f"DEBUG: {move_name} categorized as NEUTRAL")
            else:
                resisted_moves.append((mv, dmg, raw_mult))
                print(f"DEBUG: {move_name} categorized as RESISTED")

        print(f"DEBUG: Found {len(super_effective_moves)} super effective, {len(neutral_moves)} neutral, {len(resisted_moves)} resisted moves")

        # Check if we can KO with any move
        for m, dmg, _ in sorted(moves, key=lambda x: x[1], reverse=True):
            if dmg >= opp_hp - 1e-6:
                return self.create_order(m)

        # PRIORITY 1: Use super effective moves if available
        if super_effective_moves:
            # Sort by damage within super effective moves
            best_se_move = max(super_effective_moves, key=lambda x: x[1])
            move_name = getattr(best_se_move[0], 'name', getattr(best_se_move[0], 'display_name', 'Unknown'))
            print(f"DEBUG: Selected SUPER EFFECTIVE move: {move_name} (damage: {best_se_move[1]:.3f})")
            return self.create_order(best_se_move[0])

        # PRIORITY 2: If no super effective moves, consider switching to a better Pokemon
        if battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types)
            if counter:
                # Check if the counter has super effective moves against opponent
                counter_has_se = False
                for mv in counter.moves:
                    if hasattr(mv, 'type') and mv.type:
                        eff = self.type_multiplier(mv.type, opp_types)
                        if eff > 1.0:
                            counter_has_se = True
                            break
                
                # Switch if counter has super effective moves or if we're at a disadvantage
                disadvantaged = self.opponent_has_advantage(my_types, opp_types, thresh=1.0)
                if counter_has_se or disadvantaged:
                    print(f"DEBUG: Switching to {counter.species} (has SE: {counter_has_se}, disadvantaged: {disadvantaged})")
                    return self.create_order(counter)

        # PRIORITY 3: Use neutral moves if available
        if neutral_moves:
            best_neutral_move = max(neutral_moves, key=lambda x: x[1])
            move_name = getattr(best_neutral_move[0], 'name', getattr(best_neutral_move[0], 'display_name', 'Unknown'))
            print(f"DEBUG: Selected NEUTRAL move: {move_name} (damage: {best_neutral_move[1]:.3f})")
            return self.create_order(best_neutral_move[0])

        # PRIORITY 4: If only resisted moves remain, try switching one more time
        if resisted_moves and battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types)
            if counter:
                print(f"DEBUG: Switching due to only resisted moves available")
                return self.create_order(counter)

        # PRIORITY 5: Use best resisted move as last resort
        if resisted_moves:
            best_resisted_move = max(resisted_moves, key=lambda x: x[1])
            move_name = getattr(best_resisted_move[0], 'name', getattr(best_resisted_move[0], 'display_name', 'Unknown'))
            print(f"DEBUG: Selected RESISTED move: {move_name} (damage: {best_resisted_move[1]:.3f})")
            return self.create_order(best_resisted_move[0])

        # Fallback to random move if no damaging moves available
        return self.choose_random_move(battle)