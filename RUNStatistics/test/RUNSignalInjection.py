#!/usr/bin/env python

###################
### Make Fitting
###################

#from ROOT import RooRealVar, RooDataHist, RooArgList, RooArgSet, RooAddPdf, RooFit, RooGenericPdf, RooWorkspace, RooMsgService, RooHistPdf
from ROOT import *
from array import array
import argparse
import glob,sys, os
import warnings
import random
import numpy as np
from multiprocessing import Process
#try: 
#	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
#	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis 
#	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
#except ImportError:
#	sys.path.append('../python') 
#	import CMS_lumi as CMS_lumi 
#	from histoLabels import labels, labelAxis 
#	import tdrstyle as tdrstyle
#
#gSystem.SetIncludePath('-I$ROOFITSYS/include')
#if os.access('RooPowerFunction.cxx', os.R_OK): ROOT.gROOT.ProcessLine('.L RooPowerFunction.cxx+')

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
#tdrstyle.setTDRStyle()
#CMS_lumi.writeExtraText = 1
TVirtualFitter.SetMaxIterations(50000000)		######### Trick to increase number of iterations

gStyle.SetOptFit()
gStyle.SetStatY(0.91)
gStyle.SetStatX(0.95)
gStyle.SetStatW(0.15)
gStyle.SetStatH(0.15) 
gStyle.SetTextSize(0.5)

xline = array('d', [0,2000])
yline = array('d', [0,0])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

######## Fit Functions
P4 = TF1("P4", "[0]* TMath::Power(1-(x/13000.0),[1]) / (TMath::Power(x/13000.0,[2]+([3]*log(x/13000.))))",0,2000);
#P1 = TF1("P1", "[0] / (TMath::Power(x/13000.0,[1]))",0,2000);
#P4 = TF1("P4", "( [0]*TMath::Power(1-x/13000,[1]) ) / ( TMath::Power(x/13000,[2]) )",0,2000);
expoPoli = TF1("expoPoli", "exp([0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x)", 0, 1000 )
landau = TF1("landau","[0]*TMath::Landau(-x,[1],[2])",50,300)
gaus = TF1("gaus", "gaus", 0, 2000);
P4Gaus = TF1("P4Gaus", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))+gaus(4)",0,2000);
massBins = [0, 30, 60, 90, 120, 150, 180, 210, 250, 290, 330, 370, 410, 460, 510, 560, 610, 670, 730, 790, 860, 930, 1000, 1080, 1160, 1240, 1330, 1420, 1520, 1620, 1730, 1840, 2000]


