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
descList: list  # value = [('PMI1', <function <lambda> at 0xffffa87b40e0>), ('PMI2', <function <lambda> at 0xffff9a1cf7e0>), ('PMI3', <function <lambda> at 0xffff9a1cf920>), ('NPR1', <function <lambda> at 0xffff9a1cf9c0>), ('NPR2', <function <lambda> at 0xffff9a1cfa60>), ('RadiusOfGyration', <function <lambda> at 0xffff9a1cfb00>), ('InertialShapeFactor', <function <lambda> at 0xffff9a1cfba0>), ('Eccentricity', <function <lambda> at 0xffff9a1cfc40>), ('Asphericity', <function <lambda> at 0xffff9a1cfce0>), ('SpherocityIndex', <function <lambda> at 0xffff9a1cfd80>), ('PBF', <function <lambda> at 0xffff9a1cfe20>)]
