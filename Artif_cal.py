import numpy as np

##ランダム聖遺物作成クラス
class Artifact:
    def __init__(self):
        pass
        #self.subop_count = subop_count
        #self.subop_type = subop_type

    def subop_count(self):
        self.subop_count = np.random.choice([4, 5])

    def subop_type(self):
        self.subtype = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        #0 DMVal, 1 DM%, 2 DFVal, 3 DFe%, 4 hpVal, 5 hp%, 6 EM, 7 EC, 8 CR, 9 CD

    def subop_growsParametor(self):
        pass
