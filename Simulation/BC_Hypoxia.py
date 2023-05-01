# libararies
from cc3d import CompuCellSetup
from BC_HypoxiaSteppables import BC_HypoxiaSteppable

# register steppables
CompuCellSetup.register_steppable(steppable=BC_HypoxiaSteppable(frequency=1))

# run cc3d
CompuCellSetup.run()
