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
    outputFileName = 'Rootfiles/11116BtagABCDTau32Inverse/RUNBkgEstimationUDD323_'+grooming+'_'+signalName+'_low_'+args.version+'p6.root'
    outputFile = TFile( outputFileName, 'RECREATE' )

    outputTextFileName = 'Rootfiles/11116BtagABCDTau32Inverse/RUNBkgEstimationUDD323_cutlist_'+grooming+'_'+signalName+'_low_'+args.version+'p6.txt'
    outputTextFile = open( outputTextFileName, 'w' )
    outputTextFile.write( 'List of Cuts:\n\n' )
    for sam in dictSamples:
	    allHistos[ "cutFlow_"+sam ] = TH1F( "cutflow_"+sam, "cutflow_"+sam, len(listCuts) + 1, 0., len(listCuts) + 1)
	    allHistos[ "cutFlow_Scaled_"+sam ] = TH1F( "cutflow_Scaled_"+sam, "cutflow_Scaled_"+sam, len(listCuts) + 1, 0., len(listCuts) + 1)
	    allHistos[ "cutFlow_Scaled_Weights_"+sam ] = TH1F( "cutflow_scaled_weights_"+sam, "cutflow_scaled_weights_"+sam, len(listCuts)+1, 0., len(listCuts)+1 )
	    allHistos[ "massAve_"+sam ] = TH1F( "massAve_"+sam, "massAve_"+'_'+sam, 100, 0., 500. )
	    allHistos[ "jet1Pt_"+sam ] = TH1F( "jet1Pt_"+sam, "jet1Pt_"+sam, 2000, 0., 2000. )
	    allHistos[ "jet2Pt_"+sam ] = TH1F( "jet2Pt_"+'_'+sam, "jet2Pt_"+'_'+sam, 2000, 0., 2000. )
	    allHistos[ "HT_"+sam ] = TH1F( "HT_"+sam, "HT_"+sam, 5000, 0., 5000. )

	    for var0 in listCuts:
		    outputTextFile.write( '\t\t' + var0[0] + ': At least ' + str(var0[3]) + ' of\n\n' )
		    for i in xrange( 0, len(var0[1]) ):
			    outputTextFile.write( str('\t\t\t\t'+var0[1][i] + ' ' + var0[2] + ' ' + str(var0[4]) + '\n' ) )
			    allHistos[ var0[1][i]+'_'+sam ] = TH1F( var0[1][i]+'_'+sam, var0[1][0]+'_'+sam, 50, 0., 5. )
			    allHistos[ var0[1][i]+'_n-1_'+sam ] = TH1F( var0[1][i]+'_n-1_'+sam, var0[1][i]+'_n-1_'+sam, 50, 0., 5. )
			    for var1 in listCuts:
				    allHistos[ var0[1][i]+'_'+var1[0]+'_'+sam ] = TH1F( var0[1][i]+'_'+var1[0]+'_'+sam, var0[1][i]+'_'+var1[0]+'_'+sam, 50, 0., 5. )
		    
		    outputTextFile.write( '\n\n' )
				    
		    allHistos[ "massAve_"+var0[0]+'_'+sam ] = TH1F( "massAve_"+var0[0]+'_'+sam, "massAve_"+var0[0]+'_'+sam, 100, 0., 500. )
		    allHistos[ "jet1Pt_"+var0[0]+'_'+sam ] = TH1F( "jet1Pt_"+var0[0]+'_'+sam, "jet1Pt_"+var0[0]+'_'+sam, 2000, 0., 2000. )
		    allHistos[ "jet2Pt_"+var0[0]+'_'+sam ] = TH1F( "jet2Pt_"+var0[0]+'_'+sam, "jet2Pt_"+var0[0]+'_'+sam, 2000, 0., 2000. )
		    allHistos[ "HT_"+var0[0]+'_'+sam ] = TH1F( "HT_"+var0[0]+'_'+sam, "HT_"+var0[0]+'_'+sam, 5000, 0., 5000. )


