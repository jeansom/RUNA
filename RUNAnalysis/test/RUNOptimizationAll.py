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

    outputTextFile = 'OptimizationFiles/RPVStopStopToJets_UDD323_Signal_Bkg_'+str(mass)+'81216_'+BTAG+'.csv'
    output = open( outputTextFile, 'wt' )

    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    OptimizedCuts = TH1F( "OptimizedCuts", "Optimized Cuts", 0, len(combinations)+1, len(combinations)+1 )

    #-------------------------Event Loop-------------------------#

    #Signal
    SigTable = {}
    Sig = []
    
    SigTableScaled = {}
    SigScaled = []
    for k in xrange( len(combinations) ):
	    Sig.append(0)		    
	    SigScaled.append(0)
    for sigSample in SigSamples:
	    for k in xrange( len(combinations) ):
		    Sig[k] = 0
		    SigScaled[k] = 0
	    SigFile, sigEvents, sigNumEntries = getTree( SigSamples[ sigSample ], treename )
	    signalName = sigSample
	    d = 0
	    print '-'*40
	    print '---- Signal ', signalName
	    for i in xrange(sigNumEntries):
		    sigEvents.GetEntry(i)
			#---- progress of the reading --------
		    fraction = 10.*i/(1.*sigNumEntries)
		    if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		    d = TMath.FloorNint(fraction)
		    
		    sigSF = sigEvents.lumiWeight * sigEvents.puWeight
		    sigMassAve = ( sigEvents.prunedMassAve if 'Boosted' in version else sigEvents.avgMass  )

		    sigJet1CSVv2 = sigEvents.jet1btagCSVv2
		    sigJet2CSVv2 = sigEvents.jet2btagCSVv2
		    sigSubjet11CSVv2 = sigEvents.subjet11btagCSVv2
		    sigSubjet12CSVv2 = sigEvents.subjet12btagCSVv2
		    sigSubjet21CSVv2 = sigEvents.subjet21btagCSVv2
		    sigSubjet22CSVv2 = sigEvents.subjet22btagCSVv2
		    
		    
		    jet1L = (sigJet1CSVv2 > .460)
		    jet1M = (sigJet1CSVv2 > 0.800)
		    jet1T = (sigJet1CSVv2 > 0.935)
		    
		    jet2L = (sigJet2CSVv2 > .460)
		    jet2M = (sigJet2CSVv2 > 0.800)
		    jet2T = (sigJet2CSVv2 > 0.935)
	    
		    subjet11L = (sigSubjet11CSVv2 > 0.460)
		    subjet11M = (sigSubjet11CSVv2 > 0.800)
		    
		    subjet12L = (sigSubjet12CSVv2 > 0.460)
		    subjet12M = (sigSubjet12CSVv2 > 0.800)
		    
		    subjet21L = (sigSubjet21CSVv2 > 0.460)
		    subjet21M = (sigSubjet21CSVv2 > 0.800)
		    
		    subjet22L = (sigSubjet22CSVv2 > 0.460)
		    subjet22M = (sigSubjet22CSVv2 > 0.800)
		    
		    oneJetL = jet1L or jet2L
		    oneJetM = jet1M or jet2M
		    oneJetT = jet1T or jet2T
		    
		    numSubjetsLJet1 = 0
		    if subjet11L: numSubjetsLJet1+=1
		    if subjet12L: numSubjetsLJet1+=1
		    
		    numSubjetsMJet1 = 0
		    if subjet11M: numSubjetsMJet1+=1
		    if subjet12M: numSubjetsMJet1+=1
		    
		    
		    numSubjetsLJet2 = 0
		    if subjet21L: numSubjetsLJet2+=1
		    if subjet12L: numSubjetsLJet2+=1
		    
		    numSubjetsMJet2 = 0
		    if subjet21M: numSubjetsMJet2+=1
		    if subjet22M: numSubjetsMJet2+=1
		    
		
		    oneSubjetL = (numSubjetsLJet1 == 1) or (numSubjetsLJet2 == 1)
		    oneSubjetM = (numSubjetsMJet1 == 1) or (numSubjetsMJet2 == 1)
		    
		    oneSubjetperJetL = (numSubjetsLJet1 == 1) and (numSubjetsLJet2 == 1)
		    oneSubjetperJetM = (numSubjetsMJet1 == 1) and (numSubjetsMJet2 == 1)
		    
		    btagCut = True
		    
		    if( "oneJet" in BTAG ):
			    if( "L" in BTAG ): btagCut = oneJetL
			    if( "M" in BTAG ): btagCut = oneJetM
			    if( "T" in BTAG ): btagCut = oneJetT
		    if( "oneSubjetL" in BTAG ): btagCut = oneSubjetL
		    if( "oneSubjetM" in BTAG ): btagCut = oneSubjetM
		    if( "oneSubjetperJetL" in BTAG ): btagCut = oneSubjetperJetL
		    if( "oneSubjetperJetM" in BTAG ): btagCut = oneSubjetperJetM

		    if ( ( sigMassAve > int(mass)-window ) and ( sigMassAve < int(mass)+window )  and btagCut): 
			    for k in xrange( len(combinations) ):
				    sigCutsList = []
				    for j in xrange( len(combinations[k]) ):
				      
					    if ( getattr( sigEvents, varList[j][0] ) < combinations[k][j]):
						    sigCutsList.append( True )
					    else:
						    sigCutsList.append( False )
				    if all( sigCutsList ):
					    SigScaled[k] += sigSF
					    Sig[k] += 1
					    if SigScaled[k] < 0: print SigScaled[k]
			    SigTable[ signalName ] = tuple(Sig)
			    SigTableScaled[ signalName ] = tuple(SigScaled)

	    print 'Writing ' + signalName + ' values to ' + outputTextFile
