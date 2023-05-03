from cc3d.core.PySteppables import *

import numpy as np


class BC_HypoxiaSteppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        for cell in self.cell_list:
            cell.targetVolume = 46  # ((2492 [um**3])**(1/3) / 2[px/um])**(2) = 45.952[px**2]
            cell.lambdaVolume = 4

    def step(self, mcs):
        secretor = self.get_field_secretor ("oxygen")
        for cell in self.cell_list:
            secretor.uptakeInsideCell(cell, 0.05,0.0025)

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """
        pass

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
        pass