####### ABCD Plots
	    ABCDName = variables[0][0]+"Vs"+variables[1][0]+"_"
	    allHistos[ ABCDName+sam ] = TH2F( ABCDName+sam, ABCDName+sam, variables[0][5], variables[0][3], variables[0][4], variables[1][5], variables[1][3], variables[1][4] )
	    allHistos[ "massAve_"+ABCDName+"_ABCDProj" ] = TH1F( "massAve_"+ABCDName+"_ABCDProj", "massAve"+ABCDName+"_ABCDProj", 100, 0., 500. )
	    allHistos[ "massAve_"+ABCDName+"_BC" ] = TH1F( "massAve_"+ABCDName+"_BC", "massAve"+ABCDName+"_BC", 100, 0., 500. )
	    allHistos[ "massAve_"+ABCDName+"_Bkg" ] = TH1F( "massAve_"+ABCDName+"_Bkg", "massAve"+ABCDName+"_Bkg", 100, 0., 500. )
	    
	    for k in [ 'A', 'B', 'C', 'D' ]:
		    allHistos[ "jet1Pt_"+ABCDName+"_"+k ] = TH1F( "jet1Pt_"+ABCDName+'_'+k, "jet1Pt_"+ABCDName+'_'+k, 2000, 0, 2000 )
		    allHistos[ "jet2Pt_"+ABCDName+"_"+k ] = TH1F( "jet2Pt_"+ABCDName+'_'+k, "jet2Pt_"+ABCDName+'_'+k, 2000, 0, 2000 )
		    allHistos[ "HT_"+ABCDName+"_"+k ]  = TH1F( "HT_"+ABCDName+'_'+k, "HT_"+ABCDName+'_'+k, 5000, 0, 5000 )
		    allHistos[ "ptAve_"+ABCDName+"_"+k ] = TH1F( "ptAve_"+ABCDName+'_'+k, "ptAve_"+ABCDName+'_'+k, 2000, 0, 2000 )
		    allHistos[ "massAve_"+ABCDName+'_'+k ] = TH1F( "massAve_"+ABCDName+'_'+k, "massAve_"+ABCDName+'_'+k, 100, 0., 500. )
		    allHistos[ "massAveVsjet1Pt_"+ABCDName+"_"+k ] = TH2F( "massAveVsjet1Pt_"+ABCDName+"_"+k, "massAveVsjet1Pt_"+ABCDName+"_"+k, 100, 0., 500., 2000, 0, 2000 )
		    allHistos[ "massAveVsjet2Pt_"+ABCDName+"_"+k ] = TH2F( "massAveVsjet2Pt_"+ABCDName+"_"+k, "massAveVsjet2Pt_"+ABCDName+"_"+k, 100, 0., 500., 2000, 0, 2000 )
		    allHistos[ "massAveVsHT_"+ABCDName+"_"+k ] = TH2F( "massAveVsHT_"+ABCDName+"_"+k, "massAveVsHT_"+ABCDName+"_"+k, 100, 0., 500., 5000, 0, 5000 )
		    allHistos[ "massAveVsptAve_"+ABCDName+"_"+k ] = TH2F( "massAveVsptAve_"+ABCDName+"_"+k, "massAveVsptAve_"+ABCDName+"_"+k, 100, 0., 500., 2000, 0, 2000 )

		    allHistos[ ABCDName + '_' + k ] = TH2F( ABCDName+'_'+k, ABCDName+'_'+k, variables[0][5], variables[0][3], variables[0][4], variables[1][5], variables[1][3], variables[1][4] )

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
	    cutFlowList = OrderedDict()
	    cutFlowScaledList = OrderedDict()
	    cutFlowScaledListWeights = OrderedDict()
	    cutFlowList[ 'Process' ] = 0
	    cutFlowList[ 'Preselection' ] = 0
	    cutFlowScaledList[ 'Process' ] = 0
	    cutFlowScaledList[ 'Preselection' ] = 0
	    cutFlowScaledListWeights[ 'Process' ] = 0
	    cutFlowScaledListWeights[ 'Preselection' ] = 0
	    for k in listCuts: 
		    cutFlowList[ k[0] ] = 0
		    cutFlowScaledList[ k[0] ] = 0
		    cutFlowScaledListWeights[ k[0] ] = 0


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
			    cutFlowList[ 'Preselection' ] += 1
			    cutFlowScaledList[ 'Preselection' ] += scale
			    cutFlowScaledList[ 'Preselection' ] += (puWeight*puWeight)
			    sigCutsList = []
			    allHistos[ "HT_"+sam ].Fill( HT, scale )
			    allHistos[ "massAve_"+sam ].Fill( massAve, scale )
			    allHistos[ "jet1Pt_"+sam ].Fill( jet1Pt, scale )
			    allHistos[ "jet2Pt_"+sam ].Fill( jet2Pt, scale )

			    for var in listCuts:
				    singleCutList = 0
				    for i in xrange( 0, len(var[1]) ):
					    allHistos[ var[1][i] + '_' +sam ].Fill( getattr( events, var[1][i] ), scale )
					    nextCut = False
					    if ( '<' in var[2] ):
						    if ( getattr( events, var[1][i] ) < var[4] ): singleCutList+=1
					    else:
						    if ( getattr( events, var[1][i] ) > var[4] ): singleCutList += 1
				    if singleCutList >= var[3]: sigCutsList.append(True)
				    else: sigCutsList.append(False)
				    if all( sigCutsList ):
					    allHistos[ 'massAve_'+var[0]+'_'+sam ].Fill( massAve, scale ) 
					    allHistos[ "HT_"+var[0]+"_"+sam ].Fill( HT, scale )
					    allHistos[ "massAve_"+var[0]+"_"+sam ].Fill( massAve, scale )
					    allHistos[ "jet1Pt_"+var[0]+"_"+sam ].Fill( jet1Pt, scale )
					    allHistos[ "jet2Pt_"+var[0]+"_"+sam ].Fill( jet2Pt, scale )
					    cutFlowList[ var[0] ] += 1
					    cutFlowScaledList[ var[0] ] += scale
					    cutFlowScaledList[ var[0] ] += (puWeight*puWeight)
					    for var1 in listCuts:
						    for i in xrange( 0, len(var1[1] ) ):
							    allHistos[ var1[1][i] + '_' + var[0] + '_'+sam ].Fill( getattr( events, var1[1][i] ), scale )
		    
			    '''
			    if ( all( sigCutsList ) and btagCut ):

				    allHistos[ 'massAve_btag_'+sam ].Fill( massAve, scale )
				    allHistos[ "HT_btag_"+sam ].Fill( HT, scale )
				    allHistos[ "jet1Pt_btag_"+sam ].Fill( jet1Pt, scale )
				    allHistos[ "jet2Pt_btag_"+sam ].Fill( jet2Pt, scale )
				    for var in listCuts:
					    allHistos[ var[0] + "_btag_"+sam ].Fill( getattr( events, var[1][i] ), scale )
				    
					    '''
			    for var in listCuts:
				    for j in xrange( 0, len(var[1] ) ):
					    sigCutsList = []
					    for var1 in listCuts:
						    if var1[0] not in var[0]:
							    singleCutList = 0
							    for i in xrange( 0, len(var[1]) ):
								    allHistos[ var[1][i] + '_' +sam ].Fill( getattr( events, var[1][i] ), scale )
								    nextCut = False
								    if ( '<' in var[2] ):
									    if ( getattr( events, var[1][i] ) < var[4] ): singleCutList+=1
								    else:
									    if ( getattr( events, var[1][i] ) > var[4] ): singleCutList += 1
							    if singleCutList >= var[3]: sigCutsList.append(True)
							    else: sigCutsList.append(False)
					    if ( all(sigCutsList)):
						    allHistos[ var[1][j]+"_n-1_"+sam ].Fill( getattr( events, var[1][i] ), scale )

			    
			    
