# from __future__ import annotations
# from typing import Optional, Tuple

# from poke_env.battle import AbstractBattle
# from poke_env.player import Player

# # TEAM (GEN 9 UBERS)
# team = """
# Annihilape @ Leftovers
# Ability: Defiant
# Tera Type: Fighting
# EVs: 110 HP / 120 Atk / 80 Def / 50 SpA / 148 Spe
# Adamant Nature
# - Rage Fist
# - Drain Punch
# - Bulk Up
# - Taunt

# Koraidon @ Choice Scarf
# Ability: Orichalcum Pulse
# Tera Type: Steel
# EVs: 252 Atk / 4 Def / 252 Spe
# Jolly Nature
# - Low Kick
# - Dragon Claw
# - U-turn
# - Flare Blitz

# Gliscor @ Toxic Orb
# Ability: Poison Heal
# Tera Type: Water
# EVs: 252 HP / 232 SpD / 24 Spe
# Careful Nature
# - Spikes
# - Earthquake
# - Toxic
# - Protect

# Zacian-Crowned @ Rusted Sword
# Ability: Intrepid Sword
# Tera Type: Fairy
# EVs: 252 Atk / 4 SpD / 252 Spe
# Jolly Nature
# - Swords Dance
# - Behemoth Blade
# - Play Rough
# - Wild Charge

# Toxapex @ Rocky Helmet
# Ability: Regenerator
# Tera Type: Ground
# EVs: 252 HP / 224 Def / 32 SpD
# Bold Nature
# IVs: 0 Atk
# - Toxic
# - Recover
# - Haze
# - Baneful Bunker

# Eternatus @ Power Herb
# Ability: Pressure
# Tera Type: Fire
# EVs: 4 HP / 252 SpA / 252 Spe
# Modest Nature
# IVs: 0 Atk
# - Recover
# - Meteor Beam
# - Dynamax Cannon
# - Flamethrower
# """


# ## Helper functions and constants ##
# TYPE_POINTS = {
#     0.0: -40,   # immune
#     0.5: -10,   # resist
#     1.0: 0,     # neutral
#     2.0: 35,    # super-effective
#     4.0: 55,    # 4x SE (just in case)
# }

# # List of moves in their relative categories
# SETUP_MOVES = ["Swords Dance", "Bulk Up",]
# HAZARD_MOVES = ["Stealth Rock", "Spikes", "Toxic Spikes", "Sticky Web"]
# PROTECT_MOVES = ["Protect", "Baneful Bunker"]
# RECOVERY_MOVES = ["Recover","Drain Punch",]
# UTILITY_MOVES = ["Toxic", "Taunt", "Haze"]
# ATTACKING_MOVES = [
#     "Rage Fist", "Drain Punch",
#     "Low Kick", "Dragon Claw", "U-turn", "Flare Blitz",
#     "Earthquake",
#     "Behemoth Blade", "Play Rough", "Wild Charge",
#     "Meteor Beam", "Dynamax Cannon", "Flamethrower"
# ]
# TERA_TYPES = ["Fighting", "Steel", "Water", "Fairy", "Ground", "Fire"]

# # Safely get the name of a poke_env object
# def safe_name(o) -> str:
#     try:
#         return o.name  # poke_env objects have .name
#     except Exception:
#         return str(o)

# # Get the types of a Pokémon
# def get_types(pokemon) -> Tuple[Optional[object], Optional[object]]:
#     # Returns (type1, type2) Type objects or None
#     try:
#         t1 = getattr(pokemon, "type_1", None)
#         t2 = getattr(pokemon, "type_2", None)
#         return t1, t2
#     except Exception:
#         return None, None

# # Check if a Pokémon has a status condition
# def has_status(pokemon) -> bool:
#     try:
#         return pokemon.status is not None
#     except Exception:
#         return False

# # Get the current HP fraction of a Pokémon
# def hp_frac(pokemon) -> float:
#     try:
#         return float(pokemon.current_hp_fraction)
#     except Exception:
#         # fall back to 1 (healthy) if not known
#         return 1.0

# # Check if a move is STAB (Same Type Attack Bonus)
# def is_stab(move, user) -> bool:
#     try:
#         mt = getattr(move, "type", None)
#         t1, t2 = get_types(user)
#         return (mt is not None) and (mt == t1 or mt == t2)
#     except Exception:
#         return False

# # Get the base power of a move
# def base_power(move) -> int:
#     try:
#         return int(getattr(move, "base_power", 0) or 0)
#     except Exception:
#         return 0

# # Get the priority of a move
# def priority(move) -> int:
#     try:
#         return int(getattr(move, "priority", 0) or 0)
#     except Exception:
#         return 0

