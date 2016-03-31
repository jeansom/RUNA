#include <memory>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <iostream>

#include <TH1F.h>
#include <TROOT.h>
#include <TLorentzVector.h>
#include <TFile.h>
#include <TSystem.h>

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
//#include "DataFormats/JetsReco/interface/Jets.h"
//#include "DataFormats/PatCandidates/interface/Jets.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h"

using namespace std;

int main(int argc, char* argv[]) {


	// ----------------------------------------------------------------------
	// First Part: 
	//
	//  * enable the AutoLibraryLoader 
	//  * book the histograms of interest 
	//  * open the input file
	// ----------------------------------------------------------------------

	// load framework libraries
	gSystem->Load( "libFWCoreFWLite" );
	AutoLibraryLoader::enable();

	// initialize command line parser
	optutl::CommandLineParser parser ("Analyze FWLite Histograms");

	// set defaults
	parser.integerValue ("maxEvents"  ) = -1;
	parser.integerValue ("outputEvery") =   10;
	parser.stringValue  ("outputFile" ) = "myOutputFile.root";

	// parse arguments
	parser.parseArguments (argc, argv);
	int maxEvents_ = parser.integerValue("maxEvents");
	unsigned int outputEvery_ = parser.integerValue("outputEvery");
	std::string outputFile_ = parser.stringValue("outputFile");
	std::vector<std::string> inputFiles_ = parser.stringVector("inputFiles");

	// book a set of histograms
	fwlite::TFileService fs = fwlite::TFileService(outputFile_.c_str());
	TFileDirectory dir = fs.mkdir("analyzeRUN");
	TH1F* jetsPt_  = dir.make<TH1F>("jetsPt"  , "pt"  ,   100,   0., 300.);
	TH1F* jetsEta_ = dir.make<TH1F>("jetsEta" , "eta" ,   100,  -3.,   3.);
	TH1F* stopPt_ = dir.make<TH1F>("stopPt" , "stopPt",   100,   0., 300.);  
	TH1F* stopMass_ = dir.make<TH1F>("stopMass" , "stopMass",   100,   0., 300.);  
	TH1F* jetsPt_2j_  = dir.make<TH1F>("jetsPt_2j"  , "pt"  ,   100,   0., 300.);
	TH1F* jetsEta_2j_ = dir.make<TH1F>("jetsEta_2j" , "eta" ,   100,  -3.,   3.);
	TH1F* stopPt_2j_ = dir.make<TH1F>("stopPt_2j" , "stopPt",   100,   0., 300.);  
	TH1F* stopMass_2j_ = dir.make<TH1F>("stopMass_2j" , "stopMass",   100,   0., 300.);  
	TH1F* numFinalPart_ = dir.make<TH1F>("numFinalPart" , "numFinPart" ,   10,  0.,   10.);

	// loop the event/
	int ievt=0;  
	for(unsigned int iFile=0; iFile<inputFiles_.size(); ++iFile){

		// open input file (can be located on castor)
		TFile* inFile = TFile::Open(inputFiles_[iFile].c_str());
		if( inFile ){
			// ----------------------------------------------------------------------
			// Second Part: 
			//
			//  * loop the events in the input file 
			//  * receive the collections of interest via fwlite::Handle
			//  * fill the histograms
			//  * after the loop close the input file
			// ----------------------------------------------------------------------      
			fwlite::Event ev(inFile);
			for(ev.toBegin(); !ev.atEnd(); ++ev, ++ievt){

				edm::EventBase const & event = ev;

				// break loop if maximal number of events is reached 
				if(maxEvents_>0 ? ievt+1>maxEvents_ : false) break;
				// simple event counter
				if(outputEvery_!=0 ? (ievt>0 && ievt%outputEvery_==0) : false) 
				  std::cout << "  processing event: " << ievt << std::endl;

				// Handle to the jets pt
				edm::Handle<std::vector<reco::GenParticle>> particles;
				event.getByLabel(std::string("genParticles"), particles);
				// loop jets collection and fill histograms

				TLorentzVector stop1, stop2;				
				vector<TLorentzVector> pStop1, pStop2;
				int dumm = 0;
				for(const reco::GenParticle &p : *particles ) {

					if( !p.mother() ) continue;

					if ( p.status() == 22 ) {

						if ( p.pdgId() > 0 )  stop1.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy()  );
						else if ( p.pdgId() < 0 )  stop2.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy()  );
						else cout << "No Stop in this event" << endl;
					       	
					}
					
					TLorentzVector tmp;

					if ( p.status() == 23 ) {

						dumm++;

						if( abs( p.mother()->pdgId() ) > 100000 ) {

							if ( ( p.pdgId() == 3 ) || ( p.pdgId() == 1 )  ) {

								tmp.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy() );
								pStop2.push_back( tmp );
								//cout << p.pdgId() << " " << p.status() << " 3 or 1 " << endl;

							} else if ( ( p.pdgId() == -3 ) || ( p.pdgId() == -1 )  ) {

								tmp.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy() );
								pStop1.push_back( tmp );
								//cout << p.pdgId() << " " << p.status() << " -3 or -1 " << endl;
							}
						}
					} 

				}

				numFinalPart_->Fill( dumm );
				if ( pStop1.size() == 2 ) {

					double stop1Mass = ( pStop1[0] + pStop1[1] ).M();
				
					stopPt_2j_->Fill( stop1.Pt() );
					stopMass_2j_->Fill( stop1.M() );
					if ( ( stop1Mass - stop1.M() ) < 5 ){
						jetsPt_2j_->Fill( pStop1[0].Pt() );
						jetsPt_2j_->Fill( pStop1[1].Pt() );
						jetsEta_2j_->Fill( pStop1[0].Eta() );
						jetsEta_2j_->Fill( pStop1[1].Eta() );
					}

					if( dumm == 4 ){
						stopPt_->Fill( stop1.Pt() );
						stopMass_->Fill( stop1.M() );
						if ( ( stop1Mass - stop1.M() ) < 5 ){
							jetsPt_->Fill( pStop1[0].Pt() );
							jetsPt_->Fill( pStop1[1].Pt() );
							jetsEta_->Fill( pStop1[0].Eta() );
							jetsEta_->Fill( pStop1[1].Eta() );
						}
						else cout << "not stop" << stop1Mass << endl;
					}

				} else cout << "event " << ievt << " have more than 2 antiquarks with 23 status." << endl;

				if ( pStop2.size() == 2 ) {

					double stop2Mass = ( pStop2[0] + pStop2[1] ).M();
					stopPt_2j_->Fill( stop2.Pt() );
					stopMass_2j_->Fill( stop2.M() );
					if ( ( stop2Mass - stop2.M() ) < 5 ){
						jetsPt_2j_->Fill( pStop2[0].Pt() );
						jetsPt_2j_->Fill( pStop2[1].Pt() );
						jetsEta_2j_->Fill( pStop2[0].Eta() );
						jetsEta_2j_->Fill( pStop2[1].Eta() );
					}
					
					if( dumm == 4 ){
						stopPt_->Fill( stop2.Pt() );
						stopMass_->Fill( stop2.M() );
						if ( ( stop2Mass - stop2.M() ) < 5 ){
							jetsPt_->Fill( pStop2[0].Pt() );
							jetsPt_->Fill( pStop2[1].Pt() );
							jetsEta_->Fill( pStop2[0].Eta() );
							jetsEta_->Fill( pStop2[1].Eta() );
						}
						else cout << "not stop" << stop2Mass << endl;
					}

				} else cout << "event " << ievt << " have more than 2 antiquarks with 23 status." << endl;

			}

			// close input file
			inFile->Close();
		}
	// break loop if maximal number of events is reached:
	// this has to be done twice to stop the file loop as well
	if(maxEvents_>0 ? ievt+1>maxEvents_ : false) break;
	}
	return 0;
}


