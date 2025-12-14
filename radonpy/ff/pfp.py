#  Copyright (c) 2025. Jennifer A. Clark.

# ******************************************************************************
# ff.pfp module
# ******************************************************************************

from ..core import utils
class PFP():
    """
    pfp.PFP() class

    Force field object for Preferred Potential model using pfp_api pair style.
    This is a machine learning-based force field that doesn't require traditional
    force field parameters - all interactions are handled by the pfp_api pair style.

    Attributes:
        ff_name: pfp
        pair_style: pfp_api
        ff_class: 'ml'
        bond_style: None
        angle_style: None
        dihedral_style: None
        improper_style: None
    """
    def __init__(self):
        self.name = 'pfp'
        self.pair_style = 'pfp_api'
        self.ff_class = 'ml'
        self.bond_style = None
        self.angle_style = None
        self.dihedral_style = None
        self.improper_style = None


    def ff_assign(self, mol, **kwargs):
        """
        PFP.ff_assign

        Args:
            mol: rdkit mol object

        Returns: (boolean)
            True: Success assignment
            False: Failure assignment
        """
        if kwargs:
            utils.radon_print(f"The following kwargs are not used in PFP: {kwargs}")

        result = self.assign_ptypes(mol)

        return result


    def assign_ptypes(self, mol):
        """
        PFP.assign_ptypes

        PFP specific particle typing rules.
        For pfp_api, particle types are simply the atomic symbols.

        Args:
            mol: rdkit mol object

        Returns:
            boolean
        """
        result_flag = True
        mol.SetProp('pair_style', self.pair_style)
        
        for p in mol.GetAtoms():
            p.SetProp('ff_type', p.GetSymbol())
            p.SetDoubleProp('AtomicCharge', 0.0)
        
        return result_flag
