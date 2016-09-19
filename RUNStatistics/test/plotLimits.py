#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

from ROOT import *
import time, os, math, sys
import argparse
from collections import OrderedDict
try:
	from RUNA.RUNAnalysis.commonFunctions import *
	from RUNA.RUNAnalysis.scaleFactors import *
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from commonFunctions import *
	from scaleFactors import *
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle

gROOT.SetBatch(kTRUE);
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetTitleFont(42, "XYZ")
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelFont(42, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetCanvasBorderMode(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetCanvasColor(kWhite)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadBottomMargin(0.15)
gROOT.ForceStyle()


def plotLimits( listMasses  ):
	"""docstring for plotLimits"""
	
	masses = array('d')
	masses_exp = array('d')
	xs_theory = array('d')
	xs_obs_limits = array('d')
	xs_exp_limits = array('d')
	xs_exp_limits_1sigma = array('d')
	xs_exp_limits_1sigma_up = array('d')
	xs_exp_limits_2sigma = array('d')
	xs_exp_limits_2sigma_up = array('d')

	for mass in listMasses:
		masses.append( mass )
		masses_exp.append( mass )

	if args.theta:
		thetaExpectedFile = open('thetaFiles/theta_expected_'+args.version+'.txt','r')
		thetaObservedFile = open('thetaFiles/theta_observed_'+args.version+'.txt','r')
		for line in thetaExpectedFile:
			li=line.strip()
			if not li.startswith("#"):
				mass = float(line.split()[0])
				XS =  search( dictXS, 'RPVStopStopToJets_UDD312_M-'+str(mass) )
				xs_theory.append( XS )
				xs_exp_limits.append(float(line.split()[1]) *XS )
				xs_exp_limits_2sigma.append(float(line.split()[2]) *XS )
				xs_exp_limits_2sigma_up.append(float(line.split()[3]) *XS )
				xs_exp_limits_1sigma.append(float(line.split()[4]) *XS )
				xs_exp_limits_1sigma_up.append(float(line.split()[5]) *XS )
		for line in thetaObservedFile:
			li=line.strip()
			if not li.startswith("#"):
				mass = float(line.split()[0])
				XS =  search( dictXS, 'RPVStopStopToJets_UDD312_M-'+str(mass) )
				xs_obs_limits.append(float(line.split()[1]) *XS )

	else:
		for mass in listMasses:
			XS =  search( dictXS, 'RPVStopStopToJets_UDD312_M-'+str(mass) )
			xs_theory.append( XS )
			tmpFile, tmpTree, tmpEntries = getTree( "higgsCombineUDD312RPVSt_M-"+str(mass)+args.sys+'_'+args.version+".Asymptotic.mH120.root", "limit" )
			for i in xrange(tmpEntries):
				tmpTree.GetEntry(i)
				tmp = round( tmpTree.quantileExpected, 2)
				if tmp == 0.03: xs_exp_limits_2sigma.append( tmpTree.limit * XS )
				if tmp == 0.16: xs_exp_limits_1sigma.append( tmpTree.limit * XS )
				if tmp == 0.5: 
					xs_exp_limits.append( tmpTree.limit * XS )
					print mass, round( tmpTree.limit * XS, 2)
				if tmp == 0.84: xs_exp_limits_1sigma_up.append( tmpTree.limit * XS )
				if tmp == 0.98: xs_exp_limits_2sigma_up.append( tmpTree.limit * XS ) 
				if tmp == -1: xs_obs_limits.append( tmpTree.limit * XS )

	for i in range(0,len(masses)):
		masses_exp.append( masses[len(masses)-i-1] )
		xs_exp_limits_1sigma.append( xs_exp_limits_1sigma_up[len(masses)-i-1] )
		xs_exp_limits_2sigma.append( xs_exp_limits_2sigma_up[len(masses)-i-1] )

	graph_xs_th = TGraph(len(masses),masses,xs_theory)
	graph_xs_th.SetLineWidth(3)
	graph_xs_th.SetLineStyle(8)
	graph_xs_th.SetLineColor(6)

	graph_exp_2sigma = TGraph(len(masses_exp),masses_exp,xs_exp_limits_2sigma)
	graph_exp_2sigma.SetFillColor(kYellow)

	graph_exp_1sigma = TGraph(len(masses_exp),masses_exp,xs_exp_limits_1sigma)
	graph_exp_1sigma.SetFillColor(kGreen+1)

	graph_exp = TGraph(len(masses),masses,xs_exp_limits) 
	#graph_exp.SetMarkerStyle(24)
	graph_exp.SetLineWidth(3)
	graph_exp.SetLineStyle(2)
	graph_exp.SetLineColor(4)

	graph_obs = TGraph(len(masses),masses,xs_obs_limits)
	graph_obs.SetMarkerStyle(20)
	graph_obs.SetLineWidth(3)
	graph_obs.SetLineStyle(1)
	graph_obs.SetLineColor(1)

	c = TCanvas("c", "",800,800)
	c.cd()

	legend = TLegend(.55,.70,.90,.90)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	legend.SetTextSize(0.03)
	legend.SetHeader('95% CL upper limits')

	graph_exp_2sigma.GetXaxis().SetTitle("Resonance mass [GeV]")
	graph_exp_2sigma.GetYaxis().SetTitle("#sigma #times #it{B} [pb]")
	graph_exp_2sigma.GetYaxis().SetTitleOffset(1.1)
	graph_exp_2sigma.GetYaxis().SetRangeUser(5,1e+04)
	#graph_exp_2sigma.GetXaxis().SetNdivisions(1005)

	graph_exp_2sigma.Draw("AF")
	graph_exp_1sigma.Draw("F")
	graph_exp.Draw("L")
	graph_obs.Draw("LP")
        graph_xs_th.Draw("L")

        legend.AddEntry(graph_xs_th,"RPV #lambda_{312} (#tilde{t} #rightarrow qq)","l")
        #legend.AddEntry(graph_xs_th,"UDD312 RPV Stop #tilde{t}","l")
	legend.AddEntry(graph_obs,"Observed","lp")
	legend.AddEntry(graph_exp,"Expected","lp")
	legend.AddEntry(graph_exp_1sigma,"#pm 1#sigma","F")
	legend.AddEntry(graph_exp_2sigma,"#pm 2#sigma","F")
    	legend.Draw()

	CMS_lumi.relPosX = 0.10
	CMS_lumi.CMS_lumi(c, 4, 0)
	gPad.RedrawAxis()

	c.SetLogy()
	#fileName = 'xs_limit_%s_%s.%s'%(args.method,args.final_state + ( ('_' + args.postfix) if args.postfix != '' else '' ), args.fileFormat.lower())
	fileName = 'xs_limit_RPVStop_UDD312_Boosted'+args.sys+'_'+args.version+'.'+args.ext
	if args.theta: fileName = fileName.replace('limit', 'limit_theta')
	if 'gaus' in args.process: fileName = fileName.replace('limit', 'limit_gaus')
	print 'Processing.......', fileName
	c.SaveAs( 'Plots/'+fileName )

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', dest='process', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', dest='jj', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-b', '--booted', dest='boosted', action='store', default='Boosted', help='Boosted or non version, example: Boosted' )
	parser.add_argument('-v', '--version', dest='version', action='store', default='v05', help='Boosted or non version, example: Boosted' )
	parser.add_argument('-t', '--theta', dest='theta', action='store', type=float, default=False, help='Boosted or non version, example: Boosted' )
	parser.add_argument('-l', '--lumi', dest='lumi', action='store', type=float, default=149.9, help='Luminosity, example: 1.' )
	parser.add_argument('-e', '--extension', dest='ext', action='store', default='png', help='Extension of plots.' )
	parser.add_argument('-s', '--sys', dest='sys', action='store', default='_NOSys', help='Decay, example: jj, bj.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	
	CMS_lumi.extraText = "Preliminary"
	lumi = 2606
	CMS_lumi.lumi_13TeV = "2.7 fb^{-1}"
	if 'gaus' in args.process: massList = range( 80, 360, 10 )
	else: massList = [ 80, 90, 100, 110, 120, 130, 140, 150, 170, 180, 190, 210, 220, 230, 240, 300]
	plotLimits( massList  )
