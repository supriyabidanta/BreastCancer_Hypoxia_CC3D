
from cc3d import CompuCellSetup
        

from BC_HypoxiaSteppables import BC_HypoxiaSteppable

CompuCellSetup.register_steppable(steppable=BC_HypoxiaSteppable(frequency=1))


CompuCellSetup.run()