# # Get the type effectiveness multiplier for a move against a defender
# def type_multiplier(battle: AbstractBattle, move, defender) -> float:
#     """
#     Best-effort estimate of type effectiveness using poke_env's Type objects if available.
#     Falls back to 1.0 if type info is missing.
#     """
#     try:
#         mt = getattr(move, "type", None)
#         if mt is None:
#             return 1.0
#         d1, d2 = get_types(defender)
#         # poke_env Type has damage_multiplier(t1, t2, gen) typically
#         gen = getattr(battle, "gen", 9)
#         if hasattr(mt, "damage_multiplier"):
#             return float(mt.damage_multiplier(d1, d2, gen))
#         return 1.0
#     except Exception:
#         return 1.0

# # Check if it's the first or second turn of the battle
# def turn_one(battle: AbstractBattle) -> bool:
#     try:
#         return battle.turn == 0 or battle.turn == 1
#     except Exception:
#         return False

# # Check if a move can be used
# def can_attack(move) -> bool:
#     return base_power(move) > 0

# # Check if a move is a setup move
# def is_setup(move) -> bool:
#     return safe_name(move) in SETUP_MOVES

# # Check if a move is a hazard move
# def is_hazard(move) -> bool:
#     return safe_name(move) in HAZARD_MOVES

# # Check if a move is a recovery move
# def is_recover(move) -> bool:
#     return safe_name(move) in RECOVERY_MOVES

# # Check if a move is a utility move
# def is_utility(move) -> bool:
#     return safe_name(move) in UTILITY_MOVES

# # Check if a move is a protect-like move
# def is_protect_like(move) -> bool:
#     return safe_name(move) in PROTECT_MOVES

# # Check if the opposing side has reflect or screens
# def side_has_reflect_or_screens(battle: AbstractBattle) -> bool:
#     try:
#         sc = battle.side_conditions or {}
#         return any(k in sc for k in ("light_screen", "reflect", "aurora_veil"))
#     except Exception:
#         return False

# # ==================================================
# # Hybrid Agent (priority rules + weighted evaluation)
# # ==================================================
# class CustomAgent(Player):
#     def __init__(self, *args, **kwargs):
#         super().__init__(team=team, *args, **kwargs)

#     # Check for potential OHKO (One-Hit Knock Out)
#     def quick_ohko_check(self, battle: AbstractBattle, move) -> bool:
#         """
#         Super-light heuristic 'can KO' check without calc:
#         If opponent HP is very low and move is at least neutral and has base power >= 60 (or priority),
#         assume it can finish.
#         """
#         opp = battle.opponent_active_pokemon
#         opphp = hp_frac(opp)
#         eff = type_multiplier(battle, move, opp)
#         if not can_attack(move):
#             return False
#         return (opphp < 0.18) and (eff >= 1.0) and (base_power(move) >= 60 or priority(move) > 0)

#     # Check for bad matchups
#     def bad_matchup(self, battle: AbstractBattle) -> bool:
#         """
#         Roughly decide if we should consider switching:
#         - Very low HP
#         - Opp has clear type edge (estimated by fake STAB hitting us super effectively)
#         """
#         me = battle.active_pokemon
#         opp = battle.opponent_active_pokemon
#         if hp_frac(me) < 0.18:
#             return True
#         try:
#             t1, t2 = get_types(opp)
#             class Fake:
#                 def __init__(self, t): self.type = t; self.name = "FAKE"; self.base_power = 80; self.priority = 0
#             mult1 = type_multiplier(battle, Fake(t1), me) if t1 else 1.0
#             mult2 = type_multiplier(battle, Fake(t2), me) if t2 else 1.0
#             return max(mult1, mult2) >= 2.0
#         except Exception:
#             return False

#     # Create a move order
#     def move_weight(self, battle: AbstractBattle, move) -> float:
#         me = battle.active_pokemon
#         opp = battle.opponent_active_pokemon

#         score = 0.0
#         pow_ = base_power(move)
#         eff = type_multiplier(battle, move, opp)

#         # Core combat features
#         if can_attack(move):
#             score += pow_ * 0.8
#             score += TYPE_POINTS.get(eff, 0)
#             if is_stab(move, me):
#                 score += 18  # STAB bonus
#             if priority(move) > 0:
#                 score += 12

#         # Following code scores each move in each category
#         n = safe_name(move)
#         if n in {"Taunt"} and not has_status(opp):
#             # Taunt vs walls/hazards early
#             score += 15 if turn_one(battle) else 6
#         if is_hazard(move):
#             score += 26 if turn_one(battle) else 8
#         if n in {"Haze"}:
#             score += 22
#         if is_recover(move):
#             # Value recovers when low
#             if hp_frac(me) < 0.45:
#                 score += 40
#         if is_protect_like(move):
#             score += 12

#         # Preference for accuracy (kept small for not too much bias)
#         acc = getattr(move, "accuracy", None)
#         if isinstance(acc, (int, float)):
#             score += (acc - 80) * 0.2  # small nudge above/below 80

#         return score

#     # Weighting for switch-ins
#     def switch_weight(self, battle: AbstractBattle, switch_target) -> float:
#         opp = battle.opponent_active_pokemon
#         score = 0.0