#	    for k in xrange( len(combinations) ):
#		    print SigTable[ signalName ][k]
#		    print >> open( outputTextFile, 'w+'), str(SigTable[ signalName ][k]) + "\t\t\t" + str(SigTableScaled[ signalName ][k]) + "\t\t\t" + signalName + "\t\t\t" + str( combinations[k] )

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
	    BkgFile, bkgEvents, bkgNumEntries = getTree( BkgSamples[ bkgSample ][0], treename )
	    bkgName = bkgSample
	    d = 0
	    print '-'*40
	    print '---- Bkg ', bkgName
	    print '---      ', bkgNumEntries
	    for i in xrange(bkgNumEntries):
		    bkgEvents.GetEntry(i)
			#---- progress of the reading --------
		    fraction = 10.*i/(1.*bkgNumEntries)
		    if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		    d = TMath.FloorNint(fraction)	    
		    bkgSF = bkgEvents.lumiWeight * bkgEvents.puWeight
		    bkgMassAve = ( bkgEvents.prunedMassAve if 'Boosted' in version else bkgEvents.avgMass  )

		    bkgJet1CSVv2 = bkgEvents.jet1btagCSVv2
		    bkgJet2CSVv2 = bkgEvents.jet2btagCSVv2
		    bkgSubjet11CSVv2 = bkgEvents.subjet11btagCSVv2
		    bkgSubjet12CSVv2 = bkgEvents.subjet12btagCSVv2
		    bkgSubjet21CSVv2 = bkgEvents.subjet21btagCSVv2
		    bkgSubjet22CSVv2 = bkgEvents.subjet22btagCSVv2
		    
		    jet1L = (bkgJet1CSVv2 > .460)
		    jet1M = (bkgJet1CSVv2 > 0.800)
		    jet1T = (bkgJet1CSVv2 > 0.935)
		    
		    jet2L = (bkgJet2CSVv2 > .460)
		    jet2M = (bkgJet2CSVv2 > 0.800)
		    jet2T = (bkgJet2CSVv2 > 0.935)
		    
		    subjet11L = (bkgSubjet11CSVv2 > 0.460)
		    subjet11M = (bkgSubjet11CSVv2 > 0.800)
		    
		    subjet12L = (bkgSubjet12CSVv2 > 0.460)
		    subjet12M = (bkgSubjet12CSVv2 > 0.800)
		    
		    subjet21L = (bkgSubjet21CSVv2 > 0.460)
		    subjet21M = (bkgSubjet21CSVv2 > 0.800)
		    
		    subjet22L = (bkgSubjet22CSVv2 > 0.460)
		    subjet22M = (bkgSubjet22CSVv2 > 0.800)
		    
		    oneJetL = jet1L or jet2L
		    oneJetM = jet1M or jet2M
		    oneJetT = jet1T or jet2T
		    
		    numSubjetsLJet1 = 0
		    if subjet11L: numSubjetsLJet1+=1
		    if subjet12L: numSubjetsLJet1+=1
		    
		    numSubjetsMJet1 = 0
		    if subjet11M: numSubjetsMJet1+=1
		    if subjet12M: numSubjetsMJet1+=1
		    
		    
		    numSubjetsLJet2 = 0
		    if subjet21L: numSubjetsLJet2+=1
		    if subjet12L: numSubjetsLJet2+=1
		    
		    numSubjetsMJet2 = 0
		    if subjet21M: numSubjetsMJet2+=1
		    if subjet22M: numSubjetsMJet2+=1
		    
		    
		    oneSubjetL = (numSubjetsLJet1 == 1) or (numSubjetsLJet2 == 1)
		    oneSubjetM = (numSubjetsMJet1 == 1) or (numSubjetsMJet2 == 1)
		    
		    oneSubjetperJetL = (numSubjetsLJet1 == 1) and (numSubjetsLJet2 == 1)
		    oneSubjetperJetM = (numSubjetsMJet1 == 1) and (numSubjetsMJet2 == 1)		
		    
		    btagCut = True
		    
		    if( "oneJet" in BTAG ):
			    if( "L" in BTAG ): btagCut = oneJetL
			    if( "M" in BTAG ): btagCut = oneJetM
			    if( "T" in BTAG ): btagCut = oneJetT
		    if( "oneSubjetL" in BTAG ): btagCut = oneSubjetL
		    if( "oneSubjetM" in BTAG ): btagCut = oneSubjetM
		    if( "oneSubjetperJetL" in BTAG ): btagCut = oneSubjetperJetL
		    if( "oneSubjetperJetM" in BTAG ): btagCut = oneSubjetperJetM




		    if ( ( bkgMassAve > int(mass)-window ) and ( bkgMassAve < int(mass)+window  ) and btagCut): 
			    for k in xrange( len(combinations) ):
				    bkgCutsList = []
				    for j in xrange( len(combinations[k] ) ):
