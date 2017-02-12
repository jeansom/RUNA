#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Plotting_Header import *

#####################################
### Basic distribution definition ###
#####################################

class DIST:
    # Sets basic variables
    #### name: Distribution name
    #### File: File containing TTree
    #### Tree: TTree name
    #### weight: Any weight to apply to events (eg, lumi weight, pu weight)
    def __init__( self, name, File, Tree, weight ):
        self.name = name
        self.File = File
        self.Tree = Tree
        self.weight = weight
