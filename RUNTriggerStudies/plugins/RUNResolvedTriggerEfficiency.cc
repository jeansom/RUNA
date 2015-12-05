// -*- C++ -*-
//
// Package:    RUNA/Ntuples
// Class:      RUNResolvedTriggerEfficiency
// 
/**\class RUNResolvedTriggerEfficiency RUNResolvedTriggerEfficiency.cc Ntuples/Ntuples/plugins/RUNResolvedTriggerEfficiency.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Tue, 14 Oct 2014 23:13:13 GMT
//
//


// system include files
#include <memory>
#include <vector>
#include <TLorentzVector.h>
#include <TH2.h>
#include <TTree.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNResolvedTriggerEfficiency : public EDAnalyzer {
   public:
      explicit RUNResolvedTriggerEfficiency(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
      ~RUNResolvedTriggerEfficiency();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(Run const&, EventSetup const&) override;
      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;

      bool bjSample;
      TString baseTrigger;
      double cutjetPtvalue;
      vector<string> triggerPass;

      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;

      EDGetTokenT<vector<float>> jetPt_;
      EDGetTokenT<vector<float>> jetEta_;
      EDGetTokenT<vector<float>> jetPhi_;
      EDGetTokenT<vector<float>> jetE_;
      EDGetTokenT<vector<float>> jetMass_;
      EDGetTokenT<vector<float>> jetCSV_;
      EDGetTokenT<vector<float>> jetCSVV1_;
      EDGetTokenT<int> NPV_;
      EDGetTokenT<unsigned int> lumi_;
      EDGetTokenT<unsigned int> run_;
      EDGetTokenT<ULong64_t> event_;

      // Trigger
      EDGetTokenT<vector<float>> triggerBit_;
      EDGetTokenT<vector<string>> triggerName_;

      //Jet ID
      EDGetTokenT<vector<float>> jecFactor_;
      EDGetTokenT<vector<float>> neutralHadronEnergy_;
      EDGetTokenT<vector<float>> neutralEmEnergy_;
      EDGetTokenT<vector<float>> chargedHadronEnergy_;
      EDGetTokenT<vector<float>> chargedEmEnergy_;
      EDGetTokenT<vector<float>> chargedHadronMultiplicity_;
      EDGetTokenT<vector<float>> neutralHadronMultiplicity_;
      EDGetTokenT<vector<float>> chargedMultiplicity_;
      EDGetTokenT<vector<float>> muonEnergy_; 


};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNResolvedTriggerEfficiency::RUNResolvedTriggerEfficiency(const ParameterSet& iConfig):
	jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPt"))),
	jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetEta"))),
	jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPhi"))),
	jetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetE"))),
	jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
	jetCSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSV"))),
	jetCSVV1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVV1"))),
	NPV_(consumes<int>(iConfig.getParameter<InputTag>("NPV"))),
	lumi_(consumes<unsigned int>(iConfig.getParameter<InputTag>("Lumi"))),
	run_(consumes<unsigned int>(iConfig.getParameter<InputTag>("Run"))),
	event_(consumes<ULong64_t>(iConfig.getParameter<InputTag>("Event"))),
	// Trigger
	triggerBit_(consumes<vector<float>>(iConfig.getParameter<InputTag>("triggerBit"))),
	triggerName_(consumes<vector<string>>(iConfig.getParameter<InputTag>("triggerName"))),
	//Jet ID,
	jecFactor_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jecFactor"))),
	neutralHadronEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralHadronEnergy"))),
	neutralEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralEmEnergy"))),
	chargedHadronEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedHadronEnergy"))),
	chargedEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedEmEnergy"))),
	chargedHadronMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedHadronMultiplicity"))),
	neutralHadronMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralHadronMultiplicity"))),
	chargedMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedMultiplicity"))),
	muonEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("muonEnergy")))
{
	bjSample = iConfig.getParameter<bool>("bjSample");
	baseTrigger = iConfig.getParameter<string>("baseTrigger");
	cutjetPtvalue = iConfig.getParameter<double>("cutjetPtvalue");
	triggerPass = iConfig.getParameter<vector<string>>("triggerPass");
}


RUNResolvedTriggerEfficiency::~RUNResolvedTriggerEfficiency()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNResolvedTriggerEfficiency::analyze(const Event& iEvent, const EventSetup& iSetup) {

	Handle<vector<float> > jetPt;
	iEvent.getByToken(jetPt_, jetPt);

	Handle<vector<float> > jetEta;
	iEvent.getByToken(jetEta_, jetEta);

	Handle<vector<float> > jetPhi;
	iEvent.getByToken(jetPhi_, jetPhi);

	Handle<vector<float> > jetE;
	iEvent.getByToken(jetE_, jetE);

	Handle<vector<float> > jetMass;
	iEvent.getByToken(jetMass_, jetMass);

	Handle<vector<float> > jetCSV;
	iEvent.getByToken(jetCSV_, jetCSV);

	Handle<vector<float> > jetCSVV1;
	iEvent.getByToken(jetCSVV1_, jetCSVV1);

	Handle<int> NPV;
	iEvent.getByToken(NPV_, NPV);

	Handle<unsigned int> Lumi;
	iEvent.getByToken(lumi_, Lumi);

	Handle<unsigned int> Run;
	iEvent.getByToken(run_, Run);

	Handle<ULong64_t> ievent;
	iEvent.getByToken(event_, ievent);

	/// Trigger
	Handle<vector<float> > triggerBit;
	iEvent.getByToken(triggerBit_, triggerBit);

	Handle<vector<string> > triggerName;
	iEvent.getByToken(triggerName_, triggerName);

	/// Jet ID
	Handle<vector<float> > jecFactor;
	iEvent.getByToken(jecFactor_, jecFactor);

	Handle<vector<float> > neutralHadronEnergy;
	iEvent.getByToken(neutralHadronEnergy_, neutralHadronEnergy);

	Handle<vector<float> > neutralEmEnergy;
	iEvent.getByToken(neutralEmEnergy_, neutralEmEnergy);

	Handle<vector<float> > chargedHadronEnergy;
	iEvent.getByToken(chargedHadronEnergy_, chargedHadronEnergy);

	Handle<vector<float> > chargedEmEnergy;
	iEvent.getByToken(chargedEmEnergy_, chargedEmEnergy);

	Handle<vector<float> > chargedHadronMultiplicity;
	iEvent.getByToken(chargedHadronMultiplicity_, chargedHadronMultiplicity);

	Handle<vector<float> > neutralHadronMultiplicity;
	iEvent.getByToken(neutralHadronMultiplicity_, neutralHadronMultiplicity);

	Handle<vector<float> > chargedMultiplicity;
	iEvent.getByToken(chargedMultiplicity_, chargedMultiplicity);

	Handle<vector<float> > muonEnergy;
	iEvent.getByToken(muonEnergy_, muonEnergy);


	bool basedTriggerFired = checkTriggerBits( triggerName, triggerBit, baseTrigger  );
	bool ORTriggers = checkORListOfTriggerBits( triggerName, triggerBit, triggerPass );

	/// Applying kinematic, trigger and jet ID
	vector< TLorentzVector > JETS;
	//bool bTagCSV = 0;
	float HT = 0;

	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		bool idL = jetID( (*jetEta)[i], (*jetE)[i], (*jecFactor)[i], (*neutralHadronEnergy)[i], (*neutralEmEnergy)[i], (*chargedHadronEnergy)[i], (*muonEnergy)[i], (*chargedEmEnergy)[i], (*chargedHadronMultiplicity)[i], (*neutralHadronMultiplicity)[i], (*chargedMultiplicity)[i] ); 

		if( (*jetPt)[i] > 50  && idL ) { 
			//LogWarning("jetInfo") << i << " " << (*jetPt)[i] << " " << (*jetEta)[i] << " " << (*jetPhi)[i] << " " << (*jetMass)[i];

			HT += (*jetPt)[i];
			++numJets;

			TLorentzVector tmpJet;
			tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

			//if ( (*jetCSV)[i] > 0.244 ) bTagCSV = 1; 	// CSVL
			//if ( (*jetCSV)[i] > 0.679 ) bTagCSV = 1; 	// CSVM
			//if ( (*jetCSVV1)[i] > 0.405 ) bTagCSV = 1; 	// CSVV1L
			//if ( (*jetCSVV1)[i] > 0.783 ) bTagCSV = 1; 	// CSVV1M

			//JETtype tmpJET;
			//tmpJET.p4 = tmpJet;
			//tmpJET.mass = (*jetMass)[i];
			//tmpJET.btagCSV = bTagCSV;
			JETS.push_back( tmpJet );
	   
		}
	}


	if ( JETS.size() > 3 ) {

		if ( basedTriggerFired ) {
			histos1D_[ "jet1PtDenom_cut4Jet" ]->Fill( JETS[0].Pt() );
			histos1D_[ "jet2PtDenom_cut4Jet" ]->Fill( JETS[1].Pt() );
			histos1D_[ "jet3PtDenom_cut4Jet" ]->Fill( JETS[2].Pt() );
			histos1D_[ "jet4PtDenom_cut4Jet" ]->Fill( JETS[3].Pt() );
			histos1D_[ "HTDenom_cut4Jet" ]->Fill( HT  );
			histos2D_[ "jet4PtHTDenom_cut4Jet" ]->Fill( JETS[3].Pt(), HT );

			if ( ORTriggers ){
				histos1D_[ "jet1PtPassing_cut4Jet" ]->Fill( JETS[0].Pt() );
				histos1D_[ "jet2PtPassing_cut4Jet" ]->Fill( JETS[1].Pt() );
				histos1D_[ "jet3PtPassing_cut4Jet" ]->Fill( JETS[2].Pt() );
				histos1D_[ "jet4PtPassing_cut4Jet" ]->Fill( JETS[3].Pt() );
				histos1D_[ "HTPassing_cut4Jet" ]->Fill( HT  );
				histos2D_[ "jet4PtHTPassing_cut4Jet" ]->Fill( JETS[3].Pt(), HT );
			}

			if ( JETS[3].Pt() > cutjetPtvalue ) {
				histos1D_[ "jet1PtDenom_cut4JetPt" ]->Fill( JETS[0].Pt() );
				histos1D_[ "jet2PtDenom_cut4JetPt" ]->Fill( JETS[1].Pt() );
				histos1D_[ "jet3PtDenom_cut4JetPt" ]->Fill( JETS[2].Pt() );
				histos1D_[ "jet4PtDenom_cut4JetPt" ]->Fill( JETS[3].Pt() );
				histos1D_[ "HTDenom_cut4JetPt" ]->Fill( HT  );
				histos2D_[ "jet4PtHTDenom_cut4JetPt" ]->Fill( JETS[3].Pt(), HT );

				if ( ORTriggers ){
					histos1D_[ "jet1PtPassing_cut4JetPt" ]->Fill( JETS[0].Pt() );
					histos1D_[ "jet2PtPassing_cut4JetPt" ]->Fill( JETS[1].Pt() );
					histos1D_[ "jet3PtPassing_cut4JetPt" ]->Fill( JETS[2].Pt() );
					histos1D_[ "jet4PtPassing_cut4JetPt" ]->Fill( JETS[3].Pt() );
					histos1D_[ "HTPassing_cut4JetPt" ]->Fill( HT  );
					histos2D_[ "jet4PtHTPassing_cut4JetPt" ]->Fill( JETS[3].Pt(), HT );
				}
			}
		}
	}
	JETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNResolvedTriggerEfficiency::beginJob() {

	histos1D_[ "HTDenom_cut4Jet" ] = fs_->make< TH1D >( "HTDenom_cut4Jet", "HTDenom_cut4Jet", 300, 0., 3000. );
	histos1D_[ "HTDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "HTPassing_cut4Jet" ] = fs_->make< TH1D >( "HTPassing_cut4Jet", "HTPassing_cut4Jet", 300, 0., 3000. );
	histos1D_[ "HTPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet1PtDenom_cut4Jet", "jet1PtDenom_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet1PtPassing_cut4Jet", "jet1PtPassing_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet2PtDenom_cut4Jet", "jet2PtDenom_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet2PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet2PtPassing_cut4Jet", "jet2PtPassing_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet2PtPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet3PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet3PtDenom_cut4Jet", "jet3PtDenom_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet3PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet3PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet3PtPassing_cut4Jet", "jet3PtPassing_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet3PtPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet4PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet4PtDenom_cut4Jet", "jet4PtDenom_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet4PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet4PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet4PtPassing_cut4Jet", "jet4PtPassing_cut4Jet", 100, 0., 1000. );
	histos1D_[ "jet4PtPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "HTDenom_cut4JetPt" ] = fs_->make< TH1D >( "HTDenom_cut4JetPt", "HTDenom_cut4JetPt", 300, 0., 3000. );
	histos1D_[ "HTDenom_cut4JetPt" ]->Sumw2();
	histos1D_[ "HTPassing_cut4JetPt" ] = fs_->make< TH1D >( "HTPassing_cut4JetPt", "HTPassing_cut4JetPt", 300, 0., 3000. );
	histos1D_[ "HTPassing_cut4JetPt" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cut4JetPt" ] = fs_->make< TH1D >( "jet1PtDenom_cut4JetPt", "jet1PtDenom_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cut4JetPt" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cut4JetPt" ] = fs_->make< TH1D >( "jet1PtPassing_cut4JetPt", "jet1PtPassing_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cut4JetPt" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cut4JetPt" ] = fs_->make< TH1D >( "jet2PtDenom_cut4JetPt", "jet2PtDenom_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet2PtDenom_cut4JetPt" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cut4JetPt" ] = fs_->make< TH1D >( "jet2PtPassing_cut4JetPt", "jet2PtPassing_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet2PtPassing_cut4JetPt" ]->Sumw2();

	histos1D_[ "jet3PtDenom_cut4JetPt" ] = fs_->make< TH1D >( "jet3PtDenom_cut4JetPt", "jet3PtDenom_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet3PtDenom_cut4JetPt" ]->Sumw2();
	histos1D_[ "jet3PtPassing_cut4JetPt" ] = fs_->make< TH1D >( "jet3PtPassing_cut4JetPt", "jet3PtPassing_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet3PtPassing_cut4JetPt" ]->Sumw2();

	histos1D_[ "jet4PtDenom_cut4JetPt" ] = fs_->make< TH1D >( "jet4PtDenom_cut4JetPt", "jet4PtDenom_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet4PtDenom_cut4JetPt" ]->Sumw2();
	histos1D_[ "jet4PtPassing_cut4JetPt" ] = fs_->make< TH1D >( "jet4PtPassing_cut4JetPt", "jet4PtPassing_cut4JetPt", 100, 0., 1000. );
	histos1D_[ "jet4PtPassing_cut4JetPt" ]->Sumw2();

	histos2D_[ "jet4PtHTDenom_cut4Jet" ] = fs_->make< TH2D >( "jet4PtHTDenom_cut4Jet", "HT vs 4th Leading Jet Pt", 100, 0., 1000., 300, 0., 3000.);
	histos2D_[ "jet4PtHTDenom_cut4Jet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet4PtHTDenom_cut4Jet" ]->SetXTitle( "4th Leading Jet p_{T} [Ge]" );
	histos2D_[ "jet4PtHTDenom_cut4Jet" ]->Sumw2();

	histos2D_[ "jet4PtHTPassing_cut4Jet" ] = fs_->make< TH2D >( "jet4PtHTPassing_cut4Jet", "HT vs 4th Leading Jet Pt", 100, 0., 1000., 300, 0., 3000.);
	histos2D_[ "jet4PtHTPassing_cut4Jet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet4PtHTPassing_cut4Jet" ]->SetXTitle( "4th Leading Jet p_{T} [GeV]" );
	histos2D_[ "jet4PtHTPassing_cut4Jet" ]->Sumw2();

	histos2D_[ "jet4PtHTDenom_cut4JetPt" ] = fs_->make< TH2D >( "jet4PtHTDenom_cut4JetPt", "HT vs 4th Leading Jet Pt", 100, 0., 1000., 300, 0., 3000.);
	histos2D_[ "jet4PtHTDenom_cut4JetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet4PtHTDenom_cut4JetPt" ]->SetXTitle( "4th Leading Jet p_{T} [Ge]" );
	histos2D_[ "jet4PtHTDenom_cut4JetPt" ]->Sumw2();

	histos2D_[ "jet4PtHTPassing_cut4JetPt" ] = fs_->make< TH2D >( "jet4PtHTPassing_cut4JetPt", "HT vs 4th Leading Jet Pt", 100, 0., 1000., 300, 0., 3000.);
	histos2D_[ "jet4PtHTPassing_cut4JetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet4PtHTPassing_cut4JetPt" ]->SetXTitle( "4th Leading Jet p_{T} [GeV]" );
	histos2D_[ "jet4PtHTPassing_cut4JetPt" ]->Sumw2();


}

// ------------ method called once each job just after ending the event loop  ------------
void RUNResolvedTriggerEfficiency::endJob() {

}

void RUNResolvedTriggerEfficiency::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutjetPtvalue", 1);
	desc.add<bool>("bjSample", false);
	desc.add<string>("baseTrigger", "HLT_PFHT475");
	vector<string> HLTPass;
	HLTPass.push_back("HLT_PFHT800");
	desc.add<vector<string>>("triggerPass",	HLTPass);

	desc.add<InputTag>("Lumi", 	InputTag("eventInfo:evtInfoLumiBlock"));
	desc.add<InputTag>("Run", 	InputTag("eventInfo:evtInfoRunNumber"));
	desc.add<InputTag>("Event", 	InputTag("eventInfo:evtInfoEventNumber"));
	desc.add<InputTag>("NPV", 	InputTag("eventUserData:npv"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK4:jetAK4Pt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK4:jetAK4Eta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK4:jetAK4Phi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK4:jetAK4E"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK4:jetAK4Mass"));
	desc.add<InputTag>("jetCSV", 	InputTag("jetsAK4:jetAK4CSV"));
	desc.add<InputTag>("jetCSVV1", 	InputTag("jetsAK4:jetAK4CSVV1"));
	// JetID
	desc.add<InputTag>("jecFactor", 		InputTag("jetsAK4:jetAK4jecFactor0"));
	desc.add<InputTag>("neutralHadronEnergy", 	InputTag("jetsAK4:jetAK4neutralHadronEnergy"));
	desc.add<InputTag>("neutralEmEnergy", 		InputTag("jetsAK4:jetAK4neutralEmEnergy"));
	desc.add<InputTag>("chargedEmEnergy", 		InputTag("jetsAK4:jetAK4chargedEmEnergy"));
	desc.add<InputTag>("muonEnergy", 		InputTag("jetsAK4:jetAK4MuonEnergy"));
	desc.add<InputTag>("chargedHadronEnergy", 	InputTag("jetsAK4:jetAK4chargedHadronEnergy"));
	desc.add<InputTag>("chargedHadronMultiplicity",	InputTag("jetsAK4:jetAK4ChargedHadronMultiplicity"));
	desc.add<InputTag>("neutralHadronMultiplicity",	InputTag("jetsAK4:jetAK4neutralHadronMultiplicity"));
	desc.add<InputTag>("chargedMultiplicity", 	InputTag("jetsAK4:jetAK4chargedMultiplicity"));
	// Trigger
	desc.add<InputTag>("triggerBit",		InputTag("TriggerUserData:triggerBitTree"));
	desc.add<InputTag>("triggerName",		InputTag("TriggerUserData:triggerNameTree"));
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNResolvedTriggerEfficiency);
