
class Atom:
    def __init__(self, specie):
        self.specie = specie
        self.positons = []
        self.forces = []
        self.velocity = []
        self.acceleration = []
        self.mass = 15