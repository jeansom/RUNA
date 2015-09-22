#! /usr/bin/env python

#CONFIGURATION

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', type='string', action='store',
                  default='outplots.root',
                  dest='outname',
                  help='Name of output file')

parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print debugging info')

parser.add_option('--maxevents', type='int', action='store',
                  default=1000,
                  dest='maxevents',
                  help='Number of events to run. -1 is all events')




(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
ROOT.gROOT.Macro("~/rootlogon.C")
import copy
import random



#AK8 Jets label and Handles
### MiniAOD
#h_jetsAK8 = Handle("vector<pat::Jet>")
#l_jetsAK8 = ("slimmedJetsAK8" ) 
### AOD
#h_jetsAK8 = Handle("vector<reco::PFJet>")
#l_jetsAK8 = ("ak8PFJetsCHS" ) 
## RAW
h_jetsAK8 = Handle("vector<reco::GenJet>")
l_jetsAK8 = ("ak8GenJets" ) 
#



#HISTOGRAMS

f = ROOT.TFile(options.outname, "RECREATE")
f.cd()


h_ptAK8 = ROOT.TH1F("h_ptAK8", "AK8 Jet p_{T};p_{T} (GeV)", 300, 0, 3000)
h_HTAK8 = ROOT.TH1F("h_HTAK8", "AK8 HT;HT (GeV)", 300, 0, 3000)
h_etaAK8 = ROOT.TH1F("h_etaAK8", "AK8 Jet #eta;#eta", 120, -6, 6)
h_phiAK8 = ROOT.TH1F("h_phiAK8", "AK8 Jet #phi;#phi (radians)",100,-3.14, 3.14)#ROOT.Math.Pi(),ROOT.Math.Pi())
h_mAK8 = ROOT.TH1F("h_mAK8", "AK8 Jet Mass;Mass (GeV)", 100, 0, 1000)


#EVENT LOOP

#filesModule = __import__( options.files  )#'RPVSt100tojj_13TeV_RunIISpring15DR74_MiniAOD_cfi')
filesModule = __import__( 'RPVSt200tojj_13TeV_RunIISpring15DR74_RAW_cfi')
filesraw = filesModule.readFiles  #[ options.files ]
#filesraw = [ options.files ]
files = []
nevents = 0
for ifile in filesraw :
    if len( ifile ) > 2 : 
        s = 'root://cmsxrootd.fnal.gov/' + ifile.rstrip()
        #s = ifile.rstrip()
        files.append( s )
        print 'Added ' + s



# loop over files
for ifile in files :
    print 'Processing file ' + ifile
    events = Events (ifile)
    if options.maxevents > 0 and nevents > options.maxevents :
        break

    # loop over events in this file
    i = 0
    for event in events:
        if options.maxevents > 0 and nevents > options.maxevents :
            break
        i += 1
        nevents += 1

        if nevents % 1000 == 0 : 
            print '    ---> Event ' + str(nevents)
        if options.verbose :
            print '==============================================='
            print '    ---> Event ' + str(nevents)



        ############################################
        # Get the AK8 jets
        ############################################

        event.getByLabel ( l_jetsAK8, h_jetsAK8 )
        jetsAK8 = h_jetsAK8.product()

 	HT = 0	
        for jetAK8 in jetsAK8: 
            
		HT+= jetAK8.pt()
		h_ptAK8.Fill( jetAK8.pt() )
		h_etaAK8.Fill( jetAK8.eta() )
		h_phiAK8.Fill( jetAK8.phi() )
		h_mAK8.Fill( jetAK8.mass() )

	if (HT > 0 ): h_HTAK8.Fill( HT )

f.cd()
f.Write()
f.Close()

