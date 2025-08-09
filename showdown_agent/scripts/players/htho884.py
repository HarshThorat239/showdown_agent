from poke_env.battle import AbstractBattle, side_condition, pokemon_type
from poke_env.player import Player
from poke_env.battle.pokemon_type import PokemonType



import poke_env.battle as battle

import re



team = """
Groudon @ Heat Rock  
Ability: Drought  
Tera Type: Fire  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Spikes  
- Stealth Rock  
- Precipice Blades  
- Heat Crash  

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

Eternatus @ Power Herb  
Ability: Pressure  
Tera Type: Fire  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Dynamax Cannon  
- Sludge Bomb  
- Flamethrower  
- Meteor Beam  

Venusaur @ Choice Specs  
Ability: Chlorophyll  
Tera Type: Steel  
EVs: 4 HP / 252 SpA / 252 Spe  
Modest Nature  
IVs: 0 Atk  
- Sludge Bomb  
- Earth Power  
- Solar Beam  
- Weather Ball  

Walking Wake @ Life Orb  
Ability: Protosynthesis  
Tera Type: Water  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Hydro Steam  
- Draco Meteor  
- Dragon Pulse  
- Flamethrower  

Charizard @ Choice Scarf  
Ability: Solar Power  
Shiny: Yes  
Tera Type: Fairy  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
- Solar Beam  
- Fire Blast  
- Air Slash  
- Tera Blast  
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

    def team_preview(self, battle: AbstractBattle) -> int:
        for i, (_, p) in enumerate(battle.team.items()):
            if p.name and p.name.lower() == "groudon":
                return i
        return 0

    def type_multiplier(self, atk_type, def_types):
        mult = 1.0
        for t in def_types:
            mult *= TYPE_EFFECTIVENESS.get(atk_type, {}).get(t, 1.0)
        return mult

    def estimated_effectiveness(self, move_type, opp_types, my_types):
        eff = self.type_multiplier(move_type, opp_types)
        if move_type in my_types:
            eff *= 1.5  # STAB
        return eff

    def estimate_damage_frac(self, move, my_types, opp_types):
        if not move.base_power or move.base_power <= 0:
            return 0.0
        eff = self.estimated_effectiveness(move.type, opp_types, my_types)
        return max(0.0, min((move.base_power / 100.0) * eff, 1.0))

    def pick_best_switch(self, battle, opp_types):
        best_mon, best_score = None, float("-inf")
        for mon in battle.available_switches:
            worst_incoming = max(self.type_multiplier(otype, mon.types) for otype in opp_types)
            best_offense = max(1.5 * self.type_multiplier(ct, opp_types) for ct in mon.types)
            score = best_offense / (worst_incoming + 1e-6)
            if score > best_score:
                best_score, best_mon = score, mon
        return best_mon

    def choose_move(self, battle: AbstractBattle):
        opp = battle.opponent_active_pokemon
        me = battle.active_pokemon
        opp_types = opp.types
        my_types = me.types
        opp_hp = opp.current_hp_fraction or 1.0

        moves = []
        for mv in battle.available_moves:
            if not mv.base_power or mv.base_power <= 0:
                continue
            raw_mult = self.type_multiplier(mv.type, opp_types)
            if raw_mult == 0.0:  # skip immune
                continue
            dmg = self.estimate_damage_frac(mv, my_types, opp_types)
            moves.append((mv, dmg, raw_mult))

        # KO check
        for m, dmg, _ in sorted(moves, key=lambda x: x[1], reverse=True):
            if dmg >= opp_hp - 1e-6:
                return self.create_order(m)

        # Prefer SE > neutral > resisted
        se = [(m, dmg) for m, dmg, raw in moves if raw > 1.0]
        nt = [(m, dmg) for m, dmg, raw in moves if abs(raw - 1.0) < 1e-9]
        if se:
            return self.create_order(max(se, key=lambda x: x[1])[0])
        if nt:
            return self.create_order(max(nt, key=lambda x: x[1])[0])

        # Switch if only resisted and switch available
        if moves and battle.available_switches:
            counter = self.pick_best_switch(battle, opp_types)
            if counter:
                return self.create_order(counter)

        # Else best damage
        if moves:
            return self.create_order(max(moves, key=lambda x: x[1])[0])

        return self.choose_random_move(battle)