def createPseudoExperiment( inFileBkg, nameHisto, doFit, totalNumPSE ):
    """docstring for createPseudoExperiment"""

    hOriginal = inFileBkg.Get( nameHisto )
    hOriginal.Rebin(10)
    hPSE = hOriginal.Clone()
    hPSE.Reset()
    binSize = hOriginal.GetBinWidth(1)

    if doFit:
        Gauss = TF1( "gaus", 'gaus', 0, 300 ) #hOriginal.GetMaximum()-50, hOriginal.GetMaximum()+50 );
        hOriginal.Fit( Gauss ) #, 'ELLSR' )

    totalEvBkg = round( hOriginal.Integral() )
    randomNumEventsQCD = random.randint( totalEvBkg - round( TMath.Sqrt( totalEvBkg ) ), totalEvBkg + round( TMath.Sqrt( totalEvBkg ) ) ) 

    listPSE = []
    for numPSE in range(0, totalNumPSE ):
        print "total, random number Of events", totalEvBkg, randomNumEventsQCD
        hPSE.FillRandom( ( "gaus" if doFit else hOriginal ), int(randomNumEventsQCD) )
        c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
        gStyle.SetOptFit()
        gStyle.SetStatY(0.94)
        gStyle.SetStatX(0.9)
        gStyle.SetStatW(0.15)
        gStyle.SetStatH(0.15) 
        hPSE.GetXaxis().SetTitle( 'Average Mass [GeV]' )
        hPSE.GetYaxis().SetTitle("Events / "+ str(binSize) +" GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
        hPSE.GetYaxis().SetTitleOffset(1.2);
        hPSE.SetLineColor( kRed )
        hOriginal.SetLineColor( kBlue )
        hPSE.SetTitle( nameHisto+" PseudoExperiment")
        hPSE.SetMaximum( 1.1*( max( hPSE.GetMaximum(), hOriginal.GetMaximum() ) ) )
        hPSE.Draw("histe")
        if doFit: Gauss.Draw("same")
        hOriginal.Draw("same histe")
        c1.SaveAs( "Plots/" +nameHisto+"_PseudoExperiment"+str(numPSE)+".png")
        del c1
        listPSE.append( hPSE )
    return listPSE

if __name__ == '__main__':

    fileSignal = "../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_pruned_RPVStopStopToJets_UDD312_M-100_v03.root"
    fileBkg = "../../RUNAnalysis/test/Rootfiles/RUNMiniBoostedAnalysis_pruned_QCDPtAll_low_v03.root"
    #fileData = TFile('Rootfiles/RUNMini'+version+'Analysis_JetHTRun2015D-All_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root')

    listPSEBkg =  createPseudoExperiment( TFile.Open( fileBkg ), 'massAve_prunedMassAsymVsdeltaEtaDijet_QCDPtAll_ABCDProj', False, 100 ) 
    listPSESignal = createPseudoExperiment( TFile.Open( fileSignal), 'massAve_deltaEtaDijet_RPVStopStopToJets_UDD312_M-100', True, 100 )

sys.exit(0)
def rootFitter( inFileBkg, hist, folder, fitFunction, fitParam, minX, maxX, rebinX, plot, log=True ):
	"""Simple rootFitter"""

	##### BKG
	hInitialBkg = inFileBkg.Get(folder+hist)
	hInitialBkg.Rebin(rebinX)
	tmpHBkg = hInitialBkg.Clone()
	binSize = tmpHBkg.GetBinWidth(1)

	tmpBkgBinContent = []
	tmpBkgBinError = []
	for ibin in range( int( minX/binSize), int(maxX/binSize ) ):
		tmpBkgBinContent.append( tmpHBkg.GetBinContent(ibin) / binSize )
		tmpBkgBinError.append( tmpHBkg.GetBinError(ibin) / binSize )

	binContents = np.array(tmpBkgBinContent)
	binError = np.array(tmpBkgBinError)
	#print 'QCD bins NO normalized:', tmpBkgBinContent
	sumBinContents = np.sum(binContents)
	binContents = binContents/sumBinContents
	binError = binError/sumBinContents

	#print 'QCD bins :', binContents
	#print 'QCD bins error :', binError
	numBins = int ( (maxX - minX)/binSize )
	hBkg = TH1D("hbkg", "hbkg", numBins, minX, maxX)
	hBkg.Sumw2()
	for ibin in range( 0, numBins ):
		hBkg.SetBinContent( ibin, binContents[ibin] )
		hBkg.SetBinError( ibin, binError[ibin] )

	if( len(fitParam)>0 ):
		for k in range( len(fitParam) ): fitFunction.SetParameter(k, fitParam[k])

	fitStatus = 0
	numParam = 0
	for loop in range(0,10):
		#result = hBkg.Fit(fitFunction,"MELLS","",minX,maxX)
		result = hBkg.Fit( fitFunction,"ELLSR","",minX,maxX)
		fitStatus = int(result.Status())
		numParam = result.NFreeParameters()
		print "|----> Fit status : %d" % fitStatus
		if(fitStatus==1):
			stopProgram=0
			result.Print("V")
			break

	fitParameters =  [ fitFunction.GetParameter(k) for k in range( numParam ) ]
	print "|----> Fitter parameters for", fitFunction.GetName(), fitParameters

	numEvents = hBkg.Integral( )
	print "|----> Number of event in ", process, numEvents
	

	######### Plotting Histograms
	if plot:
		c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
		if log: c1.SetLogy()
		hBkg.GetXaxis().SetTitle( histYaxis )
		hBkg.GetYaxis().SetTitle('dN/dm_{av} / '+str(round(binSize))+' GeV' ) 
		hBkg.GetYaxis().SetTitleOffset(0.9);
		hBkg.GetXaxis().SetRangeUser( minX-50, maxX+50 )
		hBkg.SetTitle("")
		hBkg.Draw()
		c1.SaveAs(outputDir+hist+"_"+process+"_"+fitFunction.GetName()+"Fit.pdf")
		del c1
	
	return [ fitParameters, numEvents, binContents, binError ]

def FitterCombination( inFileData, inFileBkg, inFileSignal, hist, folder, bkgFunction, fitParam, minX, maxX, rebinX ):
	"""docstring for FitterCombination"""

	### Fit QCD
	BkgParameters = rootFitter( inFileBkg, hist, folder, P4, fitParam, minX, maxX, rebinX, False )
	bkgParameters = BkgParameters[0]
	bkgAcceptance = BkgParameters[1]
	points = BkgParameters[2]
	pointsErr = BkgParameters[3]

	if not 'Data' in process:
		SigParameters = rootFitter( inFileSignal, hist, folder, gaus, [], MASS-50, MASS+50, rebinX, False )
		gausParameters = SigParameters[0]
		sigAcceptance = SigParameters[1]
		sigContent = SigParameters[2]
		sigErr = SigParameters[3]
	
	if not 'MC' in process:
		DataParameters = rootFitter( inFileData, hist, folder, P4, bkgParameters, minX, maxX, rebinX, False )
		dataParameters = DataParameters[0]
		dataAcceptance = DataParameters[1]
		points = DataParameters[2]
		pointsErr = DataParameters[3]

	print '|----> DATA Plotted:', points
	print '|----> DATA Err:', pointsErr
	
	mainP4 = TF1("mainP4", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))", minX, maxX);
	mainP4.SetParameter(0, dataParameters[0] if not 'MC' in process else bkgParameters[0] )				
	mainP4.SetParameter(1, dataParameters[1] if not 'MC' in process else bkgParameters[1] )				
	mainP4.SetParameter(2, dataParameters[2] if not 'MC' in process else bkgParameters[2] )				
	mainP4.SetParameter(3, dataParameters[3] if not 'MC' in process else bkgParameters[3] )				

	minX = minX-50
	maxX = maxX-50
	hMain = TH1D("hbkg", "hbkg", len(points) , minX, maxX)
	hMain.Sumw2()
	hPull = TH1D("hpull", "hpull", len(points) , minX, maxX)
	hPull.Sumw2()
	hResidual = TH1D("hresidual", "hresidual", len(points) , minX, maxX)
	hResidual.Sumw2()

	for ibin in range( 0, len(points)):
		hMain.SetBinContent( ibin, points[ibin] )
		hMain.SetBinError( ibin, pointsErr[ibin] )
			
	hMain.Fit( mainP4, "ELLSR", "", minX, maxX )
	'''
	P4Gaus.SetParameter(0,bkgParameters[0])				
	P4Gaus.SetParameter(1,bkgParameters[1])
	P4Gaus.SetParameter(2,bkgParameters[2])
	P4Gaus.SetParameter(3,bkgParameters[3])
	P4Gaus.SetParameter(4,gausParameters[0])
	P4Gaus.SetParameter(5,gausParameters[1])
	P4Gaus.SetParameter(6,gausParameters[2])
	hMain.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	hMain.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	hMain.Fit( P4Gaus, "ELLSR", "", minX, maxX)
	P4_2 = TF1("P4_2", "[0]*pow(1-(x/13000.0),[1])/pow(x/13000.0,[2]+([3]*log(x/13000.)))", minX, maxX);
	#P4_2.SetParameter(0, P4Gaus.GetParameter(0) )
	#P4_2.SetParameter(1, P4Gaus.GetParameter(1) )
	#P4_2.SetParameter(2, P4Gaus.GetParameter(2) )
	#P4_2.SetParameter(3, P4Gaus.GetParameter(3) )
	P4_2.SetParameter(0,bkgParameters[0])				
	P4_2.SetParameter(1,bkgParameters[1])
	P4_2.SetParameter(2,bkgParameters[2])
	P4_2.SetParameter(3,bkgParameters[3])

	#gaus2.SetParameter(0, P4Gaus.GetParameter(4) )
	#gaus2.SetParameter(1, P4Gaus.GetParameter(5) )
	#gaus2.SetParameter(2, P4Gaus.GetParameter(6) )
	#print "SIGNALLLL", gaus2.Integral(MASS-30, MASS+30)
	#P4_2Parameters = [ P4_2.GetParameter(0), P4_2.GetParameter(1), P4_2.GetParameter(2), P4_2.GetParameter(3), P4Gaus.GetParameter(4), P4Gaus.GetParameter(5), P4Gauss.GetParameter(6), bkgAcceptance, sigAcceptance, minX, maxX ]
	#print P4_2Parameters
	'''


	######## Calculating Pull and Residual
	chi2 = 0 
	nof = 0
	for ibin in range(0, len(points) ):
	
		binCont = points[ibin]
		binErr = pointsErr[ibin]
		valIntegral = mainP4.Eval( hMain.GetBinCenter(ibin) ) 
		diff = (binCont - valIntegral)/ valIntegral
		#errDiff = diff * TMath.Sqrt( TMath.Power( P4Gaus.GetParError(0) / P4Gaus.GetParameter(0),2 ) + TMath.Power( P4Gaus.GetParError(1)/ P4Gaus.GetParameter(1), 2 )  + TMath.Power( P4Gaus.GetParError(2)/ P4Gaus.GetParameter(2), 2 )  + TMath.Power( P4Gaus.GetParError(3)/ P4Gaus.GetParameter(3), 2 ) )
		#errDiff = diff * TMath.Sqrt( TMath.Power( mainP4.GetParError(0) / mainP4.GetParameter(0),2 ) + TMath.Power( mainP4.GetParError(1)/ mainP4.GetParameter(1), 2 )  + TMath.Power( mainP4.GetParError(2)/ mainP4.GetParameter(2), 2 )  + TMath.Power( mainP4.GetParError(3)/ mainP4.GetParameter(3), 2 ) )
		#print binCont, binErr, valIntegral 

		if (binCont != 0):
			pull = (binCont - valIntegral)/ binErr
			chi2 += TMath.Power(pull,2)
			nof += 1
			
			hPull.SetBinContent(ibin, pull)
			hPull.SetBinError(ibin, 1.0)
	
			hResidual.SetBinContent(ibin, diff)
			hResidual.SetBinError(ibin, binErr/valIntegral )
	print '|----> ############### chi2 and nof: ', chi2, nof


	######### Plotting Histograms
	maxXPlot = maxX+500
	tdrStyle.SetPadRightMargin(0.05)
  	tdrStyle.SetPadLeftMargin(0.15)
	gStyle.SetOptFit()
	gStyle.SetStatY(0.91)
	gStyle.SetStatX(0.95)
	gStyle.SetStatW(0.15)
	gStyle.SetStatH(0.30) 
	#c3 = TCanvas('c1', 'c1',  10, 10, 750, 1000 )
	#pad1 = TPad("pad1", "Fit",0,0.40,1.00,1.00,-1)
	#pad2 = TPad("pad2", "Pull",0,0.25,1.00,0.475,-1);
	#pad3 = TPad("pad3", "Residual",0,0,1.00,0.277,-1);
	c3 = TCanvas('c1', 'c1',  10, 10, 1000, 500 )
	pad1 = TPad("pad1", "Fit",0,0.00,0.50,1.00,-1)
	pad2 = TPad("pad2", "Pull",0.50,0.50,1.00,1.00,-1);
	pad3 = TPad("pad3", "Residual",0.50,0,1.00,0.557,-1);
	pad1.Draw()
	pad2.Draw()
	pad3.Draw()

	pad1.cd()
	pad1.SetLogy()
	hMain.SetMarkerStyle(8)
	hMain.GetYaxis().SetTitle("dN/dm_{av} / "+ str(hMain.GetBinWidth(1)) +" GeV" ) # dN/dM_{bbjj} [GeV^{-1}]")
	hMain.GetYaxis().SetTitleOffset(1.2);
	hMain.SetTitle("")
	#hMain.SetMaximum( 1.5 * hMain.GetMaximum() )
	hMain.Draw()
	hMain.GetXaxis().SetRangeUser( minX, maxXPlot  )
	mainP4.SetLineColor(kBlack)
	mainP4.Draw("same")
	#gaus2.SetLineColor(kRed-4)
	#gaus2.Draw("same")
	mainP4.SetLineColor(kBlue-4)
	mainP4.Draw("same")
	CMS_lumi.relPosX = 0.13
	CMS_lumi.cmsTextSize = 0.60
	CMS_lumi.lumiTextSize = 0.50
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labels( hist, '', '', 0.20, 0.45, 'left' )


	pad2.cd()
	pad2.SetGrid()
	#pad2.SetTopMargin(0)
	gStyle.SetOptStat(0)
	hPull.GetYaxis().SetTitle("#frac{(Data - Fit)}{#sigma_{Data}}")
	hPull.GetYaxis().SetLabelSize(0.08)
	hPull.GetYaxis().SetTitleSize(0.09)
	hPull.GetYaxis().SetTitleOffset(0.70)
	hPull.GetYaxis().CenterTitle()
	hPull.SetMarkerStyle(7)
	#hPull.SetMaximum(3)
	hPull.GetXaxis().SetRangeUser( minX, maxXPlot )
	hPull.Sumw2()
	hPull.Draw("e")
	line.Draw("same")
	
	pad3.cd()
	pad3.SetGrid()
	pad3.SetTopMargin(0)
	pad3.SetBottomMargin(0.3)
	gStyle.SetOptStat(0)
	hResidual.GetXaxis().SetTitle( histYaxis )
	hResidual.GetYaxis().SetTitle("#frac{(Data - Fit)}{Fit}")
	hResidual.GetXaxis().SetTitleSize(0.10)
	hResidual.GetXaxis().SetLabelSize(0.07)
	hResidual.GetYaxis().SetLabelSize(0.07)
	hResidual.GetYaxis().SetTitleSize(0.08)
	hResidual.GetYaxis().SetTitleOffset(0.80)
	hResidual.GetYaxis().CenterTitle()
	hResidual.SetMarkerStyle(7)
	hResidual.SetMaximum(1)
	hResidual.SetMinimum(-1)
	hResidual.GetXaxis().SetRangeUser( minX, maxXPlot )
	#hResidual.Sumw2()
	hResidual.Draw("e")
	line.Draw("same")
	c3.SaveAs("Plots/"+hist+"_"+process+"_"+version+"FitP4.pdf")
	del c3

	#return P4GausParameters

