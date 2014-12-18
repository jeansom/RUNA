#include <memory>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <iostream>

#include <TH1F.h>
#include <TROOT.h>
#include <TFile.h>
#include <TSystem.h>

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h"

int main(int argc, char* argv[]) 
{
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
  parser.integerValue ("maxEvents"  ) = 10;
  parser.integerValue ("outputEvery") =   10;
  parser.stringValue  ("outputFile" ) = "myOutputFile.root";

  // parse arguments
  parser.parseArguments (argc, argv);
  int maxEvents_ = parser.integerValue("maxEvents");
  unsigned int outputEvery_ = parser.integerValue("outputEvery");
  std::string outputFile_ = parser.stringValue("outputFile");
  std::vector<std::string> inputFiles_ = parser.stringVector("inputFiles");

  // book a set of histograms
/*  fwlite::TFileService fs = fwlite::TFileService(outputFile_.c_str());
  TFileDirectory dir = fs.mkdir("analyzePatJets");
  TH1F* jetsPt_  = dir.make<TH1F>("jetsPt"  , "pt"  ,   100,   0., 300.);
  TH1F* jetsEta_ = dir.make<TH1F>("jetsEta" , "eta" ,   100,  -3.,   3.);
  TH1F* jetsPhi_ = dir.make<TH1F>("jetsPhi" , "phi" ,   100,  -5.,   5.);  
  */

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
	edm::Handle< reco::BasicJetCollection > basicJets;
	event.getByLabel(std::string("ca8PFJetsCHSPruned"), basicJets);

	// loop jets collection and fill histograms
	int dummy = 0;
	for(const reco::BasicJet &j1 : *basicJets ){
		if( (++dummy) < 3 ) {
			edm::LogWarning("basic Jet") << j1.pt() << " " << j1.mass() << " " << j1.numberOfDaughters() ;
			for (unsigned int i = 0; i < j1.numberOfDaughters(); i++) {
				edm::LogWarning("subjet") << i << " "  << j1.daughter(i)->pt() << j1.daughter(i)->mass();
			}
		}
	}
	      	//jetsPt_ ->Fill( j1 );

	edm::Handle< reco::PFJetCollection > PFJets;
	event.getByLabel(std::string("ca8PFJetsCHS"), PFJets);
	// loop jets collection and fill histograms
	int dummy2 = 0;
	for(const reco::PFJet &j1 : *PFJets ){
		if( (++dummy2) < 3 ) {
			edm::LogWarning("PF Jet") << j1.pt() << " " << j1.mass() << " " << j1.numberOfDaughters() ;
		}
	}
	/*edm::Handle<std::vector<float> > jetsEta;
	event.getByLabel(std::string("AK4jetKinematics:AK4jetEta"), jetsEta);
	for(const float &j1 : *jetsEta ) jetsEta_ ->Fill( j1 );

	// Handle to the jets phi
	edm::Handle<std::vector<float> > jetsPhi;
	event.getByLabel(std::string("AK4jetKinematics:AK4jetPhi"), jetsPhi);
	for(const float &j1 : *jetsPhi ) jetsPhi_ ->Fill( j1 );

	edm::Handle<std::vector<int> > genStatus;
	event.getByLabel(std::string("genInfo:genstatus"), genStatus);
	for(const int &p : *genStatus ) std::cout << p << std::endl; //LogDebug("GEN") << p;*/
      }  
      // close input file
      //inFile->Close();
    }
    // break loop if maximal number of events is reached:
    // this has to be done twice to stop the file loop as well
    if(maxEvents_>0 ? ievt+1>maxEvents_ : false) break;
  }
  return 0;
}


