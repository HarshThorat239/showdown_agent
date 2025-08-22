from poke_env.battle import AbstractBattle, side_condition, pokemon_type, move
from poke_env.player import Player
from poke_env.battle.pokemon_type import PokemonType
import poke_env.battle as battle


team = """
Ting-Lu @ Leftovers  
Ability: Vessel of Ruin  
Tera Type: Poison  
EVs: 252 HP / 4 Atk / 252 SpD  
Sassy Nature  
- Spikes  
- Earthquake  
- Ruination  
- Whirlwind  

Koraidon @ Life Orb  
Ability: Orichalcum Pulse  
Tera Type: Fighting  
EVs: 252 Atk / 4 SpD / 252 Spe  
Adamant Nature  
- Collision Course  
- Dragon Claw  
- Flare Blitz  
- Wild Charge  

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

Arceus-Water @ Splash Plate  
Ability: Multitype  
Tera Type: Dark  
EVs: 248 HP / 8 SpA / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Judgment  
- Thunderbolt  
- Recover  
- Ice Beam   

Zacian-Crowned @ Rusted Sword  
Ability: Intrepid Sword  
Tera Type: Fairy  
EVs: 140 HP / 252 Atk / 116 Spe  
Jolly Nature  
- Sacred Sword  
- Behemoth Blade  
- Play Rough  
- Ice Fang  

Giratina-Origin @ Griseous Core  
Ability: Levitate  
Tera Type: Fairy  
EVs: 252 HP / 4 Atk / 252 Def  
Impish Nature  
- Defog  
- Will-O-Wisp  
- Dragon Tail  
- Shadow Sneak 
 
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
     #   self.palafin_seen_once = False        # first time base Palafin has appeared
     #   self.palafin_pivot_done = False       # once we Flip Turn, don't force it again
        
        # Hazard move tracking
        self.opponent_last_move = None
        
        # Hazard moves that should trigger Defog
        self.hazard_moves = {
            'spikes', 'stealthrock', 'toxicspikes', 'stickyweb',
            'stealth rock', 'toxic spikes', 'sticky web'
        }

    def teampreview(self, battle: AbstractBattle) -> str:
        # Lead with the first Pokémon, keep default order for the rest
        order = "/team " + "".join(str(i) for i in range(1, len(battle.team) + 1))
        return order

    def _is_hazard_move(self, move_name):
        """Check if a move is a hazard move"""
        if not move_name:
            return False
        normalized_name = move_name.lower().replace(' ', '').replace('-', '')
        return normalized_name in self.hazard_moves

    def _find_giratina(self, battle):
        """Find Giratina in available switches"""
        for mon in battle.available_switches:
            species = getattr(mon, 'species', '').lower()
            print(f"DEBUG: Checking switch option: {species}")
            if 'giratina' in species:
                print(f"DEBUG: Found Giratina: {species}")
                return mon
        print(f"DEBUG: No Giratina found in available switches")
        return None

    def _has_defog(self, pokemon):
        """Check if a Pokemon has Defog move"""
        if not hasattr(pokemon, 'moves') or not pokemon.moves:
            return False
        for move in pokemon.moves:
            move_name = getattr(move, 'name', getattr(move, 'display_name', '')).lower().replace(' ', '')
            if move_name == 'defog':
                return True
        return False

    def _update_opponent_move_tracking(self, battle):
        """Update tracking of opponent's moves"""
        # This method can be called to update move tracking
        # For now, we'll rely on the battle state and opponent boosts
        pass

    # ---------- TYPE HELPERS ----------
    def type_multiplier(self, atk_type, def_types):
        mult = 1.0
        inner = TYPE_EFFECTIVENESS.get(atk_type, {})
        for i in def_types:
            if i is None:
                continue
            mult *= inner.get(i, 1.0)
        return mult

    def is_move_immune(self, move_type, opp_ability):
        """Check if move is immune due to opponent's ability"""
        if not opp_ability:
            return False
        
        ability_name = opp_ability.lower()
        immunity_map = {
            'levitate': PokemonType.GROUND,
            'flashfire': PokemonType.FIRE,
            'waterabsorb': PokemonType.WATER,
            'dryskin': PokemonType.WATER,
            'sapsipper': PokemonType.GRASS,
            'lightningrod': PokemonType.ELECTRIC,
            'stormdrain': PokemonType.WATER,
        }
        
        return immunity_map.get(ability_name) == move_type

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
            # Defensive risk: how hard opponent's typing hits this mon
            worst_incoming = max(self.type_multiplier(otype, mon.types) for otype in opp_types)
            
            # Offensive advantage: best of this mon's types vs opponent's types
            best_offense = 0.0
            if mon.types:
                best_offense = max(self.type_multiplier(ct, opp_types) for ct in mon.types if ct is not None)
            
            # Prioritize type advantage (super effective) and defensive safety
            # Score = (offensive advantage * 2) / (defensive risk + 0.5)
            # This heavily weights offensive advantage while still considering defense
            score = (best_offense * 2.0) / (worst_incoming + 0.5)
            
            if score > best_score:
                best_score, best_mon = score, mon
                # print(f"DEBUG: {mon.species} scored {score:.2f} (offense: {best_offense:.1f}, defense risk: {worst_incoming:.1f})")
        
        if best_mon:
            # print(f"DEBUG: Selected {best_mon.species} as best switch (score: {best_score:.2f})")
            pass
        return best_mon

    #def _is_flip_turn(self, mv) -> bool:
        # robust check by id and name
    #    mid = (getattr(mv, "id", "") or "").lower()
    #    if mid == "flipturn":
    #        return True
    #    mname = (getattr(mv, "name", "") or getattr(mv, "display_name", "") or "").lower().replace(" ", "")
    #    return mname == "flipturn"

    # ---------- POLICY ----------
    def choose_move(self, battle: AbstractBattle):
        opp = battle.opponent_active_pokemon
        me  = battle.active_pokemon
        opp_types = opp.types
        my_types  = me.types
        opp_hp    = opp.current_hp_fraction or 1.0
        
        # Check if opponent used a hazard move in the last turn
        opponent_used_hazard = False
        
        # Check if we have information about the last move used
        if hasattr(battle, 'last_move') and battle.last_move:
            last_move_name = getattr(battle.last_move, 'name', getattr(battle.last_move, 'display_name', ''))
            print(f"DEBUG: Last move was: {last_move_name}")
            if self._is_hazard_move(last_move_name):
                opponent_used_hazard = True
                print(f"DEBUG: Hazard move detected: {last_move_name}")
        
        # Check for hazards on the field (this indicates opponent used hazard moves)
        if not opponent_used_hazard:
            # Check if there are hazards on our side
            if hasattr(battle, 'side_conditions'):
                side_conditions = battle.side_conditions
                print(f"DEBUG: Our side conditions: {side_conditions}")
                if side_conditions:
                    # Check for common hazard conditions - handle both enum and string
                    hazard_conditions = ['spikes', 'stealthrock', 'toxicspikes', 'stickyweb']
                    for condition in side_conditions:
                        # Convert condition to string for comparison
                        condition_str = str(condition).lower()
                        if any(hazard in condition_str for hazard in hazard_conditions):
                            opponent_used_hazard = True
                            print(f"DEBUG: Hazard found in our side conditions: {condition}")
                            break
            
            # Check opponent's side conditions (they might have set up hazards)
            if not opponent_used_hazard and hasattr(battle, 'opponent_side_conditions'):
                opponent_side_conditions = battle.opponent_side_conditions
                print(f"DEBUG: Opponent side conditions: {opponent_side_conditions}")
                if opponent_side_conditions:
                    # Check for common hazard conditions - handle both enum and string
                    hazard_conditions = ['spikes', 'stealthrock', 'toxicspikes', 'stickyweb']
                    for condition in opponent_side_conditions:
                        # Convert condition to string for comparison
                        condition_str = str(condition).lower()
                        if any(hazard in condition_str for hazard in hazard_conditions):
                            opponent_used_hazard = True
                            print(f"DEBUG: Hazard found in opponent side conditions: {condition}")
                            break
            
            # Also check for any field hazards (like Stealth Rock on the field)
            if not opponent_used_hazard and hasattr(battle, 'field_conditions'):
                field_conditions = battle.field_conditions
                if field_conditions:
                    # Check for common hazard conditions
                    hazard_conditions = ['spikes', 'stealthrock', 'toxicspikes', 'stickyweb']
                    for condition in field_conditions:
                        if condition in hazard_conditions:
                            opponent_used_hazard = True
                            break
        
        # If opponent used a hazard move, switch to Giratina and use Defog
        if opponent_used_hazard and battle.available_switches:
            print(f"DEBUG: Hazard detected! Switching to Giratina")
            print(f"DEBUG: Available switches: {[getattr(m, 'species', 'Unknown') for m in battle.available_switches]}")
            giratina = self._find_giratina(battle)
            if giratina and self._has_defog(giratina):
                print(f"DEBUG: Switching to Giratina and will use Defog")
                # Switch to Giratina
                return self.create_order(giratina)
            else:
                print(f"DEBUG: Giratina not found or doesn't have Defog")
                if not giratina:
                    print(f"DEBUG: Giratina not found in available switches")
                elif not self._has_defog(giratina):
                    print(f"DEBUG: Giratina found but doesn't have Defog")
        
        # If we're currently Giratina and opponent has used hazard moves, prioritize Defog
        current_species = getattr(me, 'species', '').lower()
        if 'giratina' in current_species and opponent_used_hazard:
            # Look for Defog in available moves
            for mv in battle.available_moves:
                move_name = getattr(mv, 'name', getattr(mv, 'display_name', '')).lower().replace(' ', '')
                if move_name == 'defog':
                    return self.create_order(mv)
        
        # Check if we're Giratina and there are hazards present (proactive Defog)
        if 'giratina' in current_species:
            # Check for hazards on our side
            if hasattr(battle, 'side_conditions') and battle.side_conditions:
                side_conditions = battle.side_conditions
                hazard_conditions = ['spikes', 'stealthrock', 'toxicspikes', 'stickyweb']
                for condition in side_conditions:
                    # Convert condition to string for comparison
                    condition_str = str(condition).lower()
                    if any(hazard in condition_str for hazard in hazard_conditions):
                        # Look for Defog in available moves
                        for mv in battle.available_moves:
                            move_name = getattr(mv, 'name', getattr(mv, 'display_name', '')).lower().replace(' ', '')
                            if move_name == 'defog':
                                return self.create_order(mv)
        
        # Defensive risk of staying in: how hard opp's typing hits our current active typing
        active_defensive_risk = max(
            (self.type_multiplier(ot, my_types) for ot in opp_types if ot is not None),
            default=1.0,
        )

        # If forced to switch (e.g., after a pivot), pick best counter
        if not battle.available_moves and battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types)
            if counter:
                return self.create_order(counter)
            return self.create_order(list(battle.available_switches)[0])

        # Check if current Pokemon is Ting-Lu and prioritize setup moves
        # current_species = getattr(me, 'species', '').lower()
        # if 'ting-lu' in current_species or 'tinglu' in current_species:
        #     setup_moves = ['spikes']
        #     for mv in battle.available_moves:
        #         move_name = getattr(mv, 'name', getattr(mv, 'display_name', '')).lower().replace(' ', '')
        #         if move_name in setup_moves:
        #             # print(f"DEBUG: Ting-Lu using setup move: {move_name}")
        #             return self.create_order(mv)

        # --- PALAFIN (base form): always Flip Turn on first appearance ---
       # species = (getattr(me, "species", "") or getattr(me, "name", "")).lower()
       # is_palafin_base = ("palafin" in species) and ("hero" not in species)
       # if is_palafin_base and not self.palafin_pivot_done:
       #     for mv in battle.available_moves:
       #         if self._is_flip_turn(mv):
       #             self.palafin_seen_once = True
       #             self.palafin_pivot_done = True
       #             return self.create_order(mv)
       #     # If Flip Turn isn't usable (disabled/PP), fall through to normal logic

        # --- NEW PRIORITY-BASED MOVE SELECTION ---
        moves = []
        super_effective_moves = []
        
        neutral_moves = []
        resisted_moves = []
        
        for mv in battle.available_moves:
            # Optional: avoid re-using Flip Turn after the initial pivot
       #     if self.palafin_pivot_done and self._is_flip_turn(mv):
       #         continue
        #    if not mv.base_power or mv.base_power <= 0:
        #        continue
            
            # Get move type - handle both direct type and type_id
            move_type = getattr(mv, 'type', None)
            if move_type is None:
                move_type = getattr(mv, 'type_id', None)
            
            if move_type is None:
                continue
            
            # Debug output for troubleshooting
            move_name = getattr(mv, 'name', getattr(mv, 'display_name', 'Unknown'))
                
            raw_mult = self.type_multiplier(move_type, opp_types)
            if raw_mult == 0.0:
                continue
            
            # Check for ability-based immunities
            opp_ability = getattr(opp, 'ability', None)
            if self.is_move_immune(move_type, opp_ability):
                # print(f"DEBUG: Move {move_name} is immune due to {opp_ability}")
                continue
            dmg = self.estimate_damage_frac(mv, my_types, opp_types)
            moves.append((mv, dmg, raw_mult))
            # print(f"DEBUG: Move {move_name} (type: {move_type}) vs {opp_types} = {raw_mult}x effectiveness")
            if raw_mult > 1.0:
                # print(f"DEBUG: *** SUPER EFFECTIVE MOVE FOUND: {move_name} ***")
                pass
            
            # Categorize moves by effectiveness
            if raw_mult > 1.0:
                super_effective_moves.append((mv, dmg, raw_mult))
                # print(f"DEBUG: {move_name} categorized as SUPER EFFECTIVE")
            elif abs(raw_mult - 1.0) < 1e-9:
                neutral_moves.append((mv, dmg, raw_mult))
                # print(f"DEBUG: {move_name} categorized as NEUTRAL")
            else:
                resisted_moves.append((mv, dmg, raw_mult))
                # print(f"DEBUG: {move_name} categorized as RESISTED")

        # print(f"DEBUG: Found {len(super_effective_moves)} super effective, {len(neutral_moves)} neutral, {len(resisted_moves)} resisted moves")

        # Check if we can KO with any move (but be more conservative)
        for m, dmg, mult in sorted(moves, key=lambda x: x[1], reverse=True):
            # Only consider it a guaranteed KO if damage is significantly higher than HP
            # and the move is at least neutral effectiveness
            if dmg >= opp_hp + 0.1 and mult >= 1.0:
                move_name = getattr(m, 'name', getattr(m, 'display_name', 'Unknown'))
                # print(f"DEBUG: *** GUARANTEED KO MOVE SELECTED: {move_name} (damage: {dmg:.3f} vs HP: {opp_hp:.3f}) ***")
                return self.create_order(m)

        # NEW RULE: If any bench Pokemon has a type that is super-effective vs opponent, switch to it
        # BUT only if its defensive risk is strictly lower than our current defensive risk
        # We pick among qualifying candidates the one that maximizes (type advantage) / (worst incoming disadvantage)
        # print(f"DEBUG: Checking for type-advantaged switches...")
        if battle.available_switches:
            best_switch = None
            best_score = float("-inf")
            for candidate in battle.available_switches:
                # Offensive advantage: best of candidate's types vs opponent's types
                offensive_advantage = 0.0
                if candidate.types:
                    offensive_advantage = max(
                        self.type_multiplier(ct, opp_types) for ct in candidate.types if ct is not None
                    )
                # Only consider candidates with clear offensive advantage (>1x) AND strictly better defense than current
                if offensive_advantage > 1.0:
                    # Defensive risk: how hard opp's typing hits candidate's typing
                    defensive_risk = 1.0
                    if candidate.types:
                        defensive_risk = max(
                            self.type_multiplier(ot, candidate.types) for ot in opp_types if ot is not None
                        )
                    if not (defensive_risk < active_defensive_risk):
                        continue
                    score = offensive_advantage / (defensive_risk + 1e-6)
                    if score > best_score:
                        best_score = score
                        best_switch = candidate
            if best_switch is not None:
                # print(f"DEBUG: Switching to type-advantaged {best_switch.species} (score {best_score:.2f})")
                return self.create_order(best_switch)

        # PRIORITY 1: Use super effective moves if available
        if super_effective_moves:
           # print(f"DEBUG: Found {len(super_effective_moves)} super effective moves:")
            for mv, dmg, mult in super_effective_moves:
                mv_name = getattr(mv, 'name', getattr(mv, 'display_name', 'Unknown'))
            #    print(f"DEBUG:   - {mv_name}: damage={dmg:.3f}, effectiveness={mult}")
            
            # Sort by effectiveness first, then by damage within same effectiveness
            best_se_move = max(super_effective_moves, key=lambda x: (x[2], x[1]))  # (effectiveness, damage)
            move_name = getattr(best_se_move[0], 'name', getattr(best_se_move[0], 'display_name', 'Unknown'))
            # print(f"DEBUG: Selected SUPER EFFECTIVE move: {move_name} (damage: {best_se_move[1]:.3f}, effectiveness: {best_se_move[2]})")
            # print(f"DEBUG: *** RETURNING SUPER EFFECTIVE MOVE: {move_name} ***")
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
                
                # Switch if counter has super effective moves or if we're at a disadvantage,
                # BUT only if its defensive risk is strictly lower than our current defensive risk
                disadvantaged = self.opponent_has_advantage(my_types, opp_types, thresh=1.0)
                counter_defensive_risk = max(
                    (self.type_multiplier(ot, counter.types) for ot in opp_types if ot is not None),
                    default=1.0,
                )
                if (counter_has_se or disadvantaged) and (counter_defensive_risk < active_defensive_risk):
                    # print(f"DEBUG: Switching to {counter.species} (has SE: {counter_has_se}, disadvantaged: {disadvantaged}, def_risk {counter_defensive_risk:.2f} < {active_defensive_risk:.2f})")
                    return self.create_order(counter)

        # PRIORITY 3: Use neutral moves if available
        if neutral_moves:
            best_neutral_move = max(neutral_moves, key=lambda x: x[1])
            move_name = getattr(best_neutral_move[0], 'name', getattr(best_neutral_move[0], 'display_name', 'Unknown'))
            # print(f"DEBUG: Selected NEUTRAL move: {move_name} (damage: {best_neutral_move[1]:.3f})")
            return self.create_order(best_neutral_move[0])

        # PRIORITY 4: If only resisted moves remain, try switching one more time
        if resisted_moves and battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types)
            if counter:
                counter_defensive_risk = max(
                    (self.type_multiplier(ot, counter.types) for ot in opp_types if ot is not None),
                    default=1.0,
                )
                if counter_defensive_risk < active_defensive_risk:
                    # print(f"DEBUG: Switching due to only resisted moves available (safer defense {counter_defensive_risk:.2f} < {active_defensive_risk:.2f})")
                    return self.create_order(counter)

        # PRIORITY 5: Use best resisted move as last resort
        if resisted_moves:
            best_resisted_move = max(resisted_moves, key=lambda x: x[1])
            move_name = getattr(best_resisted_move[0], 'name', getattr(best_resisted_move[0], 'display_name', 'Unknown'))
            # print(f"DEBUG: Selected RESISTED move: {move_name} (damage: {best_resisted_move[1]:.3f})")
            return self.create_order(best_resisted_move[0])

        # Fallback to random move if no damaging moves available
        return self.choose_random_move(battle)