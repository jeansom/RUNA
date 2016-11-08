#!/usr/bin/env python

'''
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time
import argparse
from collections import OrderedDict
from multiprocessing import Process
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2F, TMath
from array import array
try: 
	from RUNA.RUNAnalysis.commonFunctions import *
	from RUNA.RUNAnalysis.cuts import selection
        from RUNA.RUNAnalysis.bkgVariables import bkgVariables
	from RUNA.RUNAnalysis.scaleFactors import scaleFactor
except ImportError: 
	sys.path.append('../python') 
	from commonFunctions import *
	from cuts import selection
	from scaleFactors import scaleFactor

gROOT.SetBatch()

def BkgEstimation( dictSamples, listCuts, variables, signalName ):
    outputFileName = 'Rootfiles/MiniBkgTau32Inverse/RUNBkgEstimationUDD323_'+grooming+'_'+signalName+'_low_'+args.version+'p6.root'
    outputFile = TFile( outputFileName, 'RECREATE' )

    outputTextFileName = 'Rootfiles/11116BtagABCDTau32/RUNBkgEstimationUDD323_cutlist_'+grooming+'_'+signalName+'_low_'+args.version+'p6.txt'
    outputTextFile = open( outputTextFileName, 'w' )
    outputTextFile.write( 'List of Cuts:\n\n' )

####### ABCD Plots
    for sam in dictSamples:
	    ABCDName = variables[0][0]+"Vs"+variables[1][0]+"_"	    
	    for k in [ 'A', 'B', 'C', 'D' ]:
		    allHistos[ "massAve_"+ABCDName+'_'+k ] = TH1F( "massAve_"+ABCDName+'_'+k, "massAve_"+ABCDName+'_'+k, 100, 0., 500. )

    for histo in allHistos: allHistos[histo].Sumw2()


    ptWindow = (args.ptWindow).split( "-" )
    ptMin = 999
    ptMax = -999
    if 'All' not in args.ptWindow:
	    ptMin = float( ptWindow[0] )
	    ptMax = float( ptWindow[1] )
    
    for sam in dictSamples:
	    
	    inputFile, events, numEntries = getTree( dictSamples[ sam ], ('BoostedAnalysisPlots/RUNATree' ) )
	    
	    print '-'*40
	    print '------> ', sam
	    print '------> Number of events: '+str(numEntries)
	    d = 0

	    for i in xrange( numEntries ):
		    events.GetEntry(i)


		    #---- progress of the reading --------
		    fraction = 10.*i/(1.*numEntries)
		    if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
		    d = TMath.FloorNint(fraction)
		
		    massAve = events.massAve
		    HT = events.HT
		    jet1Pt = events.jet1Pt
		    jet2Pt = events.jet2Pt
		    lumiWeight = events.lumiWeight
		    puWeight = events.puWeight
		    subjet11Btag = ( events.subjet11btagCSVv2 > 0.800 )
		    subjet12Btag = ( events.subjet12btagCSVv2 > 0.800 )
		    subjet21Btag = ( events.subjet21btagCSVv2 > 0.800 )
		    subjet22Btag = ( events.subjet22btagCSVv2 > 0.800 )

		    if 'DATA' in sam: scale = 1
		    else: scale = 2666 * puWeight * lumiWeight

		    btagCut = False
		    if( ( subjet11Btag or subjet12Btag ) and ( subjet21Btag or subjet22Btag ) ): btagCut = True

		    ######### Pre-selection
		    HTCut = ( HT > 900 )
		    dijetCut = ( events.numJets > 1 )

		    jetPtCut = False
		    if ptMin > ptMax: jetPtCut = ( jet1Pt > 150 ) and ( jet2Pt > 150 )
		    else: jetPtCut = ( jet1Pt > ptMin ) and ( jet1Pt < ptMax) and ( jet2Pt > ptMin ) and ( jet1Pt < ptMax )

		    if HTCut and dijetCut and jetPtCut:
################# ABCD Method
			    sigCutsList = []
			    for var in listCuts:
				    if ( var[0] not in variables[0][0] and var[0] not in variables[1][0] ) :
					    singleCutList = 0
					    for i in xrange( 0, len(var[1]) ):
						    nextCut = False
						    if ( '<' in var[2] ):
							    if ( getattr( events, var[1][i] ) < var[4] ): singleCutList+=1
						    else:
							    if ( getattr( events, var[1][i] ) > var[4] ): singleCutList += 1
					    if singleCutList >= var[3]: sigCutsList.append(True)
					    else: sigCutsList.append(False)
			    if all(sigCutsList):
				    var1 = False
				    var2 = False

				    numVar1 = 0
				    numVar2 = 0
				    for i in xrange( 0, len(variables[0][7]) ):
					    if variables[0][2]:
						    if ( getattr( events, variables[0][7][i] ) < variables[0][1] ): 
							    numVar1 += 1
					    else:
						    if ( getattr( events, variables[0][7][i] ) > variables[0][1] ):
							    numVar1 += 1

				    if numVar1 >= variables[0][6]: var1 = True

				    for i in xrange( 0, len(variables[1][7]) ):
					    if variables[1][2]:
						    if ( getattr( events, variables[1][7][i] ) < varables[1][1] ): 
							    numVar2 += 1
					    else:
						    if ( getattr( events, variables[1][7][i] ) > variables[1][1] ):
							    numVar2 += 1
				    if numVar2 >= variables[1][6]: var2 = True

				    

				    if( var1 and var2 ):
					    allHistos[ "massAve_"+ABCDName+"_A" ].Fill( massAve, scale )

				    if( var1 and not var2 ):
					    allHistos[ "massAve_"+ABCDName+"_B" ].Fill( massAve, scale )
				    if( not var1 and var2 ):
					    allHistos[ "massAve_"+ABCDName+"_C" ].Fill( massAve, scale )
				    if( not var1 and not var2 ):
					    allHistos[ "massAve_"+ABCDName+"_D" ].Fill( massAve, scale )

						    
    outputFile.Write()
        ##### Closing
    print 'Writing output file: '+ outputFileName
    outputFile.Close()
    outputTextFile.close()

					    
						    
						
	    
#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store',  dest='grooming', default='pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='single', help='Process: all or single.' )
	parser.add_argument( '-d', '--decay', action='store',  dest='decay', default='UDD312', help='Decay: UDD312 or UDD323.' )
	parser.add_argument( '-s', '--sample', action='store',   dest='samples', default='RPV', help='Type of sample' )
	parser.add_argument( '-r', '--range', action='store',  dest='RANGE', default='low', help='Range: low, med, high.' )
	parser.add_argument( '-u', '--unc', action='store',  dest='unc', default='', help='Process: all or single.' )
	parser.add_argument( '-b', '--batchSys', action='store',  dest='batchSys', type=bool, default=False, help='Process: all or single.' )
	parser.add_argument( '-v', '--version', action='store', default='v05', dest='version', help='Version of the RUNAnalysis file.' )
        parser.add_argument( '-w', '--ptWindow', action='store', default='All', dest='ptWindow', help='Pt window to run over ( ex: 100-200 )' )
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	process = args.process
	grooming = args.grooming
	samples = args.samples

	folder = 'RootFiles/'

	allSamples = {}
	allSamples[ 'DATA' ] = folder+'/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass) ] = folder+'/RUNAnalysis_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_RunIISummer16MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'QCDHTAll' ] = folder+'/RUNAnalysis_QCDHTAll_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'QCDPtAll' ] = folder+'/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'TTJets' ] = folder+'/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'WJetsToQQ' ] = folder+'/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'ZJetsToQQ' ] = folder+'/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'WWTo4Q' ] = folder+'/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'ZZTo4Q' ] = folder+'/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'WZ' ] = folder+'/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'

	variablesList = ( 'Dibosons' if 'Dibosons' in mass else 'RPVStopStopToJets_'+args.decay+'_M-'+mass )
	try: variables = bkgVariables[ variablesList ]
	except KeyError: 
		print 'Mass', mass, 'not in list.'
		sys.exit(0)

	try: cuts = selection[ variablesList ]
	except KeyError: 
		print 'Mass', mass, 'not in list.'
		sys.exit(0)
		

	if 'RPV' in samples: samples = 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass)
	if 'single' in process: 
		for q in allSamples:
			if q in samples:
				dictSamples = { q: allSamples[ q ] } 
				signalSample = q
	else: 
		dictSamples = allSamples
		signalSample = 'RPVStopStopToJets_'+args.decay+'_M-'+mass+'_All'

	allHistos = {}

	

	if ('RPV' in samples) and args.unc:
		for uncType in [ args.unc+'Up', args.unc+'Down' ]: 
			p = Process( target=BkgEstimation, args=( dictSamples, cuts, variables, signalSample ) )
			p.start()
			p.join()
	else:
		p = Process( target=BkgEstimation, args=( dictSamples, cuts, variables, signalSample ) )
		p.start()
		p.join()
