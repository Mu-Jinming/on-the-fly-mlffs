class MDStep:
    # atomNum, lattice, atoms
    def __init__(self, MDIndex):
        self.MDIndex = MDIndex
        self.lines = [] #包含每一步的mddump原始数据
        self.lattice = []
        self.atoms = [] #每一步包含的所有原子
        self.atomNum = 0
        self.deltaT = 0.1