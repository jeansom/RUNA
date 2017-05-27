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
    def __init__( self, name, Dist_Plus, Dist_Minus, Dist_Sig ):
        self.name = name
        self.DP = Dist_Plus # Distributions to add in bkg est
        self.DM = Dist_Minus # Distributions to subtract in bkg est
        self.SIG = Dist_Sig
    # Makes basic ABCD plot using Dist_Plus - Dist_Minus
    #### var_array: [ x var, y var, x n bins, x min, x max, y n bins, y min, y max ]
    #### presel: Set of cuts to apply as preselection before defining ABCD regions
    def MakeABCDRegions( self, var_array, presel ):
        self.PABCD = TH2F( "added_ABCD_" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # ABCD Plot to add
        self.MABCD = TH2F( "subbed_ABCD_" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # ABCD Plot to subtract
        for i in self.DP: # Adds all the ABCD plots for the plus distributions
            quick2dplot( i.File, i.Tree, self.PABCD, var_array[0], var_array[1], presel, i.Weight )
        for i in self.DM: # Adds all the ABCD plots for the minus distributions
            quick2dplot( i.File, i.Tree, self.MABCD, var_array[0], var_array[1], presel, i.Weight )

        self.ABCD = self.PABCD.Clone( "ABCD_" + self.name ) #Final ABCD Plot
        self.ABCD.Add( self.MABCD, -1. ) # Subtracts minus ABCD Plots from plus ABCD Plots
        
    # Creates the B and D plot
    # The variable that defines the B and D regions is on the Y Axis
    # The variable to bin the fit in is on the x axis
    #### var_array: [ x var, y var, x n bins, x min, x max, y n bins, y min, y max ]
    #### presel: Set of cuts to apply as preselection before defining B vs D, includes the inverse of the cut that defines B vs A
    def SetRegions( self, var_array, presel ):
        self.X = var_array[0] # variable to bin the fit in
        self.Pplots = TH2F( "added" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # Plot with the samples to add for the bkg est, 2D
        self.Mplots = TH2F( "subbed" + self.name, "", var_array[2], var_array[3], var_array[4], var_array[5], var_array[6], var_array[7] ) # Plot with the samples to subtract for the bkg est, 2D
        self.PplotsB = TH1F( "addedB" + self.name, "", var_array[2], var_array[3], var_array[4] ) # Plot with the samples to add for the bkg est, B
        self.MplotsB = TH1F( "subbedB" + self.name, "", var_array[2], var_array[3], var_array[4] ) # Plot with the samples to subtract for the bkg est, B
        self.PplotsD = TH1F( "addedD" + self.name, "", var_array[2], var_array[3], var_array[4] ) # Plot with the samples to add for the bkg est, D
        self.MplotsD = TH1F( "subbedD" + self.name, "", var_array[2], var_array[3], var_array[4] ) # Plot with the samples to subtract for the bkg est, D

        # Actual making of plots
        for i in self.DP: # Adds all the plus distributions together in self.Pplots
            print i.name
            quick2dplot( i.File, i.Tree, self.Pplots, var_array[0], var_array[1], presel, i.weight )
        for j in self.DM: # Adds all the minus distributions together in self.Mplots
            print i.name
            quick2dplot( j.File, j.Tree, self.Mplots, var_array[0], var_array[1], presel, j.weight )
        
        self.TwoDPlot = self.Pplots.Clone( "TwoDPlot_"+self.name) #Final 2D plot
        self.TwoDPlot.Add( self.Mplots, -1. ) # Subtracts minus plots from plus plots

        self.BPlot = self.PplotsB.Clone( "BPlot_"+self.name ) # Final B Plot
        self.BPlot.Add( self.MplotsB, -1. ) # Subtracts minus B plots from plus B plots

        self.DPlot = self.PplotsD.Clone( "DPlot_"+self.name ) # Final D Plot
        self.DPlot.Add( self.MplotsD, -1. ) # Subtracts minus D plots from plus D plots


    # Fits the ratio B/D to a function of form FIT
    #### cut: cut which defines B vs D
    #### bins: bins to measure B/D in 
    #### center: the x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
    #### FIT: Form to fit B/D to, should be a member of one of the Converters.py classes, already initialized and set up
    #### binBoundaries: not actually used, ignore
    def GetRates( self, cut, bins, truthbins, center, FIT, binBoundaries  ):
        self.center = center
        GComp = AlphabetSlicer( self.TwoDPlot, bins, cut[0], cut[1], center ) # Returns a TGraphAsymErrors containing B/D

        if len(truthbins)>0:
            TG = (AlphabetSlicer( self.TwoDPlot, truthbins, cut[0],cut[1],center))
            self.truthG = TG[0]
            self.G = GComp[0]
            self.x = TG[1]+GComp[1]
            self.y = TG[2]+GComp[2]
            self.exl = TG[3]+GComp[3]
            self.exh = TG[4]+GComp[4]
            self.eyl = TG[5]+GComp[5]
            self.eyh= TG[6]+GComp[6]
        else: 
            TG = []
            self.truthG = None
            self.G = GComp[0]
            self.x = GComp[1]
            self.y = GComp[2]
            self.exl = GComp[3]
            self.exh = GComp[4]
            self.eyl = GComp[5]
            self.eyh= GComp[6]

        self.fitter = False
        self.Fit = FIT
        self.binBoundaries = binBoundaries
        self.fitVal, self.fitErr = AlphabetFitter( self.G, self.Fit, self.fitter, bins, truthbins ) # Does the entire fitting; creates all three distributions (nominal, up, down); saves as self.Fit.fit, self.Fit.ErrUp, self.Fit.ErrDn

    # Makes the actual background estimation plots (nominal, up, down, signal region, antitag region...)
    #### binBoundaries: Boundary of the bins for the estimation plot
    #### antitag: cut that defines C region
    #### tag: cut that defines signal (A) region
    def MakeEst( self, variable, binBoundaries, antitag, tag, fit, rhoBinBoundaries ):
        if self.G.GetN() > 0:
            self.Fit.MakeConvFactor( self.X, self.center ) # Creates a string of the fit to B/D with self.X-self.center plugged in
        if not self.G.GetN() > 0:
            self.Fit.ConvFact = "(0)"
            self.Fit.ConvFactUp = "(0)"
            self.Fit.ConvFactDn = "(0)"
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
        self.hists_SIG = []

        for i in self.SIG:
            temphist = TH1F( "Hist_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            quickplot( i.File, i.Tree, temphist, variable, tag, i.weight )
            self.hists_SIG.append(temphist)

        # First for each distribution to be added
        for i in self.DP:
            # Makes a histogram for each distribution
            temphist = TH1F( "Hist_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistN = TH1F( "Hist_NOMINAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistU = TH1F( "Hist_UP"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistD = TH1F( "Hist_DOWN"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistA = TH1F( "Hist_ATAG"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))

            # 2d plot used to find the final estimate, make sure rhoBinBoundaries has small enough bins
            temphist2DN = TH2F( "Hist2D_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries), len(rhoBinBoundaries)-1, array('d',rhoBinBoundaries))

            quickplot( i.File, i.Tree, temphist, variable, tag, i.weight )
            quick2dplot( i.File, i.Tree, temphist2DN, variable, self.X, antitag, "("+i.weight+")" )

            # Loop through bins in 2d plot
            for j in xrange(1,(temphist2DN.GetXaxis().GetNbins()+1)):
                for k in xrange(1,(temphist2DN.GetYaxis().GetNbins()+1)):
                    rhoVal = temphist2DN.GetYaxis().GetBinCenter(k) # Value to use to find the transfer factor
                    bin = temphistN.FindBin(temphist2DN.GetXaxis().GetBinCenter(j)) # Bin in the final estimate

                    con = temphistN.GetBinContent(bin)
                    conU = temphistU.GetBinContent(bin)
                    conD = temphistD.GetBinContent(bin)
                    conA = temphistA.GetBinContent(bin)

                    # If not fitting the TF, find the value of B/D for the bin (rhoVal)
                    if not fit: 
                        for l in xrange(len(self.x)):
                            if rhoVal < (self.exh[l]+self.x[l]) and rhoVal >= (self.x[l]-self.exl[l]):
                                temphistN.SetBinContent(bin, con+((temphist2DN.GetBinContent(j,k))*self.y[l]))
                                temphistU.SetBinContent(bin, conU+((temphist2DN.GetBinContent(j,k))*(self.y[l]+self.eyh[l])))
                                temphistD.SetBinContent(bin, conD+((temphist2DN.GetBinContent(j,k))*(self.y[l]-self.eyl[l])))
                    elif fit: # If fitting
                        temphistN.SetBinContent(bin, con+((temphist2DN.GetBinContent(j,k))*self.Fit.ConvFact.Eval(temphist2DN.GetYaxis().GetBinCenter(k))))
                        temphistU.SetBinContent(bin, conU+((temphist2DN.GetBinContent(j,k))*(self.Fit.ConvFactUp.Eval(temphist2DN.GetYaxis().GetBinCenter(k)))))
                        temphistD.SetBinContent(bin, conD+((temphist2DN.GetBinContent(j,k))*(self.Fit.ConvFactDn.Eval(temphist2DN.GetYaxis().GetBinCenter(k)))))

                    temphistA.SetBinContent(bin, conA+((temphist2DN.GetBinContent(j,k))))

            # Adds the histograms for each distribution together
            self.hists_MSR.append( temphist )
            self.hists_EST.append( temphistN )
            self.hists_EST_UP.append( temphistU )
            self.hists_EST_DN.append( temphistD )
            self.hists_ATAG.append( temphistA )

        # Now for each distribution to be subtracted, do the same thing as before
        for i in self.DM:
            temphist = TH1F( "Hist_SUB_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistN = TH1F( "Hist_SUB_NOMINAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistU = TH1F( "Hist_SUB_UP"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistD = TH1F( "Hist_SUB_DOWN"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphistA = TH1F( "Hist_SUB_ATAG"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
            temphist2DN = TH2F( "Hist2D_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries), len(rhoBinBoundaries)-1, array('d',rhoBinBoundaries))
            quickplot( i.File, i.Tree, temphist, variable, tag, i.weight )
            quick2dplot( i.File, i.Tree, temphist2DN, variable, self.X, antitag, "("+i.weight+")" )

            for j in xrange(1,(temphist2DN.GetXaxis().GetNbins()+1)):
                for k in xrange(1,(temphist2DN.GetYaxis().GetNbins()+1)):
                    rhoVal = temphist2DN.GetYaxis().GetBinCenter(k)
                    bin = temphistN.FindBin(temphist2DN.GetXaxis().GetBinCenter(j))
                    con = temphistN.GetBinContent(bin)
                    conU = temphistU.GetBinContent(bin)
                    conD = temphistD.GetBinContent(bin)
                    conA = temphistA.GetBinContent(bin)
                    if not fit:
                        for l in xrange(len(self.x)):
                            if rhoVal <= (self.exh[l]+self.x[l]) and rhoVal > (self.x[l]-self.exl[l]):
                                temphistN.SetBinContent(bin, con+((temphist2DN.GetBinContent(j,k))*self.y[l]))
                                temphistU.SetBinContent(bin, conU+((temphist2DN.GetBinContent(j,k))*(self.y[l]+self.eyh[l])))
                                temphistD.SetBinContent(bin, conD+((temphist2DN.GetBinContent(j,k))*(self.y[l]-self.eyl[l])))
                    elif fit:
                        temphistN.SetBinContent(bin, con+((temphist2DN.GetBinContent(j,k))*self.Fit.ConvFact.Eval(temphist2DN.GetYaxis().GetBinCenter(k))))
                        temphistU.SetBinContent(bin, conU+((temphist2DN.GetBinContent(j,k))*(self.Fit.ConvFactUp.Eval(temphist2DN.GetYaxis().GetBinCenter(k)))))
                        temphistD.SetBinContent(bin, conD+((temphist2DN.GetBinContent(j,k))*(self.Fit.ConvFactDn.Eval(temphist2DN.GetYaxis().GetBinCenter(k)))))

                    temphistA.SetBinContent(bin, conA+((temphist2DN.GetBinContent(j,k))))

            # Adds the histograms for each distribution together
            self.hists_MSR_SUB.append( temphist )
            self.hists_EST_SUB.append( temphistN )
            self.hists_EST_SUB_UP.append( temphistU )
            self.hists_EST_SUB_DN.append( temphistD )
            self.hists_ATAG_SUB.append( temphistA )
