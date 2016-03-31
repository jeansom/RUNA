// -*- C++ -*-
//
// Package:    RUNA/RUNAnalysis
// Class:      comparisonJTB
// 
/**\class comparisonJTB comparisonJTB.cc RUNA/RUNAnalysis/plugins/comparisonJTB.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Thu, 12 Feb 2015 15:36:16 GMT
//
//


// system include files
#include <memory>

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

class comparisonJTB : public edm::EDAnalyzer {
   public:
      explicit comparisonJTB(const edm::ParameterSet&);
      ~comparisonJTB();


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

      double scale;
      edm::EDGetTokenT<std::vector<float>> jetPt_;
      edm::EDGetTokenT<std::vector<float>> jetEta_;
      edm::EDGetTokenT<std::vector<float>> jetPhi_;
      edm::EDGetTokenT<std::vector<float>> jetE_;
      edm::EDGetTokenT<std::vector<float>> jetMass_;
      edm::EDGetTokenT<std::vector<float>> jetTau1_;
      edm::EDGetTokenT<std::vector<float>> jetTau2_;
      edm::EDGetTokenT<std::vector<float>> jetTau3_;
      edm::EDGetTokenT<std::vector<float>> jetTrimmedMass_;
      edm::EDGetTokenT<std::vector<float>> jetPrunedMass_;
      edm::EDGetTokenT<std::vector<float>> jetFilteredMass_;
      edm::EDGetTokenT<std::vector<float>> jetNumberOfDaughters_;
      edm::EDGetTokenT<std::vector<float>> jetSubjetIndex0_;
      edm::EDGetTokenT<std::vector<float>> jetSubjetIndex1_;

      edm::EDGetTokenT<std::vector<float>> subjetPt_;
      edm::EDGetTokenT<std::vector<float>> subjetEta_;
      edm::EDGetTokenT<std::vector<float>> subjetPhi_;
      edm::EDGetTokenT<std::vector<float>> subjetE_;
      edm::EDGetTokenT<std::vector<float>> subjetMass_;

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
comparisonJTB::comparisonJTB(const edm::ParameterSet& iConfig):
	jetPt_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetPt"))),
	jetEta_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetEta"))),
	jetPhi_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetPhi"))),
	jetE_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetE"))),
	jetMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetMass"))),
	jetTau1_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau1"))),
	jetTau2_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau2"))),
	jetTau3_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau3"))),
	jetTrimmedMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTrimmedMass"))),
	jetPrunedMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetPrunedMass"))),
	jetFilteredMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetFilteredMass"))),
	jetNumberOfDaughters_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetNumberOfDaughters"))),
	jetSubjetIndex0_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetSubjetIndex0"))),
	jetSubjetIndex1_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetSubjetIndex1"))),
	subjetPt_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("subjetPt"))),
	subjetEta_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("subjetEta"))),
	subjetPhi_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("subjetPhi"))),
	subjetE_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("subjetE"))),
	subjetMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("subjetMass")))
{
   //now do what ever initialization is needed

}


comparisonJTB::~comparisonJTB()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
comparisonJTB::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<std::vector<float> > jetPt;
	iEvent.getByToken(jetPt_, jetPt);

	edm::Handle<std::vector<float> > jetEta;
	iEvent.getByToken(jetEta_, jetEta);

	edm::Handle<std::vector<float> > jetPhi;
	iEvent.getByToken(jetPhi_, jetPhi);

	edm::Handle<std::vector<float> > jetE;
	iEvent.getByToken(jetE_, jetE);

	edm::Handle<std::vector<float> > jetMass;
	iEvent.getByToken(jetMass_, jetMass);

	edm::Handle<std::vector<float> > jetTau1;
	iEvent.getByToken(jetTau1_, jetTau1);

	edm::Handle<std::vector<float> > jetTau2;
	iEvent.getByToken(jetTau2_, jetTau2);

	edm::Handle<std::vector<float> > jetTau3;
	iEvent.getByToken(jetTau3_, jetTau3);

	edm::Handle<std::vector<float> > jetTrimmedMass;
	iEvent.getByToken(jetTrimmedMass_, jetTrimmedMass);

	edm::Handle<std::vector<float> > jetFilteredMass;
	iEvent.getByToken(jetFilteredMass_, jetFilteredMass);

	edm::Handle<std::vector<float> > jetPrunedMass;
	iEvent.getByToken(jetPrunedMass_, jetPrunedMass);

	edm::Handle<std::vector<float> > jetNumberOfDaughters;
	iEvent.getByToken(jetNumberOfDaughters_, jetNumberOfDaughters);

	edm::Handle<std::vector<float> > jetSubjetIndex1;
	iEvent.getByToken(jetSubjetIndex1_, jetSubjetIndex1);

	edm::Handle<std::vector<float> > jetSubjetIndex0;
	iEvent.getByToken(jetSubjetIndex0_, jetSubjetIndex0);

	edm::Handle<std::vector<float> > subjetPt;
	iEvent.getByToken(subjetPt_, subjetPt);

	edm::Handle<std::vector<float> > subjetEta;
	iEvent.getByToken(subjetEta_, subjetEta);

	edm::Handle<std::vector<float> > subjetPhi;
	iEvent.getByToken(subjetPhi_, subjetPhi);

	edm::Handle<std::vector<float> > subjetE;
	iEvent.getByToken(subjetE_, subjetE);

	edm::Handle<std::vector<float> > subjetMass;
	iEvent.getByToken(subjetMass_, subjetMass);

	for (size_t i = 0; i < jetPt->size(); i++) {
		
		if ( (*jetPt)[i] < 100 ) continue;

		histos1D_[ "jetPt" ]->Fill( (*jetPt)[i] );
		histos1D_[ "jetEta" ]->Fill( (*jetEta)[i] );
		histos1D_[ "jetMass" ]->Fill( (*jetMass)[i] );
		histos1D_[ "jetTau1" ]->Fill( (*jetTau1)[i] );
		histos1D_[ "jetTau2" ]->Fill( (*jetTau2)[i] );
		histos1D_[ "jetTau3" ]->Fill( (*jetTau3)[i] );
		histos1D_[ "jetTrimmedMass" ]->Fill( (*jetTrimmedMass)[i] );
		histos1D_[ "jetPrunedMass" ]->Fill( (*jetPrunedMass)[i] );
		histos1D_[ "jetFilteredMass" ]->Fill( (*jetFilteredMass)[i] );
		histos1D_[ "jetNumberOfDaughters" ]->Fill( (*jetNumberOfDaughters)[i] );
		histos1D_[ "jetSubjetIndex1" ]->Fill( (*jetSubjetIndex1)[i] );
		histos1D_[ "jetSubjetIndex0" ]->Fill( (*jetSubjetIndex0)[i] );

		//LogWarning("subjet") << i << " " << (*jetPt)[i] << " " << (*jetNumberOfDaughters)[i] << " " << (*jetSubjetIndex0)[i] << " " << (*jetSubjetIndex1)[i] << " " << subjetPt->size();
		if( i == 0 ){

			histos1D_[ "jet1Pt" ]->Fill( (*jetPt)[0] );
			histos1D_[ "jet1Eta" ]->Fill( (*jetEta)[0] );
			histos1D_[ "jet1Mass" ]->Fill( (*jetMass)[0] );
			histos1D_[ "jet1Tau1" ]->Fill( (*jetTau1)[0] );
			histos1D_[ "jet1Tau2" ]->Fill( (*jetTau2)[0] );
			histos1D_[ "jet1Tau3" ]->Fill( (*jetTau3)[0] );
			histos1D_[ "jet1TrimmedMass" ]->Fill( (*jetTrimmedMass)[0] );
			histos1D_[ "jet1PrunedMass" ]->Fill( (*jetPrunedMass)[0] );
			histos1D_[ "jet1FilteredMass" ]->Fill( (*jetFilteredMass)[0] );
			histos1D_[ "jet1NumberOfDaughters" ]->Fill( (*jetNumberOfDaughters)[i] );
			histos1D_[ "jet1SubjetIndex1" ]->Fill( (*jetSubjetIndex1)[0] );
			histos1D_[ "jet1SubjetIndex0" ]->Fill( (*jetSubjetIndex0)[0] );
		}
	}
}


// ------------ method called once each job just before starting event loop  ------------
void 
comparisonJTB::beginJob()
{
	histos1D_[ "jetPt" ] = fs_->make< TH1D >( "jetPt", "jetPt", 100, 0., 1000. );
	histos1D_[ "jetPt" ]->Sumw2();
	histos1D_[ "jetEta" ] = fs_->make< TH1D >( "jetEta", "jetEta", 100, -5., 5. );
	histos1D_[ "jetEta" ]->Sumw2();
	histos1D_[ "jetMass" ] = fs_->make< TH1D >( "jetMass", "jetMass", 30, 0., 300. );
	histos1D_[ "jetMass" ]->Sumw2();
	histos1D_[ "jetTau1" ] = fs_->make< TH1D >( "jetTau1", "jetTau1", 20, 0., 1. );
	histos1D_[ "jetTau1" ]->Sumw2();
	histos1D_[ "jetTau2" ] = fs_->make< TH1D >( "jetTau2", "jetTau2", 20, 0., 1. );
	histos1D_[ "jetTau2" ]->Sumw2();
	histos1D_[ "jetTau3" ] = fs_->make< TH1D >( "jetTau3", "jetTau3", 20, 0., 1. );
	histos1D_[ "jetTau3" ]->Sumw2();
	histos1D_[ "jetPrunedMass" ] = fs_->make< TH1D >( "jetPrunedMass", "jetPrunedMass", 30, 0., 300. );
	histos1D_[ "jetPrunedMass" ]->Sumw2();
	histos1D_[ "jetFilteredMass" ] = fs_->make< TH1D >( "jetFilteredMass", "jetFilteredMass", 30, 0., 300. );
	histos1D_[ "jetFilteredMass" ]->Sumw2();
	histos1D_[ "jetTrimmedMass" ] = fs_->make< TH1D >( "jetTrimmedMass", "jetTrimmedMass", 30, 0., 300. );
	histos1D_[ "jetTrimmedMass" ]->Sumw2();
	histos1D_[ "jetNumberOfDaughters" ] = fs_->make< TH1D >( "jetNumberOfDaughters", "jetNumberOfDaughters", 20, 0., 20. );
	histos1D_[ "jetNumberOfDaughters" ]->Sumw2();
	histos1D_[ "jetSubjetIndex0" ] = fs_->make< TH1D >( "jetSubjetIndex0", "jetSubjetIndex0", 20, 0., 20. );
	histos1D_[ "jetSubjetIndex0" ]->Sumw2();
	histos1D_[ "jetSubjetIndex1" ] = fs_->make< TH1D >( "jetSubjetIndex1", "jetSubjetIndex1", 20, 0., 20. );
	histos1D_[ "jetSubjetIndex1" ]->Sumw2();
	histos1D_[ "jet1Pt" ] = fs_->make< TH1D >( "jet1Pt", "jet1Pt", 100, 0., 1000. );
	histos1D_[ "jet1Pt" ]->Sumw2();
	histos1D_[ "jet1Eta" ] = fs_->make< TH1D >( "jet1Eta", "jet1Eta", 100, -5., 5. );
	histos1D_[ "jet1Eta" ]->Sumw2();
	histos1D_[ "jet1Mass" ] = fs_->make< TH1D >( "jet1Mass", "jet1Mass", 30, 0., 300. );
	histos1D_[ "jet1Mass" ]->Sumw2();
	histos1D_[ "jet1Tau1" ] = fs_->make< TH1D >( "jet1Tau1", "jet1Tau1", 20, 0., 1. );
	histos1D_[ "jet1Tau1" ]->Sumw2();
	histos1D_[ "jet1Tau2" ] = fs_->make< TH1D >( "jet1Tau2", "jet1Tau2", 20, 0., 1. );
	histos1D_[ "jet1Tau2" ]->Sumw2();
	histos1D_[ "jet1Tau3" ] = fs_->make< TH1D >( "jet1Tau3", "jet1Tau3", 20, 0., 1. );
	histos1D_[ "jet1Tau3" ]->Sumw2();
	histos1D_[ "jet1PrunedMass" ] = fs_->make< TH1D >( "jet1PrunedMass", "jet1PrunedMass", 30, 0., 300. );
	histos1D_[ "jet1PrunedMass" ]->Sumw2();
	histos1D_[ "jet1FilteredMass" ] = fs_->make< TH1D >( "jet1FilteredMass", "jet1FilteredMass", 30, 0., 300. );
	histos1D_[ "jet1FilteredMass" ]->Sumw2();
	histos1D_[ "jet1TrimmedMass" ] = fs_->make< TH1D >( "jet1TrimmedMass", "jet1TrimmedMass", 30, 0., 300. );
	histos1D_[ "jet1TrimmedMass" ]->Sumw2();
	histos1D_[ "jet1NumberOfDaughters" ] = fs_->make< TH1D >( "jet1NumberOfDaughters", "jet1NumberOfDaughters", 20, 0., 20. );
	histos1D_[ "jet1NumberOfDaughters" ]->Sumw2();
	histos1D_[ "jet1SubjetIndex0" ] = fs_->make< TH1D >( "jet1SubjetIndex0", "jet1SubjetIndex0", 20, 0., 20. );
	histos1D_[ "jet1SubjetIndex0" ]->Sumw2();
	histos1D_[ "jet1SubjetIndex1" ] = fs_->make< TH1D >( "jet1SubjetIndex1", "jet1SubjetIndex1", 20, 0., 20. );
	histos1D_[ "jet1SubjetIndex1" ]->Sumw2();
}

// ------------ method called once each job just after ending the event loop  ------------
void 
comparisonJTB::endJob() 
{
}

//define this as a plug-in
DEFINE_FWK_MODULE(comparisonJTB);