def rooFitter( inFileBkg, inFileSignal, hist, folder, MASS, outputRootFile, minX, maxX ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )

	P4GausParameters = FitterCombination( inFileBkg, inFileSignal, hist, folder, P4, minX, maxX )
	bkgAcc = P4GausParameters[7]
	#sigAcc = P4GausParameters[8]
	
	hSignal = inFileSignal.Get(folder+hist)
	sigAcc = hSignal.Integral(hSignal.GetXaxis().FindBin(minX), hSignal.GetXaxis().FindBin( maxX ))/hSignal.Integral(1,hSignal.GetXaxis().FindBin( maxX) )
	hBkg = inFileBkg.Get(folder+hist)
	hData = hBkg.Clone()
	#hData.Add( hSignal )

	mass = RooRealVar( 'mass', 'mass', minX, maxX  )
	rooSigHist = RooDataHist( 'rooSigHist', 'rooSigHist', RooArgList(mass), hSignal )
	rooSigHist.Print()

	signal = RooHistPdf('signal','signal',RooArgSet(mass),rooSigHist)
        signal.Print()
        signal_norm = RooRealVar('signal_norm','signal_norm',0,-1e+05,1e+05)
        #if args.fitBonly: signal_norm.setConstant()
        signal_norm.Print()

        p1 = RooRealVar('p1','p1',P4GausParameters[1], 0., 1000.)
        p2 = RooRealVar('p2','p2',P4GausParameters[2], 0., 50.)
        p3 = RooRealVar('p3','p3',P4GausParameters[3], -10., 10.)
	sqrtS = 13000

        background = RooGenericPdf('background','(pow(1-@0/%.1f,@1)/pow(@0/%.1f,@2+@3*log(@0/%.1f)))'%(sqrtS,sqrtS,sqrtS),RooArgList(mass,p1,p2,p3))
        background.Print()
        dataInt = hData.Integral(hData.GetXaxis().FindBin( minX ), hData.GetXaxis().FindBin(maxX) )
        background_norm = RooRealVar('background_norm','background_norm',dataInt,0.,1e+07)
        background_norm.Print()

        # S+B model
        model = RooAddPdf("model","s+b",RooArgList(background,signal),RooArgList(background_norm,signal_norm))

        rooDataHist = RooDataHist('rooDatahist','rooDathist',RooArgList(mass),hData)
        rooDataHist.Print()

	res = model.fitTo(rooDataHist, RooFit.Save(kTRUE), RooFit.Strategy(0))
	res.Print()

	myWS = RooWorkspace("myWS")
	getattr(myWS,'import')(signal)
        getattr(myWS,'import')(background)
        getattr(myWS,'import')(background_norm)
        getattr(myWS,'import')(rooDataHist,RooFit.Rename("data_obs"))
        myWS.Print()
        myWS.writeToFile(outputRootFile, True)
 # -----------------------------------------
        # write a datacard

        datacard = open('/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_1_5/src/MyLimits/datacard_RPVStop'+str(MASS)+'.txt','w')
        datacard.write('imax 1\n')
        datacard.write('jmax 1\n')
        datacard.write('kmax *\n')
        datacard.write('---------------\n')
	datacard.write("shapes * * "+outputRootFile+" myWS:$PROCESS \n")
        datacard.write('---------------\n')
        datacard.write('bin 1\n')
        datacard.write('observation -1\n')
        datacard.write('------------------------------\n')
        datacard.write('bin          1          1\n')
        datacard.write('process      signal     background\n')
        datacard.write('process      0          1\n')
        datacard.write('rate         '+str(sigAcc)+'      '+str(bkgAcc)+'\n')
        datacard.write('------------------------------\n')
        #flat parameters --- flat prior
        datacard.write('background_norm  flatParam\n')
        datacard.write('p1  flatParam\n')
        datacard.write('p2  flatParam\n')
        datacard.write('p3  flatParam\n')
        datacard.close()

