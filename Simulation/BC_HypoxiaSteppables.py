from cc3d.core.PySteppables import *

import numpy as np

r_sigma_s = 38.0# saturation
r_sigma_h = 10.0 #hypoxia
r_sigma_t = 6.0 #proliferation

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
            cell.dict['hypoxia'] = 0

    def step(self, mcs):
        field=self.getConcentrationField('oxygen')
        for cell in self.cellList:
            # check if cell in hypoxia condition
            r_o2 = field[cell.xCOM, cell.yCOM, cell.zCOM]
            
            if (r_o2 < r_sigma_t):  # proliferation
                cell.type = self.Necrotic
            if (r_o2 < r_sigma_h):  # hypoxia
                cell.type = self.GFP
            if (r_o2 < r_sigma_s):  # saturation
                cell.type = self.DsRed
            

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

