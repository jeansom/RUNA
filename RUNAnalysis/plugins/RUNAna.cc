// -*- C++ -*-
//
// Package:    Ntuples/Ntuples
// Class:      RUNAna
// 
/**\class RUNAna RUNAna.cc Ntuples/Ntuples/plugins/RUNAna.cc

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
//
// class declaration
//

class RUNAna : public edm::EDAnalyzer {
   public:
      explicit RUNAna(const edm::ParameterSet&);
      ~RUNAna();

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      //edm::GetterOfProducts< vector<float> > getterOfProducts_;
      //edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      edm::Service<TFileService> fs_;
      std::map< std::string, TH1D* > histos1D_;
      std::vector< std::string > cutLabels;
      std::map< std::string, double > cutmap;

      double scale;
      edm::EDGetTokenT<std::vector<float>> jetPt_;
      edm::EDGetTokenT<std::vector<float>> jetEta_;
      edm::EDGetTokenT<std::vector<float>> jetPhi_;
      edm::EDGetTokenT<std::vector<float>> jetE_;
      edm::EDGetTokenT<std::vector<float>> jetMass_;
      edm::EDGetTokenT<std::vector<float>> jetTau1_;
      edm::EDGetTokenT<std::vector<float>> jetTau2_;
      edm::EDGetTokenT<std::vector<float>> jetTau3_;
      edm::EDGetTokenT<std::vector<math::PtEtaPhiELorentzVector>> jet1Subjets_;
      edm::EDGetTokenT<std::vector<math::PtEtaPhiELorentzVector>> jet2Subjets_;
      edm::EDGetTokenT<std::vector<math::PtEtaPhiELorentzVector>> jet3Subjets_;
      edm::EDGetTokenT<std::vector<math::PtEtaPhiELorentzVector>> jet4Subjets_;

      //Jet ID
      edm::EDGetTokenT<std::vector<float>> neutralHadronEnergyFraction_;
      edm::EDGetTokenT<std::vector<float>> HFHadronEnergyFraction_;
      edm::EDGetTokenT<std::vector<float>> photonEnergy_; // neutral EM fraction
      edm::EDGetTokenT<std::vector<float>> chargedHadronMultiplicity_;
      edm::EDGetTokenT<std::vector<float>> neutralHadronMultiplicity_;
      edm::EDGetTokenT<std::vector<float>> muonEnergy_; 
      edm::EDGetTokenT<std::vector<float>> electronEnergy_; 
      edm::EDGetTokenT<std::vector<float>> chargedHadronEnergyFraction_;
      edm::EDGetTokenT<std::vector<float>> jecFactor_;

};

//
// constants, enums and typedefs
//
typedef struct {
	TLorentzVector p4;
	double mass;
	double tau1;
	double tau2;
	double tau3;
	std::vector< math::PtEtaPhiELorentzVector > subjets ;
} JETtype;
//
// static data member definitions
//

//
// constructors and destructor
//
RUNAna::RUNAna(const edm::ParameterSet& iConfig):
//	getterOfProducts_(edm::ProcessMatch(*), this) {
//	triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
	jetPt_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetPt"))),
	jetEta_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetEta"))),
	jetPhi_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetPhi"))),
	jetE_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetE"))),
	jetMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetMass"))),
	jetTau1_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau1"))),
	jetTau2_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau2"))),
	jetTau3_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau3"))),
	jet1Subjets_(consumes<std::vector<math::PtEtaPhiELorentzVector>>(iConfig.getParameter<edm::InputTag>("jet1Subjets"))),
	jet2Subjets_(consumes<std::vector<math::PtEtaPhiELorentzVector>>(iConfig.getParameter<edm::InputTag>("jet2Subjets"))),
	jet3Subjets_(consumes<std::vector<math::PtEtaPhiELorentzVector>>(iConfig.getParameter<edm::InputTag>("jet3Subjets"))),
	jet4Subjets_(consumes<std::vector<math::PtEtaPhiELorentzVector>>(iConfig.getParameter<edm::InputTag>("jet4Subjets"))),
	//Jet ID,
	neutralHadronEnergyFraction_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("neutralHadronEnergyFraction"))),
	HFHadronEnergyFraction_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("HFHadronEnergyFraction"))),
	photonEnergy_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("photonEnergy"))),
	chargedHadronMultiplicity_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("chargedHadronMultiplicity"))),
	neutralHadronMultiplicity_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("neutralHadronMultiplicity"))),
	muonEnergy_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("muonEnergy"))),
	electronEnergy_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("electronEnergy"))),
	chargedHadronEnergyFraction_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("chargedHadronEnergyFraction"))),
	jecFactor_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jecFactor")))
{
	scale = iConfig.getParameter<double>("scale");
//	callWhenNewProductsRegistered(getterOfProducts_);
}


RUNAna::~RUNAna()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

	using namespace edm;

	/*std::vector<edm::Handle< vector<float> > > handles;
	getterOfProducts_.fillHandles(event, handles);
	*/

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

	edm::Handle<std::vector< math::PtEtaPhiELorentzVector > > jet1Subjets;
	iEvent.getByToken(jet1Subjets_, jet1Subjets );

	edm::Handle<std::vector< math::PtEtaPhiELorentzVector > > jet2Subjets;
	iEvent.getByToken(jet2Subjets_, jet2Subjets );

	edm::Handle<std::vector< math::PtEtaPhiELorentzVector > > jet3Subjets;
	iEvent.getByToken(jet3Subjets_, jet3Subjets );

	edm::Handle<std::vector< math::PtEtaPhiELorentzVector > > jet4Subjets;
	iEvent.getByToken(jet4Subjets_, jet4Subjets );

	/// Jet ID
	edm::Handle<std::vector<float> > neutralHadronEnergyFraction;
	iEvent.getByToken(neutralHadronEnergyFraction_, neutralHadronEnergyFraction);

	edm::Handle<std::vector<float> > HFHadronEnergyFraction;
	iEvent.getByToken(HFHadronEnergyFraction_, HFHadronEnergyFraction);

	edm::Handle<std::vector<float> > photonEnergy;
	iEvent.getByToken(photonEnergy_, photonEnergy);

	edm::Handle<std::vector<float> > chargedHadronMultiplicity;
	iEvent.getByToken(chargedHadronMultiplicity_, chargedHadronMultiplicity);

	edm::Handle<std::vector<float> > neutralHadronMultiplicity;
	iEvent.getByToken(neutralHadronMultiplicity_, neutralHadronMultiplicity);

	edm::Handle<std::vector<float> > muonEnergy;
	iEvent.getByToken(muonEnergy_, muonEnergy);

	edm::Handle<std::vector<float> > electronEnergy;
	iEvent.getByToken(electronEnergy_, electronEnergy);

	edm::Handle<std::vector<float> > chargedHadronEnergyFraction;
	iEvent.getByToken(chargedHadronEnergyFraction_, chargedHadronEnergyFraction);

	edm::Handle<std::vector<float> > jecFactor;
	iEvent.getByToken(jecFactor_, jecFactor);

	cutmap["Processed"] += 1;

	int numJets = 0;
	double HT = 0;
	bool cutHT = 0;
	std::vector< JETtype > JETS;
	for (size_t i = 0; i < jetPt->size(); i++) {

	   if( TMath::Abs( (*jetEta)[i] ) > 2.5 ) continue;

	   double chf = (*chargedHadronEnergyFraction)[i];
	   double nhf = (*neutralHadronEnergyFraction)[i] + (*HFHadronEnergyFraction)[i] ;
	   double jec = 1. / ( (*jecFactor)[i] * (*jetE)[i] );
	   double nEMf = (*photonEnergy)[i] * jec;
	   double cEMf = (*electronEnergy)[i] * jec;
	   double muf = (*muonEnergy)[i] * jec;
	   int chm = (*chargedHadronMultiplicity)[i];
	   int npr = (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i] ;

	   bool idL = ( (npr>1) && (nEMf<0.99) && (nhf<0.99) && (muf<0.8) && (cEMf<0.9) && (chf>0) && (chm>0) );

	   if( (*jetPt)[i] > 150  && idL ) { 
		   //LogWarning("jetInfo") << i << " " << (*jetPt)[i] << " " << (*jetEta)[i] << " " << (*jetPhi)[i];
		   HT += (*jetPt)[i];
		   ++numJets;

		   TLorentzVector tmpJet;
		   tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

		   JETtype tmpJET;
		   tmpJET.p4 = tmpJet;
		   tmpJET.mass = (*jetMass)[i];
		   tmpJET.tau1 = (*jetTau1)[i];
		   tmpJET.tau2 = (*jetTau2)[i];
		   tmpJET.tau3 = (*jetTau3)[i];
		   
		   /// Vector of zeros
		   std::vector< math::PtEtaPhiELorentzVector > tmpSubjets;
		   math::PtEtaPhiELorentzVector tmpZeros( 0, 0, 0, 0 );
		   if( i==0 ) {
			  tmpSubjets.push_back( (*jet1Subjets)[0] ); 
			  tmpSubjets.push_back( (*jet1Subjets)[1] ); 
			  //LogWarning("test") << i << " " << (*jet1Subjets)[0].pt() << " " <<  (*jet1Subjets)[1].pt();
		   } else if( i==1 ) {
			  tmpSubjets.push_back( (*jet2Subjets)[0] ); 
			  tmpSubjets.push_back( (*jet2Subjets)[1] ); 
		   } else tmpSubjets.push_back( tmpZeros );

		   tmpJET.subjets = tmpSubjets;
		   //LogWarning("Subjet1") << i << " " << tmpSubjets.size() << " " <<  tmpSubjets[0].pt() << " " << tmpSubjets[1].pt();
		   JETS.push_back( tmpJET );
		   tmpSubjets.clear();
	   
		   histos1D_[ "jetPt" ]->Fill( (*jetPt)[i], scale  );
		   histos1D_[ "jetEta" ]->Fill( (*jetEta)[i], scale  );
		   histos1D_[ "HT" ]->Fill( HT, scale  );
		   histos1D_[ "jetMass" ]->Fill( (*jetMass)[i], scale  );
	   }
	}

	std::sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1.p4; tmpP2 = p2.p4;  return tmpP1.M() > tmpP2.M(); }); 
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
	   if( JETS[0].subjets.size() > 1 ) {
		   jet1SubjetPtRatio = std::min( JETS[0].subjets[0].pt(), JETS[0].subjets[1].pt() ) / std::max( JETS[0].subjets[0].pt(), JETS[0].subjets[1].pt() );
		   histos1D_[ "jet1Subjet1Pt_cutHT" ]->Fill( JETS[0].subjets[0].pt(), scale );
		   histos1D_[ "jet1Subjet2Pt_cutHT" ]->Fill( JETS[0].subjets[1].pt(), scale );
		   histos1D_[ "jet1SubjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, scale );
		   histos1D_[ "subjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, scale );
	   }
	   if( JETS[1].subjets.size() > 1 ) {
		   jet2SubjetPtRatio = std::min( JETS[1].subjets[0].pt(), JETS[1].subjets[1].pt() ) / std::max( JETS[1].subjets[0].pt(), JETS[1].subjets[1].pt() );
		   histos1D_[ "jet2Subjet1Pt_cutHT" ]->Fill( JETS[1].subjets[0].pt(), scale );
		   histos1D_[ "jet2Subjet2Pt_cutHT" ]->Fill( JETS[1].subjets[1].pt(), scale );
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
		   }
	   }
	} 

}


