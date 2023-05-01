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
        """
        Called every frequency MCS while executing the simulation
        :param mcs: current Monte Carlo step
        """
        for cell in self.cell_list:
            print("cell.id=",cell.id)

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

