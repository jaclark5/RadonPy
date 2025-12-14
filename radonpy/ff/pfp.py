#  Copyright (c) 2025. Jennifer A. Clark.

# ******************************************************************************
# ff.pfp module
# ******************************************************************************

import os
import json


class PFP():
    """
    pfp.PFP() class

    Force field object with typing rules for Preferred Potential model.
    By default reads data file in force fields subdirectory.

    Attributes:
        ff_name: pfp
        pair_style: pfp_api
        ff_class: 'ml'
        bond_style: None
        angle_style: None
        dihedral_style: None
        improper_style: None
    """
    def __init__(self, db_file=None):
        if db_file is None:
            db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ff_dat', 'gaff.json')
        self.param = self.load_ff_json(db_file)
        self.name = 'pfp'
        self.pair_style = 'pfp_api'
        self.ff_class = 'ml'
        self.bond_style = None
        self.angle_style = None
        self.dihedral_style = None
        self.improper_style = None


    def ff_assign(self, mol, charge=None, retryMDL=True, useMDL=True):
        """
        PFP.ff_assign

        Args:
            mol: rdkit mol object

        Returns: (boolean)
            True: Success assignment
            False: Failure assignment
        """

        result = self.assign_ptypes(mol)

        return result


    def assign_ptypes(self, mol):
        """
        GAFF.assign_ptypes

        GAFF specific particle typing rules.

        Args:
            mol: rdkit mol object

        Returns:
            boolean
        """
        result_flag = True
        mol.SetProp('pair_style', self.pair_style)
        
        for p in mol.GetAtoms():
            p.SetProp('ff_type', p.GetSymbol())
        
        return result_flag


    def load_ff_json(self, json_file):
        with open(json_file) as f:
            j = json.loads(f.read())

        ff = self.Container()
        ff.pt = {}
        ff.bt = {}
        ff.at = {}
        ff.dt = {}
        ff.it = {}

        ff.ff_name = j.get('ff_name')
        ff.ff_class = j.get('ff_class')
        ff.pair_style = j.get('pair_style')
        
        for pt in j.get('particle_types'):
            pt_obj = self.Container()
            for key in pt.keys():
                setattr(pt_obj, key, pt[key])
            ff.pt[pt['name']] = pt_obj
        
        return ff
            
    
    class Container(object):
        pass
