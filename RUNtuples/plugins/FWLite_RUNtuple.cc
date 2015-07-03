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
//#include "DataFormats/JetsReco/interface/Jets.h"
//#include "DataFormats/PatCandidates/interface/Jets.h"
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
  parser.integerValue ("maxEvents"  ) = 1000;
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
  TFileDirectory dir = fs.mkdir("analyzePatJets");
  TH1F* jetsPt_  = dir.make<TH1F>("jetsPt"  , "pt"  ,   100,   0., 300.);
  TH1F* jetsEta_ = dir.make<TH1F>("jetsEta" , "eta" ,   100,  -3.,   3.);
  TH1F* jetsPhi_ = dir.make<TH1F>("jetsPhi" , "phi" ,   100,  -5.,   5.);  

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
	edm::Handle<std::vector<float> > jetsPt;
	event.getByLabel(std::string("jetsAK4:jetAK4Pt"), jetsPt);
	// loop jets collection and fill histograms
	for(const float &j1 : *jetsPt )  jetsPt_ ->Fill( j1 );

	edm::Handle<std::vector<float> > jetsEta;
	event.getByLabel(std::string("jetsAK4:jetAK4Eta"), jetsEta);
	for(const float &j1 : *jetsEta ) jetsEta_ ->Fill( j1 );

	// Handle to the jets phi
	edm::Handle<std::vector<float> > jetsPhi;
	event.getByLabel(std::string("jetsAK4:jetAK4Phi"), jetsPhi);
	for(const float &j1 : *jetsPhi ) jetsPhi_ ->Fill( j1 );

	/*
	edm::Handle<std::vector<int> > genStatus;
	event.getByLabel(std::string("genInfo:genstatus"), genStatus);
	for(const int &p : *genStatus ) std::cout << p << std::endl; //LogDebug("GEN") << p;
	*/

	edm::Handle<std::vector<std::string> > triggerNames;
	event.getByLabel(std::string("TriggerUserData:triggerNameTree"), triggerNames);
	// loop jets collection and fill histograms
	for(const std::string &j1 : *triggerNames )  std::cout << j1 << std::endl;

	edm::Handle<std::vector<float> > triggerBit;
	event.getByLabel(std::string("TriggerUserData:triggerBitTree"), triggerBit);
	// loop jets collection and fill histograms
	for(const float &j1 : *triggerBit )  std::cout << j1 << std::endl;
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


