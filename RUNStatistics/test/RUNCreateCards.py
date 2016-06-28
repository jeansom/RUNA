#!/usr/bin/env python

################################
### Creating datacards
################################

from ROOT import TFile, TH1F, TH1D, TGraph, kTRUE, kFALSE, gROOT, gSystem, gStyle, TMath, TCanvas
from ROOT import RooRealVar, RooDataHist, RooArgList, RooArgSet, RooAddPdf, RooFit, RooGenericPdf, RooWorkspace, RooMsgService, RooHistPdf
from array import array
from collections import OrderedDict
import argparse
import glob,sys, os
import warnings
import random
import numpy as np
from multiprocessing import Process
try: 
	from RUNA.RUNAnalysis.scaleFactors import *
except ImportError: 
	sys.path.append('../python') 
	from scaleFactors import *


currentDir = os.getcwdu()
gSystem.SetIncludePath('-I$ROOFITSYS/include')
if os.access('RooPowerFunction.cxx', os.R_OK): ROOT.gROOT.ProcessLine('.L RooPowerFunction.cxx+')

#xline = array('d', [0,2000])
#yline = array('d', [0,0])
#line = TGraph(2, xline, yline)
#line.SetLineColor(kRed)


def shapeCards( process, isData, datahistosFile, histosFile, signalFile, signalSample, hist, signalMass, minMass, maxMass, reBin, outputName ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )
	
	signalHistosFile = TFile( signalFile )
	hSignal = signalHistosFile.Get(hist+'_'+signalSample)
	#hSignal.Scale( 10 )
	hSignal.Rebin( reBin )
	sigAcc = round(hSignal.Integral( hSignal.GetXaxis().FindBin( minMass ), hSignal.GetXaxis().FindBin( maxMass )), 2)
	#htmpSignal = hSignal.Clone()
	#htmpSignal.Scale(100)
	#signalXS = search(dictXS, 'RPVStopStopToJets_UDD312_M-'+str(signalMass) )
	#hSignal.Scale( lumi*signalXS / hSignal.Integral())

	massAve = RooRealVar( 'massAve', 'massAve', minMass, maxMass  )
	#massAveSig = RooRealVar( 'massAveSig', 'massAveSig', minMass, maxMass  )
	rooSigHist = RooDataHist( 'rooSigHist', 'rooSigHist', RooArgList(massAve), hSignal )
	rooSigHist.Print()

	signal = RooHistPdf('signal','signal',RooArgSet(massAve),rooSigHist)
        signal.Print()
        #signal_norm = RooRealVar('signal_norm','signal_norm',0,-1e+04,1e+04)
        #if args.fitBonly: signal_norm.setConstant()
        #signal_norm.Print()

	hBkg = datahistosFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_DATA_ABCDProj')
	hBkg.Rebin( reBin )
	#hBkg = histosFile.Get(hist+'_QCDPtAll_BCD')
	bkgAcc = round(hBkg.Integral( hBkg.GetXaxis().FindBin( minMass ), hBkg.GetXaxis().FindBin( maxMass )), 2)
	#hBkg.Scale(1/hBkg.Integral())
	hPseudo = hBkg.Clone()
