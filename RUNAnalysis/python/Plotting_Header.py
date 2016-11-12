#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

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

def quickplot( File, tree, plot, var, Cut, Weight ):
    temp = plot.Clone( "temp" ) # Allows adding multiple distributions to single plot
    chain = ROOT.TChain( tree )
    chain.Add( File )
    chain.Draw( var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff" ) # Makes plot, adds cut, adds weights; "goff" = No graphics are generated
    plot.Add( temp ) # Adds the temporary plot to the original

# Fills a 2D plot from a file
#### File: Name of file containing TTree
#### tree: Name of TTree in File
#### plot: Histogram to fill
#### var: Variable to plot on x axis
#### var2: Variable to plot on y axis
#### Cut: Cut to apply to tree
#### Weight: Weight to apply to each entry

def quick2dplot( File, tree, plot, var, var2, Cut, Weight ):
    temp = plot.Clone( "temp" ) # Allows adding multiple distributions to single plot
    chain = ROOT.TChain( tree )
    chain.Add( File )
    chain.Draw( var2+":"+var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff" ) # Makes plot, adds cut, adds weights; "goff" = No graphics are generated
    plot.Add( temp ) # Adds the temporary plot to the original

# Makes a profile plot (both X and Y)
#### name: Profile plot name
#### plot: 2D plot to make profile of
def quickprofiles( name, plot ):
    X = plot.ProfileX( name+"_X" ) # X profile
    Y = plot.ProfileY( name+"_Y" ) # Y profile
    X.SetLineWidth(2)
    Y.SetLineWidth(2)
    X.SetLineColor(kRed)
    Y.SetLineColor(kGreen)
    return [X,Y]

# Takes a set of plots and sets the maximum and each to the maximum of them all
#### somset: Set of plots
#### log: Will the plots be on a log scale (then minimum should not be 0)
def FindAndSetMax( someset, log=True ):
    maximum = 0.0
    for i in someset: # Finds Maximum
        i.SetStats(0)
        t = i.GetMaximum()
        if t > maximum:
            maximum = t

    for j in someset: # Sets Maximum, Minimum
        if log: j.GetYaxis().SetRangeUser( 0.001, maximum*1.35 )
        else: j.GetYaxis().SetRangeUser( 0, maximum*1.35 )
