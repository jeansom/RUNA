#!/usr/bin/env python

'''
File: MyAnalyzer.py --mass 50 (optional) --debug -- final --jetAlgo AK5
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time, re
import csv
from math import *
from string import *
from array import array
import argparse
from ROOT import * 
from collections import OrderedDict
from multiprocessing import Process
import numpy as np
try: 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
	from RUNA.RUNAnalysis.commonFunctions import *
	from RUNA.RUNAnalysis.TCutTest import *
except ImportError: 
	sys.path.append('../python') 
	import tdrstyle as tdrstyle
	from commonFunctions import *


TMVA.Tools.Instance()
gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)


#----------------------------------------------------------------------
### Main Optimization
def makeTable( BkgSamples, SigSamples, treename, varList, mass, window, cutsList, BTAG ):
    """docstring for makeTable"""



    cuts = {}
    cutlist = ()
    cutLengths = {}
    combinations = []
    for var in varList:
	    length = 0
	    cutVar = []
	    minVal = var[2]
	    maxVal = var[3]
	    step = var[5]
	    i = minVal
	    while i <= maxVal:
                    cutVar.append( i )
                    length+=1
		    i += step
	    cutLengths[ var[0] ] = length
	    cuts[ var[0] ] = cutVar
    possCombs( 0, varList, cuts, combinations, cutlist )

    outputTextFile = 'OptimizationFiles/RPVStopStopToJets_UDD323_Signal_Bkg_'+str(mass)+'11216_'+BTAG+'.csv'
    output = open( outputTextFile, 'wt' )

    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    OptimizedCuts = TH1F( "OptimizedCuts", "Optimized Cuts", len(combinations)+1, 0, len(combinations)+1 )

    #-------------------------Event Loop-------------------------#

    #Signal
    SigTable = {}
    Sig = []
    
    SigTableScaled = {}
    SigScaled = []
    print len(combinations)
    for k in xrange( len(combinations) ):
	    Sig.append(0)		    
	    SigScaled.append(0)
    for sigSample in SigSamples:
	    for k in xrange( len(combinations) ):
		    Sig[k] = 0
		    SigScaled[k] = 0

	    SigScaled = TH1F("SigScaled", "", 500, 0, 500)
	    Sig = TH1F("Sig", "", 500, 0, 500)

	    for k in xrange( len(combinations) ):
		    cut = ""
		    for j in xrange( len(combinations[k])):
			    cut = cut+varList[j][0]+"<"+str(combinations[k][j])
			    if j < len(combinations[k]) - 1: 
				    cut= cut+"&"

		    quickplot(SigSamples[sigSample], "BoostedAnalysisPlots/RUNATree", SigScaled, "massAve", cut, "lumiWeight*puWeight")
		    quickplot(SigSamples[sigSample], "BoostedAnalysisPlots/RUNATree", Sig, "massAve", cut, "1.0") 
		    SigScaled[k] = SigScaled.Integral(0,5000)
		    Sig[k] = Sig.Integral(0,5000)
	    SigTable[ sigSample ] = tuple(Sig)
	    SigTableScaled[ sigSample ] = tuple(SigScaled)


    #Background
    BkgTable = {}
    Bkg = []

    BkgTableScaled = {}
    BkgScaled = []

    for k in xrange( len(combinations) ):
	    Bkg.append(0)
	    BkgScaled.append(0)
    
    for bkgSample in BkgSamples:
	    for k in xrange( len(combinations) ):
		    Bkg[k] = 0
		    BkgScaled[k] = 0
		    
	    BkgScaled = TH1F("SigScaled", "", 500, 0, 500)
	    Bkg = TH1F("Sig", "", 500, 0, 500)

	    for k in xrange( len(combinations) ):
		    cut = ""
		    for j in xrange( len(combinations[k])):
			    cut = cut+varList[j][0]+"<"+str(combinations[k][j])
			    if j < len(combinations[k]) - 1: 
				    cut= cut+"&"
		    quickplot(BkgSamples[bkgSample], "BoostedAnalysisPlots/RUNATree", BkgScaled, "massAve", cut, "lumiWeight*puWeight") 
		    quickplot(BkgSamples[bkgSample], "BoostedAnalysisPlots/RUNATree", Bkg, "massAve", cut, "1.0") 
		    BkgScaled[k] = BkgScaled.Integral(0,5000)
		    Bkg[k] = Bkg.Integral(0,5000)

	    
	    BkgTable[ bkgSample ] = tuple(Bkg)
	    BkgTableScaled[ bkgSample ] = tuple(BkgScaled)
	    print 'Writing ' + bkgSample + ' values to ' + outputTextFile
#	    for k in xrange( len(combinations) ):
#		    print >> open( outputTextFile, 'w+'), str(BkgTable[ bkgName ][k]) + '\t\t\t' + str(BkgTableScaled[ bkgName ][k]) + '\t\t\t' + bkgName + "\t\t\t" + str( combinations[k] ) 



    for k in xrange( len(combinations) ):
	    comb = ""
	    for j in xrange( len(combinations[k])):
		    comb += str(combinations[k][j])
		    comb += "  "
		    writer.writerow([ comb ] )
	    for sig in SigSamples:
		    writer.writerow( [str(sig), str(SigTableScaled[ sig ][k]*2666), str(SigTable[ sig ][k])] )
	    for bkg in BkgSamples:
		    writer.writerow( [str(bkg), str(BkgTableScaled[ bkg ][k]*2666), str(BkgTable[ bkg ][k])] )
    output.close()
				    
    totalBkgTable = []
    for k in xrange( len(combinations) ):
	    totalBkgTable.append(0)
    for bkgSample in BkgSamples:
	    for k in xrange( len(combinations) ):
		    totalBkgTable[k] += BkgTable[ bkgSample ][k]

    Sig_SqrtB = []

    for sig in SigSamples:
	    for k in xrange( len(combinations) ):
		    if totalBkgTable[k] is not 0:
			    print str(SigTable[ sig ][k]/sqrt( totalBkgTable[k] ) ) + "\t\t\t" + str( combinations[k] )
			    Sig_SqrtB.append( 2666*SigTable[ sig ][k]/sqrt( totalBkgTable[k] ) )
    Sig_SqrtB.sort()
    for k in xrange(len(Sig_SqrtB)):
	    OptimizedCuts.Fill(k+1,Sig_SqrtB(k))						 
    C = TCanvas( "C", "", 0, len(Sig_SqrtB+5) )
    C.cd()
    OptimizedCuts.Draw()
    C.SaveAs("OptimizedCuts.gif")


def possCombs(currentVarIndex, varList, cuts, combinations, cutlist = () ):
    tempCutList = []
    cutlist2 = list(cutlist)
    if  currentVarIndex is len(varList):
        combinations.append(cutlist)
    else:
	    tempCutList = cuts[ varList[ currentVarIndex ][0] ]
	    for i in xrange(len(tempCutList)):
		    cutlist2.append(tempCutList[i])
		    possCombs( currentVarIndex + 1, varList, cuts, combinations, tuple(cutlist2) )
		    del cutlist2[-1]
                
            
                
#----------------------------------------------------------------------

#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-t', '--typeROC', action='store',  dest='typeROC', default='var', help='Type of ROC: variables only (var) or bkgs only (bkg)')
	parser.add_argument( '-P', '--printValue', action='store',  dest='printValue', type=bool, default=False, help='Print values of ROCs')
	parser.add_argument( '-q', '--quantity', action='store',  dest='quantity', default='massAsym', help='Variable to print ROC.')
	parser.add_argument( '-s', '--selection', action='store',  dest='selection', default='', help='Selection, like _cutDEta' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='Simple', help='Process: simple or TMVA' )
	parser.add_argument( '-v', '--version', action='store',  dest='version', default='Boosted', help='Variable to optimize, as histogram in rootfile.' )
	parser.add_argument( '-e', '--eff', action='store', dest='effS', type=int, default=0, help='Mass of the Stop' )
	parser.add_argument('-Q', '--QCD', action='store', default='Pt', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-E', '--extension', action='store', dest='ext', default='png', help='Extension of plots.' )
	parser.add_argument( '-b', '--batchSys', action='store',  dest='batchSys', type=bool, default=False, help='Process: all or single.' )
	parser.add_argument( '-n', '--num', action='store', type=int, dest='num', default=0, help='num' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	selection = args.selection
	process = args.process
	version = args.version
	typeROC = args.typeROC
	quantity = args.quantity
	printValue = args.printValue
	effS = args.effS
	qcd = args.QCD

	if args.batchSys: folder = '/cms/gomez/archiveEOS/Archive/763patch2/v5/'
	else: folder = 'RootFiles/'

	bkgSamples = OrderedDict()
	bkgSamples[ 'QCD'+qcd+'All' ] = [ folder+'/RUNAnalysis_QCD'+qcd+'All_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kBlue-4 ]
	bkgSamples[ 'TTJets' ] = [ folder+'/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kGreen ]
	bkgSamples[ 'WJetsToQQ' ] = [ folder+'/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kMagenta ]
	bkgSamples[ 'ZJetsToQQ' ] = [ folder+'/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kOrange ]
	bkgSamples[ 'WWTo4Q' ] = [ folder+'/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kMagenta+2 ]
	bkgSamples[ 'ZZTo4Q' ] = [ folder+'/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kOrange+2 ]
	bkgSamples[ 'WZ' ] = [ folder+'/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root', kCyan ]

	sigSamples = {}
	sigSamples[ 'RPVSt'+str(mass) ] = folder+'/RUNAnalysis_RPVStopStopToJets_UDD323_M-'+str(mass)+'_RunIISummer16MiniAODv2_v76x_v2p0_v05.root'
#	sigSamples[ 'RPVSt'+str(mass) ] = folder+'/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v2p0_v05.root'
	#sigSamples[ 'WWTo4Q' ] = folder+'/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'ZZTo4Q' ] = folder+'/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'WZ' ] = folder+'/RUNAnalysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'TTJets' ] = folder+'/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'WJetsToQQ' ] = folder+'/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'
	#sigSamples[ 'ZJetsToQQ' ] = folder+'/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'

	SigSample = folder+'/RUNAnalysis_RPVStopStopToJets_UDD323_M-'+str(mass)+'-madgraph_RunIISummer16MiniAODv2-74X_Asympt25ns_v09_v03.root'
	treename = "ResolvedAnalysisPlots/RUNATree" if ( 'Resolved' in version ) else 'BoostedAnalysisPlots/RUNATree'
	print treename

	var = [
                ##    0        1        2     3     4         5        6
		## Version, Variable, nSteps, minX, maxX, Below value, step
		#[ 'Resolved', 'mindR', 50, 0., 5., True, 0., 0.8 ],
		[ 'Resolved', 'deltaEta', 50, 0., 5., True, 0., 0.65 ],
		[ 'Resolved', 'massAsym', 20, 0., 1., True, 0., 0.64 ],
		[ 'Resolved', 'cosThetaStar1', 20, 0., 1., True, 0., 0.70 ],
		[ 'Resolved', 'cosThetaStar2', 20, 0., 1., True, 0., 0.70 ],
		[ 'Resolved', 'delta1', 30, -500, 1000,  False, 0, 0.6 ],
		[ 'Resolved', 'delta2', 30, -500, 1000, False, 0, 0.6 ],
		#[ 'Resolved', 'xi1', 20, 0., 1., True, 0, 0.6 ],
		#[ 'Resolved', 'xi2', 20, 0., 1., True , 0, 0.6],
		##### RPV St 100
#		[ 'Boosted', "prunedMassAsym", 20, 0., 1., True, 0.2, 0.9 ],
#		[ 'Boosted', "jet1CosThetaStar", 20, 0., 1, True, 0., 0.8 ],
#		[ 'Boosted', "jet2CosThetaStar", 20, 0., 1, True, 0., 0.8 ],
#		[ 'Boosted', "jet1Tau21", 20, 0., 1., True, 0.5, 0.8  ],
#		[ 'Boosted', "jet2Tau21", 20, 0., 1., True, 0.5, 0.80 ],
#		[ 'Boosted', "jet1Tau31", 20, 0., 1., True, 0.3, 0.7 ],
#		[ 'Boosted', "jet2Tau31", 20, 0., 1., True, 0.3, 0.7 ],
#		[ 'Boosted', "jet1Tau32", 20, 0., 1., True, 0., 0  ],
#		[ 'Boosted', "jet2Tau32", 20, 0., 1., True, 0., 0  ],
#		[ 'Boosted', "deltaEtaDijet", 50, 0., 5., True, 0.4, 0.6 ],
#		[ 'Boosted', "jet1SubjetPtRatio", 20, 0., 1., True, 0., 0  ],
#		[ 'Boosted', "jet2SubjetPtRatio", 20, 0., 1., True, 0., 0  ],
		[ 'Boosted', "prunedMassAsym", 20, 0.05, 0.2, True, 0.05 ],
		#[ 'Boosted', "jet1CosThetaStar", 20, 0., 1, True, 0. ],
		#[ 'Boosted', "jet2CosThetaStar", 20, 0., 1, True, 0. ],
		[ 'Boosted', "jet1Tau21", 20, 0.35, 0.65, True, .05 ],
		[ 'Boosted', "jet2Tau21", 20, 0.35, 0.65, True, .05 ],
		#[ 'Boosted', "jet1Tau31", 20, 0., 1., True, 0. ],
		#[ 'Boosted', "jet2Tau31", 20, 0., 1., True, 0. ],
		#[ 'Boosted', "jet1Tau32", 20, 0., 1., True, 0. ],
		#[ 'Boosted', "jet2Tau32", 20, 0., 1., True, 0. ],
		[ 'Boosted', "deltaEtaDijet", 50, 0.5, 2.0, True, .5 ],
		#[ 'Boosted', "jet1SubjetPtRatio", 20, 0., 1., True, 0. ],
		#[ 'Boosted', "jet2SubjetPtRatio", 20, 0., 1., True, 0. ],
	]

        variables = [ x[1:] for x in var if (version in x[0] ) ]
	cuts = [ x[1:] for x in var if ( ( version in x[0] ) and ( x[6]!=x[3] ) ) ]      

	if args.num == 0:
		p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts, "oneJetL" ) )
		print "oneJetL"
	if args.num == 1:
		p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts, "oneJetM" ) )
		print "oneJetM"
	if args.num == 2:
		p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts, "oneJetT" ) )
		print "oneJetT"
	if args.num == 3:
		p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts, "oneSubjetL" ) )	
		print "oneSubjetL"
	if args.num == 4:
		p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts, "oneSubjetM" ) )	
		print "oneSubjetM"
	if args.num == 5:
		p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts, "oneSubjetperJetL" ) )	
		print "oneSubjetperJetL"
	if args.num == 6:
		p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, mass, 10, cuts, "oneSubjetperJetM" ) )	
		print "oneSubjetperJetM"

        p0.start()
        p0.join()


