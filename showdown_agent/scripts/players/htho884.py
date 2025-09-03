from poke_env.battle import AbstractBattle, side_condition, pokemon_type, move
from poke_env.player import Player
from poke_env.battle.pokemon_type import PokemonType
import poke_env.battle as battle

# Take speed into account when have a move which is x4 or x2 but opp is low on hp (75% or less)
team = """

Ribombee @ Focus Sash
Ability: Shield Dust
Tera Type: Ghost
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
IVs: 0 Atk
- Sticky Web
- Moonblast
- Bug Buzz
- Energy Ball

Eternatus @ Life Orb
Ability: Pressure
Tera Type: Dragon
EVs: 64 HP / 252 SpA / 192 Spe
Modest Nature
IVs: 0 Atk
- Dynamax Cannon
- Sludge Bomb
- Recover
- Fire Blast  

Koraidon @ Expert Belt  
Ability: Orichalcum Pulse  
Tera Type: Fighting  
EVs: 252 Atk / 4 SpD / 252 Spe  
Adamant Nature  
- Collision Course  
- Scale Shot  
- Flare Blitz  
- Iron Head  

Ho-Oh @ Choice Scarf  
Ability: Regenerator  
Tera Type: Fairy  
EVs: 252 Atk / 252 Spe  
Jolly Nature  
- Sacred Fire  
- Brave Bird  
- Earthquake  
- Iron Head

Zacian-Crowned @ Rusted Sword  
Ability: Intrepid Sword  
Tera Type: Fairy  
EVs: 4 HP / 252 Atk / 252 Spe  
Jolly Nature  
- Sacred Sword  
- Behemoth Blade  
- Play Rough  
- Ice Fang  

Kyogre @ Choice Scarf  
Ability: Drizzle  
Tera Type: Water  
EVs: 4 HP / 252 SpA / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Water Spout
- Thunder    
- Surf  
- Ice Beam 

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

    
        self.toxic_spikes = 0 
        self.curse = False
        self.opponent_last_move = None
        # Hazard moves that should trigger Defog
        self.hazard_moves = {
            'SPIKES', 'stealthrock', 'toxicspikes', 'stickyweb',
            'STEALTH_ROCK', 'toxic spikes', 'sticky web', 'STICKYWEB',
            'STICKY_WEB', 'spikes'
        }
        
        # State tracking for opponent switches after KO
        self.last_opponent_species = None
        self.opponent_just_switched_after_ko = False
        self.last_opponent_hp = None
        
        # Move memory tracking
        self.last_attack_move = None
        self.last_attack_damage = None
        self.last_attack_target = None
        self.last_attack_target_hp_before = None
    def teampreview(self, battle: AbstractBattle) -> str:
        # Reset battle-specific state at the start of each battle
        self.toxic_spikes = 0
        self.last_opponent_species = None
        self.opponent_just_switched_after_ko = False
        self.last_opponent_hp = None
        
        # Reset move memory tracking
        self.last_attack_move = None
        self.last_attack_damage = None
        self.last_attack_target = None
        self.last_attack_target_hp_before = None
        
        # Lead with the first PokÃ©mon, keep default order for the rest
        order = "/team " + "".join(str(i) for i in range(1, len(battle.team) + 1))
        return order

    # ---------- TYPE HELPERS ----------
    def type_multiplier(self, atk_type, def_types, battle=None):
        mult = 1.0
        inner = TYPE_EFFECTIVENESS.get(atk_type, {})
        for i in def_types:
            if i is None:
                continue
            mult *= inner.get(i, 1.0)
        
        # Apply weather effects if battle object is provided
        if battle and hasattr(battle, 'weather') and battle.weather:
            weather_name = battle.weather.get('name', '').lower()
            
            # Sunny Day boosts Fire moves by 50%
            if weather_name == 'sun' and atk_type == PokemonType.FIRE:
                mult *= 1.5
            
            # Rain/Drizzle boosts Water moves by 50%
            elif weather_name == 'rain' and atk_type == PokemonType.WATER:
                mult *= 1.5
        
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
            'voltabsorb': PokemonType.ELECTRIC,
            'motordrive': PokemonType.ELECTRIC,
            'soundproof': None,  # Immune to sound-based moves (handled separately)
            'bulletproof': None,  # Immune to ball/bomb/bullet moves (handled separately)
            'overcoat': None,  # Immune to powder moves and weather effects
            'magicguard': None,  # Immune to indirect damage
            'wonderguard': None,  # Only damaged by super effective moves
            'filter': None,  # Reduces super effective damage
            'solidrock': None,  # Reduces super effective damage
            'prismarmor': None,  # Reduces super effective damage
            'shadowshield': None,  # Reduces damage when at full HP
            'multiscale': None,  # Reduces damage when at full HP
        }
        
        # Check for type-based immunities
        if immunity_map.get(ability_name) == move_type:
            return True
            
        # Check for special ability immunities
        if ability_name == 'soundproof':
            # This would need move name checking, but we don't have that context here
            # Return False for now as this method focuses on type immunities
            return False
            
        return False

    def would_be_immune_to_opponent_moves(self, candidate_pokemon, opp_types, opp_ability):
        """
        Check if a candidate Pokemon would be immune to opponent's likely moves.
        This considers both type immunities and ability-based immunities.
        """
        if not candidate_pokemon.types or not opp_types:
            return False, 0.0
            
        immunity_score = 0.0
        
        # Check type-based immunities
        for opp_type in opp_types:
            if opp_type is None:
                continue
                
            # Check if candidate has immunity to this type
            for candidate_type in candidate_pokemon.types:
                if candidate_type is None:
                    continue
                    
                # Check ability-based immunities
                candidate_ability = getattr(candidate_pokemon, 'ability', None)
                if candidate_ability and self.is_move_immune(opp_type, candidate_ability):
                    immunity_score += 2.0
                    print(f"DEBUG: {candidate_pokemon.species} immune to {opp_type} due to {candidate_ability}")
                    break
                    
                # Check type chart immunities (0x effectiveness)
                if hasattr(self, 'type_multiplier'):
                    mult = self.type_multiplier(opp_type, [candidate_type], None)
                    if mult == 0.0:
                        immunity_score += 1.5
                        print(f"DEBUG: {candidate_pokemon.species} type-immune to {opp_type}")
                        break
        
        return immunity_score > 0.0, immunity_score

    def check_weather_immunities(self, candidate_pokemon, battle):
        """
        Check if a Pokemon has immunities based on weather conditions.
        """
        if not hasattr(battle, 'weather') or not battle.weather:
            return 0.0
            
        # Handle weather as either a string or dictionary
        weather = battle.weather
        if isinstance(weather, dict):
            # If weather is a dictionary, try to get the weather name
            weather_name = weather.get('name', '').lower() if hasattr(weather, 'get') else str(weather).lower()
        else:
            weather_name = str(weather).lower()
            
        immunity_score = 0.0
        
        # Check for weather-based immunities
        if 'sandstorm' in weather_name:
            # Rock, Ground, Steel types are immune to sandstorm damage
            if candidate_pokemon.types:
                for pokemon_type in candidate_pokemon.types:
                    if pokemon_type in [PokemonType.ROCK, PokemonType.GROUND, PokemonType.STEEL]:
                        immunity_score += 0.5
                        break
        elif 'hail' in weather_name:
            # Ice types are immune to hail damage
            if candidate_pokemon.types:
                for pokemon_type in candidate_pokemon.types:
                    if pokemon_type == PokemonType.ICE:
                        immunity_score += 0.5
                        break
                        
        return immunity_score

    def check_status_immunities(self, candidate_pokemon, opp_types):
        """
        Check if a Pokemon has immunities to common status conditions.
        This is useful for switching decisions against status-heavy opponents.
        """
        immunity_score = 0.0
        
        if not candidate_pokemon.types:
            return immunity_score
            
        # Check for type-based status immunities
        for pokemon_type in candidate_pokemon.types:
            if pokemon_type == PokemonType.POISON:
                # Poison types are immune to poison status
                immunity_score += 0.5
            elif pokemon_type == PokemonType.ELECTRIC:
                # Electric types are immune to paralysis
                immunity_score += 0.3
            elif pokemon_type == PokemonType.FIRE:
                # Fire types are immune to burn
                immunity_score += 0.3
            elif pokemon_type == PokemonType.ICE:
                # Ice types are immune to freeze
                immunity_score += 0.3
                
        # Check for ability-based status immunities
        candidate_ability = getattr(candidate_pokemon, 'ability', None)
        if candidate_ability:
            ability_name = candidate_ability.lower()
            if ability_name in ['limber', 'vitalspirit']:
                # Immune to paralysis
                immunity_score += 0.5
            elif ability_name in ['waterveil', 'magmaarmor']:
                # Immune to burn
                immunity_score += 0.5
            elif ability_name in ['insomnia', 'vitalspirit']:
                # Immune to sleep
                immunity_score += 0.5
            elif ability_name in ['immunity', 'pastelveil']:
                # Immune to poison
                immunity_score += 0.5
                
        return immunity_score

    def check_hazard_immunities(self, candidate_pokemon, battle):
        """
        Check if a Pokemon has immunities to entry hazards.
        This is crucial for switching decisions when the opponent has set up hazards.
        """
        immunity_score = 0.0
        
        if not candidate_pokemon.types:
            return immunity_score
            
        # Check for type-based hazard immunities
        for pokemon_type in candidate_pokemon.types:
            if pokemon_type == PokemonType.FLYING:
                # Flying types are immune to Spikes and Toxic Spikes
                immunity_score += 1.0
                
        # Check for ability-based hazard immunities
        candidate_ability = getattr(candidate_pokemon, 'ability', None)
        if candidate_ability:
            ability_name = candidate_ability.lower()
            if ability_name == 'levitate':
                # Immune to Spikes and Toxic Spikes
                immunity_score += 1.0
            elif ability_name == 'magicguard':
                # Immune to all indirect damage including hazards
                immunity_score += 1.5
            elif ability_name == 'overcoat':
                # Immune to powder moves and weather effects
                immunity_score += 0.5
                
        return immunity_score

    def estimated_effectiveness(self, move_type, opp_types, my_types, battle=None):
        eff = self.type_multiplier(move_type, opp_types, battle)
        if move_type in my_types:
            eff *= 1.5
        return eff

    def estimate_damage_frac(self, mv, my_types, opp_types, battle=None):
        bp = getattr(mv, "base_power", 0) or 0
        if bp <= 0:
            return 0.0
        
        # Get move type - handle both direct type and type_id
        move_type = getattr(mv, 'type', None)
        if move_type is None:
            move_type = getattr(mv, 'type_id', None)
        
        if move_type is None:
            return 0.0
            
        eff = self.estimated_effectiveness(move_type, opp_types, my_types, battle)
        return max(0.0, min((bp / 100.0) * eff, 1.0))

    def opponent_has_advantage(self, my_types, opp_types, thresh=1.0, battle=None):
        return any(self.type_multiplier(otype, my_types, battle) > thresh for otype in opp_types)

    def pick_best_switch(self, battle, opp_types, current_pokemon=None, super_effective_moves=None):
        """
        Enhanced method to pick the best switch using complex scoring system.
        Considers offensive advantage, defensive risk, current bonus, switch penalties, and move immunities.
        """
        if not battle.available_switches:
            return None
            
        # Handle forced switch scenario (current_pokemon is None)
        is_forced_switch = current_pokemon is None
        
        # If current_pokemon not provided, use the active one
        if current_pokemon is None:
            current_pokemon = battle.active_pokemon
            
        # If super_effective_moves not provided, calculate them
        if super_effective_moves is None:
            super_effective_moves = []
            for mv in battle.available_moves:
                move_type = getattr(mv, 'type', None)
                if move_type is None:
                    move_type = getattr(mv, 'type_id', None)
                if move_type is None:
                    continue
                    
                raw_mult = self.type_multiplier(move_type, opp_types, battle)
                if raw_mult > 1.0:
                    super_effective_moves.append(mv)
        
        # Get opponent's ability for immunity checking
        opp_ability = None
        if hasattr(battle, 'opponent_active_pokemon') and battle.opponent_active_pokemon:
            opp_ability = getattr(battle.opponent_active_pokemon, 'ability', None)
        
        # Initialize variables that will be used in both forced and regular switch scenarios
        current_defensive_risk = 1.0  # Default value
        current_offensive_advantage = 0.0  # Default value
        current_score = 0.0  # Default value
        
        # For forced switches, we don't have a current Pokemon to compare against
        if is_forced_switch:
            print(f"DEBUG: *** FORCED SWITCH EVALUATION - No current Pokemon to compare against ***")
            best_switch = None
            best_score = float("-inf")  # Start with worst possible score
        else:
            # Calculate current Pokemon's defensive risk
            current_defensive_risk = max(
                (self.type_multiplier(ot, current_pokemon.types, battle) for ot in opp_types if ot is not None),
                default=1.0,
            )
            
            # Calculate current Pokemon's offensive advantage
            if current_pokemon.types:
                current_offensive_advantage = max(
                    self.type_multiplier(ct, opp_types, battle) for ct in current_pokemon.types if ct is not None
                )
            
            # Calculate current Pokemon's score
            current_base_score = current_offensive_advantage * 2.0 - current_defensive_risk
            current_defensive_bonus = 0.0  # Current Pokemon can't have defensive bonus against itself
            current_bonus = 1.0  # Current Pokemon always gets current bonus
            switch_penalty = 1.0 if super_effective_moves else 0.0
            current_score = current_base_score + current_defensive_bonus + current_bonus - switch_penalty
            
            print(f"DEBUG: Current {current_pokemon.species} score breakdown: base={current_base_score:.2f}, def_bonus={current_defensive_bonus:.2f}, current_bonus={current_bonus:.2f}, switch_penalty={switch_penalty:.2f}, total={current_score:.2f}")
            
            best_switch = None
            best_score = current_score  # Start with current Pokemon's score
        
        for candidate in battle.available_switches:
            # Offensive advantage: best of candidate's types vs opponent's types
            offensive_advantage = 0.0
            if candidate.types:
                offensive_advantage = max(
                    self.type_multiplier(ct, opp_types, battle) for ct in candidate.types if ct is not None
                )
            print(f"DEBUG: {candidate.species} offensive advantage vs opponent: {offensive_advantage:.2f}")
            
            # For forced switches, consider all candidates; for regular switches, only consider those with offensive advantage
            if is_forced_switch or offensive_advantage > 1.0:
                # Defensive risk: how hard opp's typing hits candidate's types
                defensive_risk = 1.0
                if candidate.types:
                    defensive_risk = max(
                        self.type_multiplier(ot, candidate.types, battle) for ot in opp_types if ot is not None
                    )
                print(f"DEBUG: {candidate.species} defensive risk vs opponent: {defensive_risk:.2f} (current: {current_defensive_risk:.2f})")
                
                # IMMUNITY BONUS: Check if candidate is immune to opponent's likely moves
                immunity_bonus = 0.0
                if opp_ability and candidate.types:
                    # Check if candidate is immune to any of opponent's types due to abilities
                    for opp_type in opp_types:
                        if opp_type and self.is_move_immune(opp_type, opp_ability):
                            # Check if candidate would be immune to this move type
                            for candidate_type in candidate.types:
                                if candidate_type and self.is_move_immune(opp_type, getattr(candidate, 'ability', None)):
                                    immunity_bonus += 2.0  # Significant bonus for immunity
                                    print(f"DEBUG: {candidate.species} gets immunity bonus for {opp_type} moves")
                                    break
                
                # Use the enhanced immunity checking method
                has_immunity, immunity_score = self.would_be_immune_to_opponent_moves(candidate, opp_types, opp_ability)
                if has_immunity:
                    immunity_bonus += immunity_score
                    print(f"DEBUG: {candidate.species} gets enhanced immunity bonus: {immunity_score:.2f}")
                
                # Check for weather-based immunities
                weather_immunity_bonus = self.check_weather_immunities(candidate, battle)
                if weather_immunity_bonus > 0.0:
                    immunity_bonus += weather_immunity_bonus
                    print(f"DEBUG: {candidate.species} gets weather immunity bonus: {weather_immunity_bonus:.2f}")
                
                # Check for status immunities
                status_immunity_bonus = self.check_status_immunities(candidate, opp_types)
                if status_immunity_bonus > 0.0:
                    immunity_bonus += status_immunity_bonus
                    print(f"DEBUG: {candidate.species} gets status immunity bonus: {status_immunity_bonus:.2f}")
                
                # Check for hazard immunities
                hazard_immunity_bonus = self.check_hazard_immunities(candidate, battle)
                if hazard_immunity_bonus > 0.0:
                    immunity_bonus += hazard_immunity_bonus
                    print(f"DEBUG: {candidate.species} gets hazard immunity bonus: {hazard_immunity_bonus:.2f}")
                
                # Total immunity bonus for scoring
                total_immunity_bonus = immunity_bonus
                
                # For type-advantaged switches, we're more lenient on defensive risk
                # Only reject if the defensive risk is significantly worse (2x or more)
                # For forced switches, be even more lenient since we have to pick someone
                if not is_forced_switch and defensive_risk >= 2.0 and current_defensive_risk < 2.0:
                    print(f"DEBUG: Rejected {candidate.species} - too high defensive risk ({defensive_risk:.2f})")
                    continue
                
                # Calculate score with multiple factors for better decision making
                # Base score from offensive advantage
                base_score = offensive_advantage * 2.0 - defensive_risk
                
                # Bonus for better defensive typing (if defensive risk is lower than current)
                defensive_bonus = 0.0
                if not is_forced_switch and defensive_risk < current_defensive_risk:
                    defensive_bonus = (current_defensive_risk - defensive_risk) * 0.5
                
                # Bonus for being the current active Pokemon (prevent unnecessary switches)
                candidate_current_bonus = 0.0
                if not is_forced_switch and candidate.species == current_pokemon.species:
                    candidate_current_bonus = 1.0
                
                # Penalty for switching when we have super effective moves
                candidate_switch_penalty = 0.0
                if super_effective_moves:
                    candidate_switch_penalty = 1.0
                
                # Add immunity bonus to the score
                score = base_score + defensive_bonus + candidate_current_bonus + total_immunity_bonus - candidate_switch_penalty
                print(f"DEBUG: {candidate.species} score breakdown: base={base_score:.2f}, def_bonus={defensive_bonus:.2f}, current_bonus={candidate_current_bonus:.2f}, immunity_bonus={total_immunity_bonus:.2f}, switch_penalty={candidate_switch_penalty:.2f}, total={score:.2f}")
                
                # For forced switches, pick the best absolute score; for regular switches, only if better than current
                if is_forced_switch:
                    if score > best_score:
                        best_score = score
                        best_switch = candidate
                else:
                    # Only switch if the candidate has a strictly better score than current
                    if score > best_score:
                        best_score = score
                        best_switch = candidate
        
        if is_forced_switch:
            if best_switch is not None:
                print(f"DEBUG: *** FORCED SWITCH: Selected {best_switch.species} as best Pokemon to send out (score {best_score:.2f}) ***")
            else:
                print(f"DEBUG: *** FORCED SWITCH: No suitable Pokemon found, will use fallback ***")
        else:
            if best_switch is not None and best_switch.species != current_pokemon.species:
                print(f"DEBUG: Selected {best_switch.species} as best switch (score {best_score:.2f})")
            else:
                print(f"DEBUG: Keeping current Pokemon {current_pokemon.species} (best score {best_score:.2f})")
            
        return best_switch

    
    def check_side_conditions(self, battle):
        print(f"DEBUG: Checking side conditions...")
        print(f"DEBUG: battle.side_conditions exists: {hasattr(battle, 'side_conditions')}")
        
        if hasattr(battle, 'side_conditions'):
            side_conditions = battle.side_conditions
            print(f"DEBUG: side_conditions: {side_conditions}")
            if side_conditions:
                for condition in side_conditions:
                    print(f"DEBUG: Checking condition '{condition}' against hazard_moves: {self.hazard_moves}")
                    
                    # Handle both string and object representations
                    condition_str = str(condition).upper()
                    print(f"DEBUG: Normalized condition string: '{condition_str}'")
                    
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
                        print(f"DEBUG: No hazard match found for '{condition_str}'")
            else:
                print(f"DEBUG: No side conditions found")
        else:
            print(f"DEBUG: battle object has no side_conditions attribute")
        
        print(f"DEBUG: No hazards detected - continuing with normal move selection")
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
        print(f"DEBUG: Checking side conditions...")
        print(f"DEBUG: battle.side_conditions exists: {hasattr(battle, 'side_conditions')}")
        
        if hasattr(battle, 'side_conditions'):
            side_conditions = battle.opponent_side_conditions
            print(f"DEBUG: side_conditions: {side_conditions}")
            if side_conditions:
                for condition in side_conditions:
                    print(f"DEBUG: Checking condition '{condition}' against hazard_moves: {self.hazard_moves}")
                    
                    # Handle both string and object representations
                    condition_str = str(condition).upper()
                    print(f"DEBUG: Normalized condition string: '{condition_str}'")
                    
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
                        print(f"DEBUG: No hazard match found for '{condition_str}'")
            else:
                print(f"DEBUG: No side conditions found")
        else:
            print(f"DEBUG: battle object has no side_conditions attribute")
        
        print(f"DEBUG: No hazards detected - continuing with normal move selection")
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
            print(f"DEBUG: *** OPPONENT SWITCHED IN {current_opp_species} AFTER KO ***")
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
            (self.type_multiplier(ot, my_types, battle) for ot in opp_types if ot is not None),
            default=1.0,
        )

        # If forced to switch (e.g., after a pivot), use enhanced evaluation to pick best counter
        if not battle.available_moves and battle.available_switches:
            print(f"DEBUG: *** FORCED SWITCH - Using enhanced evaluation to pick best Pokemon ***")
            
            # Use the enhanced pick_best_switch method to find the best Pokemon to send out
            # Pass None as current_pokemon since we're not switching from an active Pokemon
            best_counter = self.pick_best_switch(battle, opp_types, None, super_effective_moves)
            if best_counter:
                print(f"DEBUG: *** FORCED SWITCH: Sending out {best_counter.species} ***")
                return self.create_order(best_counter)
            
            # Fallback: if no good switch found, pick the first available
            fallback_switch = list(battle.available_switches)[0]
            print(f"DEBUG: *** FORCED SWITCH FALLBACK: Sending out {fallback_switch.species} ***")
            return self.create_order(fallback_switch)

    
            
       
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
                
            raw_mult = self.type_multiplier(move_type, opp_types, battle)
            if raw_mult == 0.0:
                continue
            
            # Check for ability-based immunities
            opp_ability = getattr(opp, 'ability', None)
            if self.is_move_immune(move_type, opp_ability):
                # print(f"DEBUG: Move {move_name} is immune due to {opp_ability}")
                continue
            # Bulletproof: immune to moves with "ball", "bomb", or "bullet" in the name
            if opp_ability and str(opp_ability).lower() == 'bulletproof':
                name_lower = str(move_name).lower()
                if any(keyword in name_lower for keyword in ['ball', 'bomb', 'bullet']):
                    # print(f"DEBUG: Skipping {move_name} due to Bulletproof immunity")
                    continue
            dmg = self.estimate_damage_frac(mv, my_types, opp_types, battle)
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
                print(f"DEBUG: {move_name} categorized as SUPER EFFECTIVE")
            elif abs(raw_mult - 1.0) < 1e-9:
                neutral_moves.append((mv, dmg, raw_mult))
                print(f"DEBUG: {move_name} categorized as NEUTRAL")
            else:
                resisted_moves.append((mv, dmg, raw_mult))
                print(f"DEBUG: {move_name} categorized as RESISTED")

        # Only use Defog if Giratina is active AND there are actual hazards to clear
        if me.species == 'ribombee':   
            enemy_hazards = self.check_enemy_hazards(battle)
            if not enemy_hazards:
                print(f"DEBUG: Enemy has no spikes - using spikes")
                return self.create_order(list(battle.available_moves)[0])
            else:
                print(f"DEBUG: Enemy already has spikes - not using spikes")  

        if me.species == 'eternatus' and (me.current_hp_fraction or 1.0) < 0.45:
            for mv in battle.available_moves:
                if getattr(mv, 'name', '').lower() == 'recover':
                    return self.create_order(mv)


        if me.item == 'choicescarf':
            # If all available moves are resisted or immune, and a switch is available,
            # switch to a pokemon with both defensive and offensive advantage.
            if not super_effective_moves and not neutral_moves and resisted_moves:
                # Try to switch to a Pokemon with advantage over the opponent's current active Pokemon
                best_switch = self.pick_best_switch(
                    battle,
                    current_pokemon=me,
                    opp_types=opp.types if hasattr(opp, "types") else [],
                    super_effective_moves=super_effective_moves if super_effective_moves else None,
                )
                if best_switch is not None and best_switch.species != me.species:
                    print(f"DEBUG: Switching to {best_switch.species} for advantage over {opp.species}")
                    return self.create_order(best_switch)
                # If no good switch found, continue as normal
                
        # SPECIAL LOGIC: Handle opponent switches after KO
        if self.opponent_just_switched_after_ko:
            print(f"DEBUG: *** SPECIAL LOGIC: Opponent switched in {opp.species} after KO ***")

            # Look for moves with 3x or higher effectiveness first
            high_effective_moves = []
            for mv, dmg, mult in moves:
                if mult >= 3.0:
                    high_effective_moves.append((mv, dmg, mult))
                
            if high_effective_moves:
                best_high_move = max(high_effective_moves, key=lambda x: x[1])  # Sort by damage
                move_name = getattr(best_high_move[0], 'name', getattr(best_high_move[0], 'display_name', 'Unknown'))
                print(f"DEBUG: *** USING {best_high_move[2]}x EFFECTIVE MOVE: {move_name} vs {opp.species} at {opp_hp:.1%} HP ***")
                return self.create_order(best_high_move[0])
            
            # Check if opponent is below 80% HP
            if opp_hp < 0.8:
                print(f"DEBUG: *** Opponent {opp.species} is at {opp_hp:.1%} HP - checking for x4/x2 effective moves ***")
                
                # Look for x2 effective moves
                x2_effective_moves = []
                for mv, dmg, mult in moves:
                    if mult >= 2.0:
                        x2_effective_moves.append((mv, dmg, mult))
                
                if x2_effective_moves:
                    best_x2_move = max(x2_effective_moves, key=lambda x: x[1])  # Sort by damage
                    move_name = getattr(best_x2_move[0], 'name', getattr(best_x2_move[0], 'display_name', 'Unknown'))
                    print(f"DEBUG: *** USING x2 EFFECTIVE MOVE: {move_name} vs {opp.species} at {opp_hp:.1%} HP ***")
                    return self.create_order(best_x2_move[0])
                
                print(f"DEBUG: *** No x4/x2 effective moves available - proceeding with normal logic ***")
            else:
                print(f"DEBUG: *** Opponent {opp.species} is at {opp_hp:.1%} HP (>=80%) - using normal logic ***")

       
        if super_effective_moves and me.base_stats['spe'] >= opp.base_stats['spe']: 
           # Look for moves with 3x or higher effectiveness first
            high_effective_moves = []
            for mv, dmg, mult in moves:
                if mult >= 3.0:
                    high_effective_moves.append((mv, dmg, mult))
                
            if high_effective_moves:
                best_high_move = max(high_effective_moves, key=lambda x: x[1])  # Sort by damage
                move_name = getattr(best_high_move[0], 'name', getattr(best_high_move[0], 'display_name', 'Unknown'))
                print(f"DEBUG: *** USING {best_high_move[2]}x EFFECTIVE MOVE: {move_name} vs {opp.species} at {opp_hp:.1%} HP ***")
                return self.create_order(best_high_move[0])
            
            # Check if opponent is below 80% HP
            if opp_hp < 0.8:
                print(f"DEBUG: *** Opponent {opp.species} is at {opp_hp:.1%} HP - checking for x4/x2 effective moves ***")
                
                # Look for x2 effective moves
                x2_effective_moves = []
                for mv, dmg, mult in moves:
                    if mult >= 2.0:
                        x2_effective_moves.append((mv, dmg, mult))
                
                if x2_effective_moves:
                    best_x2_move = max(x2_effective_moves, key=lambda x: x[1])  # Sort by damage
                    move_name = getattr(best_x2_move[0], 'name', getattr(best_x2_move[0], 'display_name', 'Unknown'))
                    print(f"DEBUG: *** USING x2 EFFECTIVE MOVE: {move_name} vs {opp.species} at {opp_hp:.1%} HP ***")
                    return self.create_order(best_x2_move[0])
                
                print(f"DEBUG: *** No x4/x2 effective moves available - proceeding with normal logic ***")
            else:
                print(f"DEBUG: *** Opponent {opp.species} is at {opp_hp:.1%} HP (>=80%) - using normal logic ***")

        # If opponent's base HP is less than 80, use the highest power neutral move available
        if hasattr(opp, 'base_stats') and opp.base_stats.get('hp', 100) < 35:
            print(f"DEBUG: Opponent {opp.species} has base HP {opp.base_stats.get('hp', 0)} (<80) - looking for highest power neutral move")
            neutral_moves_available = [m for m in moves if m[2] == 1.0]  # effectiveness == 1.0
            if neutral_moves_available:
                best_neutral_move = max(neutral_moves_available, key=lambda x: x[1])  # x[1] is estimated damage
                move_name = getattr(best_neutral_move[0], 'name', getattr(best_neutral_move[0], 'display_name', 'Unknown'))
                print(f"DEBUG: *** USING HIGHEST POWER NEUTRAL MOVE: {move_name} vs {opp.species} (base HP {opp.base_stats.get('hp', 0)}) ***")
                return self.create_order(best_neutral_move[0])


        # PRIORITY 1: Switch to Pokemon with type advantage against opponent
        # Use the enhanced pick_best_switch method for consistent switch evaluation
        print(f"DEBUG: Checking for type-advantaged switches against {opp.species} ({opp_types})...")
        
        if battle.available_switches:
            best_switch = self.pick_best_switch(battle, opp_types, me, super_effective_moves)
            if best_switch is not None and best_switch.species != me.species:
                print(f"DEBUG: Switching to type-advantaged {best_switch.species}")
                return self.create_order(best_switch)
            else:
                print(f"DEBUG: Keeping current Pokemon {me.species}")

        

        # PRIORITY 2: Use super effective moves if available
        if super_effective_moves:
            print(f"DEBUG: Found {len(super_effective_moves)} super effective moves:")
            for mv, dmg, mult in super_effective_moves:
                # Try multiple ways to get move name
                mv_name = getattr(mv, 'name', None)
                if mv_name is None:
                    mv_name = getattr(mv, 'display_name', None)
                if mv_name is None:
                    mv_name = getattr(mv, 'id', 'Unknown')
                print(f"DEBUG:   - {mv_name}: damage={dmg:.3f}, effectiveness={mult}")
            
            # Sort by effectiveness first, then by damage within same effectiveness
            best_se_move = max(super_effective_moves, key=lambda x: (x[2], x[1]))  # (effectiveness, damage)
            # Try multiple ways to get move name
            move_name = getattr(best_se_move[0], 'name', None)
            if move_name is None:
                move_name = getattr(best_se_move[0], 'display_name', None)
            if move_name is None:
                move_name = getattr(best_se_move[0], 'id', 'Unknown')
            print(f"DEBUG: Selected SUPER EFFECTIVE move: {move_name} (damage: {best_se_move[1]:.3f}, effectiveness: {best_se_move[2]})")
            print(f"DEBUG: *** RETURNING SUPER EFFECTIVE MOVE: {move_name} ***")
            return self.create_order(best_se_move[0])
        
        
        # PRIORITY 3: If no super effective moves, consider switching to a better Pokemon
        if battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types, me, super_effective_moves)
            if counter:
                # Check if the counter has super effective moves against opponent
                counter_has_se = False
                for mv in counter.moves:
                    if hasattr(mv, 'type') and mv.type:
                        eff = self.type_multiplier(mv.type, opp_types, battle)
                        if eff > 1.0:
                            counter_has_se = True
                            break
                
                # Switch if counter has super effective moves or if we're at a disadvantage,
                # BUT only if its defensive risk is strictly lower than our current defensive risk
                disadvantaged = self.opponent_has_advantage(my_types, opp_types, 1.0, battle)
                counter_defensive_risk = max(
                    (self.type_multiplier(ot, counter.types, battle) for ot in opp_types if ot is not None),
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
            print(f"DEBUG: Selected NEUTRAL move: {move_name} (damage: {best_neutral_move[1]:.3f})")
            return self.create_order(best_neutral_move[0])

        # PRIORITY 5: If only resisted moves remain, try switching one more time
        if resisted_moves and battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types, me, super_effective_moves)
            if counter:
                counter_defensive_risk = max(
                    (self.type_multiplier(ot, counter.types, battle) for ot in opp_types if ot is not None),
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