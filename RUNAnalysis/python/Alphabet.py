#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Alphabet_Header import *
from RUNA.RUNAnalysis.Plotting_Header import *
from RUNA.RUNAnalysis.Converters import *
from RUNA.RUNAnalysis.Distribution_Header import *

########################################################################################
### This class has the methods needed to perform an ABCD background estimation.      ###
### It creates the A, B, C, D regions (see diagram below) based on two variables,    ###
### then creates a B/D plot, fits it to a transfer function, and calculates          ###
### C * (B/D) using the transfer function to create the final background estimation. ###
###                                                                                  ###
###                                 -----------                                      ###
###                            Fail | B  |  D |                                      ###
###                                 |----------                                      ###
###                            Pass | A  |  C |                                      ###
###                                 -----------                                      ###
###                                 Pass   Fail                                      ###
########################################################################################

class Alphabet:
    # Sets basic variables
    #### name: name for plots, etc
    #### Dist_Plus: Samples to add for background estimation
    #### Dist_Minus: Samples to subtract for background estimation
    def __init__( self, name, Dist_Plus, Dist_Minus ):
        self.name = name
        self.DP = Dist_Plus
        self.DM = Dist_Minus
        
    # Makes basic ABCD plot using Dist_Plus - Dist_Minus
    #### var_array: [ x var, y var, x n bins, x min, x max, y n bins, y min, y max ]
    #### presel: Set of cuts to apply as preselection before defining ABCD regions
    def MakeABCDRegions( self, var_array, presel ):
        self.PABCD = TH2F( "added_ABCD_" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # ABCD Plot to add
        self.MABCD = TH2F( "subbed_ABCD_" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # ABCD Plot to subtract
        for i in self.DP:
            quick2dplot( i.File, i.Tree, self.PABCD, var_array[0], var_array[1], presel, i.Weight )
        for i in self.DM:
            quick2dplot( i.File, i.Tree, self.MABCD, var_array[0], var_array[1], presel, i.Weight )

        self.ABCD = self.PABCD.Clone( "ABCD_" + self.name ) #Final ABCD Plot
        self.ABCD.Add( self.MABCD, -1. )
        
    # Creates the B and D plot
    # The variable that defines the B and D regions is on the Y Axis
    # The variable to bin the fit in is on the x axis
    #### var_array: [ x var, y var, x n bins, x min, x max, y n bins, y min, y max ]
    #### presel: Set of cuts to apply as preselection before defining B vs D, includes the inverse of the cut that defines B vs A
    def SetRegions( self, var_array, presel ):
        self.X = var_array[0] # variable to bin the fit in
        self.Pplots = TH2F( "added" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # Plot with the samples to add for the bkg est
        self.Mplots = TH2F( "subbed" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # Plot with the samples to subtract for the bkg est
        # Actual making of plots
        for i in self.DP:
            quick2dplot( i.File, i.Tree, self.Pplots, var_array[0], var_array[1], presel, i.weight )
        for j in self.DM:
            quick2dplot( j.File, j.Tree, self.Mplots, var_array[0], var_array[1], presel, j.weight )
        
            self.TwoDPlot = self.Pplots.Clone( "TwoDPlot_"+self.name) #Final 2D plot
            self.TwoDPlot.Add( self.Mplots, -1. )

    ############################################################
    ########### SKIPPED TRUTHBINS - WHAT ARE THEY? #############
    ############################################################
    # Fits the ratio B/D to a function of form FIT
    #### cut: cut which defines B vs D
    #### bins: bins to measure B/D in 
    #### center: the x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
    #### FIT: Form to fit B/D to, should be a member of one of the Converters.py classes, already initialized and set up
    def GetRates( self, cut, bins, center, FIT ):
        self.center = center
        self.G = AlphabetSlicer( self.TwoDPlot, bins, cut[0], cut[1], center ) # Returns a TGraphAsymErrors containing B/D
        self.Fit = FIT
        AlphabetFitter( self.G, self.Fit ) # Does the entire fitting; creates all three distributions (nominal, up, down); saves as self.Fit.fit, self.Fit.ErrUp, self.Fit.ErrDn

    # Makes the actual background estimation plots (nominal, up, down, signal region, antitag region...)
    #### binBoundaries: Boundary of the bins for the estimation plot
    #### antitag: cut that defines C region
    #### tag: cut that defines signal (A) region
    def MakeEst( self, variable, binBoundaries, antitag, tag ):
        self.Fit.MakeConvFactor( self.X, self.center ) # Creates a string of the fit to B/D with self.X-self.center plugged in
        
        self.hists_EST = [] # Nomimal background estimation (C * (B/D) )
        self.hists_EST_SUB = [] # Background estimation for subtracted distributions (C * (B/D))
        self.hists_EST_UP = [] # Up background estimation (C * (B/D) using fit with error up)
        self.hists_EST_SUB_UP = [] # Up background estimation for subtracted distributions (C * (B/D) using fit with error up )
        self.hists_EST_DN = [] # Down background estimation (C * (B/D) using fit with error down)
        self.hists_EST_SUB_DN = [] # Down background estimation for subtracted distributions (C * (B/D) using fit with error down )
        self.hists_MSR = [] # Actual signal region (A)
        self.hists_MSR_SUB = [] # Subtracted distributions signal regions (A)
        self.hists_ATAG = [] # Antitag region distribution (C)
        self.hists_ATAG_SUB = [] # Antitag region distribution for subtracted distributions(C)

        # First for each distribution to be added
        for i in self.DP:
            # Makes a histogram for each distribution
            temphist = TH1F( "Hist_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistN = TH1F( "Hist_NOMINAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistU = TH1F( "Hist_UP"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistD = TH1F( "Hist_DOWN"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistA = TH1F( "Hist_ATAG"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
        
            # Fills the above histograms
            quickplot( i.File, i.Tree, temphist, variable, tag, i.weight )
            quickplot( i.File, i.Tree, temphistN, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFact+")" )
            quickplot( i.File, i.Tree, temphistU, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactUp+")" )
            quickplot( i.File, i.Tree, temphistD, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactDn+")" )
            quickplot( i.File, i.Tree, temphistA, variable, antitag, i.weight )

            # Adds the histograms for each distribution together
            self.hists_MSR.append( temphist )
            self.hists_EST.append( temphistN )
            self.hists_EST_UP.append( temphistU )
            self.hists_EST_DN.append( temphistD )
            self.hists_ATAG.append( temphistA )

        # Now for each distribution to be subtracted
        for i in self.DM:
            # Makes a histogram for each distribution
            temphist = TH1F( "Hist_SUB_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistN = TH1F( "Hist_SUB_NOMINAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistU = TH1F( "Hist_SUB_UP"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistD = TH1F( "Hist_SUB_DOWN"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistA = TH1F( "Hist_SUB_ATAG"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
        
            # Fills the above histograms
            quickplot( i.File, i.Tree, temphist, variable, tag, i.weight )
            quickplot( i.File, i.Tree, temphistN, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFact+")" )
            quickplot( i.File, i.Tree, temphistU, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactUp+")" )
            quickplot( i.File, i.Tree, temphistD, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactDn+")" )
            quickplot( i.File, i.Tree, temphistA, variable, antitag, i.weight )

            # Adds the histograms for each distribution together
            self.hists_MSR_SUB.append( temphist )
            self.hists_EST_SUB.append( temphistN )
            self.hists_EST_SUB_UP.append( temphistU )
            self.hists_EST_SUB_DN.append( temphistD )
            self.hists_ATAG_SUB.append( temphistA )

        
    
