# showdown_agent/showdown_agent/scripts/bots/simple_uber.py
from poke_env.player.baselines import SimpleHeuristicsPlayer

# The framework expects this class to be named CustomAgent
class CustomAgent(SimpleHeuristicsPlayer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
