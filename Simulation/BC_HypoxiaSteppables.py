from cc3d.core.PySteppables import *

import numpy as np

r_sigma_s = 38.0  # oxygen pressure threshold to signal proliferation
r_sigma_h = 10.0  # oxygen pressure threshold to signal hypoxia
r_sigma_t = 6.0  # min oxygen pressure to signal proliferation
r_sigma_n = 5.0  # lower means necrosis
r_hypoxia_perstime = 30000000 # 3000[min] * 10[mcs/min]* 10**(3) GFP+ cells

# DsRed+ cells
r_red_speed = 0.00001469 # migration speed 0.2938[um/min] = 0.1469[px/min] =  0.1469[px/min] * 10[mcs/min]* 10**(-3)
r_red_perstime = 150000 # migration persistent time 15[min] * 10[mcs/min] * 10**(3)
r_red_bias = 0.1719 # migration bias

# GFP+ cells
r_green_speed = 0.000023775 # migration speed 0.4755[um/min] = 0.23775[px/min] =  0.23775[px/min] * 10[mcs/min]* 10**(-3)
r_green_perstime = 150000 # migration persistent time 15[min] * 10[mcs/min] * 10**(3)
r_green_bias = 0.1791 # migration bias

# GFP+ respons cell fraction
#r_greenrsp_fraction = 0.5 # "fraction of GFP+ cells with different migration bias (bias_green_rsp)
#r_greenrsp_bias = 0.5 # migration bias for GFP + cells (for fraction_rsp)

# Ki67
r_ki67_np_rate = 0.000000363  # transition rate from Ki67- to Ki67+ (for saturated signal)  0.00363[1/min] = 0.00363[1/min] * 10[mcs/min] * 10**(-3)
r_ki67_pn_rate = 0.000000107  # transition rate from Ki67+ to Ki67-  0.00107[1/min] = 0.00107[1/min] * 10[mcs/min] * 10**(-3)

# DsRed and GFP protein production rate
r_protein_prod_rate = 0.000000048   # 4.8e**(-4) * 10[mcs/min] * 10**(-3)
r_protein_deg_rate =  0.0000000068  # 6.8e**(-5) * 10[mcs/min] * 10**(-3)

# necrosis model
# we just freez cells

class BC_HypoxiaSteppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self,frequency)
        self.track_cell_level_scalar_attribute(field_name='Ki67', attribute_name='ki67int')

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        for cell in self.cell_list:
            # volume constrraint
            cell.targetVolume = 46  # ((2492 [um**3])**(1/3) / 2[px/um])**(2) = 45.952[px**2]
            cell.lambdaVolume = 4
            # cell variables
            b_ki67 = (np.random.uniform() < 0.5)
            cell.dict['ki67int'] = int(b_ki67)
            cell.dict['ki67'] = b_ki67  # False is Ki67 negative, True is Ki67 positive
            cell.dict['time_hypoxia'] = 0
            cell.dict['red'] = 0
            cell.dict['green'] = 0
            # chemotaxis specified in xml

    def step(self, mcs):
        field = self.field.oxygen
        for cell in self.cellList:
            # get cell surrounding oxygen level
            r_o2 = field[cell.xCOM, cell.yCOM, cell.zCOM]

            # deterministic necrosis
            if (r_o2 < r_sigma_n):
                cell.type = self.NECROTIC
                cell.fluctAmpl = -1
                cell.dict['ki67'] = None
                cell.dict['ki67int'] = 0

            # GFP non proliferating
            elif (r_o2 < r_sigma_t):
                cell.type = self.GFP
                cell.dict['ki67'] = cell.dict['ki67']
                cell.dict['ki67int'] = int(cell.dict['ki67'])

            # GFP proliferating or doomed for necrosis
            elif (r_o2 < r_sigma_h):
                # 0.5 chance GFP proliferate or necrosis
                if (np.random.uniform() < 0.5):
                    cell.type = self.GFP
                    if (not cell.dict['ki67']) and (np.random.uniform() < r_ki67_np_rate):
                        cell.dict['ki67'] = True
                        cell.dict['ki67int'] = 1
                else:
                    # permanent hypoxic gene switch
                    cell.type = self.HYPOXIA
                    cell.dict['ki67'] = cell.dict['ki67']
                    cell.dict['ki67int'] = int(cell.dict['ki67'])

            # red cell - stay cool!
            else:
                cell.type = self.DSRED
                if (not cell.dict['ki67']) and (np.random.uniform() < r_ki67_np_rate):
                    cell.dict['ki67'] = True
                    cell.dict['ki67int'] = 1

            # update the proteins
            if (cell.type == self.GFP):
                # bue: to be done implement protein stuff
                pass


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


class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def start(self):
        pass

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list:
            if cell.dict['ki67'] and (np.random.uniform() < r_ki67_pn_rate):
                cells_to_divide.append(cell)

        for cell in cells_to_divide:
            self.divide_cell_random_orientation(cell)

    def update_attributes(self):
        self.clone_parent_2_child()