// ------------ method called once each job just before starting event loop  ------------
void RUNAna::beginJob() {

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

	cutLabels.push_back("Processed");
	cutLabels.push_back("Kinematics");
	cutLabels.push_back("HT");
	cutLabels.push_back("Asymmetry");
	cutLabels.push_back("CosTheta");
	cutLabels.push_back("SubjetPtRatio");
	cutLabels.push_back("Tau");
	histos1D_[ "hcutflow" ] = fs_->make< TH1D >("cutflow","cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflow" ]->Sumw2();
	histos1D_[ "hcutflowSimple" ] = fs_->make< TH1D >("cutflowSimple","simple cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflowSimple" ]->Sumw2();
	for( const std::string &ivec : cutLabels ) cutmap[ ivec ] = 0;
}

// ------------ method called once each job just after ending the event loop  ------------
void RUNAna::endJob() {

	int ibin = 1;
	for( const std::string &ivec : cutLabels ) {
		histos1D_["hcutflow"]->SetBinContent( ibin, cutmap[ ivec ] * scale );
		histos1D_["hcutflow"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		histos1D_["hcutflowSimple"]->SetBinContent( ibin, cutmap[ ivec ] );
		histos1D_["hcutflowSimple"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		ibin++;
	}

}


//define this as a plug-in
DEFINE_FWK_MODULE(RUNAna);
