from poke_env.battle import AbstractBattle
from poke_env.player import Player
import random




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
type_effectiveness = {
        "Normal": {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
        "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
        "Water": {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
        "Electric": {"Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
        "Grass": {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
        "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
        "Fighting": {"Normal": 2.0, "Ice": 2.0, "Rock": 2.0, "Dark": 2.0, "Steel": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Ghost": 0.0, "Fairy": 0.5},
        "Poison": {"Grass": 2.0, "Fairy": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0},
        "Ground": {"Fire": 2.0, "Electric": 2.0, "Poison": 2.0, "Rock": 2.0, "Steel": 2.0, "Grass": 0.5, "Bug": 0.5, "Flying": 0.0},
        "Flying": {"Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
        "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Steel": 0.5, "Dark": 0.0},
        "Bug": {"Grass": 2.0, "Psychic": 2.0, "Dark": 2.0, "Fire": 0.5, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5},
        "Rock": {"Fire": 2.0, "Ice": 2.0, "Flying": 2.0, "Bug": 2.0, "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5},
        "Ghost": {"Psychic": 2.0, "Ghost": 2.0, "Normal": 0.0, "Dark": 0.5},
        "Dragon": {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
        "Dark": {"Psychic": 2.0, "Ghost": 2.0, "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
        "Steel": {"Ice": 2.0, "Rock": 2.0, "Fairy": 2.0, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
        "Fairy": {"Fighting": 2.0, "Dragon": 2.0, "Dark": 2.0, "Fire": 0.5, "Poison": 0.5, "Steel": 0.5},
    }

class CustomAgent(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(team=team, *args, **kwargs)

    def team_preview(self, battle: AbstractBattle) -> int:
        for i, (poke_id, pokemon) in enumerate(battle.team.items()):
            print(f"Slot {i}: {pokemon.name}")
            if pokemon.name.lower() == "groudon":
                print(f"-> Groudon selected at slot {i}")
                return i
        print("-> Groudon not found, defaulting to slot 0")
        return 0

    def estimated_effectiveness(self, move_type, opponent_types):
        type_chart = {
            "Fire": ["Grass", "Bug", "Ice", "Steel"],
            "Water": ["Fire", "Ground", "Rock"],
            "Ground": ["Fire", "Steel", "Rock", "Electric", "Poison"],
            "Fairy": ["Dark", "Dragon", "Fighting"],
            "Poison": ["Fairy", "Grass"],
            "Ghost": ["Ghost", "Psychic"],
            "Dragon": ["Dragon"]
        }
        effectiveness = 1.0
        for opp_type in opponent_types:
            if move_type in type_chart and opp_type in type_chart[move_type]:
                effectiveness *= 2
        return effectiveness

    def choose_move(self, battle: AbstractBattle):

        # if battle.turn == 1:
        #     print("=== ACTIVE POKÉMON ATTRIBUTES ===")
        #     for attr in dir(battle.active_pokemon):
        #         if not attr.startswith("__"):
        #             try:
        #                 value = getattr(battle.active_pokemon, attr)      ###For debugging ### for pokemon attributes
        #                 if not callable(value):
        #                     print(f"{attr}: {value}")
        #             except Exception as e:
        #                 print(f"{attr}: <error: {e}>")


        # if battle.turn == 1 and battle.active_pokemon != "Groudon":
        #     for pokemon in battle.available_switches:
        #         if pokemon == "Groudon":                                      # to send groudon to the field
        #             return self.create_order(pokemon) 
        # 1. Set up hazards if available and not already active\

        print(f"\n=== BATTLE OBJECT DEBUG: Turn {battle.turn} ===")
        for attr in dir(battle):
            if not attr.startswith("__"):
                try:
                    value = getattr(battle, attr)                   ###For debugging ### for battle attributes
                    if callable(value):
                        continue  # Skip methods
                    print(f"{attr}: {value}")
                except Exception:
                    print(f"{attr}: <unreadable>")

        hazard_moves = {"stealthrock", "spikes"}
        for move in battle.available_moves:
            if move.id in hazard_moves:
                if move.id == "stealthrock" and not battle.opponent_side_conditions.get("stealthrock"):
                    return self.create_order(move)
                if move.id == "spikes" and battle.opponent_side_conditions.get("spikes", 0) < 3:
                    return self.create_order(move)

        # 2. Use best super-effective damaging move
        best_move = None
        best_effectiveness = 1.0
        for move in battle.available_moves:
            if move.base_power > 0:
                move_type = move.type
                opp_types = battle.opponent_active_pokemon.types
                effectiveness = self.estimated_effectiveness(move_type, opp_types)
                if effectiveness > best_effectiveness:
                    best_effectiveness = effectiveness
                    best_move = move

        if best_move:
            return self.create_order(best_move)

        # 3. Switch if at type disadvantage
        if battle.available_switches:
            my_types = battle.active_pokemon.types
            opp_types = battle.opponent_active_pokemon.types
            for my_type in my_types:
                for opp_type in opp_types:
                    if self.estimated_effectiveness(opp_type, [my_type]) > 1.0:
                        return self.create_order(random.choice(battle.available_switches))

        # 4. Otherwise, use the move with highest base power
        damaging_moves = [m for m in battle.available_moves if m.base_power > 0]
        if damaging_moves:
            move = max(damaging_moves, key=lambda m: m.base_power)
            return self.create_order(move)

        # 5. Fallback
        return self.choose_random_move(battle)
    
# if __name__ == "__main__":
#     print("Testing CustomAgent class...")
#     from poke_env.battle import AbstractBattle

#     dummy_battle = None  # You can't create a real Battle object outside a server

#     agent = CustomAgent()
#     print("CustomAgent initialized.")
#     print("Team preview slot if Groudon exists:")

#     # Simulate dummy team dictionary
#     class DummyPokemon:
#         def __init__(self, name):
#             self.name = name

#     dummy_team = {
#         "p1: 1": DummyPokemon("Flutter Mane"),
#         "p1: 2": DummyPokemon("Charizard"),
#         "p1: 3": DummyPokemon("Charizard"),
#         "p1: 4": DummyPokemon("Groudon"),
#         "p1: 5": DummyPokemon("Charizard")
#     }

#     # Simulate the AbstractBattle object
#     class DummyBattle:
#         def __init__(self, team_dict):
#             self.team = team_dict

#     battle = DummyBattle(dummy_team)
#     chosen_slot = agent.team_preview(battle)
#     print(f"-> Groudon selected at slot {chosen_slot}")