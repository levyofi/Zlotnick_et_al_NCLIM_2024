from Lizard_energy import Lizard_energy
from Lizard_climbing import Lizard_climbing
import numpy as np
import Parameters as p
import sys


class Lizard_climbing_13(Lizard_climbing):

    def __init__(self, limited_emergence = True):
        Lizard_climbing.__init__(self, limited_emergence)

        self.heights = [3, 12, 21, 30, 48, 66, 84, 102, 120, 138, 156, 174, 198]
        self.heights_indexes = [0,3,6,9,10,11,12,13,14,15,16,17,18]

        self.TeT = np.empty((2, len(self.heights), 2))
        self.TeT.fill(np.NaN)