#	''' CONFIG FOR 732 WORKS PERFECT
#	x = RooRealVar( "x", "x", 50., 190. )
#	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[50,190],p1[2116,2117],p2[-62,63],p3[-5,-4]})")
#	myWS.factory("Gaussian:sig_pdf(x, mean[93,94], sigma[5,6])")
#	myWS.factory("SUM:model(nsig[0,100000]*sig_pdf, nbkg[0,1000000]*bkg_pdf)")
#	myWS.factory("SUM:model_b(nbkg[0,1000000]*bkg_pdf)")
#
#	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[70,600], p1[-4000,4000],p2[-300,300],p3[0,40]})")
#
#	'''
#
#	myWS.factory("x["+str(P4GausParameters[7])+","+str(P4GausParameters[8])+"]")
#	bins = (P4GausParameters[8]-P4GausParameters[7])/10
#	myWS.var("x").setBins(int(bins))
#	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1["+str(P4GausParameters[1])+"],p2["+str(P4GausParameters[2])+"],p3["+str(P4GausParameters[3])+"]})")
#	#myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x, p1[-2000,1000],p2[-200,200],p3[-20,20]})")
#	#myWS.factory("Gaussian:sig_pdf(x, mean["+str(MASS)+"], sigma[0,10])")
#	myWS.factory("Gaussian:sig_pdf(x, mean["+str(P4GausParameters[5])+"], sigma["+str(P4GausParameters[6])+"])")
#	#myWS.factory("Gaussian:sig_pdf(x, mean[93.29], sigma[5.52])")
#	#myWS.factory("Gaussian:sig_pdf(x, mean[90,100], sigma[0,10])")
#	myWS.factory("SUM:model_bkg( nbkg[0,100000]*bkg_pdf )")
#	#myWS.factory("SUM:model_sig( nsig[0,10000]*sig_pdf )")
#	myWS.factory("SUM:model( nbkg[0,100000]*bkg_pdf , nsig[0,100000]*sig_pdf)")
#	myWS.Print()
#
#	bkg_pdf = myWS.pdf("model_bkg")
#	#signal_pdf = myWS.pdf("model_sig")
#	#bkg_pdf = myWS.pdf("bkg_pdf")
#	#signal_pdf = myWS.pdf("sig_pdf")
#	pdf = myWS.pdf("model")
#
#	mass = RooArgList( myWS.var("x") )
#	h1 = inFileBkg.Get(folder+'/' + hist)
#	Bkg = h1.Clone()
#	#Bkg.Scale( 1.5 )
#	hData = h1.Clone()
#	bkg = RooDataHist( 'bkg', 'bkg', mass, Bkg)
#
#	#hSignal.Scale(0.1)
#	data_sig = RooDataHist( 'data_sig', 'data_sig', mass, hSignal)
#	#getattr( myWS, 'import')(data_sig)
#	hData.Add( hSignal )
#	data = RooDataHist( 'data', 'data', mass, hData)
#
#	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
#	c1.SetLogy()
#	xframe = myWS.var("x").frame()
#	bkg.plotOn( xframe )
#	xframe.Draw()
#	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
#
#	#### MINOS better than MIGRAD http://pprc.qmul.ac.uk/~bevan/yeti/fitting.pdf
#	nll = bkg_pdf.createNLL(bkg, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
#	m = RooMinuit(nll)
#	m.migrad()
#	m.hesse()
#	m.minos()
#	#bkg_pdf.fitTo( bkg, RooFit.Extended(kTRUE), RooFit.SumW2Error(kFALSE) )
#	#bkg_pdf.fitTo( bkg, RooFit.Extended(), RooFit.Strategy(2), RooFit.Minos(), RooFit.Save(), RooFit.PrintEvalErrors(-1), RooFit.SumW2Error(kTRUE) ) 
#	#bkg_pdf.fitTo( bkg, RooFit.Strategy(2), RooFit.Minos(), RooFit.Save(), RooFit.PrintEvalErrors(-1), RooFit.SumW2Error(kTRUE) ) 
#	#bkg_pdf.fitTo( bkg,RooFit.Save(true),RooFit.Minimizer("Minuit2", "Migrad"),RooFit.SumW2Error(kTRUE), RooFit.PrintEvalErrors(-1) )
#	bkg_pdf.plotOn( xframe )
#	#bkg_pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
#	bkg_pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
#	xframe.Draw()
#	xframe.SetMaximum(100000)
#	xframe.SetMinimum(0.00001)
#	c1.SaveAs('Plots/'+hist+"_QCD_"+PU+"_FitP4Gaus_rooFit.pdf")
#	del c1
#
#	'''
#	c2 = TCanvas('c2', 'c2',  10, 10, 750, 500 )
#	c2.SetLogy()
#	x2frame = myWS.var("y").frame()
#	data_sig1.plotOn( x2frame )
#	x2frame.Draw()
#	x2frame.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
#
#	#### MINOS better than MIGRAD http://pprc.qmul.ac.uk/~bevan/yeti/fitting.pdf
#	nll2 = signal_pdf.createNLL(data_sig1, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
#	m2 = RooMinuit(nll2)
#	m2.migrad()
#	m2.hesse()
#	m2.minos()
#	signal_pdf.plotOn( x2frame )
#	signal_pdf.paramOn( x2frame, RooFit.Layout(0.6,0.9,0.94))
#	x2frame.Draw()
#	c2.SaveAs('Plots/'+hist+"_RPVSt100tojj_"+PU+"_FitP4Gaus_rooFit.pdf")
#	del c2
#	'''
#
#	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
#	xframe = myWS.var("x").frame()
#	data.plotOn( xframe )
#	xframe.Draw()
#	xframe.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
#	#pdf.fitTo( data, RooFit.Save(true), RooFit.PrintEvalErrors(-1) ) # RooFit.Minimizer("Minuit2", "Migrad") )
#	#pdf.fitTo( data,RooFit.Save(true),RooFit.Minimizer("Minuit2", "Migrad"),RooFit.SumW2Error(kTRUE), RooFit.PrintEvalErrors(-1) )
#	nll_data = pdf.createNLL(data, RooFit.Offset(1), RooFit.NumCPU(3), RooFit.Optimize(2) )
#	m_data = RooMinuit(nll_data)
#	m_data.migrad()
#	m_data.hesse()
#	m_data.minos()
#	pdf.plotOn( xframe )
#	pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
#	pdf.plotOn( xframe, RooFit.Components("sig_pdf"), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
#	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
#	xframe.Draw()
#	c1.SaveAs('Plots/'+hist+'_QCD_RPVSt'+str(MASS)+'tojj_'+PU+'_FitP4Gaus_rooFit.pdf')
#	del c1
#
#	#### PSEUDOEXPERIMENT AS DATA
#	'''
#	numBkg = round( myWS.var("nbkg").getVal() )
#	#numBkg = round( myWS.var("nbkg").getVal()+myWS.var("nsig").getVal() )
#	numData = random.randint( numBkg-round(sqrt(numBkg)), numBkg+round(sqrt(numBkg)) )
#	data_obs = myWS.pdf("model_bkg").generateBinned(RooArgSet(mass),numData, RooFit.Name("data_obs")) 
#	#print myWS.var("nbkg").getVal(), myWS.var("nsig").getVal()
#	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
#	c1.SetLogy()
#	xframe = myWS.var("x").frame()
#	data_obs.plotOn( xframe )
#	xframe.Draw()
#	c1.SaveAs('Plots/'+hist+"_PseudoExp_"+PU+"_FitP4Gaus_rooFit.pdf")
#	del c1
#	'''
#
#	####### QCD AS DATA
#	#data_obs = RooDataHist( 'data_obs', 'data_obs', mass, Bkg)
#	data_obs = RooDataHist( 'data_obs', 'data_obs', mass, hData)
#
#	getattr( myWS, 'import')(data_obs)
#	'''
#	modelConfig = RooStats.ModelConfig( 'modelConfig', myWS )
#	modelConfig.SetPdf( myWS.pdf("model") )
#	#modelConfig.SetPdf( myWS.pdf("model_sig") )
#	modelConfig.SetPdf( myWS.pdf("model_bkg") )
#	poi = RooArgSet( myWS.var("nsig") )
#	modelConfig.SetParametersOfInterest( poi )
#	obs = RooArgSet( myWS.var("x") )
#	modelConfig.SetObservables( obs )
#	myWS.defineSet("nuisParams","p1,p2,p3,nbkg")
#	modelConfig.SetNuisanceParameters( myWS.set("nuisParams") )
#	getattr( myWS, 'import')(modelConfig)
#	'''
#
#	myWS.writeToFile(outputRootFile, true )
#	myWS.Print()
#
#	####### Creating datacard
#	outputfile = open('/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_1_5/src/MyLimits/datacard_RPVStop'+str(MASS)+'.txt','w')
#	outputfile.write("imax 1 channels\n")
#	outputfile.write("jmax 1 backgrounds\n")
#	outputfile.write("kmax 0 *\n")
#	outputfile.write("-------------------------------\n")
#	outputfile.write("shapes * * "+outputRootFile+" myWS:$PROCESS \n")
#	outputfile.write("-------------------------------\n")
#	outputfile.write("bin           1\n")
#	outputfile.write("observation  -1\n")
#	outputfile.write("-------------------------------\n")
#	outputfile.write("bin           1          1\n")
#	outputfile.write("process     sig_pdf bkg_pdf\n")
#	outputfile.write("process       0          1\n")
#	outputfile.write('rate          '+str( round( myWS.var("nsig").getVal() ) )+' '+str( round( myWS.var("nbkg").getVal() ) )+' \n')
#	outputfile.write("-------------------------------\n")
#	outputfile.write("# lumi    lnN     1.045         -     \n")
#	outputfile.write("# GausSigma  param       45.1220       5.7784  \n")
#	outputfile.write("# GausMean  param       1000.0000       10.0000  \n")
#	outputfile.write("# SigNormFit   lnN    1.0600       - \n")
#	outputfile.write("# SigNormPDF   lnN    1.0300       - \n")
#	outputfile.write("# SigNormJES   lnN    1.0400       - \n")
#	outputfile.write("# SigNormPU   lnN    1.0300        - \n")
#	outputfile.write("# SigNormISR   lnN    1.1000        - \n")
#	outputfile.write("# SigNormBtag   lnN    1.0000       - -\n")
#	outputfile.write("# b  param       78.8566       33.5562\n")
#	outputfile.write("# c  param       -8.4161       10.6159\n")
#	outputfile.write("# d  param       -0.8140       1.5043\n")
#	outputfile.write("# BkgNorm    lnN     -       2.0000\n")
#	outputfile.close()

