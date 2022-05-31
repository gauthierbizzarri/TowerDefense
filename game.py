from units.oldguard import OldGuard

class Game():
    def __init__(self):
        super(Game, self).__init__()
        self.units = []




    def add_unit(self,unit):
        # Add unit to Game.units
        self.units.append(unit)
