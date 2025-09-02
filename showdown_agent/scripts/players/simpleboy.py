from poke_env.player.baselines import SimpleHeuristicsPlayer



team = """

Kyogre @ Choice Specs  
Ability: Drizzle  
Tera Type: Water  
EVs: 4 Def / 252 SpA / 252 Spe  
Modest Nature  
IVs: 0 Atk  
- Water Spout  
- Ice Beam  
- Origin Pulse  
- Thunder  

Eternatus @ Life Orb  
Ability: Pressure  
Tera Type: Dragon  
EVs: 4 Def / 252 SpA / 252 Spe  
Modest Nature  
IVs: 0 Atk  
- Dynamax Cannon  
- Fire Blast  
- Sludge Bomb  
- Recover  

Giratina-Origin @ Griseous Core  
Ability: Levitate  
Shiny: Yes  
Tera Type: Steel  
EVs: 200 HP / 252 Atk / 40 SpD / 16 Spe  
Adamant Nature  
- Poltergeist  
- Dragon Tail  
- Defog  
- Shadow Sneak  

Koraidon @ Choice Scarf  
Ability: Orichalcum Pulse  
Tera Type: Ghost  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Flare Blitz  
- U-turn  
- Low Kick  
- Outrage  

Arceus-Fairy @ Pixie Plate  
Ability: Multitype  
Tera Type: Water  
EVs: 248 HP / 164 Def / 96 Spe  
Bold Nature  
IVs: 0 Atk  
- Judgment  
- Recover  
- Stealth Rock  
- Roar  

Ting-Lu @ Custap Berry  
Ability: Vessel of Ruin  
Tera Type: Water  
EVs: 248 HP / 8 Def / 252 SpD  
Sassy Nature  
IVs: 9 Spe  
- Earthquake  
- Ruination  
- Whirlwind  
- Spikes

"""
class CustomAgent(SimpleHeuristicsPlayer):
    def __init__(self, **kwargs):
        super().__init__(team=team, **kwargs)