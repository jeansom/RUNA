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

      double scale;
      edm::EDGetTokenT<std::vector<float>> jetPt_;
      edm::EDGetTokenT<std::vector<float>> jetEta_;
      edm::EDGetTokenT<std::vector<float>> jetPhi_;
      edm::EDGetTokenT<std::vector<float>> jetE_;
      edm::EDGetTokenT<std::vector<float>> jetMass_;
      edm::EDGetTokenT<std::vector<float>> jetTrimmedMass_;
      edm::EDGetTokenT<std::vector<float>> jetPrunedMass_;
      edm::EDGetTokenT<std::vector<float>> jetFilteredMass_;
      edm::EDGetTokenT<std::vector<float>> jetTau1_;
      edm::EDGetTokenT<std::vector<float>> jetTau2_;
      edm::EDGetTokenT<std::vector<float>> jetTau3_;

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
	jetTrimmedMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTrimmedMass"))),
	jetPrunedMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetPrunedMass"))),
	jetFilteredMass_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetFilteredMass"))),
	jetTau1_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau1"))),
	jetTau2_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau2"))),
	jetTau3_(consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("jetTau3"))),
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
void
RUNAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
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

   edm::Handle<std::vector<float> > jetTrimmedMass;
   iEvent.getByToken(jetTrimmedMass_, jetTrimmedMass);

   edm::Handle<std::vector<float> > jetFilteredMass;
   iEvent.getByToken(jetFilteredMass_, jetFilteredMass);

   edm::Handle<std::vector<float> > jetPrunedMass;
   iEvent.getByToken(jetPrunedMass_, jetPrunedMass);

   edm::Handle<std::vector<float> > jetTau1;
   iEvent.getByToken(jetTau1_, jetTau1);

   edm::Handle<std::vector<float> > jetTau2;
   iEvent.getByToken(jetTau2_, jetTau2);

   edm::Handle<std::vector<float> > jetTau3;
   iEvent.getByToken(jetTau3_, jetTau3);

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


   int numJets = 0;
   double HT = 0;
   bool cutHT = 0;
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
		   if (HT > 700) cutHT = 1;
		   ++numJets;

		   histos1D_[ "jetPt" ]->Fill( (*jetPt)[i], scale  );
		   histos1D_[ "jetEta" ]->Fill( (*jetEta)[i], scale  );
		   histos1D_[ "HT" ]->Fill( HT, scale  );
		   histos1D_[ "jetMass" ]->Fill( (*jetMass)[i], scale  );
		   histos1D_[ "jetTrimmedMass" ]->Fill( (*jetTrimmedMass)[i], scale  );
		   histos1D_[ "jetPrunedMass" ]->Fill( (*jetPrunedMass)[i], scale  );
		   histos1D_[ "jetFilteredMass" ]->Fill( (*jetFilteredMass)[i], scale  );
	   }
   }

   histos1D_[ "jetNum" ]->Fill( numJets );

   //bool cutAsym = 0;
   if(cutHT ){
	   histos1D_[ "jetMass_cutHT" ]->Fill( (*jetMass)[0], scale );
	   histos1D_[ "jetTrimmedMass_cutHT" ]->Fill( (*jetTrimmedMass)[0], scale  );
	   histos1D_[ "jetPrunedMass_cutHT" ]->Fill( (*jetPrunedMass)[0], scale  );
	   histos1D_[ "jetFilteredMass_cutHT" ]->Fill( (*jetFilteredMass)[0], scale  );

	   double massAve = ( (*jetMass)[0] + (*jetMass)[1] ) / 2.0;
	   double massAveTrim = ( (*jetTrimmedMass)[0] + (*jetTrimmedMass)[1] ) / 2.0;
	   double massAvePrun = ( (*jetPrunedMass)[0] + (*jetPrunedMass)[1] ) / 2.0;
	   double massAveFilt = ( (*jetFilteredMass)[0] + (*jetFilteredMass)[1] ) / 2.0;

	   double massAsym = abs( (*jetMass)[0] - (*jetMass)[1] ) / ( (*jetMass)[0] + (*jetMass)[1] );
	   double massAsymTrim = abs( (*jetTrimmedMass)[0] - (*jetTrimmedMass)[1] ) / ( (*jetTrimmedMass)[0] + (*jetTrimmedMass)[1] );
	   double massAsymPrun = abs( (*jetPrunedMass)[0] - (*jetPrunedMass)[1] ) / ( (*jetPrunedMass)[0] + (*jetPrunedMass)[1] );
	   double massAsymFilt = abs( (*jetFilteredMass)[0] - (*jetFilteredMass)[1] ) / ( (*jetFilteredMass)[0] + (*jetFilteredMass)[1] );

	   histos1D_[ "massAsymmetry_cutHT" ]->Fill( massAsym, scale  );
	   histos1D_[ "massAsymmetryTrim_cutHT" ]->Fill( massAsymTrim, scale  );
	   histos1D_[ "massAsymmetryPrun_cutHT" ]->Fill( massAsymPrun, scale  );
	   histos1D_[ "massAsymmetryFilt_cutHT" ]->Fill( massAsymFilt, scale  );

	   histos1D_[ "massAve_cutHT" ]->Fill( massAve, scale  );
	   histos1D_[ "massAveTrim_cutHT" ]->Fill( massAveTrim, scale  );
	   histos1D_[ "massAvePrun_cutHT" ]->Fill( massAvePrun, scale  );
	   histos1D_[ "massAveFilt_cutHT" ]->Fill( massAveFilt, scale  );

	   TLorentzVector tmpJet1, tmpJet2, tmpCM;
	   tmpJet1.SetPtEtaPhiE( (*jetPt)[0], (*jetEta)[0], (*jetPhi)[0], (*jetE)[0] );
	   tmpJet2.SetPtEtaPhiE( (*jetPt)[1], (*jetEta)[1], (*jetPhi)[1], (*jetE)[1] );

	   tmpCM = tmpJet1 + tmpJet2;
	   //LogWarning("Jets") << tmpJet1.Eta() << " " << tmpJet2.Eta() << " " << tmpCM.Eta();
	   tmpJet1.Boost( -tmpCM.BoostVector() );
	   tmpJet2.Boost( -tmpCM.BoostVector() );
	   //LogWarning("JetsBoost") << tmpJet1.Eta() << " " << tmpJet2.Eta();
	   double cosThetaStar = ( tmpJet1.Px() * tmpCM.Px() +  tmpJet1.Py() * tmpCM.Py() + tmpJet1.Pz() * tmpCM.Pz() ) / (tmpJet1.E() * tmpCM.E() ) ;
	   //LogWarning("cos theta") << cosThetaStar ;
	   bool cutCosThetaStar = abs( cosThetaStar ) < 0.3;
	   
	   if( massAsym < 0.1 ){
		   histos1D_[ "massAve_cutAsym" ]->Fill( massAve, scale  );
		   histos1D_[ "cosThetaStar_cutAsym" ]->Fill( cosThetaStar, scale  );

		   if( cutCosThetaStar ){
		   	histos1D_[ "massAve_cutCosTheta" ]->Fill( massAve, scale  );
		   }
	   }

	   if( massAsymTrim < 0.1 ){
		   histos1D_[ "massAveTrim_cutAsym" ]->Fill( massAveTrim, scale  );
		   histos1D_[ "cosThetaStarTrim_cutAsym" ]->Fill( cosThetaStar, scale  );

		   if( cutCosThetaStar ){
		   	histos1D_[ "massAveTrim_cutCosTheta" ]->Fill( massAveTrim, scale  );
		   }
	   }

	   if( massAsymPrun < 0.1 ){
		   histos1D_[ "massAvePrun_cutAsym" ]->Fill( massAvePrun, scale  );
		   histos1D_[ "cosThetaStarPrun_cutAsym" ]->Fill( cosThetaStar, scale  );

		   if( cutCosThetaStar ){
		   	histos1D_[ "massAvePrun_cutCosTheta" ]->Fill( massAvePrun, scale  );
		   }
	   }

	   if( massAsymFilt < 0.1 ){
		   histos1D_[ "massAveFilt_cutAsym" ]->Fill( massAveFilt, scale  );
		   histos1D_[ "cosThetaStarFilt_cutAsym" ]->Fill( cosThetaStar, scale  );

		   if( cutCosThetaStar ){
		   	histos1D_[ "massAveFilt_cutCosTheta" ]->Fill( massAveFilt, scale  );
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
	histos1D_[ "jetTrimmedMass" ] = fs_->make< TH1D >( "jetTrimmedMass", "jetTrimmedMass", 30, 0., 300. );
	histos1D_[ "jetTrimmedMass" ]->Sumw2();
	histos1D_[ "jetPrunedMass" ] = fs_->make< TH1D >( "jetPrunedMass", "jetPrunedMass", 30, 0., 300. );
	histos1D_[ "jetPrunedMass" ]->Sumw2();
	histos1D_[ "jetFilteredMass" ] = fs_->make< TH1D >( "jetFilteredMass", "jetFilteredMass", 30, 0., 300. );
	histos1D_[ "jetFilteredMass" ]->Sumw2();

	histos1D_[ "jetMass_cutHT" ] = fs_->make< TH1D >( "jetMass_cutHT", "jetMass_cutHT", 30, 0., 300. );
	histos1D_[ "jetMass_cutHT" ]->Sumw2();
	histos1D_[ "jetTrimmedMass_cutHT" ] = fs_->make< TH1D >( "jetTrimmedMass_cutHT", "jetTrimmedMass_cutHT", 30, 0., 300. );
	histos1D_[ "jetTrimmedMass_cutHT" ]->Sumw2();
	histos1D_[ "jetPrunedMass_cutHT" ] = fs_->make< TH1D >( "jetPrunedMass_cutHT", "jetPrunedMass_cutHT", 30, 0., 300. );
	histos1D_[ "jetPrunedMass_cutHT" ]->Sumw2();
	histos1D_[ "jetFilteredMass_cutHT" ] = fs_->make< TH1D >( "jetFilteredMass_cutHT", "jetFilteredMass_cutHT", 30, 0., 300. );
	histos1D_[ "jetFilteredMass_cutHT" ]->Sumw2();
	histos1D_[ "massAsymmetry_cutHT" ] = fs_->make< TH1D >( "massAsymmetry_cutHT", "massAsymmetry_cutHT", 20, 0., 1. );
	histos1D_[ "massAsymmetry_cutHT" ]->Sumw2();
	histos1D_[ "massAsymmetryTrim_cutHT" ] = fs_->make< TH1D >( "massAsymmetryTrim_cutHT", "massAsymmetryTrim_cutHT", 20, 0., 1. );
	histos1D_[ "massAsymmetryTrim_cutHT" ]->Sumw2();
	histos1D_[ "massAsymmetryPrun_cutHT" ] = fs_->make< TH1D >( "massAsymmetryPrun_cutHT", "massAsymmetryPrun_cutHT", 20, 0., 1. );
	histos1D_[ "massAsymmetryPrun_cutHT" ]->Sumw2();
	histos1D_[ "massAsymmetryFilt_cutHT" ] = fs_->make< TH1D >( "massAsymmetryFilt_cutHT", "massAsymmetryFilt_cutHT", 20, 0., 1. );
	histos1D_[ "massAsymmetryFilt_cutHT" ]->Sumw2();
	histos1D_[ "massAve_cutHT" ] = fs_->make< TH1D >( "massAve_cutHT", "massAve_cutHT", 30, 0., 300. );
	histos1D_[ "massAve_cutHT" ]->Sumw2();
	histos1D_[ "massAveTrim_cutHT" ] = fs_->make< TH1D >( "massAveTrim_cutHT", "massAveTrim_cutHT", 30, 0., 300. );
	histos1D_[ "massAveTrim_cutHT" ]->Sumw2();
	histos1D_[ "massAvePrun_cutHT" ] = fs_->make< TH1D >( "massAvePrun_cutHT", "massAvePrun_cutHT", 30, 0., 300. );
	histos1D_[ "massAvePrun_cutHT" ]->Sumw2();
	histos1D_[ "massAveFilt_cutHT" ] = fs_->make< TH1D >( "massAveFilt_cutHT", "massAveFilt_cutHT", 30, 0., 300. );
	histos1D_[ "massAveFilt_cutHT" ]->Sumw2();

	histos1D_[ "massAve_cutAsym" ] = fs_->make< TH1D >( "massAve_cutAsym", "massAve_cutAsym", 30, 0., 300. );
	histos1D_[ "massAve_cutAsym" ]->Sumw2();
	histos1D_[ "massAveTrim_cutAsym" ] = fs_->make< TH1D >( "massAveTrim_cutAsym", "massAveTrim_cutAsym", 30, 0., 300. );
	histos1D_[ "massAveTrim_cutAsym" ]->Sumw2();
	histos1D_[ "massAvePrun_cutAsym" ] = fs_->make< TH1D >( "massAvePrun_cutAsym", "massAvePrun_cutAsym", 30, 0., 300. );
	histos1D_[ "massAvePrun_cutAsym" ]->Sumw2();
	histos1D_[ "massAveFilt_cutAsym" ] = fs_->make< TH1D >( "massAveFilt_cutAsym", "massAveFilt_cutAsym", 30, 0., 300. );
	histos1D_[ "massAveFilt_cutAsym" ]->Sumw2();
	histos1D_[ "cosThetaStar_cutAsym" ] = fs_->make< TH1D >( "cosThetaStar_cutAsym", "cosThetaStar_cutAsym", 20, -1., 1. );
	histos1D_[ "cosThetaStar_cutAsym" ]->Sumw2();
	histos1D_[ "cosThetaStarTrim_cutAsym" ] = fs_->make< TH1D >( "cosThetaStarTrim_cutAsym", "cosThetaStarTrim_cutAsym", 20, -1., 1. );
	histos1D_[ "cosThetaStarTrim_cutAsym" ]->Sumw2();
	histos1D_[ "cosThetaStarPrun_cutAsym" ] = fs_->make< TH1D >( "cosThetaStarPrun_cutAsym", "cosThetaStarPrun_cutAsym", 20, -1., 1. );
	histos1D_[ "cosThetaStarPrun_cutAsym" ]->Sumw2();
	histos1D_[ "cosThetaStarFilt_cutAsym" ] = fs_->make< TH1D >( "cosThetaStarFilt_cutAsym", "cosThetaStarFilt_cutAsym", 20, -1., 1. );
	histos1D_[ "cosThetaStarFilt_cutAsym" ]->Sumw2();

	histos1D_[ "massAve_cutCosTheta" ] = fs_->make< TH1D >( "massAve_cutCosTheta", "massAve_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAve_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAveTrim_cutCosTheta" ] = fs_->make< TH1D >( "massAveTrim_cutCosTheta", "massAveTrim_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAveTrim_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAvePrun_cutCosTheta" ] = fs_->make< TH1D >( "massAvePrun_cutCosTheta", "massAvePrun_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAvePrun_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAveFilt_cutCosTheta" ] = fs_->make< TH1D >( "massAveFilt_cutCosTheta", "massAveFilt_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAveFilt_cutCosTheta" ]->Sumw2();
}

// ------------ method called once each job just after ending the event loop  ------------
void 
RUNAna::endJob() 
{
}


//define this as a plug-in
DEFINE_FWK_MODULE(RUNAna);
