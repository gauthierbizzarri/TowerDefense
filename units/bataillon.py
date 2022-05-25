
class Bataillon():

    def __init__(self,units,grid):
        self.units = units
        self.grid = grid
        # DEFINITION UNITE DE CENTRE DE GRAVITE
        # BATAILLON DE 6 GRENADIERS

    def move_bataillon(self):
        for unit in self.units:
            # CREATE PATH FOR UNIT :
            self.grid.unset_unit(unit)
            unit.add_path(self.units[0].line,self.units[1].row+5)
            self.grid.set_unit(unit)

            unit.move()