#	hPseudo.Reset()
        #background_norm = RooRealVar('background_norm','background_norm',bkgAcc,0.,1e+07)
        #background_norm = RooRealVar('background_norm','background_norm',1.,0.,1e+07)
        #background_norm.Print()

	###### Adding statistical uncertanty
	hBkgStatUncUp = hBkg.Clone()
	hBkgStatUncUp.Reset()
	hBkgStatUncDown = hBkg.Clone()
	hBkgStatUncDown.Reset()
	for i in range( hBkg.GetNbinsX()+1 ):
		cont = hBkg.GetBinContent(i) 
		contErr = hBkg.GetBinError(i)
		hBkgStatUncUp.SetBinContent( i,  cont + (1*contErr) )
		hBkgStatUncDown.SetBinContent( i, cont - (1*contErr) )
	hBkgStatUncUpDataHist = RooDataHist( 'hBkgStatUncUp', 'hBkgStatUncUp', RooArgList(massAve), hBkgStatUncUp )
	hBkgStatUncDownDataHist = RooDataHist( 'hBkgStatUncDown', 'hBkgStatUncDown', RooArgList(massAve), hBkgStatUncDown )


	massAveBkg = RooRealVar( 'massAveBkg', 'massAveBkg', minMass, maxMass  )
	if 'template' in process:
		rooBkgHist = RooDataHist( 'rooBkgHist', 'rooBkgHist', RooArgList(massAve), hBkg )
		rooBkgHist.Print()
		background = RooHistPdf('background','background',RooArgSet(massAve),rooBkgHist)
		background.Print()

	else:
		p1 = RooRealVar('p1','p1', 1 ,0.,100.)
		p2 = RooRealVar('p2','p2', 1 ,0.,60.)
		p3 = RooRealVar('p3','p3', 1 , -10.,10.)

		background = RooGenericPdf('background','(pow(1-@0/%.1f,@1)/pow(@0/%.1f,@2+@3*log(@0/%.1f)))'%(1300,1300,1300),RooArgList(massAveBkg,p1,p2,p3))
		background.Print()
		### S+B model


	############# JES and JER uncertainties
        hSigSyst = {}
        hSigSystDataHist = {}
        signalCDF = TGraph(hSignal.GetNbinsX()+1)
        hBkgSyst = {}
        hBkgSystDataHist = {}

        # JES and JER uncertainties
	if args.jesUnc or args.jerUnc or args.bkgUnc:
		signalCDF.SetPoint(0,0.,0.)
		integral = 0.
		for i in range(1, hSignal.GetNbinsX()+1):
			x = hSignal.GetXaxis().GetBinLowEdge(i+1)
			integral = integral + hSignal.GetBinContent(i)
			signalCDF.SetPoint(i,x,integral)

		if args.jesUnc:
			print ' |---> Adding JES'
			hSigSyst['JESUp'] = hSignal.Clone()
			hSigSyst['JESDown'] = hSignal.Clone()

		if args.jerUnc:
			print ' |---> Adding JER'
			hSigSyst['JERUp'] = hSignal.Clone()
			hSigSyst['JERDown'] = hSignal.Clone()

		if args.bkgUnc:
			print ' |---> Adding bkg unc'
			hBkgSyst['BkgUncUp'] = hBkg.Clone()
			hBkgSyst['BkgUncDown'] = hBkg.Clone()

        # reset signal histograms
        for key in hSigSyst:
		hSigSyst[key].Reset()
		hSigSyst[key].SetName(hSigSyst[key].GetName() + '_' + key)
        for key in hBkgSyst:
		hBkgSyst[key].Reset()
		hBkgSyst[key].SetName(hBkgSyst[key].GetName() + '_' + key)

        # produce JES signal shapes
        if args.jesUnc:
		for q in range(1, hSignal.GetNbinsX()+1):
			xLow = hSignal.GetXaxis().GetBinLowEdge(q)
			xUp = hSignal.GetXaxis().GetBinLowEdge(q+1)
			jes = 1. - jesValue
			xLowPrime = jes*xLow
			xUpPrime = jes*xUp
			hSigSyst['JESDown'].SetBinContent(q, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
			jes = 1. + jesValue
			xLowPrime = jes*xLow
			xUpPrime = jes*xUp
			hSigSyst['JESUp'].SetBinContent(q, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
		hSigSystDataHist['JESUp'] = RooDataHist('hSignalJESUp','hSignalJESUp',RooArgList(massAve),hSigSyst['JESUp'])
		hSigSystDataHist['JESDown'] = RooDataHist('hSignalJESDown','hSignalJESDown',RooArgList(massAve),hSigSyst['JESDown'])

        # produce JER signal shapes
	if args.jerUnc:
		for i in range(1, hSignal.GetNbinsX()+1):
			xLow = hSignal.GetXaxis().GetBinLowEdge(i)
			xUp = hSignal.GetXaxis().GetBinLowEdge(i+1)
			jer = 1. - jerValue
			xLowPrime = jer*(xLow-float(signalMass))+float(signalMass)
			xUpPrime = jer*(xUp-float(signalMass))+float(signalMass)
			hSigSyst['JERDown'].SetBinContent(i, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
			jer = 1. + jerValue
			xLowPrime = jer*(xLow-float(signalMass))+float(signalMass)
			xUpPrime = jer*(xUp-float(signalMass))+float(signalMass)
			hSigSyst['JERUp'].SetBinContent(i, signalCDF.Eval(xUpPrime) - signalCDF.Eval(xLowPrime))
		hSigSystDataHist['JERUp'] = RooDataHist('hSignalJERUp','hSignalJERUp',RooArgList(massAve),hSigSyst['JERUp'])
		hSigSystDataHist['JERDown'] = RooDataHist('hSignalJERDown','hSignalJERDown',RooArgList(massAve),hSigSyst['JERDown'])

	# produce bkg shapes
        if args.bkgUnc:
		for q in range(0, hBkg.GetNbinsX()):
			binCont = hBkg.GetBinContent( q )
			bkgUncUp = 1. + (args.bkgUncValue/100.)
			hBkgSyst['BkgUncUp'].SetBinContent(q, binCont*bkgUncUp )
			bkgUncDown = 1. - (args.bkgUncValue/100.)
			hBkgSyst['BkgUncDown'].SetBinContent(q, binCont*bkgUncDown )
		hBkgSystDataHist['BkgUncUp'] = RooDataHist('hBkgBkgUncUp','hBkgBkgUncUp',RooArgList(massAve),hBkgSyst['BkgUncUp'])
		hBkgSystDataHist['BkgUncDown'] = RooDataHist('hBkgBkgUncDown','hBkgBkgUncDown',RooArgList(massAve),hBkgSyst['BkgUncDown'])

	if not isData:
		newNumEvents = random.randint( bkgAcc-round(TMath.Sqrt(bkgAcc)), bkgAcc+round(TMath.Sqrt(bkgAcc)) )
		print 'Events in MC:', bkgAcc, ', in PseudoExperiment:', newNumEvents
		hPseudo.FillRandom( hBkg, newNumEvents ) 
		#hPseudo.Scale(1/hPseudo.Integral())

	#hData = histosFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_ABCDProj')
	hData = datahistosFile.Get('massAve_prunedMassAsymVsdeltaEtaDijet_DATA_ABCDProj')
	#hData.Rebin( reBin )
	#hData = histosFile.Get(hist+'_QCDPtAll_A')
	#hData.Add(htmpSignal)
	#hData.Scale(1/hData.Integral())
	massAveData = RooRealVar( 'massAveData', 'massAveData', minMass, maxMass  )
        rooDataHist = RooDataHist('rooDatahist','rooDatahist',RooArgList(massAve), hData if isData else hPseudo )
        rooDataHist.Print()

	#model = RooAddPdf("model","s+b",RooArgList(background,signal),RooArgList(background_norm,signal_norm))
	#res = model.fitTo(rooDataHist, RooFit.Save(kTRUE), RooFit.Strategy(0))
	#res.Print()
	myWS = RooWorkspace("myWS")
	getattr(myWS,'import')(rooSigHist,RooFit.Rename("signal"))
	#getattr(myWS,'import')(signal,RooFit.Rename("signal")) 
        getattr(myWS,'import')(rooBkgHist,RooFit.Rename("background"))
        #getattr(myWS,'import')(background,RooFit.Rename("background"))
        #getattr(myWS,'import')(signal_norm)
        #getattr(myWS,'import')(background_norm)
        if args.jesUnc:
		getattr(myWS,'import')(hSigSystDataHist['JESUp'],RooFit.Rename("signal__JESUp"))
		getattr(myWS,'import')(hSigSystDataHist['JESDown'],RooFit.Rename("signal__JESDown"))
        if args.jerUnc:
		getattr(myWS,'import')(hSigSystDataHist['JERUp'],RooFit.Rename("signal__JERUp"))
		getattr(myWS,'import')(hSigSystDataHist['JERDown'],RooFit.Rename("signal__JERDown"))
        if args.bkgUnc:
		getattr(myWS,'import')(hBkgSystDataHist['BkgUncUp'],RooFit.Rename("background__BkgUncUp"))
		getattr(myWS,'import')(hBkgSystDataHist['BkgUncDown'],RooFit.Rename("background__BkgUncDown"))
	getattr(myWS,'import')(hBkgStatUncUpDataHist, RooFit.Rename("background__BkgStatUncUp") )
	getattr(myWS,'import')(hBkgStatUncDownDataHist, RooFit.Rename("background__BkgStatUncDown") )
        getattr(myWS,'import')(rooDataHist,RooFit.Rename("data_obs"))
        myWS.Print()
	outputRootFile = currentDir+'/Rootfiles/workspace_'+outputName+'.root'
        myWS.writeToFile(outputRootFile, True)
	print ' |----> Workspace created in root file:\n', outputRootFile
 # -----------------------------------------
        # write a datacard

	dataCardName = currentDir+'/Datacards/datacard_'+outputName+'.txt'
        datacard = open( dataCardName ,'w')
        datacard.write('imax 1\n')
        datacard.write('jmax 1\n')
        datacard.write('kmax *\n')
        datacard.write('---------------\n')
        if args.jesUnc or args.jerUnc or args.lumiUnc or args.bkgUnc or args.unc: 
		datacard.write('shapes * * '+outputRootFile+' myWS:$PROCESS myWS:$PROCESS__$SYSTEMATIC\n')
	else: datacard.write("shapes * * "+outputRootFile+" myWS:$PROCESS \n")
        datacard.write('---------------\n')
        datacard.write('bin '+signalSample+'\n')
        datacard.write('observation -1\n')
        datacard.write('------------------------------\n')
        datacard.write('bin          '+signalSample+'          '+signalSample+'\n')
        datacard.write('process      signal     background\n')
        datacard.write('process      0          1\n')
        datacard.write('rate         -1         -1\n')
        #datacard.write('rate         '+str(sigAcc)+'         '+str(bkgAcc)+'\n')
        datacard.write('------------------------------\n')
	if args.lumiUnc: datacard.write('lumi  lnN    %f         -\n'%(lumiValue))
	if args.puUnc: datacard.write('pu  lnN    %f         -\n'%(puValue))
        if args.jesUnc: datacard.write('JES  shape   1          -\n')
	if args.jerUnc: datacard.write('JER  shape   1          -\n')
        #flat parameters --- flat prior
	#if args.bkgUnc: datacard.write('BkgUnc  shape   -	   '+str( round( 1/ (args.bkgUncValue/34.1), 2 ) )+'\n')
	if args.bkgUnc: datacard.write('BkgUnc  shape   -	   1 \n')
	datacard.write('BkgStatUnc  shape   -	   1 \n')
		#NcombineUnc = ( 1 / TMath.Sqrt( args.bkgUncValue / 100. ) ) - 1
		#datacard.write('background_norm  gmN '+str(int(round(NcombineUnc)))+'  -  '+str( round(bkgAcc/NcombineUnc,2) )+'\n')
        #datacard.write('p1  flatParam\n')
        datacard.close()
	print ' |----> Datacard created:\n', dataCardName

	##########
	if args.theta:
		outputFileTheta = currentDir+'/Rootfiles/theta_histos_'+RANGE+'_v05.root'
		print ' |----> Creating Theta file\n', outputFileTheta
		outFile = TFile( outputFileTheta, 'update')
		tmpName = 'rpvstopjj'+str(signalMass) 
		hSignal.SetName('massAve__'+tmpName)
		hSignal.Write()
		hSigSyst['JESDown'].SetName('massAve__'+tmpName+'__jes__down' )
		hSigSyst['JESDown'].Write()
		hSigSyst['JESUp'].SetName('massAve__'+tmpName+'__jes__up' )
		hSigSyst['JESUp'].Write()
		hSigSyst['JERDown'].SetName('massAve__'+tmpName+'__jer__down' )
		hSigSyst['JERDown'].Write()
		hSigSyst['JERUp'].SetName('massAve__'+tmpName+'__jer__up' )
		hSigSyst['JERUp'].Write()
		if (signalMass == 100) or (signalMass == 170):
			hBkg.SetName('massAve__background')
			hBkg.Write()
			hBkgSyst['BkgUncDown'].SetName('massAve__background__unc__down')
			hBkgSyst['BkgUncDown'].Write()
			hBkgSyst['BkgUncUp'].SetName('massAve__background__unc__up')
			hBkgSyst['BkgUncUp'].Write()
			hData.SetName('massAve__DATA')
			hData.Write()
		outFile.Close()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--technique', action='store', dest='technique', default='template', help='Process: template or fit.' )
	parser.add_argument('-d', '--data', dest='isData', type=bool, default=True, help='Data: data or pseudoData.' )
	parser.add_argument('-i', '--injSig', dest='signalInjec', type=bool, default=False, help='Signal injection test.' )
	#parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-l', '--lumiUnc', dest='lumiUnc', type=bool, default=False, help='Luminosity, example: 1.' )
	parser.add_argument('-n', '--bkgUnc', dest='bkgUnc', type=bool, default=False, help='Normalization unc.' )
	parser.add_argument('-nV', '--bkgUncValue', dest='bkgUncValue', type=int, default=50, help='Value for bkg nomralization uncertainty.' )
	parser.add_argument('-p', '--bkgPU', dest='bkgPU', type=bool, default=False, help='Pileup unc.' )
    	parser.add_argument('-s', "--jesUnc", dest="jesUnc", type=bool, default=False, help="Relative uncertainty in the jet energy scale")
    	parser.add_argument('-r', "--jerUnc", dest="jerUnc", type=bool, default=False, help="Relative uncertainty in the jet resolution")
	parser.add_argument('-u', '--unc', dest='unc', type=bool, default=False, help='Luminosity, example: 1.' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-b', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-R', '--rebin', dest='reBin', type=int, default=1, help='Data: data or pseudoData.' )
    	parser.add_argument('-e', "--theta", dest="theta", type=bool, default=False, help="Create theta file.")

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	if args.unc: 
		args.lumiUnc = True
		args.jesUnc = True
		args.jerUnc = True
		args.bkgUnc = True
		args.puUnc = True

	###### Input parameters
	masses = OrderedDict()
#	masses[ 80 ] = 'massAve_deltaEtaDijet'
#	masses[ 90 ] = 'massAve_deltaEtaDijet'
#	masses[ 100 ] = 'massAve_deltaEtaDijet'
#	masses[ 110 ] = 'massAve_deltaEtaDijet'
#	masses[ 120 ] = 'massAve_deltaEtaDijet'
#	masses[ 130 ] = 'massAve_deltaEtaDijet'
#	masses[ 140 ] = 'massAve_deltaEtaDijet'
#	masses[ 150 ] = 'massAve_deltaEtaDijet'
#	masses[ 170 ] = 'massAve_deltaEtaDijet'
#	masses[ 180 ] = 'massAve_deltaEtaDijet'
#	masses[ 190 ] = 'massAve_deltaEtaDijet'
#	masses[ 210 ] = 'massAve_deltaEtaDijet'
#	masses[ 220 ] = 'massAve_deltaEtaDijet'
#	masses[ 230 ] = 'massAve_deltaEtaDijet'
#	masses[ 240 ] = 'massAve_deltaEtaDijet'
	masses[ 300 ] = 'massAve_deltaEtaDijet'
	masses[ 350 ] = 'massAve_deltaEtaDijet'
	jesValue = 0.05
	jerValue = 0.1
	puValue = 1.015
	lumiValue = 1.027
	lumi = 2666
	minMass = 0 
	maxMass = 500 

	if args.theta:
		files = glob.glob(currentDir+'/Rootfiles/theta_histos*')
		for f in files: os.remove(f)

	for mass in masses:
		signalSample = 'RPVStopStopToJets_UDD312_M-'+str(mass)
		if mass < 160: RANGE='low'
		else: RANGE='high'
		dataFileHistos = currentDir+'/../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_DATA_'+RANGE+'_v05.root'
		bkgFileHistos = currentDir+'/../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCDPtAll_'+RANGE+'_v05.root'
		signalFileHistos = currentDir+'/../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_'+RANGE+'_v05.root'
		#if args.unc: outputName = signalSample+'_v05_BkgEst30'
		if args.unc: outputName = signalSample+'_v05'
		else: outputName = signalSample+'_NOSys_v05'
		if args.signalInjec: outputName = outputName.replace( signalSample, signalSample+'_signalInjectionTest' )

		print '#'*50 
		print ' |----> Creating datacard and workspace for RPV St', str(mass)
		print '#'*50 
		p = Process( target=shapeCards, args=( args.technique, args.isData, TFile(dataFileHistos), TFile(bkgFileHistos), signalFileHistos, signalSample, masses[ mass ], mass, minMass, maxMass, args.reBin, outputName ) )
		p.start()
		p.join()
