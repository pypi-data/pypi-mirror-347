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
descList: list  # value = [('PMI1', <function <lambda> at 0x10576ecb0>), ('PMI2', <function <lambda> at 0x108672ef0>), ('PMI3', <function <lambda> at 0x108672f80>), ('NPR1', <function <lambda> at 0x108673010>), ('NPR2', <function <lambda> at 0x1086730a0>), ('RadiusOfGyration', <function <lambda> at 0x108673130>), ('InertialShapeFactor', <function <lambda> at 0x1086731c0>), ('Eccentricity', <function <lambda> at 0x108673250>), ('Asphericity', <function <lambda> at 0x1086732e0>), ('SpherocityIndex', <function <lambda> at 0x108673370>), ('PBF', <function <lambda> at 0x108673400>)]