#					    print str(varList[j][0]) + " " + str( getattr( bkgEvents, varList[j][0] ) ) + " " + str( combinations[k][j] ) + " " + str( i )
					    if ( getattr( bkgEvents, varList[j][0] ) < combinations[k][j]):						    
						    bkgCutsList.append( True )
					    else:
						    bkgCutsList.append( False )
				    if all( bkgCutsList ):
					    BkgScaled[k] += bkgSF
					    Bkg[k] += 1
#					    print i
	    BkgTable[ bkgName ] = tuple(Bkg)
	    BkgTableScaled[ bkgName ] = tuple(BkgScaled)
	    print 'Writing ' + bkgName + ' values to ' + outputTextFile
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
	    OptimizedCuts->Fill(k+1,Sig_SqrtB(k))



						    
						    
    

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
		[ 'Boosted', "prunedMassAsym", 20, 0.0, 0.2, True, 0.05 ],
		#[ 'Boosted', "jet1CosThetaStar", 20, 0., 1, True, 0. ],
		#[ 'Boosted', "jet2CosThetaStar", 20, 0., 1, True, 0. ],
		[ 'Boosted', "jet1Tau21", 20, 0.35, 0.65, True, .05 ],
		[ 'Boosted', "jet2Tau21", 20, 0.35, 0.65, True, .05 ],
		#[ 'Boosted', "jet1Tau31", 20, 0., 1., True, 0. ],
		#[ 'Boosted', "jet2Tau31", 20, 0., 1., True, 0. ],
		#[ 'Boosted', "jet1Tau32", 20, 0., 1., True, 0. ],
		#[ 'Boosted', "jet2Tau32", 20, 0., 1., True, 0. ],
		[ 'Boosted', "deltaEtaDijet", 50, 0.0, 2.0, True, .5 ],
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


