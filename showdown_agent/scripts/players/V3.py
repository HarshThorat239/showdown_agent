from poke_env.battle import AbstractBattle, side_condition, pokemon_type, move
from poke_env.player import Player
from poke_env.battle.pokemon_type import PokemonType
import poke_env.battle as battle

# Take speed into account when have a move which is x4 or x2 but opp is low on hp (75% or less)
team = """

Glimmora @ Focus Sash  
Ability: Toxic Debris  
Tera Type: Rock  
EVs: 252 HP / 252 Def  
Lax Nature  
- Spikes    
- Mortal Spin  
- Sludge Wave  
- Power Gem 

Iron Moth @ Booster Energy  
Ability: Quark Drive  
Tera Type: Fire  
EVs: 124 HP / 132 SpA / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Discharge  
- Flamethrower  
- Sludge Wave  
- Energy Ball  

Koraidon @ Expert Belt  
Ability: Orichalcum Pulse  
Tera Type: Fighting  
EVs: 252 Atk / 4 SpD / 252 Spe  
Adamant Nature  
- Collision Course  
- Dragon Claw  
- Flare Blitz  
- Iron Head  

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

Zacian-Crowned @ Rusted Sword  
Ability: Intrepid Sword  
Tera Type: Fairy  
EVs: 4 HP / 252 Atk / 252 Spe  
Jolly Nature  
- Sacred Sword  
- Behemoth Blade  
- Play Rough  
- Ice Fang  

Deoxys-Attack @ Focus Sash  
Ability: Pressure  
Tera Type: Ice  
EVs: 4 HP / 252 SpA / 252 Spe  
Hasty Nature  
IVs: 0 Atk  
- Psychic
- Ice Beam  
- Focus Blast  
- Thunderbolt  

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
        self.toxic_spikes = 0 
        self.curse = False
        self.opponent_last_move = None
        # Hazard moves that should trigger Defog
        self.hazard_moves = {
            'SPIKES', 'stealthrock', 'toxicspikes', 'stickyweb',
            'stealth rock', 'toxic spikes', 'sticky web', 'STICKYWEB',
            'STICKY WEB'
        }
        
        # State tracking for opponent switches after KO
        self.last_opponent_species = None
        self.opponent_just_switched_after_ko = False
        self.last_opponent_hp = None
    def teampreview(self, battle: AbstractBattle) -> str:
        # Reset battle-specific state at the start of each battle
        self.toxic_spikes = 0
        self.last_opponent_species = None
        self.opponent_just_switched_after_ko = False
        self.last_opponent_hp = None
        
        # Lead with the first PokÃ©mon, keep default order for the rest
        order = "/team " + "".join(str(i) for i in range(1, len(battle.team) + 1))
        return order

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

    def check_side_conditions(self, battle):
        # print(f"DEBUG: Checking side conditions...")
        # print(f"DEBUG: battle.side_conditions exists: {hasattr(battle, 'side_conditions')}")
        
        if hasattr(battle, 'side_conditions'):
            side_conditions = battle.side_conditions
            # print(f"DEBUG: side_conditions: {side_conditions}")
            if side_conditions:
                for condition in side_conditions:
                    # print(f"DEBUG: Checking condition '{condition}' against hazard_moves: {self.hazard_moves}")
                    
                    # Handle both string and object representations
                    condition_str = str(condition).upper()
                    # print(f"DEBUG: Normalized condition string: '{condition_str}'")
                    
                    # Check if any hazard move is contained in the condition string
                    hazard_detected = False
                    for hazard in self.hazard_moves:
                        if hazard.upper() in condition_str:
                            print(f"DEBUG: *** HAZARD DETECTED: {hazard} found in '{condition_str}' *** - Should use Defog!")
                            hazard_detected = True
                            break
                    
                    if hazard_detected:
                        return True
                    else:
                        # print(f"DEBUG: No hazard match found for '{condition_str}'")
            else:
                # print(f"DEBUG: No side conditions found")
        else:
            # print(f"DEBUG: battle object has no side_conditions attribute")
        
        # print(f"DEBUG: No hazards detected - continuing with normal move selection")
        return False
    
    def check_hp(self, battle):
        me = battle.active_pokemon
        if me.current_hp_fraction is not None and me.current_hp_fraction < 0.5:
            return True
        return False

    def check_enemy_hazards(self, battle):
        """
        Check if the enemy has spikes or stealth rock set up.
        Returns a dictionary with hazard information.
        """
        # print(f"DEBUG: Checking side conditions...")
        # print(f"DEBUG: battle.side_conditions exists: {hasattr(battle, 'side_conditions')}")
        
        if hasattr(battle, 'side_conditions'):
            side_conditions = battle.opponent_side_conditions
            # print(f"DEBUG: side_conditions: {side_conditions}")
            if side_conditions:
                for condition in side_conditions:
                    # print(f"DEBUG: Checking condition '{condition}' against hazard_moves: {self.hazard_moves}")
                    
                    # Handle both string and object representations
                    condition_str = str(condition).upper()
                    # print(f"DEBUG: Normalized condition string: '{condition_str}'")
                    
                    # Check if any hazard move is contained in the condition string
                    hazard_detected = False
                    for hazard in self.hazard_moves:
                        if hazard.upper() in condition_str:
                            print(f"DEBUG: *** HAZARD DETECTED: {hazard} found in '{condition_str}' ***")
                            hazard_detected = True
                            break
                    
                    if hazard_detected:
                        return True
                    else:
                        # print(f"DEBUG: No hazard match found for '{condition_str}'")
            else:
                # print(f"DEBUG: No side conditions found")
        else:
            # print(f"DEBUG: battle object has no side_conditions attribute")
        
        # print(f"DEBUG: No hazards detected - continuing with normal move selection")
        return False
        
    

    # ---------- POLICY ----------
    def choose_move(self, battle: AbstractBattle):
        opp = battle.opponent_active_pokemon
        me  = battle.active_pokemon
        opp_types = opp.types
        my_types  = me.types
        opp_hp    = opp.current_hp_fraction or 1.0
        
        # Detect opponent switches after KO
        current_opp_species = opp.species if opp else None
        current_opp_hp = opp_hp
        
        # Check if opponent just switched in after we defeated their previous PokÃ©mon
        if (self.last_opponent_species is not None and 
            current_opp_species != self.last_opponent_species and
            self.last_opponent_hp is not None and self.last_opponent_hp <= 0.0):
            self.opponent_just_switched_after_ko = True
            # print(f"DEBUG: *** OPPONENT SWITCHED IN {current_opp_species} AFTER KO ***")
        else:
            self.opponent_just_switched_after_ko = False
            
        # Update tracking variables
        self.last_opponent_species = current_opp_species
        self.last_opponent_hp = current_opp_hp

        moves = []
        super_effective_moves = []
        neutral_moves = []
        resisted_moves = []

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

    
        # if self.check_side_conditions(battle):
        # # Switch to Glimmora if available and use the first move available
        #     for poke in battle.available_switches:
        #         if getattr(poke, 'species', '').lower() == 'glimmora':
        #             print("DEBUG: Switching to Glimmora for hazard control.")
        #             return self.create_order(poke)
        #     if me.species.lower() == 'glimmora' and battle.available_moves:
        #         print("DEBUG: Glimmora is active, clearing hazards")
        #         return self.create_order(list(battle.available_moves)[1])

        # Only use Defog if Giratina is active AND there are actual hazards to clear
        if me.species == 'glimmora':
            # print(f"DEBUG: Glimmora is active")
            hazards_detected = self.check_side_conditions(battle)

            if hazards_detected:
                # print(f"DEBUG: Hazards detected - using mortal spin to clear them")
                return self.create_order(list(battle.available_moves)[1])
            else:
                # print(f"DEBUG: Hazards detected but Defog not found, continuing with normal move selection")    
                   
            enemy_hazards = self.check_enemy_hazards(battle)

            if not enemy_hazards:
                # print(f"DEBUG: Enemy has no spikes - using spikes")
                return self.create_order(list(battle.available_moves)[0])
            else:
                # print(f"DEBUG: Enemy already has spikes - not using spikes")          

            
            
       
        for mv in battle.available_moves:
            # Get move type - handle both direct type and type_id
            move_type = getattr(mv, 'type', None)
            if move_type is None:
                move_type = getattr(mv, 'type_id', None)
            if move_type is None:
                continue    
            # Debug output for troubleshooting
            move_name = getattr(mv, 'name', getattr(mv, 'display_name', 'Unknown'))
            
            # # ADDED DEBUG: Print move type detection for Flutter Mane vs Kingambit
            # if me.species == 'fluttermane' and opp.species == 'kingambit':
            #     print(f"DEBUG: Move {move_name} - type detection: type={getattr(mv, 'type', None)}, type_id={getattr(mv, 'type_id', None)}, final_type={move_type}")
                
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
            
            # # ADDED DEBUG: Print detailed move information for Flutter Mane vs Kingambit
            # if me.species == 'fluttermane' and opp.species == 'kingambit':
            #     print(f"DEBUG: Move {move_name} (type: {move_type}) vs {opp_types} = {raw_mult}x effectiveness, damage: {dmg:.3f}")
            
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

        # Debug: Show all available moves and their effectiveness
        # print(f"DEBUG: All available moves for {me.species} vs {opp.species} ({opp_types}):")
        # for mv in battle.available_moves:
        #     # Get move type - handle both direct type and type_id
        #     move_type = getattr(mv, 'type', None)
        #     if move_type is None:
        #         move_type = getattr(mv, 'type_id', None)
            
        #     # Get move name
        #     move_name = getattr(mv, 'name', None)
        #     if move_name is None:
        #         move_name = getattr(mv, 'display_name', None)
        #     if move_name is None:
        #         move_name = getattr(mv, 'id', 'Unknown')
            
        #     # Get effectiveness
        #     effectiveness = 1.0
        #     if move_type is not None:
        #         effectiveness = self.type_multiplier(move_type, opp_types)
            
        #     # Get PP and disabled status
        #     pp = getattr(mv, 'pp', 'Unknown')
        #     disabled = getattr(mv, 'disabled', False)
            
        #     print(f"DEBUG:   - {move_name} (type: {move_type}): effectiveness={effectiveness:.2f}, pp={pp}, disabled={disabled}")
        
        # print(f"DEBUG: Found {len(super_effective_moves)} super effective, {len(neutral_moves)} neutral, {len(resisted_moves)} resisted moves")

        # SPECIAL LOGIC: Handle opponent switches after KO
        if self.opponent_just_switched_after_ko:
            # print(f"DEBUG: *** SPECIAL LOGIC: Opponent switched in {opp.species} after KO ***")

            # Look for x4 effective moves first
            x4_effective_moves = []
            for mv, dmg, mult in moves:
                if mult >= 4.0:
                    x4_effective_moves.append((mv, dmg, mult))
                
                if x4_effective_moves:
                    best_x4_move = max(x4_effective_moves, key=lambda x: x[1])  # Sort by damage
                    move_name = getattr(best_x4_move[0], 'name', getattr(best_x4_move[0], 'display_name', 'Unknown'))
                    # print(f"DEBUG: *** USING x4 EFFECTIVE MOVE: {move_name} vs {opp.species} at {opp_hp:.1%} HP ***")
                    return self.create_order(best_x4_move[0])
            
            # Check if opponent is below 80% HP
            if opp_hp < 0.8:
                # print(f"DEBUG: *** Opponent {opp.species} is at {opp_hp:.1%} HP - checking for x4/x2 effective moves ***")
                
                # Look for x2 effective moves
                x2_effective_moves = []
                for mv, dmg, mult in moves:
                    if mult >= 2.0:
                        x2_effective_moves.append((mv, dmg, mult))
                
                if x2_effective_moves:
                    best_x2_move = max(x2_effective_moves, key=lambda x: x[1])  # Sort by damage
                    move_name = getattr(best_x2_move[0], 'name', getattr(best_x2_move[0], 'display_name', 'Unknown'))
                    # print(f"DEBUG: *** USING x2 EFFECTIVE MOVE: {move_name} vs {opp.species} at {opp_hp:.1%} HP ***")
                    return self.create_order(best_x2_move[0])
                
                # print(f"DEBUG: *** No x4/x2 effective moves available - proceeding with normal logic ***")
           

       
        if super_effective_moves and me.base_stats['spe'] > opp.base_stats['spe']:
            
            # First, check if any super effective moves can KO
            for m, dmg, mult in sorted(super_effective_moves, key=lambda x: (x[2], x[1]), reverse=True):
                # Sort by effectiveness first, then by damage within same effectiveness
                if dmg >= opp_hp + 0.1:
                    move_name = getattr(m, 'name', getattr(m, 'display_name', 'Unknown'))
                    return self.create_order(m)
            
            # If no super effective moves can KO, then check neutral moves
            for m, dmg, mult in sorted(moves, key=lambda x: x[1], reverse=True):
                # Only consider it a guaranteed KO if damage is significantly higher than HP
                # and the move is at least neutral effectiveness
                if dmg >= opp_hp + 0.1 and mult >= 1.0:
                    move_name = getattr(m, 'name', getattr(m, 'display_name', 'Unknown'))
                    return self.create_order(m)

        # PRIORITY 1: Switch to Pokemon with type advantage against opponent
        # If any bench Pokemon has a type that is super-effective vs opponent, switch to it
        # We prioritize offensive advantage over defensive risk for type-advantaged switches
        # print(f"DEBUG: Checking for type-advantaged switches against {opp.species} ({opp_types})...")
        
        # First, evaluate the current active Pokemon
        current_offensive_advantage = 0.0
        if me.types:
            current_offensive_advantage = max(
                self.type_multiplier(ct, opp_types) for ct in me.types if ct is not None
            )
        # print(f"DEBUG: Current {me.species} offensive advantage vs {opp.species}: {current_offensive_advantage:.2f}")
        # print(f"DEBUG: Current {me.species} defensive risk vs {opp.species}: {active_defensive_risk:.2f}")
        
        # Calculate current Pokemon's score
        current_base_score = current_offensive_advantage * 2.0 - active_defensive_risk
        current_defensive_bonus = 0.0  # Current Pokemon can't have defensive bonus against itself
        current_bonus = 1.0  # Current Pokemon always gets current bonus
        switch_penalty = 1.0 if super_effective_moves else 0.0
        current_score = current_base_score + current_defensive_bonus + current_bonus - switch_penalty
        # print(f"DEBUG: Current {me.species} score breakdown: base={current_base_score:.2f}, def_bonus={current_defensive_bonus:.2f}, current_bonus={current_bonus:.2f}, switch_penalty={switch_penalty:.2f}, total={current_score:.2f}")
        
        best_switch = None
        best_score = current_score  # Start with current Pokemon's score
        
        if battle.available_switches:
            for candidate in battle.available_switches:
                # Offensive advantage: best of candidate's types vs opponent's types
                offensive_advantage = 0.0
                if candidate.types:
                    offensive_advantage = max(
                        self.type_multiplier(ct, opp_types) for ct in candidate.types if ct is not None
                    )
                # print(f"DEBUG: {candidate.species} offensive advantage vs {opp.species}: {offensive_advantage:.2f}")
                
                # Only consider candidates with clear offensive advantage (>1x)
                if offensive_advantage > 1.0:
                    # Defensive risk: how hard opp's typing hits candidate's typing
                    defensive_risk = 1.0
                    if candidate.types:
                        defensive_risk = max(
                            self.type_multiplier(ot, candidate.types) for ot in opp_types if ot is not None
                        )
                    # print(f"DEBUG: {candidate.species} defensive risk vs {opp.species}: {defensive_risk:.2f} (current: {active_defensive_risk:.2f})")
                    
                    # For type-advantaged switches, we're more lenient on defensive risk
                    # Only reject if the defensive risk is significantly worse (2x or more)
                    if defensive_risk >= 2.0 and active_defensive_risk < 2.0:
                        # print(f"DEBUG: Rejected {candidate.species} - too high defensive risk ({defensive_risk:.2f})")
                        continue
                    
                    # Calculate score with multiple factors for better decision making
                    # Base score from offensive advantage
                    base_score = offensive_advantage * 2.0 - defensive_risk
                    
                    # Bonus for better defensive typing (if defensive risk is lower than current)
                    defensive_bonus = 0.0
                    if defensive_risk < active_defensive_risk:
                        defensive_bonus = (active_defensive_risk - defensive_risk) * 0.5
                    
                    # Bonus for being the current active Pokemon (prevent unnecessary switches)
                    current_bonus = 0.0
                    if candidate.species == me.species:
                        current_bonus = 1.0
                    
                    # Penalty for switching when we have super effective moves
                    switch_penalty = 0.0
                    if super_effective_moves:
                        switch_penalty = 1.0
                    
                    score = base_score + defensive_bonus + current_bonus - switch_penalty
                    # print(f"DEBUG: {candidate.species} score breakdown: base={base_score:.2f}, def_bonus={defensive_bonus:.2f}, current_bonus={current_bonus:.2f}, switch_penalty={switch_penalty:.2f}, total={score:.2f}")
                    
                    # Only switch if the candidate has a strictly better score than current
                    if score > best_score:
                        best_score = score
                        best_switch = candidate
            if best_switch is not None and best_switch.species != me.species:
                # print(f"DEBUG: Switching to type-advantaged {best_switch.species} (score {best_score:.2f})")
                return self.create_order(best_switch)
            else:
                # print(f"DEBUG: Keeping current Pokemon {me.species} (best score {best_score:.2f})")

        # PRIORITY 2: Use super effective moves if available
        if super_effective_moves:
            # print(f"DEBUG: Found {len(super_effective_moves)} super effective moves:")
            for mv, dmg, mult in super_effective_moves:
                # Try multiple ways to get move name
                mv_name = getattr(mv, 'name', None)
                if mv_name is None:
                    mv_name = getattr(mv, 'display_name', None)
                if mv_name is None:
                    mv_name = getattr(mv, 'id', 'Unknown')
                # print(f"DEBUG:   - {mv_name}: damage={dmg:.3f}, effectiveness={mult}")
            
            # Sort by effectiveness first, then by damage within same effectiveness
            best_se_move = max(super_effective_moves, key=lambda x: (x[2], x[1]))  # (effectiveness, damage)
            # Try multiple ways to get move name
            move_name = getattr(best_se_move[0], 'name', None)
            if move_name is None:
                move_name = getattr(best_se_move[0], 'display_name', None)
            if move_name is None:
                move_name = getattr(best_se_move[0], 'id', 'Unknown')
            # print(f"DEBUG: Selected SUPER EFFECTIVE move: {move_name} (damage: {best_se_move[1]:.3f}, effectiveness: {best_se_move[2]})")
            # print(f"DEBUG: *** RETURNING SUPER EFFECTIVE MOVE: {move_name} ***")
            return self.create_order(best_se_move[0])
        # else:
        #     # ADDED DEBUG: If no super effective moves found, show what moves are available
        #     if me.species == 'fluttermane' and opp.species == 'kingambit':
        #         print(f"DEBUG: *** NO SUPER EFFECTIVE MOVES FOUND for Flutter Mane vs Kingambit ***")
        #         print(f"DEBUG: Available moves: {[getattr(mv, 'name', getattr(mv, 'display_name', 'Unknown')) for mv in battle.available_moves]}")
        #         print(f"DEBUG: Move effectiveness: {[(getattr(mv, 'name', getattr(mv, 'display_name', 'Unknown')), mult) for mv, dmg, mult in moves]}")


        
        # PRIORITY 3: If no super effective moves, consider switching to a better Pokemon
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

         # Check if we can KO with any move (but be more conservative)
        for m, dmg, mult in sorted(moves, key=lambda x: x[1], reverse=True):
            # Only consider it a guaranteed KO if damage is significantly higher than HP
            # and the move is at least neutral effectiveness
            if dmg >= opp_hp + 0.1 and mult >= 1.0:
                move_name = getattr(m, 'name', getattr(m, 'display_name', 'Unknown'))
                # print(f"DEBUG: *** GUARANTEED KO MOVE SELECTED: {move_name} (damage: {dmg:.3f} vs HP: {opp_hp:.3f}) ***")
                return self.create_order(m)


        # PRIORITY 4: Use neutral moves if available
        if neutral_moves:
            best_neutral_move = max(neutral_moves, key=lambda x: x[1])
            move_name = getattr(best_neutral_move[0], 'name', getattr(best_neutral_move[0], 'display_name', 'Unknown'))
            # print(f"DEBUG: Selected NEUTRAL move: {move_name} (damage: {best_neutral_move[1]:.3f})")
            return self.create_order(best_neutral_move[0])

        # PRIORITY 5: If only resisted moves remain, try switching one more time
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

        # PRIORITY 6: Use best resisted move as last resort
        if resisted_moves:
            best_resisted_move = max(resisted_moves, key=lambda x: x[1])
            move_name = getattr(best_resisted_move[0], 'name', getattr(best_resisted_move[0], 'display_name', 'Unknown'))
            # print(f"DEBUG: Selected RESISTED move: {move_name} (damage: {best_resisted_move[1]:.3f})")
            return self.create_order(best_resisted_move[0])

        # Fallback to random move if no damaging moves available
        return self.choose_random_move(battle)