def rooFitterTree( inFileBkg, inFileSignal, inFileData, hist, folder ):
	"""function to run Roofit and save workspace for RooStats"""
	warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*class stack<RooAbsArg\*,deque<RooAbsArg\*> >' )
	
	myWS = RooWorkspace("myWS")

	x = RooRealVar( "x", "x", 50., 180. )
	myWS.factory("EXPR:bkg_pdf('pow(1-(x/13000.0),p1)/pow(x/13000.0,p2+p3*log(x/13000.))', {x[50,180],p1[0,1000],p2[0,100],p3[0,10]})")
	myWS.factory("Gaussian:sig_pdf(x, mean[90,110], sigma[0,10])")
	myWS.factory("SUM:model(nsig[0,10000]*sig_pdf, nbkg[0,1000000]*bkg_pdf)")
	myWS.Print()

	#x = myWS.var("x")
	mass = myWS.var("mass")
	pdf = myWS.pdf("model")

	#mass = RooArgList( x )
	massAveForFit = RooRealVar( "massAveForFit", "massAveForFit", 50., 180. )
	bkgTree = inFileBkg.Get(folder+'/RUNATree' )
	bkg = RooDataSet( "bkg", "bkg", RooArgSet(massAveForFit), RooFit.Import( bkgTree ) )
	signalTree = inFileSignal.Get(folder+'/RUNATree' )
	signal = RooDataSet( "signal", "signal", RooArgSet(massAveForFit), RooFit.Import( signalTree ) )
	dataTree = inFileData.Get(folder+'/RUNATree' )
	data = RooDataSet( "data", "data", RooArgSet(massAveForFit), RooFit.Import( dataTree ) )
	
	getattr( myWS, 'import')(data)

	c1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	xframe = massAveForFit.frame()
	data.plotOn( xframe )
	xframe.Draw()
	xframe.GetXaxis().SetTitle( histYaxis )
	pdf.fitTo( data, RooFit.Save(true), RooFit.Minimizer("Minuit2", "Migrad") )
	#pdf.fitTo( data, RooFit.Save(true) , RooFit.Minimizer("Minuit2", "Migrad"), RooFit.SumW2Error(kTRUE) )
	pdf.plotOn( xframe )
	pdf.plotOn( xframe, RooFit.Components("bkg_pdf"), RooFit.LineStyle(kDashed) )
	pdf.plotOn( xframe, RooFit.Components("sig_pdf"), RooFit.LineColor(kRed), RooFit.LineStyle(kDashed) );
	pdf.paramOn( xframe, RooFit.Layout(0.6,0.9,0.94))
	xframe.Draw()
	c1.SaveAs('Plots/'+hist+"_QCD_RPVSt100tojj_"+PU+"_FitP4Gaus_rooFitTree.pdf")
	del c1

	modelConfig = RooStats.ModelConfig( 'modelConfig', myWS )
	modelConfig.SetPdf( myWS.pdf("model") )
	poi = RooArgSet( myWS.var("nsig") )
	modelConfig.SetParametersOfInterest( poi )
	obs = RooArgSet( myWS.var("x") )
	modelConfig.SetObservables( obs )
	myWS.defineSet("nuisParams","p1,p2,p3,nbkg")
	modelConfig.SetNuisanceParameters( myWS.set("nuisParams") )

	getattr( myWS, 'import')(modelConfig)
	myWS.writeToFile("Rootfiles/workspace_QCD_RPVSt100tojj_FitP4Gaus_"+PU+"_rooFitTree.root", True )
	myWS.Print()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--process', action='store', default='Full', help='Type of fit to use.' )
	parser.add_argument('-v', '--version', action='store', default='Resolved', help='For Boosted of Resolved.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-m', '--mass', action='store', type=int, default=350, help='Decay, example: jj, bj.' )
	parser.add_argument('-pu', '--PU', action='store', default='Asympt25ns', help='PU, example: PU40bx25.' )
	parser.add_argument('-l', '--lumi', action='store', default='1000', help='Luminosity, example: 1.' )
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	process = args.process
	version = args.version
	jj = args.decay
	PU = args.PU
	lumi = args.lumi
	MASS = args.mass

	CMS_lumi.lumi_13TeV = '2.45 fb^{-1}'

	outputDir = "Plots/"
	fileSignal = TFile('Rootfiles/RUNMini'+version+'Analysis_RPVStopStopToJets_UDD312_M-'+str(MASS)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root')
	fileBkg = TFile('Rootfiles/RUNMini'+version+'Analysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root')
	fileData = TFile('Rootfiles/RUNMini'+version+'Analysis_JetHTRun2015D-All_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root')
	outputRootFile = '/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_4_5_patch1/src/RUNA/RUNAnalysis/test/Rootfiles/workspace_QCD_RPVSt'+str(MASS)+'tojj_FitP4Gaus_'+PU+'_rooFit_'+lumi+'fb.root'

	###### Input parameters
	#hist = 'massAve_cutEtaBand' # str ( sys.argv[1] )
	if 'Resolved' in version: 
		hist = 'massAve_cutDelta'
		histYaxis = "Average Dijet Mass [GeV]"
		minFit = 240
		maxFit = 1000
		rebinX = 2
	#elif 'Boosted' in version: 
	else:
		hist = 'massAve_cutCosThetaMassAsym'
		histYaxis = "Average Mass [GeV]"
		minFit = 140
		maxFit = 350
		rebinX = 1
	#folder = "ResolvedAnalysisPlots/"      # str ( sys.argv[2] )
	folder = ""      # str ( sys.argv[2] )
	

	if 'full' in process:
		CMS_lumi.extraText = "Preliminary"
		p = Process( target=FitterCombination, args=( fileData, fileBkg, fileSignal, hist, folder, P4, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX ))
	elif 'Data' in process:
		CMS_lumi.extraText = "Preliminary"
		p = Process( target=FitterCombination, args=( fileData, fileBkg, '', hist, folder, P4, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX ))
	elif 'MC' in process:
		CMS_lumi.extraText = "Preliminary Simulation"
		p = Process( target=FitterCombination, args=( '', fileBkg, fileSignal, hist, folder, P4, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX ))
	elif 'QCD' in process:
		CMS_lumi.extraText = "Preliminary Simulation"
		p = Process( target=rootFitter, args=( fileBkg, hist, folder, P4, [ 0.1, 100, 2, 0.1 ], minFit, maxFit, rebinX, True ) ) 
	elif 'RPV' in process:
		process = 'RPVSt'+str(MASS)+'tojj'
		CMS_lumi.extraText = "Preliminary Simulation"
		p = Process( target=rootFitter, args=( fileSignal, hist, folder, gaus, [ ], MASS-50, MASS+50, rebinX, True, False ) ) 
	elif 'rooFit' in process:
		rooFitter( fileData, fileSignal, hist, folder, MASS, outputRootFile, 200.0, 1000.0  )
		#rooFitter( fileBkg, fileSignal, hist, folder, MASS, outputRootFile, 250.0, 450.0  )
	else:
		rooFitterTree( fileBkg, fileSignal, fileData, hist, folder )
	p.start()
	p.join()

	


