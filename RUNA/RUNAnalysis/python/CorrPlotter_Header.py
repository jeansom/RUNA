#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Alphabet import *
from RUNA.RUNAnalysis.Plotting_Header import *
#############################################################
### Provides methods to make 1D, 2D, and Profile Plots.   ###
### Also sets the maximum and minimum for a set of plots. ###
#############################################################

# Fills a plot from a file
#### File: Name of file containing TTree
#### tree: Name of TTree in File
#### plot: Histogram to fill
#### var: Variable to plot 
#### Cut: Cut to apply to tree
#### Weight: Weight to apply to each entry

def GetQuantileProfiles(Th2f, cut, name):
    q1 = []
    nxbins = Th2f.GetXaxis().GetNbins();
    xlo = Th2f.GetXaxis().GetBinLowEdge(1);
    xhi = Th2f.GetXaxis().GetBinUpEdge(Th2f.GetXaxis().GetNbins() );
    for i in range(nxbins):
        H = Th2f.ProjectionY("ProjY"+str(i),i+1,i+1)
        probSum = array('d', [cut])
        q = array('d', [0.0]*len(probSum))
        H.GetQuantiles(len(probSum), q, probSum)
        q1.append(q[0])
    H1 = TH1F(name, "", nxbins,xlo,xhi)
    for i in range(nxbins):
        H1.SetBinContent(i+1,q1[i])
    return H1


def CorrPlotter(name, Input, V0, V1, Cuts, presel, tagB, tagD):
    print "making correlation plot ..."
    Vars = [V0[0], V1[0], V0[1],V0[2],V0[3], V1[1], V1[2],V1[3]]
    A = Alphabet("A_"+V1[0]+V1[0], Input, [])
    A.SetRegions(Vars, Cuts, tagB, tagD)
    A.TwoDPlot.SetStats(0)
    A.TwoDPlot.GetYaxis().SetTitle(V1[4])
    A.TwoDPlot.GetXaxis().SetTitle(V0[4])
    ProfsM = []
    for i in [9,8,7,6,5,4,3,2,1,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]:
        ProfsM.append(GetQuantileProfiles(A.TwoDPlot, 0.1*i, name+V1[0]+V0[0]+str(i)))
    return [A.TwoDPlot, ProfsM]

def GetQuantileProfiles2(Th2f, cut, name):
    q1 = []
    nxbins = Th2f.GetXaxis().GetNbins();
    xlo = Th2f.GetXaxis().GetBinLowEdge(1);
    xhi = Th2f.GetXaxis().GetBinUpEdge(Th2f.GetXaxis().GetNbins() );
    for i in range(nxbins):
        H = Th2f.ProjectionY("ProjY"+str(i),i+1,i+1)
        probSum = array('d', [cut])
        q = array('d', [0.0]*len(probSum))
        H.GetQuantiles(len(probSum), q, probSum)
        q1.append(q[0])
    H1 = TH1F(name, "", nxbins,xlo,xhi)
    for i in range(nxbins):
        H1.SetBinContent(i+1,q1[i])
    return H1
