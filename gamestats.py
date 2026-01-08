import json
from pathlib import Path
class GameStats:
    def __init__(self, ai_game):
        self.settings =  ai_game.settings
        self.reset_stats()
        path = Path('data.json')
        with open(path,'r') as f:
            self.high_score = json.load(f)
        
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1