#!/usr/bin/env python

import os, sys
from ROOT import gROOT, TFile, TH2D
from array import array

gROOT.SetBatch(1)

#----------------------------------------------------------------------------------
# Configurable parameters

datasets = [
  # RPV Signal
  [
    'StealthSbottomTo3b_MSb_175', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'  # jet type and b-tagging label
  ],
  [
      'StealthSbottomTo3b_MSb_200', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'  # jet type and b-tagging label
  ],
  [
    'StealthSbottomTo3b_MSb_250', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'  # jet type and b-tagging label
  ],
  [
  'StealthSbottomTo3b_MSb_300', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'  # jet type and b-tagging label
  ],
  [
      'StealthSbottomTo3b_MSb_350', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'  # jet type and b-tagging label
  ],
  [
      'StealthSbottomTo3b_MSb_400', # dataset name
      {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
       'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'  # jet type and b-tagging label
  ],
  [
  'StealthSbottomTo3b_MSb_500', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'AK5PF_CSVM'  # jet type and b-tagging label
  ],

]
pathToInputFiles = '/cms/clseitz/ThreeJet/BtagMap/Stealth'
inputFileSubdirectory = 'bTaggingEffAnalyzerAK5PF'
outputFileSuffix = 'bTaggingEfficiencyMap'

#----------------------------------------------------------------------------------

def produceEfficiencyMaps(dataset, inputPath, subdirectory, suffix):

  inputFilename = os.path.join(inputPath, dataset[0]+'_BtagMap.root')

  inputFile = TFile(inputFilename, 'READ')

  outputFilename = dataset[0]+ '_' + dataset[2] + '_' + suffix + '.root'
  #outputFilename = 'test.root'
  outputFile = TFile(outputFilename, 'RECREATE')

  for partonFlavor in ['b', 'c', 'udsg']:

    denominatorHisto = subdirectory + '/h2_BTaggingEff_Denom_' + partonFlavor
    numeratorHisto = subdirectory + '/h2_BTaggingEff_Num_' + partonFlavor

    denominatorIn = inputFile.Get(denominatorHisto)
    numeratorIn = inputFile.Get(numeratorHisto)

    xShift = denominatorIn.GetXaxis().GetBinWidth(1)/2.
    yShift = denominatorIn.GetYaxis().GetBinWidth(1)/2.

    binsX = array('d', dataset[1][partonFlavor][0])
    binsY = array('d', dataset[1][partonFlavor][1])

    denominatorOut = TH2D('denominator_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
    numeratorOut   = TH2D('numerator_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
    efficiencyOut  = TH2D('efficiency_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)

    # loop over all bins
    for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
      for j in range(1,denominatorOut.GetYaxis().GetNbins()+1):

	binXMin = denominatorIn.GetXaxis().FindBin(denominatorOut.GetXaxis().GetBinLowEdge(i)+xShift)
	binXMax = denominatorIn.GetXaxis().FindBin(denominatorOut.GetXaxis().GetBinUpEdge(i)-xShift)
	binYMinPos = denominatorIn.GetYaxis().FindBin(denominatorOut.GetYaxis().GetBinLowEdge(j)+yShift)
	binYMaxPos = denominatorIn.GetYaxis().FindBin(denominatorOut.GetYaxis().GetBinUpEdge(j)-yShift)
	binYMinNeg = denominatorIn.GetYaxis().FindBin(-denominatorOut.GetYaxis().GetBinUpEdge(j)+yShift)
	binYMaxNeg = denominatorIn.GetYaxis().FindBin(-denominatorOut.GetYaxis().GetBinLowEdge(j)-yShift)

	denominator = denominatorIn.Integral(binXMin,binXMax,binYMinPos,binYMaxPos)
	denominator = denominator + denominatorIn.Integral(binXMin,binXMax,binYMinNeg,binYMaxNeg)
	numerator = numeratorIn.Integral(binXMin,binXMax,binYMinPos,binYMaxPos)
	numerator = numerator + numeratorIn.Integral(binXMin,binXMax,binYMinNeg,binYMaxNeg)

	denominatorOut.SetBinContent(i,j,denominator)
	numeratorOut.SetBinContent(i,j,numerator)
	if(denominator>0.): efficiencyOut.SetBinContent(i,j,numerator/denominator)

    # check if there are any bins with 0 or 100% efficiency
    for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
      for j in range(1,denominatorOut.GetYaxis().GetNbins()+1):

	efficiency = efficiencyOut.GetBinContent(i,j)
	if(efficiency==0. or efficiency==1.):
	  print 'Warning! Bin(%i,%i) for %s jets has a b-tagging efficiency of %.3f'%(i,j,partonFlavor,efficiency)

    # set efficiencies in overflow bins
    for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
      efficiencyOut.SetBinContent(i, denominatorOut.GetYaxis().GetNbins()+1, efficiencyOut.GetBinContent(i, denominatorOut.GetYaxis().GetNbins()))

    for j in range(1,denominatorOut.GetYaxis().GetNbins()+2):
      efficiencyOut.SetBinContent(denominatorOut.GetXaxis().GetNbins()+1, j, efficiencyOut.GetBinContent(denominatorOut.GetXaxis().GetNbins(), j))

    outputFile.cd()

    denominatorOut.Write()
    numeratorOut.Write()
    efficiencyOut.Write()

  outputFile.Close()

  print '-------------------------------------------------------------------------------------------'
  print 'b-tagging efficiency map for'
  print dataset[0]
  print 'successfully created and stored in %s'%outputFilename
  print ''


def main():

  for dataset in datasets:
    produceEfficiencyMaps(dataset, pathToInputFiles, inputFileSubdirectory, outputFileSuffix)

if __name__ == "__main__":
  main()