#         # Pivot preference (Gliscor/Toxapex)
#         if "Gliscor" in safe_name(switch_target):
#             score += 18
#         if "Toxapex" in safe_name(switch_target):
#             score += 22

#         # Avoid switching into something too low
#         if hp_frac(switch_target) < 0.25:
#             score -= 25

#         # Favor resistances to opp STABs
#         try:
#             t1, t2 = get_types(opp)
#             class Fake:
#                 def __init__(self, t): self.type = t; self.name = "FAKE"; self.base_power = 80; self.priority = 0
#             if t1:
#                 m1 = type_multiplier(battle, Fake(t1), switch_target)
#                 score += {0.5: 12, 0.25: 16, 1.0: 0, 2.0: -15, 4.0: -30}.get(m1, 0)
#             if t2:
#                 m2 = type_multiplier(battle, Fake(t2), switch_target)
#                 score += {0.5: 12, 0.25: 16, 1.0: 0, 2.0: -15, 4.0: -30}.get(m2, 0)
#         except Exception:
#             pass

#         return score

#     # Main decision-making function
#     def choose_move(self, battle: AbstractBattle):
#         me = battle.active_pokemon
#         opp = battle.opponent_active_pokemon

#         # -----------------------------
#         # Priority rule 1: secure KO
#         # -----------------------------
#         for m in battle.available_moves or []:
#             if self.quick_ohko_check(battle, m):
#                 return self.create_order(m)

#         # -----------------------------
#         # Priority rule 2: early hazards
#         # -----------------------------
#         if turn_one(battle):
#             for m in battle.available_moves or []:
#                 if is_hazard(m) and "Gliscor" in safe_name(me):
#                     return self.create_order(m)

#         # -----------------------------
#         # Priority rule 3: emergency recover / protect
#         # -----------------------------
#         if hp_frac(me) < 0.33:
#             # Try Recover first if we have it
#             for m in battle.available_moves or []:
#                 if is_recover(m):
#                     return self.create_order(m)
#             # Else Protect-like if present
#             for m in battle.available_moves or []:
#                 if is_protect_like(m):
#                     return self.create_order(m)

#         # -----------------------------
#         # Consider switching on bad matchup
#         # -----------------------------
#         if self.bad_matchup(battle) and battle.available_switches:
#             sw_scores = {sw: self.switch_weight(battle, sw) for sw in battle.available_switches}
#             # Only switch if it's clearly beneficial
#             if sw_scores and max(sw_scores.values()) >= 12:
#                 return self.create_order(max(sw_scores, key=sw_scores.get))

#         # -----------------------------
#         # Weighted scoring over moves
#         # -----------------------------
#         if battle.available_moves:
#             move_scores = {m: self.move_weight(battle, m) for m in battle.available_moves} # Creating a dictionary of moves along with their scores

#             # Small, role-based nudges:
#             # - Zacian: prefer Behemoth Blade / Play Rough for pressure
#             if "Zacian" in safe_name(me):
#                 for m in list(move_scores):
#                     if safe_name(m) in {"Behemoth Blade", "Play Rough"}:
#                         move_scores[m] += 8

#             # - Koraidon: pivot with U-turn if effectiveness is poor
#             if "Koraidon" in safe_name(me):
#                 worst_eff = min(type_multiplier(battle, m, opp) for m in battle.available_moves if can_attack(m)) \
#                             if any(can_attack(m) for m in battle.available_moves) else 1.0
#                 for m in list(move_scores):
#                     if safe_name(m) == "U-turn" and worst_eff <= 0.5:
#                         move_scores[m] += 10

#             # - Eternatus: prioritize Meteor Beam only if we can exploit Power Herb or safe turn
#             if "Eternatus" in safe_name(me):
#                 for m in list(move_scores):
#                     if safe_name(m) == "Meteor Beam":
#                         move_scores[m] += 8 if hp_frac(me) > 0.6 else -6 # this line is added to ensures score is lower when low on HP to avoid using Meteor Beam recklessly

            
#             best_move = max(move_scores, key=move_scores.get)
#             return self.create_order(best_move)
        
#             # Debugging to see the weight of moves
#             # print(f"\nTurn {battle.turn} | Active: {safe_name(me)} vs {safe_name(opp)}")
#             # for move, score in move_scores.items():
#             #     print(f"  Move: {safe_name(move):<20} | Score: {score:.2f}")
            
#             # best_move = max(move_scores, key=move_scores.get)
#             # print(f"👉 Chosen move: {safe_name(best_move)} (Score: {move_scores[best_move]:.2f})\n")

#             # return self.create_order(best_move)


#         # -----------------------------
#         # No moves? Try best switch
#         # -----------------------------
#         if battle.available_switches:
#             sw_scores = {sw: self.switch_weight(battle, sw) for sw in battle.available_switches}
#             if sw_scores:
#                 return self.create_order(max(sw_scores, key=sw_scores.get))

#         # Fallback
#         return self.choose_random_move(battle)