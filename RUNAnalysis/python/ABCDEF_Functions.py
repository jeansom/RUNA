#
import os
import math
from array import array
import optparse
import argparse
import ROOT
from ROOT import *
import scipy

import RUNA.RUNAnalysis.Alphabet_Header
from RUNA.RUNAnalysis.Alphabet_Header import *
import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.Converters
from RUNA.RUNAnalysis.Converters import *
import RUNA.RUNAnalysis.Distribution_Header
from RUNA.RUNAnalysis.Distribution_Header import *
import RUNA.RUNAnalysis.Alphabet
from RUNA.RUNAnalysis.Alphabet import *
import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi

def AppendMultiple( lists, items ):
    if (len(lists) == len(items)):
        for i in xrange(len(lists)): lists[i].append(items[i])

def RatioErr(BP, DP):
            if BP<0: BP = 0
            if DP<0: DP = 0
            isZero = ( DP == 0 or BP == 0 )

            eB, eD = math.sqrt(BP), math.sqrt(DP)

            if isZero: Ei = 0.
            else: Ei = float((BP/DP)*(eB/BP+eD/DP))

            eyh = (float(Ei))

            if DP > 0 and float(BP/DP)-Ei > 0: eyl = (float(Ei))
            else:
                if isZero: eyl = (0.)
                else: eyl = (float(BP/DP))

            return eyl, eyh

def GetBins( h, x1, x2, y1, y2 ):
    return h.GetXaxis().FindBin(x1), h.GetXaxis().FindBin(x2), h.GetYaxis().FindBin(y1), h.GetYaxis().FindBin(y2)

def FixWeights( h ):
    for bin in xrange(1, h.GetNbinsX()+1 ):
        h.SetBinContent(bin, h.GetBinContent(bin))

def FitErrors( bins, fit, fitResult ):
        listBinCenter = []
        fitErrors = []
        fitValues = []
        for i in xrange(0,len(bins)):
            if isinstance(bins[i], list): binCenter = float((bins[i][0]+bins[i][1])/2.)
            else: binCenter = float(bins[i])
            err = array('d',[0])
            fitResult.GetConfidenceIntervals( 1, 1, 1, array('d', [binCenter]), err, 0.683, False )
            AppendMultiple( [listBinCenter, fitErrors, fitValues], [float(binCenter), float(err[0]), float(fit.Eval(binCenter))] )

        ConvFactUp = TGraph( len(fitValues), array('d', listBinCenter ), numpy.add( fitValues, fitErrors ) )
	ConvFactDown = TGraph( len(fitValues), array('d', listBinCenter ), numpy.subtract( fitValues, fitErrors ) )

        return ConvFactUp, ConvFactDown

def PullErrors(EST, Pull2, DATA, ESTUP, ESTDN, A):
    Boxes = []
    sBoxes = []
    pBoxes = []
    maxy = 0.

    for i in xrange(1, EST.GetNbinsX()+1):
        P = Pull2.GetBinContent(i)
        Ve = DATA.GetBinError(i)
        Pull2.SetBinError(i,1.)
        u = ESTUP.GetBinContent(i)-EST.GetBinContent(i)
        d = EST.GetBinContent(i)-ESTDN.GetBinContent(i)
        if A.GetBinContent(i)==0: 
            a = 0
        else:
            a = A.GetBinError(i)*EST.GetBinContent(i)/A.GetBinContent(i) # othe
        y1 = EST.GetBinContent(i) - math.sqrt((d*d)+(a*a))
        y2 = EST.GetBinContent(i) + math.sqrt((u*u)+(a*a))
        x1 = EST.GetBinCenter(i) - (0.5*EST.GetBinWidth(i))
        x2 = EST.GetBinCenter(i) + (0.5*EST.GetBinWidth(i))
        s1 = EST.GetBinContent(i) - a
        if s1 < 0: s1 = 0
        s2 = EST.GetBinContent(i) + a
        if maxy < y2:
            maxy = y2
        if Ve > 1.:
            yP1 = -math.sqrt((d*d) + (a*a))/Ve # Bottom of pull error
            yP2 = math.sqrt((u*u) + (a*a))/Ve # Top of pull error
        else:
            yP1 = -math.sqrt((d*d) + (a*a)) # Bottom of pull error
            yP2 = math.sqrt((u*u) + (a*a)) # Top of pull error
        if Ve > 1:
            Pull2.SetBinContent( i, P/Ve ) # Filling normal pull
        tempbox = TBox(x1,y1,x2,y2)
        temppbox = TBox(x1,yP1,x2,yP2)
        tempsbox = TBox(x1,s1,x2,s2)
        AppendMultiple( [Boxes, sBoxes, pBoxes], [tempbox, tempsbox, temppbox] )
    return Boxes, sBoxes, pBoxes
