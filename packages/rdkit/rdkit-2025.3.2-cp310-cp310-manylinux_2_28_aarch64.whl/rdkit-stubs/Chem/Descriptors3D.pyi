"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0xffffa3e04310>), ('PMI2', <function <lambda> at 0xffff96ac5900>), ('PMI3', <function <lambda> at 0xffff96ac5990>), ('NPR1', <function <lambda> at 0xffff96ac5a20>), ('NPR2', <function <lambda> at 0xffff96ac5ab0>), ('RadiusOfGyration', <function <lambda> at 0xffff96ac5b40>), ('InertialShapeFactor', <function <lambda> at 0xffff96ac5bd0>), ('Eccentricity', <function <lambda> at 0xffff96ac5c60>), ('Asphericity', <function <lambda> at 0xffff96ac5cf0>), ('SpherocityIndex', <function <lambda> at 0xffff96ac5d80>), ('PBF', <function <lambda> at 0xffff96ac5e10>)]
