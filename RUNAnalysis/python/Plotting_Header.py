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

    # Friend tree, optional
    friendName = [ File.replace(".root","")+"_friendDDT_20_tau21.root" ] # If you want to add a friend Tree, put the name here
    for friendT in friendName:
        if( os.path.isfile(friendT) ):
            chainF = ROOT.TChain( "TF_20_tau21" )
            chainF.Add(friendT)
            chain.AddFriend(chainF)

    chain.Draw( var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff" ) # Makes plot, adds cut, adds weights; "goff" = No graphics are generated
    plot.Add( temp ) # Adds the temporary plot to the original

# Same as quickplot but 2d
#### var: Variable to plot on x axis
#### var2: Variable to plot on y axis

def quick2dplot( File, tree, plot, var, var2, Cut, Weight ):
    temp = plot.Clone( "temp" ) # Allows adding multiple distributions to single plot
    chain = ROOT.TChain( tree )
    chain.Add( File )
    friendName = [ File.replace(".root","")+"_friendDDT_20_tau21.root" ]
    for friendT in friendName:
        if( os.path.isfile(friendT) ):
            chainF = ROOT.TChain( "TF_20_tau21" )
            chainF.Add(friendT)
            chain.AddFriend(chainF)
    chain.Draw( var2+":"+var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff" ) # Makes plot, adds cut, adds weights; "goff" = No graphics are generated
    plot.Add( temp ) # Adds the temporary plot to the original

# Same as quickplot but 3d
#### var: Variable to plot on x axis
#### var2: Variable to plot on y axis
#### var3: Variable to plot on z axis

def quick3dplot( File, tree, plot, var, var2, var3, Cut, Weight ):
    temp = plot.Clone( "temp" ) # Allows adding multiple distributions to single plot
    chain = ROOT.TChain( tree )
    chain.Add( File )
    friendName = [ File.replace(".root","")+"_friendDDT_20_tau21.root" ]
    for friendT in friendName:
        if( os.path.isfile(friendT) ):
            chainF = ROOT.TChain( "TF_20_tau21" )
            chainF.Add(friendT)
            chain.AddFriend(chainF)
    chain.Draw( var3+":"+var2+":"+var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff" ) # Makes plot, adds cut, adds weights; "goff" = No graphics are generated
    plot.Add( temp ) # Adds the temporary plot to the original

# Makes profile plots (both X and Y)
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
        if isinstance( i, ROOT.TH1 ): i.SetStats(0)
        t = i.GetMaximum()
        if t > maximum:
            maximum = t
    for j in someset: # Sets Maximum, Minimum
        if log:
            j.SetMaximum(maximum*2)
            j.SetMinimum(1)

        else: 
            j.SetMaximum(maximum*1.35)
            j.SetMinimum(0)

# Formats a float for printing
#### N: a float
def formatFloatForPrint(N):
    if N > 1000.:
        String = str(int(N))
    elif N > 1.:
        String = "{0:3.2f}".format(N)
    elif N > 0.001:
        String = "{0:2.1f}%".format(N*100.)
    elif N > 0.0000001:
        String = "{0:2.2f} ppm".format(N*1000000.)
    else:
        String = str(N)
    return String

def removeNegativeBins(h1):
    for bin in xrange( 1, h1.GetNbinsX()+1 ):
        con = h1.GetBinContent(bin)
        if con < 0:
            h1.SetBinContent( bin, 0 )

from scipy.stats import chisquare
def ComputeChi2(points, fit):
    n = points.GetN()
    x = [ROOT.Double(0)]*n
    y = [ROOT.Double(0)]*n
    y2 = [0]*n
    for i in range(0,n):
        points.GetPoint(i, x[i], y[i])
        y2[i] = fit.Eval(y[i])
    x = scipy.array(x)
    y= scipy.array(y)
    y2 = scipy.array(y2)
    return chisquare(y,y2)[0]
