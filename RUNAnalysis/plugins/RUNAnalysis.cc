// -*- C++ -*-
//
// Package:    Ntuples/Ntuples
// Class:      RUNAnalysis
// 
/**\class RUNAnalysis RUNAnalysis.cc Ntuples/Ntuples/plugins/RUNAnalysis.cc

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

#include "FWCore/Framework/interface/GetterOfProducts.h"
#include "FWCore/Framework/interface/ProcessMatch.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//
typedef struct Jet_struc {
	TLorentzVector p4;
	TLorentzVector subjet0;
	TLorentzVector subjet1;
	double mass;
	double tau1;
	double tau2;
	double tau3;
} JETtype;
//
// class declaration
//
class RUNAnalysis : public EDAnalyzer {
   public:
      explicit RUNAnalysis(const ParameterSet&);
      ~RUNAnalysis();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(Run const&, EventSetup const&) override;
      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      //GetterOfProducts< vector<float> > getterOfProducts_;
      //EDGetTokenT<TriggerResults> triggerBits_;
      Service<TFileService> fs_;
      map< string, TH1D* > histos1D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      double scale;
      EDGetTokenT<vector<float>> jetPt_;
      EDGetTokenT<vector<float>> jetEta_;
      EDGetTokenT<vector<float>> jetPhi_;
      EDGetTokenT<vector<float>> jetE_;
      EDGetTokenT<vector<float>> jetMass_;
      EDGetTokenT<vector<float>> jetTau1_;
      EDGetTokenT<vector<float>> jetTau2_;
      EDGetTokenT<vector<float>> jetTau3_;
      EDGetTokenT<vector<float>> jetNSubjets_;
      EDGetTokenT<vector<float>> jetSubjetIndex0_;
      EDGetTokenT<vector<float>> jetSubjetIndex1_;
      EDGetTokenT<vector<float>> jetSubjetIndex2_;
      EDGetTokenT<vector<float>> jetSubjetIndex3_;
      EDGetTokenT<vector<vector<int>>> jetKeys_;

      //Jet ID
      EDGetTokenT<vector<float>> jecFactor_;
      EDGetTokenT<vector<float>> neutralHadronEnergy_;
      EDGetTokenT<vector<float>> neutralEmEnergy_;
      EDGetTokenT<vector<float>> chargeEmEnergy_;
      EDGetTokenT<vector<float>> muonEnergy_; 

      // Subjets
      EDGetTokenT<vector<float>> subjetPt_;
      EDGetTokenT<vector<float>> subjetEta_;
      EDGetTokenT<vector<float>> subjetPhi_;
      EDGetTokenT<vector<float>> subjetE_;
      EDGetTokenT<vector<float>> subjetMass_;

};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNAnalysis::RUNAnalysis(const ParameterSet& iConfig):
//	getterOfProducts_(ProcessMatch(*), this) {
//	triggerBits_(consumes<TriggerResults>(iConfig.getParameter<InputTag>("bits"))),
	jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPt"))),
	jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetEta"))),
	jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPhi"))),
	jetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetE"))),
	jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
	jetTau1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau1"))),
	jetTau2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau2"))),
	jetTau3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau3"))),
	jetNSubjets_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetNSubjets"))),
	jetSubjetIndex0_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex0"))),
	jetSubjetIndex1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex1"))),
	jetSubjetIndex2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex2"))),
	jetSubjetIndex3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex3"))),
	jetKeys_(consumes<vector<vector<int>>>(iConfig.getParameter<InputTag>("jetKeys"))),
	//Jet ID,
	jecFactor_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jecFactor"))),
	neutralHadronEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralHadronEnergy"))),
	neutralEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralEmEnergy"))),
	chargeEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargeEmEnergy"))),
	muonEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("muonEnergy"))),
	// Subjets
	subjetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetPt"))),
	subjetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetEta"))),
	subjetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetPhi"))),
	subjetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetE"))),
	subjetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetMass")))
{
	scale = iConfig.getParameter<double>("scale");
}


RUNAnalysis::~RUNAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNAnalysis::analyze(const Event& iEvent, const EventSetup& iSetup) {


	/*vector<Handle< vector<float> > > handles;
	getterOfProducts_.fillHandles(event, handles);
	*/

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

	Handle<vector<float> > jetTau1;
	iEvent.getByToken(jetTau1_, jetTau1);

	Handle<vector<float> > jetTau2;
	iEvent.getByToken(jetTau2_, jetTau2);

	Handle<vector<float> > jetTau3;
	iEvent.getByToken(jetTau3_, jetTau3);

	Handle<vector<float> > jetNSubjets;
	iEvent.getByToken(jetNSubjets_, jetNSubjets);

	Handle<vector<float> > jetSubjetIndex0;
	iEvent.getByToken(jetSubjetIndex0_, jetSubjetIndex0);

	Handle<vector<float> > jetSubjetIndex1;
	iEvent.getByToken(jetSubjetIndex1_, jetSubjetIndex1);

	Handle<vector<float> > jetSubjetIndex2;
	iEvent.getByToken(jetSubjetIndex2_, jetSubjetIndex2);

	Handle<vector<float> > jetSubjetIndex3;
	iEvent.getByToken(jetSubjetIndex3_, jetSubjetIndex3);

	Handle<vector<vector<int> > > jetKeys;
	iEvent.getByToken(jetKeys_, jetKeys);

	/// Jet ID
	Handle<vector<float> > jecFactor;
	iEvent.getByToken(jecFactor_, jecFactor);

	Handle<vector<float> > neutralHadronEnergy;
	iEvent.getByToken(neutralHadronEnergy_, neutralHadronEnergy);

	Handle<vector<float> > neutralEmEnergy;
	iEvent.getByToken(neutralEmEnergy_, neutralEmEnergy);

	Handle<vector<float> > chargeEmEnergy;
	iEvent.getByToken(chargeEmEnergy_, chargeEmEnergy);

	Handle<vector<float> > muonEnergy;
	iEvent.getByToken(muonEnergy_, muonEnergy);

	/// Subjets
	Handle<vector<float> > subjetPt;
	iEvent.getByToken(subjetPt_, subjetPt);

	Handle<vector<float> > subjetEta;
	iEvent.getByToken(subjetEta_, subjetEta);

	Handle<vector<float> > subjetPhi;
	iEvent.getByToken(subjetPhi_, subjetPhi);

	Handle<vector<float> > subjetE;
	iEvent.getByToken(subjetE_, subjetE);

	Handle<vector<float> > subjetMass;
	iEvent.getByToken(subjetMass_, subjetMass);

	//for (size_t i = 0; i < jetKeys->size(); i++) {
	/*
	for ( const vector<int> &keys : *jetKeys ) {
		for ( const int &tmp : keys) {
		//for (size_t j = 0; j < keys.size(); j++) {
			LogWarning("jetKeys") <<  tmp ;
		}
	}*/

	cutmap["Processed"] += 1;

	vector< JETtype > JETS;
	int numJets = 0;
	double HT = 0;
	bool cutHT = 0;
	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		double jec = 1. / ( (*jecFactor)[i] * (*jetE)[i] );
		double nhf = (*neutralHadronEnergy)[i] * jec;
		double nEMf = (*neutralEmEnergy)[i] * jec;
		double cEMf = (*chargeEmEnergy)[i] * jec;
		double muf = (*muonEnergy)[i] * jec;
		//int npr = (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i] ;  //// REMEMBER TO INCLUDE # of constituents

		bool idL = ( (nhf<0.99) && (nEMf<0.99) && (muf<0.8) && (cEMf<0.9) );

		if( (*jetPt)[i] > 150  && idL ) { 
			//LogWarning("jetInfo") << i << " " << (*jetPt)[i] << " " << (*jetEta)[i] << " " << (*jetPhi)[i];
			HT += (*jetPt)[i];
			++numJets;

			TLorentzVector tmpJet;
			tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

			/// Vector of zeros
			TLorentzVector tmpSubjet0, tmpSubjet1, tmpZeros;
			tmpZeros.SetPtEtaPhiE( 0, 0, 0, 0 );

			//LogWarning("jetSubjetIndex") << (*jetSubjetIndex0)[i] << " " <<  (*jetSubjetIndex1)[i] << " " << (*jetSubjetIndex2)[i] << " " << (*jetSubjetIndex3)[i];

			for (size_t j = 0; j < subjetPt->size(); j++) {
				if( j == (*jetSubjetIndex0)[i] ) {
					//LogWarning("subjets0") << j << " " << (*jetSubjetIndex0)[i] << " " <<  subjetPt->size() << " " << (*subjetPt)[j];
					tmpSubjet0.SetPtEtaPhiE( (*subjetPt)[j], (*subjetEta)[j], (*subjetPhi)[j], (*subjetE)[j] );
				} //else tmpSubjet0 = tmpZeros ; 
					
				if( j == (*jetSubjetIndex1)[i] ) {
					tmpSubjet1.SetPtEtaPhiE( (*subjetPt)[j], (*subjetEta)[j], (*subjetPhi)[j], (*subjetE)[j] );
				} //else tmpSubjet1 = tmpZeros ; 
			}

			JETtype tmpJET;
			tmpJET.p4 = tmpJet;
			tmpJET.subjet0 = tmpSubjet0;
			tmpJET.subjet1 = tmpSubjet1;
			tmpJET.mass = (*jetMass)[i];
			tmpJET.tau1 = (*jetTau1)[i];
			tmpJET.tau2 = (*jetTau2)[i];
			tmpJET.tau3 = (*jetTau3)[i];
			JETS.push_back( tmpJET );
	   
			histos1D_[ "jetPt" ]->Fill( (*jetPt)[i], scale  );
			histos1D_[ "jetEta" ]->Fill( (*jetEta)[i], scale  );
			histos1D_[ "HT" ]->Fill( HT, scale  );
			histos1D_[ "jetMass" ]->Fill( (*jetMass)[i], scale  );
		}
	}

	sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1.p4; tmpP2 = p2.p4;  return tmpP1.M() > tmpP2.M(); }); 
	if( numJets > 0 ) cutmap["Kinematics"] += 1;
	histos1D_[ "jetNum" ]->Fill( numJets );
	if (HT > 700) cutHT = 1;

	//bool cutAsym = 0;
	if( ( numJets > 1 ) && cutHT ){
	   cutmap["HT"] += 1;
	   histos1D_[ "jetMass_cutHT_Ptsort" ]->Fill( (*jetMass)[0], scale );
	   histos1D_[ "jetMass_cutHT" ]->Fill( JETS[0].mass, scale );

	   double massAve = ( JETS[0].mass + JETS[1].mass ) / 2.0;
	   double massAsym = abs( JETS[0].mass - JETS[1].mass ) / ( JETS[0].mass + JETS[1].mass );

	   histos1D_[ "massAsymmetry_cutHT" ]->Fill( massAsym, scale  );
	   histos1D_[ "massAve_cutHT" ]->Fill( massAve, scale  );

	   TLorentzVector tmpJet1, tmpJet2, tmpCM;
	   tmpJet1 = JETS[0].p4;
	   tmpJet2 = JETS[1].p4;

	   tmpCM = tmpJet1 + tmpJet2;
	   //LogWarning("Jets") << tmpJet1.Eta() << " " << tmpJet2.Eta() << " " << tmpCM.Eta();
	   tmpJet1.Boost( -tmpCM.BoostVector() );
	   tmpJet2.Boost( -tmpCM.BoostVector() );
	   //LogWarning("JetsBoost") << tmpJet1.Eta() << " " << tmpJet2.Eta();
	   double cosThetaStar = ( tmpJet1.Px() * tmpCM.Px() +  tmpJet1.Py() * tmpCM.Py() + tmpJet1.Pz() * tmpCM.Pz() ) / (tmpJet1.E() * tmpCM.E() ) ;
	   //LogWarning("cos theta") << cosThetaStar ;

	   double jet1Tau21 = JETS[0].tau2 / JETS[0].tau1;
	   double jet1Tau31 = JETS[0].tau3 / JETS[0].tau1;
	   double jet1Tau32 = JETS[0].tau3 / JETS[0].tau2;
	   histos1D_[ "jet1Tau1_cutHT" ]->Fill( JETS[0].tau1, scale );
	   histos1D_[ "jet1Tau2_cutHT" ]->Fill( JETS[0].tau2, scale );
	   histos1D_[ "jet1Tau3_cutHT" ]->Fill( JETS[0].tau3, scale );
	   histos1D_[ "jet1Tau21_cutHT" ]->Fill( jet1Tau21, scale );
	   histos1D_[ "jet1Tau31_cutHT" ]->Fill( jet1Tau31, scale );
	   histos1D_[ "jet1Tau32_cutHT" ]->Fill( jet1Tau32, scale );


	   double jet1SubjetPtRatio = -999;
	   double jet2SubjetPtRatio = -999;
	   //LogWarning("presubjet0") <<  JETS[0].subjet0.Pt() << " " <<  JETS[0].subjet1.Pt();
	   if( ( JETS[0].subjet0.Pt() > 0 ) && ( JETS[0].subjet1.Pt() > 0 )) {
	   //LogWarning("subjet0") <<  JETS[0].subjet0.Pt() << " " <<  JETS[0].subjet1.Pt();
		   jet1SubjetPtRatio = min( JETS[0].subjet0.Pt(), JETS[0].subjet1.Pt() ) / max( JETS[0].subjet0.Pt(), JETS[0].subjet1.Pt() );
		   histos1D_[ "jet1Subjet1Pt_cutHT" ]->Fill( JETS[0].subjet0.Pt(), scale );
		   histos1D_[ "jet1Subjet2Pt_cutHT" ]->Fill( JETS[0].subjet1.Pt(), scale );
		   histos1D_[ "jet1SubjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, scale );
		   histos1D_[ "subjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, scale );
	   }
	   if( ( JETS[1].subjet0.Pt() > 0 ) && ( JETS[1].subjet1.Pt() > 0 )) {
		   jet2SubjetPtRatio = min( JETS[1].subjet0.Pt(), JETS[1].subjet1.Pt() ) / max( JETS[1].subjet0.Pt(), JETS[1].subjet1.Pt() );
		   histos1D_[ "jet2Subjet1Pt_cutHT" ]->Fill( JETS[1].subjet0.Pt(), scale );
		   histos1D_[ "jet2Subjet2Pt_cutHT" ]->Fill( JETS[1].subjet1.Pt(), scale );
		   histos1D_[ "jet2SubjetPtRatio_cutHT" ]->Fill( jet2SubjetPtRatio, scale );
		   histos1D_[ "subjetPtRatio_cutHT" ]->Fill( jet2SubjetPtRatio, scale );
	   }


	   if( massAsym < 0.1 ){
		   cutmap["Asymmetry"] += 1;
		   histos1D_[ "massAve_cutAsym" ]->Fill( massAve, scale  );
		   histos1D_[ "cosThetaStar_cutAsym" ]->Fill( cosThetaStar, scale  );
		   histos1D_[ "jet1Tau21_cutAsym" ]->Fill( jet1Tau21, scale  );
		   histos1D_[ "jet1Tau31_cutAsym" ]->Fill( jet1Tau31, scale  );
		   histos1D_[ "jet1Tau32_cutAsym" ]->Fill( jet1Tau32, scale  );
		   histos1D_[ "subjetPtRatio_cutAsym" ]->Fill( jet1SubjetPtRatio, scale );
		   histos1D_[ "subjetPtRatio_cutAsym" ]->Fill( jet2SubjetPtRatio, scale );

		   if( TMath::Abs( cosThetaStar ) < 0.3 ){
			   cutmap["CosTheta"] += 1;
			   histos1D_[ "massAve_cutCosTheta" ]->Fill( massAve, scale  );
			   histos1D_[ "jet1Tau21_cutCosTheta" ]->Fill( jet1Tau21, scale  );
			   histos1D_[ "jet1Tau31_cutCosTheta" ]->Fill( jet1Tau31, scale  );
			   histos1D_[ "jet1Tau32_cutCosTheta" ]->Fill( jet1Tau32, scale  );
			   histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet1SubjetPtRatio, scale );
			   histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet2SubjetPtRatio, scale );

			   if( ( jet1SubjetPtRatio > 0.3 ) && ( jet2SubjetPtRatio > 0.3 ) ){
				   cutmap["SubjetPtRatio"] += 1;
				   histos1D_[ "massAve_cutSubjetPtRatio" ]->Fill( massAve, scale  );
				   histos1D_[ "jet1Tau21_cutSubjetPtRatio" ]->Fill( jet1Tau21, scale  );
				   histos1D_[ "jet1Tau31_cutSubjetPtRatio" ]->Fill( jet1Tau31, scale  );
				   histos1D_[ "jet1Tau32_cutSubjetPtRatio" ]->Fill( jet1Tau32, scale  );
			   }

				if(  jet1Tau31 < 0.5 ){
					cutmap["Tau31"] += 1;
					histos1D_[ "massAve_cutTau31" ]->Fill( massAve, scale  );
				}
				if(  jet1Tau21 < 0.6 ){
					cutmap["Tau21"] += 1;
					histos1D_[ "massAve_cutTau21" ]->Fill( massAve, scale  );
				}
		   }
	   }
	} 
	JETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNAnalysis::beginJob() {

	histos1D_[ "jetPt" ] = fs_->make< TH1D >( "jetPt", "jetPt", 100, 0., 1000. );
	histos1D_[ "jetPt" ]->Sumw2();
	histos1D_[ "jetEta" ] = fs_->make< TH1D >( "jetEta", "jetEta", 100, -5., 5. );
	histos1D_[ "jetEta" ]->Sumw2();
	histos1D_[ "jetNum" ] = fs_->make< TH1D >( "jetNum", "jetNum", 10, 0., 10. );
	histos1D_[ "jetNum" ]->Sumw2();
	histos1D_[ "jetMass" ] = fs_->make< TH1D >( "jetMass", "jetMass", 30, 0., 300. );
	histos1D_[ "jetMass" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 150, 0., 1500. );
	histos1D_[ "HT" ]->Sumw2();

	histos1D_[ "jetMass_cutHT_Ptsort" ] = fs_->make< TH1D >( "jetMass_cutHT_Ptsort", "jetMass_cutHT_Ptsort", 30, 0., 300. );
	histos1D_[ "jetMass_cutHT_Ptsort" ]->Sumw2();
	histos1D_[ "jetMass_cutHT" ] = fs_->make< TH1D >( "jetMass_cutHT", "jetMass_cutHT", 30, 0., 300. );
	histos1D_[ "jetMass_cutHT" ]->Sumw2();
	histos1D_[ "massAsymmetry_cutHT" ] = fs_->make< TH1D >( "massAsymmetry_cutHT", "massAsymmetry_cutHT", 20, 0., 1. );
	histos1D_[ "massAsymmetry_cutHT" ]->Sumw2();
	histos1D_[ "massAve_cutHT" ] = fs_->make< TH1D >( "massAve_cutHT", "massAve_cutHT", 30, 0., 300. );
	histos1D_[ "massAve_cutHT" ]->Sumw2();
	histos1D_[ "jet1Tau1_cutHT" ] = fs_->make< TH1D >( "jet1Tau1_cutHT", "jet1Tau1_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau1_cutHT" ]->Sumw2();
	histos1D_[ "jet1Tau2_cutHT" ] = fs_->make< TH1D >( "jet1Tau2_cutHT", "jet1Tau2_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau2_cutHT" ]->Sumw2();
	histos1D_[ "jet1Tau3_cutHT" ] = fs_->make< TH1D >( "jet1Tau3_cutHT", "jet1Tau3_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau3_cutHT" ]->Sumw2();
	histos1D_[ "jet1Tau21_cutHT" ] = fs_->make< TH1D >( "jet1Tau21_cutHT", "jet1Tau21_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutHT" ]->Sumw2();
	histos1D_[ "jet1Tau31_cutHT" ] = fs_->make< TH1D >( "jet1Tau31_cutHT", "jet1Tau31_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutHT" ]->Sumw2();
	histos1D_[ "jet1Tau32_cutHT" ] = fs_->make< TH1D >( "jet1Tau32_cutHT", "jet1Tau32_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau32_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet1Pt_cutHT" ] = fs_->make< TH1D >( "jet1Subjet1Pt_cutHT", "jet1Subjet1Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet1Subjet1Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet2Pt_cutHT" ] = fs_->make< TH1D >( "jet1Subjet2Pt_cutHT", "jet1Subjet2Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet1Subjet2Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet1SubjetPtRatio_cutHT" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutHT", "jet1SubjetPtRatio_cutHT", 20, 0, 1.);
	histos1D_[ "jet1SubjetPtRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet1Pt_cutHT" ] = fs_->make< TH1D >( "jet2Subjet1Pt_cutHT", "jet2Subjet1Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet2Subjet1Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet2Pt_cutHT" ] = fs_->make< TH1D >( "jet2Subjet2Pt_cutHT", "jet2Subjet2Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet2Subjet2Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet2SubjetPtRatio_cutHT" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutHT", "jet2SubjetPtRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet2SubjetPtRatio_cutHT" ]->Sumw2();
	histos1D_[ "subjetPtRatio_cutHT" ] = fs_->make< TH1D >( "subjetPtRatio_cutHT", "subjetPtRatio_cutHT", 20, 0., 1. );
	histos1D_[ "subjetPtRatio_cutHT" ]->Sumw2();

	histos1D_[ "massAve_cutAsym" ] = fs_->make< TH1D >( "massAve_cutAsym", "massAve_cutAsym", 30, 0., 300. );
	histos1D_[ "massAve_cutAsym" ]->Sumw2();
	histos1D_[ "cosThetaStar_cutAsym" ] = fs_->make< TH1D >( "cosThetaStar_cutAsym", "cosThetaStar_cutAsym", 20, -1., 1. );
	histos1D_[ "cosThetaStar_cutAsym" ]->Sumw2();
	histos1D_[ "jet1Tau21_cutAsym" ] = fs_->make< TH1D >( "jet1Tau21_cutAsym", "jet1Tau21_cutAsym", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutAsym" ]->Sumw2();
	histos1D_[ "jet1Tau31_cutAsym" ] = fs_->make< TH1D >( "jet1Tau31_cutAsym", "jet1Tau31_cutAsym", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutAsym" ]->Sumw2();
	histos1D_[ "jet1Tau32_cutAsym" ] = fs_->make< TH1D >( "jet1Tau32_cutAsym", "jet1Tau32_cutAsym", 20, 0., 1. );
	histos1D_[ "jet1Tau32_cutAsym" ]->Sumw2();
	histos1D_[ "subjetPtRatio_cutAsym" ] = fs_->make< TH1D >( "subjetPtRatio_cutAsym", "subjetPtRatio_cutAsym", 20, 0., 1. );
	histos1D_[ "subjetPtRatio_cutAsym" ]->Sumw2();

	histos1D_[ "massAve_cutCosTheta" ] = fs_->make< TH1D >( "massAve_cutCosTheta", "massAve_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAve_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1Tau21_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau21_cutCosTheta", "jet1Tau21_cutCosTheta", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1Tau31_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau31_cutCosTheta", "jet1Tau31_cutCosTheta", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1Tau32_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau32_cutCosTheta", "jet1Tau32_cutCosTheta", 20, 0., 1. );
	histos1D_[ "jet1Tau32_cutCosTheta" ]->Sumw2();
	histos1D_[ "subjetPtRatio_cutCosTheta" ] = fs_->make< TH1D >( "subjetPtRatio_cutCosTheta", "subjetPtRatio_cutCosTheta", 20, 0., 1. );
	histos1D_[ "subjetPtRatio_cutCosTheta" ]->Sumw2();

	histos1D_[ "massAve_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAve_cutSubjetPtRatio", "massAve_cutSubjetPtRatio", 30, 0., 300. );
	histos1D_[ "massAve_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1Tau21_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1Tau21_cutSubjetPtRatio", "jet1Tau21_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1Tau31_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1Tau31_cutSubjetPtRatio", "jet1Tau31_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1Tau32_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1Tau32_cutSubjetPtRatio", "jet1Tau32_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "jet1Tau32_cutSubjetPtRatio" ]->Sumw2();

	histos1D_[ "massAve_cutTau31" ] = fs_->make< TH1D >( "massAve_cutTau31", "massAve_cutTau31", 30, 0., 300. );
	histos1D_[ "massAve_cutTau31" ]->Sumw2();
	histos1D_[ "massAve_cutTau21" ] = fs_->make< TH1D >( "massAve_cutTau21", "massAve_cutTau21", 30, 0., 300. );
	histos1D_[ "massAve_cutTau21" ]->Sumw2();


	cutLabels.push_back("Processed");
	cutLabels.push_back("Kinematics");
	cutLabels.push_back("HT");
	cutLabels.push_back("Asymmetry");
	cutLabels.push_back("CosTheta");
	cutLabels.push_back("SubjetPtRatio");
	cutLabels.push_back("Tau31");
	cutLabels.push_back("Tau21");
	histos1D_[ "hcutflow" ] = fs_->make< TH1D >("cutflow","cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflow" ]->Sumw2();
	histos1D_[ "hcutflowSimple" ] = fs_->make< TH1D >("cutflowSimple","simple cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflowSimple" ]->Sumw2();
	for( const string &ivec : cutLabels ) cutmap[ ivec ] = 0;
}

// ------------ method called once each job just after ending the event loop  ------------
void RUNAnalysis::endJob() {

	int ibin = 1;
	for( const string &ivec : cutLabels ) {
		histos1D_["hcutflow"]->SetBinContent( ibin, cutmap[ ivec ] * scale );
		histos1D_["hcutflow"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		histos1D_["hcutflowSimple"]->SetBinContent( ibin, cutmap[ ivec ] );
		histos1D_["hcutflowSimple"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		ibin++;
	}

}


//define this as a plug-in
DEFINE_FWK_MODULE(RUNAnalysis);