################# ABCD Method
			    sigCutsList = []
			    for var in listCuts:
				    if ( var[0] not in variables[0][0] and var[0] not in variables[1][0] ) :
					    singleCutList = 0
					    for i in xrange( 0, len(var[1]) ):
						    allHistos[ var[1][i] + '_' +sam ].Fill( getattr( events, var[1][i] ), scale )
						    nextCut = False
						    if ( '<' in var[2] ):
							    if ( getattr( events, var[1][i] ) < var[4] ): singleCutList+=1
						    else:
							    if ( getattr( events, var[1][i] ) > var[4] ): singleCutList += 1
					    if singleCutList >= var[3]: sigCutsList.append(True)
					    else: sigCutsList.append(False)
			    if all(sigCutsList):
				    allHistos[ ABCDName+sam ].Fill( getattr( events, variables[0][7][1] ), getattr( events, variables[1][7][1] ), scale )

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
					    allHistos[ "jet1Pt_"+ABCDName+"_A" ].Fill( jet1Pt, scale )
					    allHistos[ "jet2Pt_"+ABCDName+"_A" ].Fill( jet2Pt, scale )
					    allHistos[ "HT_"+ABCDName+"_A" ].Fill( HT, scale )
					    allHistos[ "ptAve_"+ABCDName+"_A" ].Fill( (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ "massAve_"+ABCDName+"_A" ].Fill( massAve, scale )
					    allHistos[ "massAveVsjet1Pt_"+ABCDName+"_A" ].Fill( massAve, jet1Pt, scale )
					    allHistos[ "massAveVsjet2Pt_"+ABCDName+"_A" ].Fill( massAve, jet2Pt, scale )
					    allHistos[ "massAveVsHT_"+ABCDName+"_A" ].Fill( massAve, HT, scale )
					    allHistos[ "massAveVsptAve_"+ABCDName+"_A" ].Fill( massAve, (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ ABCDName+"_A" ].Fill( getattr( events, variables[0][7][1] ), getattr( events, variables[1][7][1] ), scale )					     
				    if( var1 and not var2 ):
					    allHistos[ "jet1Pt_"+ABCDName+"_B" ].Fill( jet1Pt, scale )
					    allHistos[ "jet2Pt_"+ABCDName+"_B" ].Fill( jet2Pt, scale )
					    allHistos[ "HT_"+ABCDName+"_B" ].Fill( HT, scale )
					    allHistos[ "ptAve_"+ABCDName+"_B" ].Fill( (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ "massAve_"+ABCDName+"_B" ].Fill( massAve, scale )
					    allHistos[ "massAveVsjet1Pt_"+ABCDName+"_B" ].Fill( massAve, jet1Pt, scale )
					    allHistos[ "massAveVsjet2Pt_"+ABCDName+"_B" ].Fill( massAve, jet2Pt, scale )
					    allHistos[ "massAveVsHT_"+ABCDName+"_B" ].Fill( massAve, HT, scale )
					    allHistos[ "massAveVsptAve_"+ABCDName+"_B" ].Fill( massAve, (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ ABCDName+"_B" ].Fill( getattr( events, variables[0][7][1] ), getattr( events, variables[1][7][1] ), scale )	

				    if( not var1 and var2 ):
					    allHistos[ "jet1Pt_"+ABCDName+"_C" ].Fill( jet1Pt, scale )
					    allHistos[ "jet2Pt_"+ABCDName+"_C" ].Fill( jet2Pt, scale )
					    allHistos[ "HT_"+ABCDName+"_C" ].Fill( HT, scale )
					    allHistos[ "ptAve_"+ABCDName+"_C" ].Fill( (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ "massAve_"+ABCDName+"_C" ].Fill( massAve, scale )
					    allHistos[ "massAveVsjet1Pt_"+ABCDName+"_C" ].Fill( massAve, jet1Pt, scale )
					    allHistos[ "massAveVsjet2Pt_"+ABCDName+"_C" ].Fill( massAve, jet2Pt, scale )
					    allHistos[ "massAveVsHT_"+ABCDName+"_C" ].Fill( massAve, HT, scale )
					    allHistos[ "massAveVsptAve_"+ABCDName+"_C" ].Fill( massAve, (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ ABCDName+"_C" ].Fill( getattr( events, variables[0][7][1] ), getattr( events, variables[1][7][1] ), scale )	

				    if( not var1 and not var2 ):
					    allHistos[ "jet1Pt_"+ABCDName+"_D" ].Fill( jet1Pt, scale )
					    allHistos[ "jet2Pt_"+ABCDName+"_D" ].Fill( jet2Pt, scale )
					    allHistos[ "HT_"+ABCDName+"_D" ].Fill( HT, scale )
					    allHistos[ "ptAve_"+ABCDName+"_D" ].Fill( (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ "massAve_"+ABCDName+"_D" ].Fill( massAve, scale )
					    allHistos[ "massAveVsjet1Pt_"+ABCDName+"_D" ].Fill( massAve, jet1Pt, scale )
					    allHistos[ "massAveVsjet2Pt_"+ABCDName+"_D" ].Fill( massAve, jet2Pt, scale )
					    allHistos[ "massAveVsHT_"+ABCDName+"_D" ].Fill( massAve, HT, scale )
					    allHistos[ "massAveVsptAve_"+ABCDName+"_D" ].Fill( massAve, (float)((jet1Pt+jet2Pt)/2), scale )
					    allHistos[ ABCDName+"_D" ].Fill( getattr( events, variables[0][7][1] ), getattr( events, variables[1][7][1] ), scale )	

	    dummy = 1
	    for q in cutFlowList:
		    allHistos[ 'cutFlow_'+sam ].SetBinContent( dummy, cutFlowList[q] )
		    allHistos[ 'cutFlow_'+sam ].GetXaxis().SetBinLabel( dummy, q )
		    allHistos[ 'cutFlow_Scaled_'+sam ].SetBinContent( dummy, cutFlowScaledList[q] )
		    allHistos[ 'cutFlow_Scaled_'+sam ].GetXaxis().SetBinLabel( dummy, q )
		    allHistos[ 'cutFlow_Scaled_Weights_'+sam ].SetBinContent( dummy, cutFlowScaledListWeights[q] )
		    allHistos[ 'cutFlow_Scaled_Weights_'+sam ].GetXaxis().SetBinLabel( dummy, q )
		    dummy+=1

	    allHistos[ 'massAve_'+ABCDName+'_BC' ].Multiply( allHistos[ 'massAve_'+ABCDName+"_B" ], allHistos[ 'massAve_'+ABCDName+'_D' ], 1, 1, '' )
	    allHistos[ 'massAve_'+ABCDName+'_ABCDProj' ].Divide( allHistos[ 'massAve_'+ABCDName+'_BC' ], allHistos[ 'massAve_'+ABCDName+'_D' ], 1, 1, '')
		
						    
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
