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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f62ff49c310>), ('PMI2', <function <lambda> at 0x7f62ef2ed900>), ('PMI3', <function <lambda> at 0x7f62ef2ed990>), ('NPR1', <function <lambda> at 0x7f62ef2eda20>), ('NPR2', <function <lambda> at 0x7f62ef2edab0>), ('RadiusOfGyration', <function <lambda> at 0x7f62ef2edb40>), ('InertialShapeFactor', <function <lambda> at 0x7f62ef2edbd0>), ('Eccentricity', <function <lambda> at 0x7f62ef2edc60>), ('Asphericity', <function <lambda> at 0x7f62ef2edcf0>), ('SpherocityIndex', <function <lambda> at 0x7f62ef2edd80>), ('PBF', <function <lambda> at 0x7f62ef2ede10>)]
