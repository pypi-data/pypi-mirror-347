from .molecule import main

class MolecularWeightCalculator:
    def __call__(self, formula):
        return main(formula)

import sys
sys.modules[__name__] = MolecularWeightCalculator()