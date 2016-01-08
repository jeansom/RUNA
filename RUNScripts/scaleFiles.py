#!/usr/bin/env python
'''
File: scaleQCD.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: simple script to scale QCD Files
'''

from ROOT import TFile, TH1, TH2, TMath, gROOT, gPad, TTree
import sys, os
import argparse
from RUNA.RUNAnalysis.scaleFactors import scaleFactor
#from ROOT import *

gROOT.Reset()
gROOT.SetBatch()


listDir = []

def scaleFiles( inFileName, lumi ):
	"""docstring for scaleQCD"""

	if os.path.exists(inFileName+'_Scaled.root'): 
		os.remove(inFileName+'_Scaled.root')
		outfile = TFile( inFileName+'_Scaled.root', "RECREATE")
	else: outfile = TFile( inFileName+'_Scaled.root', "RECREATE")
	
	infile = TFile( inFileName+'.root', "READ")

	scale = lumi * scaleFactor(inFileName)

	listDir = []
	for k in infile.GetListOfKeys(): 
		name = k.GetName()
		listDir.append( name )
	for j in listDir:
		if not 'RUNATree' in j:
			outfile.mkdir(j)
			outfile.cd(j)
			dir = infile.GetDirectory(j)
			for q in dir.GetListOfKeys():
				name = q.GetName()
				h = infile.Get( j+'/'+name)
				try:
					hOut = h.Clone()
					#hOut.Scale( scale )
					if not isinstance(h,TTree): 
						hOut.Scale( scale )
						hOut.Write()
				except AttributeError:
					pass
			outfile.cd('/')
	
	outfile.Write()
	outfile.Close()
	infile.Close()

if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-s', '--sample', action='store', dest='sample', default="QCD", help='Sample to scale.' )
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default='100', help='Mass of the Stop' )
	parser.add_argument( '-p', '--pileup', action='store',  dest='pileup', default='Asympt25ns', help='Pileup' )
	parser.add_argument( '-v', '--version', action='store',  dest='version', default='v08_v01', help='Pileup' )
	parser.add_argument( '-l', '--lumi', action='store', type=float, dest='lumi', default=1000, help='Lumi' )
	
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	sample = args.sample
	mass = args.mass
	pu = args.pileup
	lumi = args.lumi
	version = args.version

	if "QCD" in sample:

		if 'Pt' in sample:
			ptBins = [
					'170to300',
					'300to470',
					'470to600',
					'600to800',
					'800to1000',
					'1000to1400',
					'1400to1800',
					'1800to2400',
					'2400to3200',
					'3200toInf'
					]

			for pt in ptBins:
				scaleFiles( 'RUNAnalysis_QCD_Pt_'+pt+'_RunIISpring15MiniAODv2-74X_'+pu+'_'+version, lumi )
		else:
			htBins = [
					'500to700',
					'700to1000',
					'1000to1500',
					'1500to2000',
					'2000toInf',
					]

			for ht in htBins:
				scaleFiles( 'RUNAnalysis_QCD_HT'+ht+'_RunIISpring15MiniAODv2-74X_'+pu+'_'+version, lumi )

	elif 'RPV' in sample:
		scaleFiles( 'RUNAnalysis_RPVSt'+mass+'tojj_RunIISpring15MiniAODv2-74X_'+pu+'_'+version, lumi )
	elif 'WWTo4Q' in sample:
		scaleFiles( 'RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_'+pu+'_'+version, lumi )
