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
descList: list  # value = [('PMI1', <function <lambda> at 0x10755a520>), ('PMI2', <function <lambda> at 0x1092e4f40>), ('PMI3', <function <lambda> at 0x1092e5080>), ('NPR1', <function <lambda> at 0x1092e5120>), ('NPR2', <function <lambda> at 0x1092e51c0>), ('RadiusOfGyration', <function <lambda> at 0x1092e5260>), ('InertialShapeFactor', <function <lambda> at 0x1092e5300>), ('Eccentricity', <function <lambda> at 0x1092e53a0>), ('Asphericity', <function <lambda> at 0x1092e5440>), ('SpherocityIndex', <function <lambda> at 0x1092e54e0>), ('PBF', <function <lambda> at 0x1092e5580>)]
