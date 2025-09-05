from poke_env.battle import AbstractBattle
from poke_env.player import Player
from poke_env.battle.pokemon_type import PokemonType

# ================== TEAM ==================
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
        super().__init__(team=team, *args, **kwargs)

        # togglable verbose logs
        self.debug = True

        # State
        self.toxic_spikes = 0
        self.curse = False
        self.opponent_last_move = None
        self.last_opponent_species = None
        self.opponent_just_switched_after_ko = False
        self.last_opponent_hp = None

        # Hazard names (normalized comparisons)
        self.hazard_tokens = {s.upper() for s in [
            'spikes','stealthrock','toxicspikes','stickyweb',
            'stealth rock','toxic spikes','sticky web',
            'SPIKES','STEALTH_ROCK','STICKY_WEB','STICKYWEB'
        ]}

    # ---------- small utilities ----------
    def log(self, *args):
        if self.debug:
            print(*args)

    def _to_enum(self, t):
        if t is None: return None
        if isinstance(t, PokemonType): return t
        if isinstance(t, str):
            try: return PokemonType[t.upper()]
            except Exception: return None
        name = getattr(t, 'name', None)
        if name:
            try: return PokemonType[name.upper()]
            except Exception: return None
        return None

    def get_move_type(self, mv):
        return getattr(mv, 'type', None) or getattr(mv, 'type_id', None)

    def get_move_name(self, mv):
        for attr in ('id', 'name', 'display_name', 'move_id'):
            val = getattr(mv, attr, None)
            if val: return str(val)
        return str(mv)

    def kyogre_spout_override(self, chosen_move, battle, me):
        """If Kyogre <60% HP and chosen is Water Spout, try Surf instead."""
        if me and me.species and me.species.lower() == 'kyogre':
            if me.current_hp_fraction is not None and me.current_hp_fraction < 0.6:
                if self.get_move_name(chosen_move).lower() == 'waterspout':
                    for mv in battle.available_moves:
                        if self.get_move_name(mv).lower() == 'surf':
                            self.log("DEBUG: Kyogre HP <60% - overriding Water Spout with Surf")
                            return mv
        return chosen_move

    # ---------- type multipliers & immunities ----------
    def type_multiplier(self, atk_type, def_types, battle=None):
        atk = self._to_enum(atk_type)
        defs = [self._to_enum(dt) for dt in (def_types or [])]

        mult = 1.0
        inner = TYPE_EFFECTIVENESS.get(atk, {})
        for dt in defs:
            if dt is None: continue
            mult *= inner.get(dt, 1.0)

        # Weather boost for Fire in sun, Water in rain (simple)
        weather = getattr(battle, 'weather', None)
        if weather:
            wname = (weather.get('name', '') if isinstance(weather, dict) else str(weather)).lower()
            if wname == 'sun' and atk == PokemonType.FIRE:
                mult *= 1.5
            elif wname == 'rain' and atk == PokemonType.WATER:
                mult *= 1.5

        return mult

    def is_move_immune(self, move_type, opp_ability):
        if not opp_ability: return False
        ability_name = str(opp_ability).lower()
        ability_immunities = {
            'levitate': PokemonType.GROUND,
            'flashfire': PokemonType.FIRE,
            'waterabsorb': PokemonType.WATER,
            'dryskin': PokemonType.WATER,
            'sapsipper': PokemonType.GRASS,
            'lightningrod': PokemonType.ELECTRIC,
            'stormdrain': PokemonType.WATER,
            'voltabsorb': PokemonType.ELECTRIC,
            'motordrive': PokemonType.ELECTRIC,
        }
        return ability_immunities.get(ability_name) == move_type

    def estimate_damage_frac(self, mv, my_types, opp_types, battle=None):
        """Very rough estimate based on base power, STAB, and effectiveness."""
        bp = getattr(mv, 'base_power', 0) or 0
        if bp <= 0: return 0.0
        mv_type = self.get_move_type(mv)
        if mv_type is None: return 0.0

        eff = self.type_multiplier(mv_type, opp_types, battle)
        if my_types and any(self._to_enum(t) == self._to_enum(mv_type) for t in my_types):
            eff *= 1.5  # STAB (simple)
        return max(0.0, min((bp / 100.0) * eff, 1.0))

    # ---------- hazard helpers ----------
    def has_hazards(self, side_conditions):
        if not side_conditions: return False
        for cond in side_conditions:
            c = str(cond).upper()
            if any(tok in c for tok in self.hazard_tokens):
                return True
        return False

    # ---------- immunity/resistance scoring helpers (kept, but tidied) ----------
    def would_be_immune_to_opponent_moves(self, candidate, opp_types, opp_ability):
        if not candidate.types or not opp_types:
            return False, 0.0
        score = 0.0
        for ot in opp_types:
            if ot is None: continue
            # ability-based
            cand_ability = getattr(candidate, 'ability', None)
            if cand_ability and self.is_move_immune(ot, cand_ability):
                score += 2.0
                continue
            # 0x type immunity
            mult = self.type_multiplier(ot, candidate.types, None)
            if mult == 0.0: score += 1.5
        return (score > 0.0), score

    def would_be_immune_to_candidate_moves(self, candidate, opp_types, opp_ability):
        if not candidate.types or not opp_types:
            return False, 0.0
        score = 0.0
        for ct in candidate.types:
            if ct is None: continue
            if opp_ability and self.is_move_immune(ct, opp_ability):
                score += 1.5
                continue
            mult = self.type_multiplier(ct, opp_types, None)
            if mult == 0.0: score += 1.0
        return (score > 0.0), score

    def get_resistance_bonus(self, candidate, opp_types, battle):
        if not candidate.types or not opp_types: return 0.0
        score = 0.0
        for ot in opp_types:
            if ot is None: continue
            mult = self.type_multiplier(ot, candidate.types, battle)
            if mult == 0.25: score += 1.5
            elif mult == 0.5: score += 0.5
        return score

    def check_weather_immunities(self, candidate, battle):
        weather = getattr(battle, 'weather', None)
        if not weather: return 0.0
        wname = (weather.get('name', '') if isinstance(weather, dict) else str(weather)).lower()
        if 'sand' in wname and candidate.types and any(t in [PokemonType.ROCK, PokemonType.GROUND, PokemonType.STEEL] for t in candidate.types):
            return 0.5
        if 'hail' in wname and candidate.types and any(t == PokemonType.ICE for t in candidate.types):
            return 0.5
        return 0.0

    def check_status_immunities(self, candidate, opp_types):
        if not candidate.types: return 0.0
        score = 0.0
        for t in candidate.types:
            if t == PokemonType.POISON: score += 0.5
            elif t == PokemonType.ELECTRIC: score += 0.3
            elif t == PokemonType.FIRE: score += 0.3
            elif t == PokemonType.ICE: score += 0.3
        abil = str(getattr(candidate, 'ability', '') or '').lower()
        # small set only; stay conservative
        if abil in ['limber', 'vitalspirit']: score += 0.5
        if abil in ['waterveil', 'magmaarmor']: score += 0.5
        if abil in ['insomnia', 'vitalspirit']: score += 0.5
        if abil in ['immunity', 'pastelveil']: score += 0.5
        return score

    def check_hazard_immunities(self, candidate):
        if not candidate.types: return 0.0
        score = 0.0
        if PokemonType.FLYING in candidate.types: score += 0.5
        abil = str(getattr(candidate, 'ability', '') or '').lower()
        if abil == 'levitate': score += 0.5
        elif abil == 'magicguard': score += 1.0
        elif abil == 'overcoat': score += 0.5
        return score

    # ---------- switch selection ----------
    def pick_best_switch(self, battle, opp_types, current_pokemon=None, super_effective_moves=None):
        if not battle.available_switches:
            return None

        opp_ability = getattr(battle.opponent_active_pokemon, 'ability', None) if getattr(battle, 'opponent_active_pokemon', None) else None
        is_forced = current_pokemon is None
        best_switch, best_score = None, float('-inf')

        # current ref scores (if not forced)
        curr_def_risk = curr_score = 0.0
        if not is_forced:
            curr_def_risk = max((self.type_multiplier(ot, current_pokemon.types, battle) for ot in opp_types if ot), default=1.0)
            curr_off_adv = max((self.type_multiplier(ct, opp_types, battle) for ct in current_pokemon.types if ct), default=0.0) if current_pokemon.types else 0.0
            curr_score = (curr_off_adv * 2.0 - curr_def_risk) + 1.0  # +1 stay-in bonus
            # add immunity/resist/weather/status/hazard bonuses
            imm = 0.0
            has_im, s = self.would_be_immune_to_opponent_moves(current_pokemon, opp_types, opp_ability); imm += s if has_im else 0.0
            has_rev, s2 = self.would_be_immune_to_candidate_moves(current_pokemon, opp_types, opp_ability); imm += s2 if has_rev else 0.0
            imm += self.get_resistance_bonus(current_pokemon, opp_types, battle)
            imm += self.check_weather_immunities(current_pokemon, battle)
            if any(t in [PokemonType.POISON, PokemonType.GHOST, PokemonType.GRASS, PokemonType.ELECTRIC] for t in opp_types if t):
                imm += self.check_status_immunities(current_pokemon, opp_types)
            imm += self.check_hazard_immunities(current_pokemon)
            if super_effective_moves: curr_score -= 1.0
            curr_score += imm
            best_score = curr_score

        for cand in battle.available_switches:
            off_adv = max((self.type_multiplier(ct, opp_types, battle) for ct in (cand.types or []) if ct), default=0.0)
            def_risk = max((self.type_multiplier(ot, cand.types, battle) for ot in opp_types if ot), default=1.0)

            bonus = 0.0
            has_im, s = self.would_be_immune_to_opponent_moves(cand, opp_types, opp_ability); bonus += s if has_im else 0.0
            has_rev, s2 = self.would_be_immune_to_candidate_moves(cand, opp_types, opp_ability); bonus += s2 if has_rev else 0.0
            bonus += self.get_resistance_bonus(cand, opp_types, battle)
            bonus += self.check_weather_immunities(cand, battle)
            if any(t in [PokemonType.POISON, PokemonType.GHOST, PokemonType.GRASS, PokemonType.ELECTRIC] for t in opp_types if t):
                bonus += self.check_status_immunities(cand, opp_types)
            bonus += self.check_hazard_immunities(cand)

            score = (off_adv * 2.0 - def_risk) + bonus
            if not is_forced and super_effective_moves:
                score -= 1.0  # discourage switching away from a SE position unless clearly better

            # be stricter if not forced
            if not is_forced and def_risk >= 2.0 and curr_def_risk < 2.0:
                continue

            if score > best_score:
                best_score = score
                best_switch = cand

        if not is_forced and best_switch and current_pokemon and best_switch.species == current_pokemon.species:
            # no need to "switch" into itself
            return None
        return best_switch

    # ---------- move collection / categorization ----------
    def collect_moves(self, battle, me, opp, opp_types):
        """Return (all, super_eff, neutral, resisted) as lists of tuples (mv, dmg, mult)."""
        opp_ability = getattr(opp, 'ability', None)
        all_moves, super_eff, neutral, resisted = [], [], [], []

        for mv in battle.available_moves or []:
            mv_type = self.get_move_type(mv)
            if mv_type is None: continue
            mult = self.type_multiplier(mv_type, opp_types, battle)
            if mult == 0.0:  # hard immunity
                continue
            if opp_ability and self.is_move_immune(mv_type, opp_ability):
                continue
            # Bulletproof etc. (optional – simple token-based)
            name_lower = self.get_move_name(mv).lower()
            if opp_ability and str(opp_ability).lower() == 'bulletproof':
                if any(tok in name_lower for tok in ['ball', 'bomb', 'bullet']):
                    continue

            dmg = self.estimate_damage_frac(mv, me.types, opp_types, battle)
            tup = (mv, dmg, mult)
            all_moves.append(tup)

            bp = getattr(mv, 'base_power', 0) or 0
            if bp <= 0:  # status / setup moves not categorized here
                continue
            if mult > 1.0: super_eff.append(tup)
            elif abs(mult - 1.0) < 1e-9: neutral.append(tup)
            else: resisted.append(tup)

        return all_moves, super_eff, neutral, resisted

    def best_effective(self, moves, min_mult):
        """Pick best by effectiveness >= min_mult then by estimated damage."""
        cands = [m for m in moves if m[2] >= min_mult]
        return max(cands, key=lambda x: (x[2], x[1])) if cands else None

    # ---------- policy ----------
    def teampreview(self, battle: AbstractBattle) -> str:
        self.toxic_spikes = 0
        self.last_opponent_species = None
        self.opponent_just_switched_after_ko = False
        self.last_opponent_hp = None
        return "/team " + "".join(str(i) for i in range(1, len(battle.team) + 1))

    def choose_move(self, battle: AbstractBattle):
        opp = battle.opponent_active_pokemon
        me  = battle.active_pokemon
        opp_types = getattr(opp, 'types', []) or []
        my_types  = getattr(me, 'types', []) or []
        opp_hp    = opp.current_hp_fraction or 1.0

        # KO-in switch detection
        curr_opp_species = getattr(opp, 'species', None)
        if (self.last_opponent_species is not None
            and curr_opp_species != self.last_opponent_species
            and self.last_opponent_hp is not None
            and self.last_opponent_hp <= 0.0):
            self.opponent_just_switched_after_ko = True
            self.log(f"DEBUG: *** OPPONENT SWITCHED IN {curr_opp_species} AFTER KO ***")
        else:
            self.opponent_just_switched_after_ko = False
        self.last_opponent_species = curr_opp_species
        self.last_opponent_hp = opp_hp

        # Forced switch: use switch picker
        if not battle.available_moves and battle.available_switches:
            self.log("DEBUG: *** FORCED SWITCH - evaluating ***")
            sw = self.pick_best_switch(battle, opp_types, None, None)
            return self.create_order(sw or list(battle.available_switches)[0])

        # # Eternatus low HP → Recover
        # if me.species and me.species.lower() == 'eternatus':
        #     if me.current_hp_fraction is not None and me.current_hp_fraction < 0.25 and opp_hp:
        #         for mv in battle.available_moves:
        #             if self.get_move_name(mv).lower() == 'recover':
        #                 return self.create_order(mv)

        # Ribombee: set Sticky Web if enemy side lacks hazards
        if me.species and me.species.lower() == 'ribombee':
            if not self.has_hazards(getattr(battle, 'opponent_side_conditions', None)):
                # assume first move is Sticky Web in the set (or find it)
                for mv in battle.available_moves:
                    if 'web' in self.get_move_name(mv).lower():
                        self.log("DEBUG: Setting Sticky Web")
                        return self.create_order(mv)
                # fallback to first move if not found
                return self.create_order(battle.available_moves[0])

        # Gather/categorize moves once
        all_moves, se_moves, neutral_moves, resisted_moves = self.collect_moves(battle, me, opp, opp_types)

        # Choice Scarf fallback: if scarfed and only resisted present → try switching
        if str(getattr(me, 'item', '')).lower() == 'choicescarf':
            if not se_moves and not neutral_moves and resisted_moves and battle.available_switches:
                sw = self.pick_best_switch(battle, opp_types, None, se_moves)
                if sw and sw.species != me.species:
                    self.log(f"DEBUG: Scarf bad matchup → switch to {sw.species}")
                    return self.create_order(sw)

        # Special: immediately after KO switch-in, try ≥3x, then ≥2x (or last-opp-mon condition)
        if self.opponent_just_switched_after_ko:
            best = self.best_effective(all_moves, 3.0) or None
            if not best:
                is_last = False
                if hasattr(battle, "opponent_team"):
                    alive = [p for p in getattr(battle, "opponent_team", []) if not getattr(p, "fainted", False)]
                    is_last = len(alive) <= 1
                if opp_hp < 0.8 or is_last:
                    best = self.best_effective(all_moves, 2.0)
            if best:
                mv = self.kyogre_spout_override(best[0], battle, me)
                return self.create_order(mv)

        # If we’re faster and have super effective, prefer ≥2x max-damage
        if se_moves and me.base_stats['spe'] >= opp.base_stats['spe']:
            best = self.best_effective(all_moves, 2.0) or max(se_moves, key=lambda x:(x[2], x[1]))
            mv = self.kyogre_spout_override(best[0], battle, me)
            return self.create_order(mv)

        # Very low base HP targets: use strongest neutral if available
        if getattr(opp, 'base_stats', {}).get('hp', 100) < 35 and neutral_moves:
            best = max(neutral_moves, key=lambda x: x[1])
            mv = self.kyogre_spout_override(best[0], battle, me)
            return self.create_order(mv)

        # Try a type-advantaged switch if any
        if battle.available_switches:
            sw = self.pick_best_switch(battle, opp_types, me, se_moves)
            if sw and sw.species != me.species:
                self.log(f"DEBUG: Switching to type-advantaged {sw.species}")
                return self.create_order(sw)

        # Priority: super effective → neutral → resisted (with Kyogre override applied)
        if se_moves:
            best = max(se_moves, key=lambda x:(x[2], x[1]))
            mv = self.kyogre_spout_override(best[0], battle, me)
            return self.create_order(mv)

        if neutral_moves:
            best = max(neutral_moves, key=lambda x: x[1])
            mv = self.kyogre_spout_override(best[0], battle, me)
            return self.create_order(mv)

        if resisted_moves:
            best = max(resisted_moves, key=lambda x: x[1])
            mv = self.kyogre_spout_override(best[0], battle, me)
            return self.create_order(mv)

        # Last resort
        return self.choose_random_move(battle)
