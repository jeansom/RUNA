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
### !!!!!!!!!!!!!!!!!NEEDS TO BE COMMENTED MORE!!!!!!!!!!!!!!!!! ###


#############################################################
### Provides methods to make 1D, 2D, and Profile Plots.   ###
### Also sets the maximum and minimum for a set of plots. ###
#############################################################

# Creates a 2D plot with the quantile profiles for a given plot
#### Th2f: The 2D plot to get the quantile profiles of
#### cut: the efficiency of the cut?
#### name: name of new quantile profile plot
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

# Makes a plot of the correlation of a given 2D plot
#### name: name of new correlation plot
#### Input: the input distribution to use to make the plot?
#### V0: Array containing information about the variable on one axis; [ name, bins, lower bound, upper bound ]?
#### V1: Array containing information about the variable on one axis; [ name, bins, lower bound, upper bound ]?
#### Cuts: the preselection to apply
#### presel: UNNEEDED????
#### tagB: cuts to define the B region
#### tagD: cuts to define the D region
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

# Alternate method to create a 2D plot with the quantile profiles for a given plot; outdated?
#### Th2f: The 2D plot to get the quantile profiles of
#### cut: the efficiency of the cut?
#### name: name of new quantile profile plot
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
