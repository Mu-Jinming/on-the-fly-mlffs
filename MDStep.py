class MDStep:
    # atomNum, lattice, atoms
    def __init__(self, MDIndex):
        self.MDIndex = MDIndex
        self.lines = [] #包含每一步的mddump原始数据
        self.lattice = []
        self.atoms = []
        self.atomNum = 0
        self.deltaT = 0.1