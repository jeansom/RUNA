// -*- C++ -*-
//
// Package:    RUNA/RUNAnalysis
// Class:      PUStudies
// 
/**\class PUStudies PUStudies.cc RUNA/RUNAnalysis/plugins/PUStudies.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Mon, 02 Feb 2015 02:44:59 GMT
//
//


// system include files
#include <memory>
#include <iostream>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
//
// class declaration
//
using namespace edm;
using namespace std;

typedef std::vector<pat::Jet> PatJetCollection;

class PUStudies : public edm::EDAnalyzer {
   public:
      explicit PUStudies(const edm::ParameterSet&);
      ~PUStudies();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::Service<TFileService> fs_;
      std::map< std::string, TH1D* > histos1D_;
	edm::EDGetTokenT<std::vector<pat::Jet> >     jetToken_;
	InputTag jetLabel_; 
	string jetType_, jetTYPE_, PU_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
PUStudies::PUStudies(const edm::ParameterSet& iConfig):
	jetLabel_             (iConfig.getParameter<edm::InputTag>("jetLabel"))
{
	jetType_ = iConfig.getParameter< string >("jetType");
	jetTYPE_ = iConfig.getParameter< string >("jetTYPE");
	PU_ = iConfig.getParameter< string >("PU");
}


PUStudies::~PUStudies()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
PUStudies::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<std::vector<pat::Jet> > jetHandle, packedjetHandle;
	iEvent.getByLabel(jetLabel_, jetHandle);
	auto_ptr<vector<pat::Jet> > jetColl( new vector<pat::Jet> (*jetHandle) );

	int numJets=0;
	double HT=0;

	string gromer = jetType_ + "PFJets" +  PU_ ;
	string njetiness = "Njettiness" + jetTYPE_ + PU_ ;
	string hepTop = "hepTopTagPFJets" + PU_ + "Links" + jetTYPE_ ;

	for (const pat::Jet & ijet : *jetHandle) {

		if( ( ijet.pt() > 100. ) && ( TMath::Abs( ijet.eta() ) < 2.5 ) ){
			histos1D_[ "jetsPt" ]->Fill( ijet.pt() );
			histos1D_[ "jetsEta" ]->Fill( ijet.eta() );
			histos1D_[ "jetsMass" ]->Fill( ijet.mass() );
			histos1D_[ "jetsFilteredMass" ]->Fill( ijet.userFloat( gromer + "FilteredLinks") );
			histos1D_[ "jetsPrunedMass" ]->Fill( ijet.userFloat( gromer + "PrunedLinks") );
			histos1D_[ "jetsTrimmedMass" ]->Fill( ijet.userFloat( gromer + "TrimmedLinks") );
			histos1D_[ "jetsSoftDropMass" ]->Fill( ijet.userFloat( gromer + "SoftDropLinks") );
			histos1D_[ "jetsMassDropFilteredMass" ]->Fill( ijet.userFloat( gromer + "MassDropFilteredLinks") );
			histos1D_[ "jetsHEPTopTagMass" ]->Fill( ijet.userFloat( hepTop ));
			histos1D_[ "jetsTau1" ]->Fill( ijet.userFloat( njetiness + ":tau1") );
			histos1D_[ "jetsTau2" ]->Fill( ijet.userFloat( njetiness + ":tau2") );
			histos1D_[ "jetsTau3" ]->Fill( ijet.userFloat( njetiness + ":tau3") );
			HT+=ijet.pt();
			
			//LogWarning("test") << ijet.bDiscriminator("jetProbabilityBJetTags") ;

			if( (numJets++) == 1 ){
				histos1D_[ "jet1Pt" ]->Fill( ijet.pt() );
				histos1D_[ "jet1Mass" ]->Fill( ijet.mass() );
				histos1D_[ "jet1FilteredMass" ]->Fill( ijet.userFloat( gromer + "FilteredLinks") );
				histos1D_[ "jet1PrunedMass" ]->Fill( ijet.userFloat( gromer + "PrunedLinks") );
				histos1D_[ "jet1TrimmedMass" ]->Fill( ijet.userFloat( gromer + "TrimmedLinks") );
				histos1D_[ "jet1SoftDropMass" ]->Fill( ijet.userFloat( gromer + "SoftDropLinks") );
				histos1D_[ "jet1MassDropFilteredMass" ]->Fill( ijet.userFloat( gromer + "MassDropFilteredLinks") );
				histos1D_[ "jet1HEPTopTagMass" ]->Fill( ijet.userFloat( hepTop ));
				histos1D_[ "jet1Tau1" ]->Fill( ijet.userFloat( njetiness + ":tau1") );
				histos1D_[ "jet1Tau2" ]->Fill( ijet.userFloat( njetiness + ":tau2") );
				histos1D_[ "jet1Tau3" ]->Fill( ijet.userFloat( njetiness + ":tau3") );
			}
		}
	}
	histos1D_[ "jetsNum" ]->Fill( numJets );
	if( HT > 0 ) histos1D_[ "HT" ]->Fill( HT );





}


// ------------ method called once each job just before starting event loop  ------------
void 
PUStudies::beginJob()
{
	histos1D_[ "jetsPt" ] = fs_->make< TH1D >( "jetsPt", "jetsPt", 100, 0., 1000. );
	histos1D_[ "jetsPt" ]->Sumw2();
	histos1D_[ "jetsEta" ] = fs_->make< TH1D >( "jetsEta", "jetsEta", 100, -5., 5. );
	histos1D_[ "jetsEta" ]->Sumw2();
	histos1D_[ "jetsNum" ] = fs_->make< TH1D >( "jetsNum", "jetsNum", 10, 0., 10. );
	histos1D_[ "jetsNum" ]->Sumw2();
	histos1D_[ "jetsMass" ] = fs_->make< TH1D >( "jetsMass", "jetsMass", 30, 0., 300. );
	histos1D_[ "jetsMass" ]->Sumw2();
	histos1D_[ "jetsPrunedMass" ] = fs_->make< TH1D >( "jetsPrunedMass", "jetsPrunedMass", 30, 0., 300. );
	histos1D_[ "jetsPrunedMass" ]->Sumw2();
	histos1D_[ "jetsFilteredMass" ] = fs_->make< TH1D >( "jetsFilteredMass", "jetsFilteredMass", 30, 0., 300. );
	histos1D_[ "jetsFilteredMass" ]->Sumw2();
	histos1D_[ "jetsTrimmedMass" ] = fs_->make< TH1D >( "jetsTrimmedMass", "jetsTrimmedMass", 30, 0., 300. );
	histos1D_[ "jetsTrimmedMass" ]->Sumw2();
	histos1D_[ "jetsMassDropFilteredMass" ] = fs_->make< TH1D >( "jetsMassDropFilteredMass", "jetsMassDropFilteredMass", 30, 0., 300. );
	histos1D_[ "jetsMassDropFilteredMass" ]->Sumw2();
	histos1D_[ "jetsSoftDropMass" ] = fs_->make< TH1D >( "jetsSoftDropMass", "jetsSoftDropMass", 30, 0., 300. );
	histos1D_[ "jetsSoftDropMass" ]->Sumw2();
	histos1D_[ "jetsHEPTopTagMass" ] = fs_->make< TH1D >( "jetsHEPTopTagMass", "jetsHEPTopTagMass", 30, 0., 300. );
	histos1D_[ "jetsHEPTopTagMass" ]->Sumw2();
	histos1D_[ "jetsTau1" ] = fs_->make< TH1D >( "jetsTau1", "jetsTau1", 20, 0., 1. );
	histos1D_[ "jetsTau1" ]->Sumw2();
	histos1D_[ "jetsTau2" ] = fs_->make< TH1D >( "jetsTau2", "jetsTau2", 20, 0., 1. );
	histos1D_[ "jetsTau2" ]->Sumw2();
	histos1D_[ "jetsTau3" ] = fs_->make< TH1D >( "jetsTau3", "jetsTau3", 20, 0., 1. );
	histos1D_[ "jetsTau3" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 150, 0., 1500. );
	histos1D_[ "HT" ]->Sumw2();
	histos1D_[ "jet1Pt" ] = fs_->make< TH1D >( "jet1Pt", "jet1Pt", 100, 0., 1000. );
	histos1D_[ "jet1Pt" ]->Sumw2();
	histos1D_[ "jet1Mass" ] = fs_->make< TH1D >( "jet1Mass", "jet1Mass", 30, 0., 300. );
	histos1D_[ "jet1Mass" ]->Sumw2();
	histos1D_[ "jet1PrunedMass" ] = fs_->make< TH1D >( "jet1PrunedMass", "jet1PrunedMass", 30, 0., 300. );
	histos1D_[ "jet1PrunedMass" ]->Sumw2();
	histos1D_[ "jet1FilteredMass" ] = fs_->make< TH1D >( "jet1FilteredMass", "jet1FilteredMass", 30, 0., 300. );
	histos1D_[ "jet1FilteredMass" ]->Sumw2();
	histos1D_[ "jet1TrimmedMass" ] = fs_->make< TH1D >( "jet1TrimmedMass", "jet1TrimmedMass", 30, 0., 300. );
	histos1D_[ "jet1TrimmedMass" ]->Sumw2();
	histos1D_[ "jet1MassDropFilteredMass" ] = fs_->make< TH1D >( "jet1MassDropFilteredMass", "jet1MassDropFilteredMass", 30, 0., 300. );
	histos1D_[ "jet1MassDropFilteredMass" ]->Sumw2();
	histos1D_[ "jet1SoftDropMass" ] = fs_->make< TH1D >( "jet1SoftDropMass", "jet1SoftDropMass", 30, 0., 300. );
	histos1D_[ "jet1SoftDropMass" ]->Sumw2();
	histos1D_[ "jet1HEPTopTagMass" ] = fs_->make< TH1D >( "jet1HEPTopTagMass", "jet1HEPTopTagMass", 30, 0., 300. );
	histos1D_[ "jet1HEPTopTagMass" ]->Sumw2();
	histos1D_[ "jet1Tau1" ] = fs_->make< TH1D >( "jet1Tau1", "jet1Tau1", 20, 0., 1. );
	histos1D_[ "jet1Tau1" ]->Sumw2();
	histos1D_[ "jet1Tau2" ] = fs_->make< TH1D >( "jet1Tau2", "jet1Tau2", 20, 0., 1. );
	histos1D_[ "jet1Tau2" ]->Sumw2();
	histos1D_[ "jet1Tau3" ] = fs_->make< TH1D >( "jet1Tau3", "jet1Tau3", 20, 0., 1. );
	histos1D_[ "jet1Tau3" ]->Sumw2();
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PUStudies::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
PUStudies::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
PUStudies::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
PUStudies::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
PUStudies::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PUStudies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PUStudies);
