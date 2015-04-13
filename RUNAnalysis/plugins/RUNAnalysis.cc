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
	bool btagCSV;
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
      //TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      bool bjSample;
      double scale;
      double cutHTvalue;
      double cutAsymvalue;
      double cutCosThetavalue;
      double cutSubjetPtRatiovalue;
      double cutTau31value;
      double cutTau21value;

      EDGetTokenT<vector<float>> jetPt_;
      EDGetTokenT<vector<float>> jetEta_;
      EDGetTokenT<vector<float>> jetPhi_;
      EDGetTokenT<vector<float>> jetE_;
      EDGetTokenT<vector<float>> jetMass_;
      EDGetTokenT<vector<float>> jetTrimmedMass_;
      EDGetTokenT<vector<float>> jetTau1_;
      EDGetTokenT<vector<float>> jetTau2_;
      EDGetTokenT<vector<float>> jetTau3_;
      EDGetTokenT<vector<float>> jetNSubjets_;
      EDGetTokenT<vector<float>> jetSubjetIndex0_;
      EDGetTokenT<vector<float>> jetSubjetIndex1_;
      EDGetTokenT<vector<float>> jetSubjetIndex2_;
      EDGetTokenT<vector<float>> jetSubjetIndex3_;
      EDGetTokenT<vector<vector<int>>> jetKeys_;
      EDGetTokenT<vector<float>> jetCSV_;
      EDGetTokenT<vector<float>> jetCSVV1_;
      EDGetTokenT<int> NPV_;

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
	jetTrimmedMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTrimmedMass"))),
	jetTau1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau1"))),
	jetTau2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau2"))),
	jetTau3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau3"))),
	jetNSubjets_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetNSubjets"))),
	jetSubjetIndex0_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex0"))),
	jetSubjetIndex1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex1"))),
	jetSubjetIndex2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex2"))),
	jetSubjetIndex3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex3"))),
	jetKeys_(consumes<vector<vector<int>>>(iConfig.getParameter<InputTag>("jetKeys"))),
	jetCSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSV"))),
	jetCSVV1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVV1"))),
	NPV_(consumes<int>(iConfig.getParameter<InputTag>("NPV"))),
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
	bjSample = iConfig.getParameter<bool>("bjSample");
	cutHTvalue = iConfig.getParameter<double>("cutHTvalue");
	cutAsymvalue = iConfig.getParameter<double>("cutAsymvalue");
	cutCosThetavalue = iConfig.getParameter<double>("cutCosThetavalue");
	cutSubjetPtRatiovalue = iConfig.getParameter<double>("cutSubjetPtRatiovalue");
	cutTau31value = iConfig.getParameter<double>("cutTau31value");
	cutTau21value = iConfig.getParameter<double>("cutTau21value");
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

	Handle<vector<float> > jetTrimmedMass;
	iEvent.getByToken(jetTrimmedMass_, jetTrimmedMass);

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

	Handle<vector<float> > jetCSV;
	iEvent.getByToken(jetCSV_, jetCSV);

	Handle<vector<float> > jetCSVV1;
	iEvent.getByToken(jetCSVV1_, jetCSVV1);

	Handle<int> NPV;
	iEvent.getByToken(NPV_, NPV);

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


	cutmap["Processed"] += 1;

	int numPV = *NPV;
	vector< JETtype > JETS;
	vector< float > tmpTriggerMass;
	int numJets = 0;
	double HT = 0;
	double rawHT = 0;
	bool cutHT = 0;
	bool cutMass = 0;
	bool bTagCSV = 0;
	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		tmpTriggerMass.push_back( (*jetTrimmedMass)[i] );

		rawHT += (*jetPt)[i];
		histos1D_[ "rawJetPt" ]->Fill( (*jetPt)[i], scale  );

		double jec = 1. / ( (*jecFactor)[i] * (*jetE)[i] );
		double nhf = (*neutralHadronEnergy)[i] * jec;
		double nEMf = (*neutralEmEnergy)[i] * jec;
		double cEMf = (*chargeEmEnergy)[i] * jec;
		double muf = (*muonEnergy)[i] * jec;
		//int npr = (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i] ;  //// REMEMBER TO INCLUDE # of constituents

		bool idL = ( (nhf<0.99) && (nEMf<0.99) && (muf<0.8) && (cEMf<0.9) );

		//if( !idL ) LogWarning("jetID") << (*jetPt)[i] << " " << jec << " " << nhf << " " << nEMf << " " << muf << " " << cEMf;

		if( (*jetPt)[i] > 150  && idL ) { 
			//LogWarning("jetInfo") << i << " " << (*jetPt)[i] << " " << (*jetEta)[i] << " " << (*jetPhi)[i] << " " << (*jetMass)[i];

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

			//if ( (*jetCSV)[i] > 0.244 ) bTagCSV = 1; 	// CSVL
			if ( (*jetCSV)[i] > 0.679 ) bTagCSV = 1; 	// CSVM
			//if ( (*jetCSVV1)[i] > 0.405 ) bTagCSV = 1; 	// CSVV1L
			//if ( (*jetCSVV1)[i] > 0.783 ) bTagCSV = 1; 	// CSVV1M

			JETtype tmpJET;
			tmpJET.p4 = tmpJet;
			tmpJET.subjet0 = tmpSubjet0;
			tmpJET.subjet1 = tmpSubjet1;
			tmpJET.mass = (*jetMass)[i];
			tmpJET.tau1 = (*jetTau1)[i];
			tmpJET.tau2 = (*jetTau2)[i];
			tmpJET.tau3 = (*jetTau3)[i];
			tmpJET.btagCSV = bTagCSV;
			JETS.push_back( tmpJET );
	   
			histos1D_[ "jetPt" ]->Fill( (*jetPt)[i], scale  );
			histos1D_[ "jetEta" ]->Fill( (*jetEta)[i], scale  );
			histos1D_[ "jetMass" ]->Fill( (*jetMass)[i], scale  );
		}
	}

	sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1.p4; tmpP2 = p2.p4;  return tmpP1.M() > tmpP2.M(); }); 
	histos1D_[ "jetNum" ]->Fill( numJets );
	histos1D_[ "NPV" ]->Fill( numPV );
	if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT, scale  );
	if ( rawHT > 0 ) histos1D_[ "rawHT" ]->Fill( rawHT, scale  );
	if ( HT > 700 ) cutHT = 1;
	sort(tmpTriggerMass.begin(), tmpTriggerMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	if ( ( tmpTriggerMass.size()> 0 ) && ( tmpTriggerMass[0] > 50) ) cutMass = 1;
	//LogWarning("mass") << tmpTriggerMass[0] << " " << tmpTriggerMass[1] ;
	tmpTriggerMass.clear();

	if( cutMass && cutHT ){
				
		cutmap["Trigger"] += 1;

		//if( ( numJets > 1 ) && ( HT > 700 ) ){
		if( ( numJets > 1 ) && ( HT > cutHTvalue ) ){
			cutmap["HT"] += 1;
			histos1D_[ "jetMass_cutHT_Ptsort" ]->Fill( (*jetMass)[0], scale );
			histos1D_[ "jetMass_cutHT" ]->Fill( JETS[0].mass, scale );

			double jet1Mass = JETS[0].mass;
			double jet2Mass = JETS[1].mass;
			double massAve = ( jet1Mass + jet2Mass ) / 2.0;
			double massAsym = abs( jet1Mass - jet2Mass ) / ( jet1Mass + jet2Mass );

			histos1D_[ "massAsymmetry_cutHT" ]->Fill( massAsym, scale  );
			histos1D_[ "massAve_cutHT" ]->Fill( massAve, scale  );
			if( numPV < 25 )  histos1D_[ "massAveLowPU_cutHT" ]->Fill( massAve, scale  );
			else if( ( numPV > 25 ) && ( numPV < 35 ) )  histos1D_[ "massAveMedPU_cutHT" ]->Fill( massAve, scale  );
			else  histos1D_[ "massAveHighPU_cutHT" ]->Fill( massAve, scale  );
			histos2D_[ "massAvevsJet1Mass_cutHT" ]->Fill( massAve, jet1Mass );
			histos2D_[ "massAvevsJet2Mass_cutHT" ]->Fill( massAve, jet2Mass );
			histos2D_[ "jet1vs2Mass_cutHT" ]->Fill( jet1Mass, jet2Mass );

			TLorentzVector tmpJet1, tmpJet2, tmpCM;
			tmpJet1 = JETS[0].p4;
			tmpJet2 = JETS[1].p4;

			tmpCM = tmpJet1 + tmpJet2;
			//LogWarning("Jets") << tmpJet1.Eta() << " " << tmpJet2.Eta() << " " << tmpCM.Eta();
			tmpJet1.Boost( -tmpCM.BoostVector() );
			tmpJet2.Boost( -tmpCM.BoostVector() );
			//LogWarning("JetsBoost") << tmpJet1.Eta() << " " << tmpJet2.Eta();
			double cosThetaStar = TMath::Abs( ( tmpJet1.Px() * tmpCM.Px() +  tmpJet1.Py() * tmpCM.Py() + tmpJet1.Pz() * tmpCM.Pz() ) / (tmpJet1.E() * tmpCM.E() ) ) ;
			//LogWarning("cos theta") << cosThetaStar ;
			histos1D_[ "cosThetaStar_cutHT" ]->Fill( cosThetaStar, scale  );

			double jet1Tau21 = JETS[0].tau2 / JETS[0].tau1;
			double jet1Tau31 = JETS[0].tau3 / JETS[0].tau1;
			double jet1Tau32 = JETS[0].tau3 / JETS[0].tau2;
			histos1D_[ "jet1Tau1_cutHT" ]->Fill( JETS[0].tau1, scale );
			histos1D_[ "jet1Tau2_cutHT" ]->Fill( JETS[0].tau2, scale );
			histos1D_[ "jet1Tau3_cutHT" ]->Fill( JETS[0].tau3, scale );
			histos1D_[ "jet1Tau21_cutHT" ]->Fill( jet1Tau21, scale );
			histos1D_[ "jet1Tau31_cutHT" ]->Fill( jet1Tau31, scale );
			histos1D_[ "jet1Tau32_cutHT" ]->Fill( jet1Tau32, scale );
			histos2D_[ "dijetCorr_cutHT" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta() );
			histos2D_[ "dijetCorrPhi_cutHT" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi() );


			double jet1SubjetPtRatio = -999;
			double jet2SubjetPtRatio = -999;
			double jet1SubjetMass21Ratio = -999;
			double jet1Subjet112MassRatio = -999;
			double jet1Subjet1JetMassRatio = - 999;
			double jet1Subjet212MassRatio = - 999;
			double jet1Subjet2JetMassRatio = - 999;
			double jet2SubjetMass21Ratio = -999;
			double jet2Subjet112MassRatio = -999;
			double jet2Subjet1JetMassRatio = - 999;
			double jet2Subjet212MassRatio = - 999;
			double jet2Subjet2JetMassRatio = - 999;
			double cosPhi13412 = -9999;
			double cosPhi31234 = -9999;
			double tmpCosPhi13412 = -9999;
			double tmpCosPhi31234 = -9999;
			double dalitzY1 = -9999;
			double dalitzY2 = -9999;
			double dalitzY3 = -9999;
			double dalitzY4 = -9999;
			double dalitzY5 = -9999;
			double dalitzY6 = -9999;
			double dalitzX1 = -9999; 
			double dalitzX2 = -9999; 
			double dalitzX3 = -9999; 
			double dalitzX4 = -9999; 
			double dalitzX5 = -9999; 
			double dalitzX6 = -9999; 

			vector<double> jet1SubjetsMass, jet2SubjetsMass;
			jet1SubjetsMass.push_back( JETS[0].subjet0.M() );
			jet1SubjetsMass.push_back( JETS[0].subjet1.M() );
			sort( jet1SubjetsMass.begin(), jet1SubjetsMass.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
			double jet1subjet12Mass = ( JETS[0].subjet0 + JETS[0].subjet1).M();
			//LogWarning("subjet0") << jet1Mass << " " <<  jet1subjet12Mass;

			jet2SubjetsMass.push_back( JETS[1].subjet0.M() );
			jet2SubjetsMass.push_back( JETS[1].subjet1.M() );
			sort( jet2SubjetsMass.begin(), jet2SubjetsMass.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
			double jet2subjet12Mass = ( JETS[1].subjet0 + JETS[1].subjet1).M();

			vector<TLorentzVector> jet1SubjetsTLV, jet2SubjetsTLV;
			jet1SubjetsTLV.push_back( JETS[0].subjet0 );
			jet1SubjetsTLV.push_back( JETS[0].subjet1 );
			sort( jet1SubjetsTLV.begin(), jet1SubjetsTLV.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.M() > p2.M(); }); 
			jet2SubjetsTLV.push_back( JETS[1].subjet0 );
			jet2SubjetsTLV.push_back( JETS[1].subjet1 );
			sort( jet2SubjetsTLV.begin(), jet2SubjetsTLV.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.M() > p2.M(); }); 

			if( ( jet1SubjetsMass[1] > 0 ) && ( jet2SubjetsMass[1] > 0 ) ) {

				//LogWarning("subjet0") <<  jet1SubjetsTLV[0].Pt() << " " <<  jet1SubjetsTLV[1].Pt();
				jet1SubjetPtRatio = min( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() ) / max( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() );
				jet1SubjetMass21Ratio =  jet1SubjetsMass[1]/jet1SubjetsMass[0];
				jet1Subjet112MassRatio = jet1SubjetsMass[0]/jet1subjet12Mass;
				jet1Subjet1JetMassRatio = jet1SubjetsMass[0]/jet1Mass;
				jet1Subjet212MassRatio = jet1SubjetsMass[1]/jet1subjet12Mass;
				jet1Subjet2JetMassRatio = jet1SubjetsMass[1]/jet1Mass;

				histos1D_[ "jet1Subjet1Pt_cutHT" ]->Fill( jet1SubjetsTLV[0].Pt(), scale );
				histos1D_[ "jet1Subjet2Pt_cutHT" ]->Fill( jet1SubjetsTLV[1].Pt(), scale );
				histos1D_[ "jet1SubjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, scale );
				histos1D_[ "jet1Subjet1Mass_cutHT" ]->Fill( jet1SubjetsMass[0], scale );
				histos1D_[ "jet1Subjet2Mass_cutHT" ]->Fill( jet1SubjetsMass[1], scale );
				histos1D_[ "jet1SubjetMass21Ratio_cutHT" ]->Fill( jet1SubjetMass21Ratio, scale );
				histos1D_[ "jet1Subjet112MassRatio_cutHT" ]->Fill( jet1Subjet112MassRatio, scale );
				histos1D_[ "jet1Subjet1JetMassRatio_cutHT" ]->Fill( jet1Subjet1JetMassRatio, scale );
				histos1D_[ "jet1Subjet212MassRatio_cutHT" ]->Fill( jet1Subjet212MassRatio, scale );
				histos1D_[ "jet1Subjet2JetMassRatio_cutHT" ]->Fill( jet1Subjet2JetMassRatio, scale );
				histos2D_[ "jet1Subjet12Mass_cutHT" ]->Fill( jet1SubjetsMass[0], jet1SubjetsMass[1] );
				histos2D_[ "jet1Subjet112vs212MassRatio_cutHT" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio );
				histos2D_[ "jet1Subjet1JetvsSubjet2JetMassRatio_cutHT" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio );

				jet2SubjetPtRatio = min( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() ) / max( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() );
				jet2SubjetMass21Ratio =  jet2SubjetsMass[1]/jet2SubjetsMass[0];
				jet2Subjet112MassRatio = jet2SubjetsMass[0]/jet2subjet12Mass;
				jet2Subjet1JetMassRatio = jet2SubjetsMass[0]/jet2Mass;
				jet2Subjet212MassRatio = jet2SubjetsMass[1]/jet2subjet12Mass;
				jet2Subjet2JetMassRatio = jet2SubjetsMass[1]/jet2Mass;

				histos1D_[ "jet2Subjet1Pt_cutHT" ]->Fill( jet2SubjetsTLV[0].Pt(), scale );
				histos1D_[ "jet2Subjet2Pt_cutHT" ]->Fill( jet2SubjetsTLV[1].Pt(), scale );
				histos1D_[ "jet2SubjetPtRatio_cutHT" ]->Fill( jet2SubjetPtRatio, scale );
				histos1D_[ "jet2Subjet1Mass_cutHT" ]->Fill( jet2SubjetsMass[0], scale );
				histos1D_[ "jet2Subjet2Mass_cutHT" ]->Fill( jet2SubjetsMass[1], scale );
				histos1D_[ "jet2SubjetMass21Ratio_cutHT" ]->Fill( jet2SubjetMass21Ratio, scale );
				histos1D_[ "jet2Subjet112MassRatio_cutHT" ]->Fill( jet2Subjet112MassRatio, scale );
				histos1D_[ "jet2Subjet1JetMassRatio_cutHT" ]->Fill( jet2Subjet1JetMassRatio, scale );
				histos1D_[ "jet2Subjet212MassRatio_cutHT" ]->Fill( jet2Subjet212MassRatio, scale );
				histos1D_[ "jet2Subjet2JetMassRatio_cutHT" ]->Fill( jet2Subjet2JetMassRatio, scale );
				histos2D_[ "jet2Subjet12Mass_cutHT" ]->Fill( jet2SubjetsMass[0], jet2SubjetsMass[1] );
				histos2D_[ "jet2Subjet112vs212MassRatio_cutHT" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio );
				histos2D_[ "jet2Subjet1JetvsSubjet2JetMassRatio_cutHT" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio );

				histos1D_[ "subjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, scale );
				histos1D_[ "subjetPtRatio_cutHT" ]->Fill( jet2SubjetPtRatio, scale );
				histos1D_[ "subjetMass21Ratio_cutHT" ]->Fill( jet1SubjetMass21Ratio, scale );
				histos1D_[ "subjetMass21Ratio_cutHT" ]->Fill( jet2SubjetMass21Ratio, scale );
				histos1D_[ "subjet112MassRatio_cutHT" ]->Fill( jet1Subjet112MassRatio, scale );
				histos1D_[ "subjet112MassRatio_cutHT" ]->Fill( jet2Subjet112MassRatio, scale );
				histos1D_[ "subjet212MassRatio_cutHT" ]->Fill( jet1Subjet212MassRatio, scale );
				histos1D_[ "subjet212MassRatio_cutHT" ]->Fill( jet2Subjet212MassRatio, scale );
				histos2D_[ "subjet12Mass_cutHT" ]->Fill( jet1SubjetsMass[0], jet1SubjetsMass[1] );
				histos2D_[ "subjet12Mass_cutHT" ]->Fill( jet2SubjetsMass[0], jet2SubjetsMass[1] );
				histos2D_[ "subjet112vs212MassRatio_cutHT" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio );
				histos2D_[ "subjet112vs212MassRatio_cutHT" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio );
				histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutHT" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio );
				histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutHT" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio );
			

				double m1 = jet1SubjetsMass[0];
				double m2 = jet1SubjetsMass[1];
				double m3 = jet2SubjetsMass[0];
				double m4 = jet2SubjetsMass[1];

				double m12 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] ).M() ;
				double m34 = ( jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				double m134 = ( jet1SubjetsTLV[0] + jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				double m123 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] + jet2SubjetsTLV[0] ).M() ;
				double m124 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] + jet2SubjetsTLV[1] ).M() ;
				double m234 = ( jet1SubjetsTLV[1] + jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				double m1234 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] + jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				
				double tmpX1 = pow(m1234,2) * ( ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2) ) ;
				double tmpX2 = pow(m12,2) * ( pow(m134,2) - pow(m34,2) - pow(m1,2) );
				double tmpX3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
				double tmpX4 = ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2);
				double tmpX5 = pow(m12,2) * pow(m1,2);
				double tmpx1 = tmpX1 - (tmpX2/2);
				double tmpx2 = tmpX3 * ( pow(tmpX4,2) - tmpX5 );
				cosPhi13412 = TMath::Abs( tmpx1 / TMath::Sqrt( tmpx2 ) );
				histos1D_[ "subjetPolAngle13412_cutHT" ]->Fill( cosPhi13412 );

				double tmpY1 = pow(m1234,2) * ( ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2) ) ;
				double tmpY2 = pow(m34,2) * ( pow(m123,2) - pow(m12,2) - pow(m3,2) );
				double tmpY3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
				double tmpY4 = ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2);
				double tmpY5 = pow(m34,2) * pow(m3,2);
				double tmpy1 = tmpY1 - (tmpY2/2);
				double tmpy2 = tmpY3 * ( pow(tmpY4,2) - tmpY5 );
				cosPhi31234 = TMath::Abs( tmpy1 / TMath::Sqrt( tmpy2 ) );
				histos1D_[ "subjetPolAngle31234_cutHT" ]->Fill( cosPhi31234 );
				histos2D_[ "subjetPolAngle13412vs31234_cutHT" ]->Fill( cosPhi13412, cosPhi31234 );

				//// THIS IS A TEST
				double M12 = jet1Mass;
				double M34 = jet2Mass;
				double M134 = ( jet1SubjetsTLV[0] + JETS[1].p4 ).M();
				double M123 = ( jet2SubjetsTLV[0] + JETS[0].p4 ).M();
				//double M234 = ( jet1SubjetsTLV[1] + JETS[1].p4 ).M();
				double M1234 = ( JETS[0].p4 + JETS[1].p4 ).M();

				double tmpZ1 = pow(M1234,2) * ( ( 2 * ( pow(M12,2) + pow(m1,2) ) ) - pow(m2,2) ) ;
				double tmpZ2 = pow(M12,2) * ( pow(M134,2) - pow(M34,2) - pow(m1,2) );
				double tmpZ3 = pow(M1234,4) - ( pow(M12,2) * pow(M34,2) ) ; 
				double tmpZ4 = ( 2 * ( pow(M12,2) + pow(m1,2) ) ) - pow(m2,2);
				double tmpZ5 = pow(M12,2) * pow(m1,2);
				double tmpz1 = tmpZ1 - (tmpZ2/2);
				double tmpz2 = tmpZ3 * ( pow(tmpZ4,2) - tmpZ5 );
				tmpCosPhi13412 = TMath::Abs( tmpz1 / sqrt( tmpz2 ) );
				histos1D_[ "tmpSubjetPolAngle13412_cutHT" ]->Fill( tmpCosPhi13412 );

				double tmpW1 = pow(M1234,2) * ( ( 2 * ( pow(M34,2) + pow(m3,2) ) ) - pow(m4,2) ) ;
				double tmpW2 = pow(M34,2) * ( pow(M123,2) - pow(M12,2) - pow(m3,2) );
				double tmpW3 = pow(M1234,4) - ( pow(M12,2) * pow(M34,2) ) ; 
				double tmpW4 = ( 2 * ( pow(M34,2) + pow(m3,2) ) ) - pow(m4,2);
				double tmpW5 = pow(M34,2) * pow(m3,2);
				double tmpw1 = tmpW1 - (tmpW2/2);
				double tmpw2 = tmpW3 * ( pow(tmpW4,2) - tmpW5 );
				tmpCosPhi31234 = TMath::Abs( tmpw1 / sqrt( tmpw2 ) );
				histos1D_[ "tmpSubjetPolAngle31234_cutHT" ]->Fill( tmpCosPhi31234 );
				histos2D_[ "tmpSubjetPolAngle13412vs31234_cutHT" ]->Fill( tmpCosPhi13412, tmpCosPhi31234 );

				//////////////////////////////////
				

				vector<double> dalitz1, Dalitz1, dalitz2, Dalitz2;
				double tmptilde = pow( m1, 2 ) + pow( m2, 2) + pow( m34, 2 ) + pow( m1234, 2);
				double mtilde12 = pow( m12, 2 ) / tmptilde;
				double mtilde134 = pow( m134, 2 ) / tmptilde;
				double mtilde234 = pow( m234, 2 ) / tmptilde;
				//double tmpMtilde = mtilde12 + mtilde134 + mtilde234;
				//LogWarning("test") << tmpMtilde << " " << tmptilde << " " << mtilde12 << " " << mtilde134 << " " <<  mtilde234;
				dalitz1.push_back( mtilde12 );
				dalitz1.push_back( mtilde134 );
				dalitz1.push_back( mtilde234 );
				sort( dalitz1.begin(), dalitz1.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
				//LogWarning("mus") << mtilde12 << " " << mtilde134 << " " << mtilde234 << " " << dalitz1[0] << " " << dalitz1[1] << " " << dalitz1[2];
				histos1D_[ "mu1_cutHT" ]->Fill( dalitz1[0], scale );
				histos1D_[ "mu2_cutHT" ]->Fill( dalitz1[1], scale );
				histos1D_[ "mu3_cutHT" ]->Fill( dalitz1[2], scale );
				histos2D_[ "mu1234_cutHT" ]->Fill( dalitz1[0], dalitz1[2] );
				histos2D_[ "mu1234_cutHT" ]->Fill( dalitz1[1], dalitz1[2] );
				histos2D_[ "mu1234_cutHT" ]->Fill( dalitz1[0], dalitz1[1] );

				/// (a,b) = (mu1, mu2)
				dalitzY1 = dalitz1[1];
				dalitzX1 = ( dalitzY1 / TMath::Sqrt(3) ) + ( ( 2 / TMath::Sqrt(3) ) * dalitz1[0] );
				histos2D_[ "dalitz1234_cutHT" ]->Fill( dalitzX1, dalitzY1 );

				/// (a,b) = (mu1, mu3)
				dalitzY2 = dalitz1[2];
				dalitzX2 = ( dalitzY2 / TMath::Sqrt(3) ) + ( ( 2 / TMath::Sqrt(3) ) * dalitz1[0] );
				histos2D_[ "dalitz1234_cutHT" ]->Fill( dalitzX2, dalitzY2 );

				/// (a,b) = (mu2, mu3)
				dalitzY3 = dalitz1[2];
				dalitzX3 = ( dalitzY3 / TMath::Sqrt(3) ) + ( ( 2 / TMath::Sqrt(3) ) * dalitz1[1] );
				histos2D_[ "dalitz1234_cutHT" ]->Fill( dalitzX3, dalitzY3 );
				LogWarning("dalitz") << dalitzX1 << " " << dalitzY1 << " " << dalitzX2 << " " << dalitzY2 << " " << dalitzX3 << " " << dalitzY3;



				double mtilde34 = pow( m34, 2 ) / tmptilde;
				double mtilde123 = pow( m123, 2 ) / tmptilde;
				double mtilde124 = pow( m124, 2 ) / tmptilde;
				dalitz2.push_back( mtilde34 );
				dalitz2.push_back( mtilde123 );
				dalitz2.push_back( mtilde124 );
				sort( dalitz2.begin(), dalitz2.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
				histos1D_[ "mu4_cutHT" ]->Fill( dalitz2[0], scale );
				histos1D_[ "mu5_cutHT" ]->Fill( dalitz2[1], scale );
				histos1D_[ "mu6_cutHT" ]->Fill( dalitz2[2], scale );
				histos2D_[ "mu3412_cutHT" ]->Fill( dalitz2[0], dalitz2[2] );
				histos2D_[ "mu3412_cutHT" ]->Fill( dalitz2[1], dalitz2[2] );
				histos2D_[ "mu3412_cutHT" ]->Fill( dalitz2[0], dalitz2[1] );

				/// (a,b) = (mu1, mu2)
				dalitzY4 = dalitz2[0];
				dalitzX4 = ( dalitzY4 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz2[1] );
				histos2D_[ "dalitz3412_cutHT" ]->Fill( dalitzY4, dalitzX4 );

				/// (a,b) = (mu1, mu3)
				dalitzY5 = dalitz2[0];
				dalitzX5 = ( dalitzY5 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz2[2] );
				histos2D_[ "dalitz3412_cutHT" ]->Fill( dalitzY5, dalitzX5 );

				/// (a,b) = (mu2, mu3)
				dalitzY6 = dalitz2[1];
				dalitzX6 = ( dalitzY6 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz2[2] );
				histos2D_[ "dalitz3412_cutHT" ]->Fill( dalitzY6, dalitzX6 );


			}


			//if( massAsym < 0.1 ){
			if( massAsym < cutAsymvalue ){
				cutmap["Asymmetry"] += 1;
				histos1D_[ "massAve_cutAsym" ]->Fill( massAve, scale  );
				if( numPV < 25 )  histos1D_[ "massAveLowPU_cutAsym" ]->Fill( massAve, scale  );
				else if( ( numPV > 25 ) && ( numPV < 35 ) )  histos1D_[ "massAveMedPU_cutAsym" ]->Fill( massAve, scale  );
				else  histos1D_[ "massAveHighPU_cutAsym" ]->Fill( massAve, scale  );
				histos1D_[ "cosThetaStar_cutAsym" ]->Fill( cosThetaStar, scale  );
				histos1D_[ "jet1Tau21_cutAsym" ]->Fill( jet1Tau21, scale  );
				histos1D_[ "jet1Tau31_cutAsym" ]->Fill( jet1Tau31, scale  );
				histos1D_[ "jet1Tau32_cutAsym" ]->Fill( jet1Tau32, scale  );
				histos2D_[ "dijetCorr_cutAsym" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta() );
				histos2D_[ "dijetCorrPhi_cutAsym" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi() );
				histos1D_[ "subjetPtRatio_cutAsym" ]->Fill( jet1SubjetPtRatio, scale );
				histos1D_[ "subjetPtRatio_cutAsym" ]->Fill( jet2SubjetPtRatio, scale );
				histos1D_[ "subjetMass21Ratio_cutAsym" ]->Fill( jet1SubjetMass21Ratio, scale );
				histos1D_[ "subjetMass21Ratio_cutAsym" ]->Fill( jet2SubjetMass21Ratio, scale );
				histos1D_[ "subjet112MassRatio_cutAsym" ]->Fill( jet1Subjet112MassRatio, scale );
				histos1D_[ "subjet112MassRatio_cutAsym" ]->Fill( jet2Subjet112MassRatio, scale );
				histos1D_[ "subjet212MassRatio_cutAsym" ]->Fill( jet1Subjet212MassRatio, scale );
				histos1D_[ "subjet212MassRatio_cutAsym" ]->Fill( jet2Subjet212MassRatio, scale );
				histos1D_[ "subjetPolAngle13412_cutAsym" ]->Fill( cosPhi13412 );
				histos1D_[ "subjetPolAngle31234_cutAsym" ]->Fill( cosPhi31234 );
				histos1D_[ "tmpSubjetPolAngle13412_cutAsym" ]->Fill( tmpCosPhi13412 );
				histos1D_[ "tmpSubjetPolAngle31234_cutAsym" ]->Fill( tmpCosPhi31234 );
				histos2D_[ "subjet12Mass_cutAsym" ]->Fill( jet1SubjetsMass[0], jet1SubjetsMass[1] );
				histos2D_[ "subjet12Mass_cutAsym" ]->Fill( jet2SubjetsMass[0], jet2SubjetsMass[1] );
				histos2D_[ "subjet112vs212MassRatio_cutAsym" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio );
				histos2D_[ "subjet112vs212MassRatio_cutAsym" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio );
				histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio );
				histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio );
				histos2D_[ "subjetPolAngle13412vs31234_cutAsym" ]->Fill( cosPhi13412, cosPhi31234 );
				histos2D_[ "tmpSubjetPolAngle13412vs31234_cutAsym" ]->Fill( tmpCosPhi13412, tmpCosPhi31234 );
				histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzY1, dalitzX1 );
				histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzY2, dalitzX2 );
				histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzY3, dalitzX3 );
				histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY4, dalitzX4 );
				histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY5, dalitzX5 );
				histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY6, dalitzX6 );

				//if( TMath::Abs( cosThetaStar ) < 0.3 ){
				if( TMath::Abs( cosThetaStar ) < cutCosThetavalue ){
					cutmap["CosTheta"] += 1;
					histos1D_[ "massAve_cutCosTheta" ]->Fill( massAve, scale  );
					if( numPV < 25 )  histos1D_[ "massAveLowPU_cutCosTheta" ]->Fill( massAve, scale  );
					else if( ( numPV > 25 ) && ( numPV < 35 ) )  histos1D_[ "massAveMedPU_cutCosTheta" ]->Fill( massAve, scale  );
					else  histos1D_[ "massAveHighPU_cutCosTheta" ]->Fill( massAve, scale  );
					histos1D_[ "jet1Tau21_cutCosTheta" ]->Fill( jet1Tau21, scale  );
					histos1D_[ "jet1Tau31_cutCosTheta" ]->Fill( jet1Tau31, scale  );
					histos1D_[ "jet1Tau32_cutCosTheta" ]->Fill( jet1Tau32, scale  );
					histos2D_[ "dijetCorr_cutCosTheta" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta() );
					histos2D_[ "dijetCorrPhi_cutCosTheta" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi() );
					histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet1SubjetPtRatio, scale );
					histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet2SubjetPtRatio, scale );
					histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet1SubjetPtRatio, scale );
					histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet2SubjetPtRatio, scale );
					histos1D_[ "subjetMass21Ratio_cutCosTheta" ]->Fill( jet1SubjetMass21Ratio, scale );
					histos1D_[ "subjetMass21Ratio_cutCosTheta" ]->Fill( jet2SubjetMass21Ratio, scale );
					histos1D_[ "subjet112MassRatio_cutCosTheta" ]->Fill( jet1Subjet112MassRatio, scale );
					histos1D_[ "subjet112MassRatio_cutCosTheta" ]->Fill( jet2Subjet112MassRatio, scale );
					histos1D_[ "subjet212MassRatio_cutCosTheta" ]->Fill( jet1Subjet212MassRatio, scale );
					histos1D_[ "subjet212MassRatio_cutCosTheta" ]->Fill( jet2Subjet212MassRatio, scale );
					histos1D_[ "subjetPolAngle13412_cutCosTheta" ]->Fill( cosPhi13412 );
					histos1D_[ "subjetPolAngle31234_cutCosTheta" ]->Fill( cosPhi31234 );
					histos1D_[ "tmpSubjetPolAngle13412_cutCosTheta" ]->Fill( tmpCosPhi13412 );
					histos1D_[ "tmpSubjetPolAngle31234_cutCosTheta" ]->Fill( tmpCosPhi31234 );
					histos2D_[ "subjet12Mass_cutCosTheta" ]->Fill( jet1SubjetsMass[0], jet1SubjetsMass[1] );
					histos2D_[ "subjet12Mass_cutCosTheta" ]->Fill( jet2SubjetsMass[0], jet2SubjetsMass[1] );
					histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio );
					histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio );
					histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio );
					histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio );
					histos2D_[ "subjetPolAngle13412vs31234_cutCosTheta" ]->Fill( cosPhi13412, cosPhi31234 );
					histos2D_[ "tmpSubjetPolAngle13412vs31234_cutCosTheta" ]->Fill( tmpCosPhi13412, tmpCosPhi31234 );
					histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzY1, dalitzX1 );
					histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzY2, dalitzX2 );
					histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzY3, dalitzX3 );
					histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY4, dalitzX4 );
					histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY5, dalitzX5 );
					histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY6, dalitzX6 );

					if( ( jet1SubjetPtRatio > cutSubjetPtRatiovalue ) && ( jet2SubjetPtRatio > cutSubjetPtRatiovalue ) ){
					//if( ( jet1SubjetPtRatio > 0.3 ) && ( jet2SubjetPtRatio > 0.3 ) ){
						cutmap["SubjetPtRatio"] += 1;
						//massAveForFit = massAve;
						histos1D_[ "massAve_cutSubjetPtRatio" ]->Fill( massAve, scale  );
						if( numPV < 25 )  histos1D_[ "massAveLowPU_cutSubjetPtRatio" ]->Fill( massAve, scale  );
						else if( ( numPV > 25 ) && ( numPV < 35 ) )  histos1D_[ "massAveMedPU_cutSubjetPtRatio" ]->Fill( massAve, scale  );
						else  histos1D_[ "massAveHighPU_cutSubjetPtRatio" ]->Fill( massAve, scale  );
						histos1D_[ "jet1Tau21_cutSubjetPtRatio" ]->Fill( jet1Tau21, scale  );
						histos1D_[ "jet1Tau31_cutSubjetPtRatio" ]->Fill( jet1Tau31, scale  );
						histos1D_[ "jet1Tau32_cutSubjetPtRatio" ]->Fill( jet1Tau32, scale  );
						histos2D_[ "dijetCorr_cutSubjetPtRatio" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta() );
						histos2D_[ "dijetCorrPhi_cutSubjetPtRatio" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi() );
						histos1D_[ "subjetMass21Ratio_cutSubjetPtRatio" ]->Fill( jet1SubjetMass21Ratio, scale );
						histos1D_[ "subjetMass21Ratio_cutSubjetPtRatio" ]->Fill( jet2SubjetMass21Ratio, scale );
						histos1D_[ "subjet112MassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet112MassRatio, scale );
						histos1D_[ "subjet112MassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet112MassRatio, scale );
						histos1D_[ "subjet212MassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet212MassRatio, scale );
						histos1D_[ "subjet212MassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet212MassRatio, scale );
						histos1D_[ "subjetPolAngle13412_cutSubjetPtRatio" ]->Fill( cosPhi13412 );
						histos1D_[ "subjetPolAngle31234_cutSubjetPtRatio" ]->Fill( cosPhi31234 );
						histos1D_[ "tmpSubjetPolAngle13412_cutSubjetPtRatio" ]->Fill( tmpCosPhi13412 );
						histos1D_[ "tmpSubjetPolAngle31234_cutSubjetPtRatio" ]->Fill( tmpCosPhi31234 );
						histos2D_[ "subjet12Mass_cutSubjetPtRatio" ]->Fill( jet1SubjetsMass[0], jet1SubjetsMass[1] );
						histos2D_[ "subjet12Mass_cutSubjetPtRatio" ]->Fill( jet2SubjetsMass[0], jet2SubjetsMass[1] );
						histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio );
						histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio );
						histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio );
						histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio );
						histos2D_[ "subjetPolAngle13412vs31234_cutSubjetPtRatio" ]->Fill( cosPhi13412, cosPhi31234 );
						histos2D_[ "tmpSubjetPolAngle13412vs31234_cutSubjetPtRatio" ]->Fill( tmpCosPhi13412, tmpCosPhi31234 );
						histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzY1, dalitzX1 );
						histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzY2, dalitzX2 );
						histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzY3, dalitzX3 );
						histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY4, dalitzX4 );
						histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY5, dalitzX5 );
						histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY6, dalitzX6 );

						if ( JETS[0].btagCSV || JETS[1].btagCSV ){
							//LogWarning("btag") <<JETS[0].btagCSV << " " << JETS[1].btagCSV;
							cutmap["btagAfterSubjetPtRatio"] += 1;
							histos1D_[ "massAve_cutBtagAfterSubjetPtRatio" ]->Fill( massAve, scale  );
						}
					}

					if( jet1Tau31 < cutTau31value ){
					//if(  jet1Tau31 < 0.5 ){
						cutmap["Tau31"] += 1;
						histos1D_[ "massAve_cutTau31" ]->Fill( massAve, scale  );
						histos2D_[ "dijetCorr_cutTau31" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta() );
						histos2D_[ "dijetCorrPhi_cutTau31" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi() );
						histos1D_[ "subjetMass21Ratio_cutTau31" ]->Fill( jet1SubjetMass21Ratio, scale );
						histos1D_[ "subjetMass21Ratio_cutTau31" ]->Fill( jet2SubjetMass21Ratio, scale );
						histos1D_[ "subjet112MassRatio_cutTau31" ]->Fill( jet1Subjet112MassRatio, scale );
						histos1D_[ "subjet112MassRatio_cutTau31" ]->Fill( jet2Subjet112MassRatio, scale );
						histos1D_[ "subjet212MassRatio_cutTau31" ]->Fill( jet1Subjet212MassRatio, scale );
						histos1D_[ "subjet212MassRatio_cutTau31" ]->Fill( jet2Subjet212MassRatio, scale );
						histos1D_[ "subjetPolAngle13412_cutTau31" ]->Fill( cosPhi13412 );
						histos1D_[ "subjetPolAngle31234_cutTau31" ]->Fill( cosPhi31234 );
						histos1D_[ "tmpSubjetPolAngle13412_cutTau31" ]->Fill( tmpCosPhi13412 );
						histos1D_[ "tmpSubjetPolAngle31234_cutTau31" ]->Fill( tmpCosPhi31234 );
						histos2D_[ "subjet12Mass_cutTau31" ]->Fill( jet1SubjetsMass[0], jet1SubjetsMass[1] );
						histos2D_[ "subjet12Mass_cutTau31" ]->Fill( jet2SubjetsMass[0], jet2SubjetsMass[1] );
						histos2D_[ "subjet112vs212MassRatio_cutTau31" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio );
						histos2D_[ "subjet112vs212MassRatio_cutTau31" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio );
						histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio );
						histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio );
						histos2D_[ "subjetPolAngle13412vs31234_cutTau31" ]->Fill( cosPhi13412, cosPhi31234 );
						histos2D_[ "tmpSubjetPolAngle13412vs31234_cutTau31" ]->Fill( tmpCosPhi13412, tmpCosPhi31234 );

						if ( JETS[0].btagCSV || JETS[1].btagCSV ){
							//LogWarning("btag") <<JETS[0].btagCSV << " " << JETS[1].btagCSV;
							cutmap["btagAfterTau31"] += 1;
							histos1D_[ "massAve_cutBtagAfterTau31" ]->Fill( massAve, scale  );
						}
					}

					//if(  jet1Tau21 < 0.6 ){
					if(  jet1Tau21 < cutTau21value ){
						cutmap["Tau21"] += 1;
						histos1D_[ "massAve_cutTau21" ]->Fill( massAve, scale  );
						histos2D_[ "subjet12Mass_cutTau21" ]->Fill( jet1SubjetsMass[0], jet1SubjetsMass[1] );
						histos2D_[ "subjet12Mass_cutTau21" ]->Fill( jet2SubjetsMass[0], jet2SubjetsMass[1] );
						if ( JETS[0].btagCSV || JETS[1].btagCSV ){
							//LogWarning("btag") <<JETS[0].btagCSV << " " << JETS[1].btagCSV;
							cutmap["btagAfterTau21"] += 1;
							histos1D_[ "massAve_cutBtagAfterTau21" ]->Fill( massAve, scale  );
						}
					} 
				}
			}
		}
	}
	JETS.clear();
	//RUNAtree->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNAnalysis::beginJob() {

	//RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
	//RUNAtree->Branch( "massAveForFit", &massAveForFit,"massAveForFit/F");

	histos1D_[ "rawJetPt" ] = fs_->make< TH1D >( "rawJetPt", "rawJetPt", 100, 0., 1000. );
	histos1D_[ "rawJetPt" ]->Sumw2();
	histos1D_[ "rawHT" ] = fs_->make< TH1D >( "rawHT", "rawHT", 150, 0., 1500. );
	histos1D_[ "rawHT" ]->Sumw2();

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
	histos1D_[ "NPV" ] = fs_->make< TH1D >( "NPV", "NPV", 80, 0., 80. );
	histos1D_[ "NPV" ]->Sumw2();

	histos1D_[ "jetMass_cutHT_Ptsort" ] = fs_->make< TH1D >( "jetMass_cutHT_Ptsort", "jetMass_cutHT_Ptsort", 30, 0., 300. );
	histos1D_[ "jetMass_cutHT_Ptsort" ]->Sumw2();
	histos1D_[ "jetMass_cutHT" ] = fs_->make< TH1D >( "jetMass_cutHT", "jetMass_cutHT", 30, 0., 300. );
	histos1D_[ "jetMass_cutHT" ]->Sumw2();
	histos1D_[ "massAsymmetry_cutHT" ] = fs_->make< TH1D >( "massAsymmetry_cutHT", "massAsymmetry_cutHT", 20, 0., 1. );
	histos1D_[ "massAsymmetry_cutHT" ]->Sumw2();
	histos1D_[ "massAve_cutHT" ] = fs_->make< TH1D >( "massAve_cutHT", "massAve_cutHT", 30, 0., 300. );
	histos1D_[ "massAve_cutHT" ]->Sumw2();
	histos1D_[ "massAveLowPU_cutHT" ] = fs_->make< TH1D >( "massAveLowPU_cutHT", "massAveLowPU_cutHT", 30, 0., 300. );
	histos1D_[ "massAveLowPU_cutHT" ]->Sumw2();
	histos1D_[ "massAveMedPU_cutHT" ] = fs_->make< TH1D >( "massAveMedPU_cutHT", "massAveMedPU_cutHT", 30, 0., 300. );
	histos1D_[ "massAveMedPU_cutHT" ]->Sumw2();
	histos1D_[ "massAveHighPU_cutHT" ] = fs_->make< TH1D >( "massAveHighPU_cutHT", "massAveHighPU_cutHT", 30, 0., 300. );
	histos1D_[ "massAveHighPU_cutHT" ]->Sumw2();
	histos2D_[ "massAvevsJet1Mass_cutHT" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutHT", "massAvevsJet1Mass_cutHT", 30, 0., 300., 30, 0., 300. );
	histos2D_[ "massAvevsJet1Mass_cutHT" ]->Sumw2();
	histos2D_[ "massAvevsJet2Mass_cutHT" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutHT", "massAvevsJet2Mass_cutHT", 30, 0., 300., 30, 0., 300. );
	histos2D_[ "massAvevsJet2Mass_cutHT" ]->Sumw2();
	histos2D_[ "jet1vs2Mass_cutHT" ] = fs_->make< TH2D >( "jet1vs2Mass_cutHT", "jet1vs2Mass_cutHT", 30, 0., 300., 30, 0., 300. );
	histos2D_[ "jet1vs2Mass_cutHT" ]->Sumw2();
	histos1D_[ "cosThetaStar_cutHT" ] = fs_->make< TH1D >( "cosThetaStar_cutHT", "cosThetaStar_cutHT", 20, 0., 1. );
	histos1D_[ "cosThetaStar_cutHT" ]->Sumw2();
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
	histos1D_[ "jet1SubjetMass21Ratio_cutHT" ] = fs_->make< TH1D >( "jet1SubjetMass21Ratio_cutHT", "jet1SubjetMass21Ratio_cutHT", 20, 0., 1. );
	histos1D_[ "jet1SubjetMass21Ratio_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet112MassRatio_cutHT" ] = fs_->make< TH1D >( "jet1Subjet112MassRatio_cutHT", "jet1Subjet112MassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Subjet112MassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet1JetMassRatio_cutHT" ] = fs_->make< TH1D >( "jet1Subjet1JetMassRatio_cutHT", "jet1Subjet1JetMassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Subjet1JetMassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet212MassRatio_cutHT" ] = fs_->make< TH1D >( "jet1Subjet212MassRatio_cutHT", "jet1Subjet212MassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Subjet212MassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet2JetMassRatio_cutHT" ] = fs_->make< TH1D >( "jet1Subjet2JetMassRatio_cutHT", "jet1Subjet2JetMassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Subjet2JetMassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet1Mass_cutHT" ] = fs_->make< TH1D >( "jet1Subjet1Mass_cutHT", "jet1Subjet1Mass_cutHT", 20, 0., 100. );
	histos1D_[ "jet1Subjet1Mass_cutHT" ]->Sumw2();
	histos1D_[ "jet1Subjet2Mass_cutHT" ] = fs_->make< TH1D >( "jet1Subjet2Mass_cutHT", "jet1Subjet2Mass_cutHT", 20, 0., 100. );
	histos1D_[ "jet1Subjet2Mass_cutHT" ]->Sumw2();
	histos2D_[ "jet1Subjet12Mass_cutHT" ] = fs_->make< TH2D >( "jet1Subjet12Mass_cutHT", "jet1Subjet12Mass_cutHT", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "jet1Subjet12Mass_cutHT" ]->Sumw2();
	histos2D_[ "jet1Subjet112vs212MassRatio_cutHT" ] = fs_->make< TH2D >( "jet1Subjet112vs212MassRatio_cutHT", "jet1Subjet112vs212MassRatio_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "jet1Subjet112vs212MassRatio_cutHT" ]->Sumw2();
	histos2D_[ "jet1Subjet1JetvsSubjet2JetMassRatio_cutHT" ] = fs_->make< TH2D >( "jet1Subjet1JetvsSubjet2JetMassRatio_cutHT", "jet1Subjet1JetvsSubjet2JetMassRatio_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "jet1Subjet1JetvsSubjet2JetMassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet1Pt_cutHT" ] = fs_->make< TH1D >( "jet2Subjet1Pt_cutHT", "jet2Subjet1Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet2Subjet1Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet2Pt_cutHT" ] = fs_->make< TH1D >( "jet2Subjet2Pt_cutHT", "jet2Subjet2Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet2Subjet2Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet2SubjetPtRatio_cutHT" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutHT", "jet2SubjetPtRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet2SubjetPtRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet2SubjetMass21Ratio_cutHT" ] = fs_->make< TH1D >( "jet2SubjetMass21Ratio_cutHT", "jet2SubjetMass21Ratio_cutHT", 20, 0., 1. );
	histos1D_[ "jet2SubjetMass21Ratio_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet112MassRatio_cutHT" ] = fs_->make< TH1D >( "jet2Subjet112MassRatio_cutHT", "jet2Subjet112MassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet2Subjet112MassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet1JetMassRatio_cutHT" ] = fs_->make< TH1D >( "jet2Subjet1JetMassRatio_cutHT", "jet2Subjet1JetMassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet2Subjet1JetMassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet212MassRatio_cutHT" ] = fs_->make< TH1D >( "jet2Subjet212MassRatio_cutHT", "jet2Subjet212MassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet2Subjet212MassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet2JetMassRatio_cutHT" ] = fs_->make< TH1D >( "jet2Subjet2JetMassRatio_cutHT", "jet2Subjet2JetMassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "jet2Subjet2JetMassRatio_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet1Mass_cutHT" ] = fs_->make< TH1D >( "jet2Subjet1Mass_cutHT", "jet2Subjet1Mass_cutHT", 20, 0., 100.);
	histos1D_[ "jet2Subjet1Mass_cutHT" ]->Sumw2();
	histos1D_[ "jet2Subjet2Mass_cutHT" ] = fs_->make< TH1D >( "jet2Subjet2Mass_cutHT", "jet2Subjet2Mass_cutHT", 20, 0., 100. );
	histos1D_[ "jet2Subjet2Mass_cutHT" ]->Sumw2();
	histos2D_[ "jet2Subjet12Mass_cutHT" ] = fs_->make< TH2D >( "jet2Subjet12Mass_cutHT", "jet2Subjet12Mass_cutHT", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "jet2Subjet12Mass_cutHT" ]->Sumw2();
	histos2D_[ "jet2Subjet112vs212MassRatio_cutHT" ] = fs_->make< TH2D >( "jet2Subjet112vs212MassRatio_cutHT", "jet2Subjet112vs212MassRatio_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "jet2Subjet112vs212MassRatio_cutHT" ]->Sumw2();
	histos2D_[ "jet2Subjet1JetvsSubjet2JetMassRatio_cutHT" ] = fs_->make< TH2D >( "jet2Subjet1JetvsSubjet2JetMassRatio_cutHT", "jet2Subjet1JetvsSubjet2JetMassRatio_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "jet2Subjet1JetvsSubjet2JetMassRatio_cutHT" ]->Sumw2();

	histos1D_[ "subjetPtRatio_cutHT" ] = fs_->make< TH1D >( "subjetPtRatio_cutHT", "subjetPtRatio_cutHT", 20, 0., 1. );
	histos1D_[ "subjetPtRatio_cutHT" ]->Sumw2();
	histos1D_[ "subjetMass21Ratio_cutHT" ] = fs_->make< TH1D >( "subjetMass21Ratio_cutHT", "subjetMass21Ratio_cutHT", 20, 0., 1. );
	histos1D_[ "subjetMass21Ratio_cutHT" ]->Sumw2();
	histos1D_[ "subjet112MassRatio_cutHT" ] = fs_->make< TH1D >( "subjet112MassRatio_cutHT", "subjet112MassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "subjet112MassRatio_cutHT" ]->Sumw2();
	histos1D_[ "subjet212MassRatio_cutHT" ] = fs_->make< TH1D >( "subjet212MassRatio_cutHT", "subjet212MassRatio_cutHT", 20, 0., 1. );
	histos1D_[ "subjet212MassRatio_cutHT" ]->Sumw2();
	histos2D_[ "subjet12Mass_cutHT" ] = fs_->make< TH2D >( "subjet12Mass_cutHT", "subjet12Mass_cutHT", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "subjet12Mass_cutHT" ]->Sumw2();
	histos2D_[ "dijetCorr_cutHT" ] = fs_->make< TH2D >( "dijetCorr_cutHT", "dijetCorr_cutHT", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorr_cutHT" ]->Sumw2();
	histos2D_[ "dijetCorrPhi_cutHT" ] = fs_->make< TH2D >( "dijetCorrPhi_cutHT", "dijetCorrPhi_cutHT", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorrPhi_cutHT" ]->Sumw2();
	histos2D_[ "subjet112vs212MassRatio_cutHT" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutHT", "subjet112vs212MassRatio_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet112vs212MassRatio_cutHT" ]->Sumw2();
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutHT" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutHT", "subjet1JetvsSubjet2JetMassRatio_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutHT" ]->Sumw2();
	histos1D_[ "subjetPolAngle13412_cutHT" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutHT", "subjetPolAngle13412_cutHT", 20, 0., 1. );
	histos1D_[ "subjetPolAngle13412_cutHT" ]->Sumw2();
	histos1D_[ "subjetPolAngle31234_cutHT" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutHT", "subjetPolAngle31234_cutHT", 20, 0., 1. );
	histos1D_[ "subjetPolAngle31234_cutHT" ]->Sumw2();
	histos2D_[ "subjetPolAngle13412vs31234_cutHT" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutHT", "subjetPolAngle13412vs31234_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjetPolAngle13412vs31234_cutHT" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle13412_cutHT" ] = fs_->make< TH1D >( "tmpSubjetPolAngle13412_cutHT", "tmpSubjetPolAngle13412_cutHT", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle13412_cutHT" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle31234_cutHT" ] = fs_->make< TH1D >( "tmpSubjetPolAngle31234_cutHT", "tmpSubjetPolAngle31234_cutHT", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle31234_cutHT" ]->Sumw2();
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutHT" ] = fs_->make< TH2D >( "tmpSubjetPolAngle13412vs31234_cutHT", "tmpSubjetPolAngle13412vs31234_cutHT", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutHT" ]->Sumw2();
	histos1D_[ "mu1_cutHT" ] = fs_->make< TH1D >( "mu1_cutHT", "mu1_cutHT", 40, 0., 1 );
	histos1D_[ "mu1_cutHT" ]->Sumw2();
	histos1D_[ "mu2_cutHT" ] = fs_->make< TH1D >( "mu2_cutHT", "mu2_cutHT", 40, 0., 1 );
	histos1D_[ "mu2_cutHT" ]->Sumw2();
	histos1D_[ "mu3_cutHT" ] = fs_->make< TH1D >( "mu3_cutHT", "mu3_cutHT", 40, 0., 1 );
	histos1D_[ "mu3_cutHT" ]->Sumw2();
	histos2D_[ "mu1234_cutHT" ] = fs_->make< TH2D >( "mu1234_cutHT", "mu1234_cutHT", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "mu1234_cutHT" ]->Sumw2();
	histos2D_[ "dalitz1234_cutHT" ] = fs_->make< TH2D >( "dalitz1234_cutHT", "dalitz1234_cutHT", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz1234_cutHT" ]->Sumw2();
	histos1D_[ "mu4_cutHT" ] = fs_->make< TH1D >( "mu4_cutHT", "mu4_cutHT", 40, 0., 1 );
	histos1D_[ "mu4_cutHT" ]->Sumw2();
	histos1D_[ "mu5_cutHT" ] = fs_->make< TH1D >( "mu5_cutHT", "mu5_cutHT", 40, 0., 1 );
	histos1D_[ "mu5_cutHT" ]->Sumw2();
	histos1D_[ "mu6_cutHT" ] = fs_->make< TH1D >( "mu6_cutHT", "mu6_cutHT", 40, 0., 1 );
	histos1D_[ "mu6_cutHT" ]->Sumw2();
	histos2D_[ "mu3412_cutHT" ] = fs_->make< TH2D >( "mu3412_cutHT", "mu3412_cutHT", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "mu3412_cutHT" ]->Sumw2();
	histos2D_[ "dalitz3412_cutHT" ] = fs_->make< TH2D >( "dalitz3412_cutHT", "dalitz3412_cutHT", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz3412_cutHT" ]->Sumw2();

	histos1D_[ "massAve_cutAsym" ] = fs_->make< TH1D >( "massAve_cutAsym", "massAve_cutAsym", 30, 0., 300. );
	histos1D_[ "massAve_cutAsym" ]->Sumw2();
	histos1D_[ "massAveLowPU_cutAsym" ] = fs_->make< TH1D >( "massAveLowPU_cutAsym", "massAveLowPU_cutAsym", 30, 0., 300. );
	histos1D_[ "massAveLowPU_cutAsym" ]->Sumw2();
	histos1D_[ "massAveMedPU_cutAsym" ] = fs_->make< TH1D >( "massAveMedPU_cutAsym", "massAveMedPU_cutAsym", 30, 0., 300. );
	histos1D_[ "massAveMedPU_cutAsym" ]->Sumw2();
	histos1D_[ "massAveHighPU_cutAsym" ] = fs_->make< TH1D >( "massAveHighPU_cutAsym", "massAveHighPU_cutAsym", 30, 0., 300. );
	histos1D_[ "massAveHighPU_cutAsym" ]->Sumw2();
	histos1D_[ "cosThetaStar_cutAsym" ] = fs_->make< TH1D >( "cosThetaStar_cutAsym", "cosThetaStar_cutAsym", 20, 0., 1. );
	histos1D_[ "cosThetaStar_cutAsym" ]->Sumw2();
	histos1D_[ "jet1Tau21_cutAsym" ] = fs_->make< TH1D >( "jet1Tau21_cutAsym", "jet1Tau21_cutAsym", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutAsym" ]->Sumw2();
	histos1D_[ "jet1Tau31_cutAsym" ] = fs_->make< TH1D >( "jet1Tau31_cutAsym", "jet1Tau31_cutAsym", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutAsym" ]->Sumw2();
	histos1D_[ "jet1Tau32_cutAsym" ] = fs_->make< TH1D >( "jet1Tau32_cutAsym", "jet1Tau32_cutAsym", 20, 0., 1. );
	histos1D_[ "jet1Tau32_cutAsym" ]->Sumw2();
	histos1D_[ "subjetPtRatio_cutAsym" ] = fs_->make< TH1D >( "subjetPtRatio_cutAsym", "subjetPtRatio_cutAsym", 20, 0., 1. );
	histos1D_[ "subjetPtRatio_cutAsym" ]->Sumw2();
	histos1D_[ "subjetMass21Ratio_cutAsym" ] = fs_->make< TH1D >( "subjetMass21Ratio_cutAsym", "subjetMass21Ratio_cutAsym", 20, 0., 1. );
	histos1D_[ "subjetMass21Ratio_cutAsym" ]->Sumw2();
	histos1D_[ "subjet112MassRatio_cutAsym" ] = fs_->make< TH1D >( "subjet112MassRatio_cutAsym", "subjet112MassRatio_cutAsym", 20, 0., 1. );
	histos1D_[ "subjet112MassRatio_cutAsym" ]->Sumw2();
	histos1D_[ "subjet212MassRatio_cutAsym" ] = fs_->make< TH1D >( "subjet212MassRatio_cutAsym", "subjet212MassRatio_cutAsym", 20, 0., 1. );
	histos1D_[ "subjet212MassRatio_cutAsym" ]->Sumw2();
	histos1D_[ "subjetPolAngle13412_cutAsym" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutAsym", "subjetPolAngle13412_cutAsym", 20, 0., 1. );
	histos1D_[ "subjetPolAngle13412_cutAsym" ]->Sumw2();
	histos1D_[ "subjetPolAngle31234_cutAsym" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutAsym", "subjetPolAngle31234_cutAsym", 20, 0., 1. );
	histos1D_[ "subjetPolAngle31234_cutAsym" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle13412_cutAsym" ] = fs_->make< TH1D >( "tmpSubjetPolAngle13412_cutAsym", "tmpSubjetPolAngle13412_cutAsym", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle13412_cutAsym" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle31234_cutAsym" ] = fs_->make< TH1D >( "tmpSubjetPolAngle31234_cutAsym", "tmpSubjetPolAngle31234_cutAsym", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle31234_cutAsym" ]->Sumw2();
	histos2D_[ "subjet12Mass_cutAsym" ] = fs_->make< TH2D >( "subjet12Mass_cutAsym", "subjet12Mass_cutAsym", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "subjet12Mass_cutAsym" ]->Sumw2();
	histos2D_[ "dijetCorr_cutAsym" ] = fs_->make< TH2D >( "dijetCorr_cutAsym", "dijetCorr_cutAsym", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorr_cutAsym" ]->Sumw2();
	histos2D_[ "dijetCorrPhi_cutAsym" ] = fs_->make< TH2D >( "dijetCorrPhi_cutAsym", "dijetCorrPhi_cutAsym", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorrPhi_cutAsym" ]->Sumw2();
	histos2D_[ "subjet112vs212MassRatio_cutAsym" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutAsym", "subjet112vs212MassRatio_cutAsym", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet112vs212MassRatio_cutAsym" ]->Sumw2();
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutAsym", "subjet1JetvsSubjet2JetMassRatio_cutAsym", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ]->Sumw2();
	histos2D_[ "subjetPolAngle13412vs31234_cutAsym" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutAsym", "subjetPolAngle13412vs31234_cutAsym", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjetPolAngle13412vs31234_cutAsym" ]->Sumw2();
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutAsym" ] = fs_->make< TH2D >( "tmpSubjetPolAngle13412vs31234_cutAsym", "tmpSubjetPolAngle13412vs31234_cutAsym", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutAsym" ]->Sumw2();
	histos2D_[ "dalitz1234_cutAsym" ] = fs_->make< TH2D >( "dalitz1234_cutAsym", "dalitz1234_cutAsym", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz1234_cutAsym" ]->Sumw2();
	histos2D_[ "dalitz3412_cutAsym" ] = fs_->make< TH2D >( "dalitz3412_cutAsym", "dalitz3412_cutAsym", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz3412_cutAsym" ]->Sumw2();

	histos1D_[ "massAve_cutCosTheta" ] = fs_->make< TH1D >( "massAve_cutCosTheta", "massAve_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAve_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAveLowPU_cutCosTheta" ] = fs_->make< TH1D >( "massAveLowPU_cutCosTheta", "massAveLowPU_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAveLowPU_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAveMedPU_cutCosTheta" ] = fs_->make< TH1D >( "massAveMedPU_cutCosTheta", "massAveMedPU_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAveMedPU_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAveHighPU_cutCosTheta" ] = fs_->make< TH1D >( "massAveHighPU_cutCosTheta", "massAveHighPU_cutCosTheta", 30, 0., 300. );
	histos1D_[ "massAveHighPU_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1Tau21_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau21_cutCosTheta", "jet1Tau21_cutCosTheta", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1Tau31_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau31_cutCosTheta", "jet1Tau31_cutCosTheta", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1Tau32_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau32_cutCosTheta", "jet1Tau32_cutCosTheta", 20, 0., 1. );
	histos1D_[ "jet1Tau32_cutCosTheta" ]->Sumw2();
	histos1D_[ "subjetPtRatio_cutCosTheta" ] = fs_->make< TH1D >( "subjetPtRatio_cutCosTheta", "subjetPtRatio_cutCosTheta", 20, 0., 1. );
	histos1D_[ "subjetPtRatio_cutCosTheta" ]->Sumw2();
	histos1D_[ "subjetMass21Ratio_cutCosTheta" ] = fs_->make< TH1D >( "subjetMass21Ratio_cutCosTheta", "subjetMass21Ratio_cutCosTheta", 20, 0., 1. );
	histos1D_[ "subjetMass21Ratio_cutCosTheta" ]->Sumw2();
	histos1D_[ "subjet112MassRatio_cutCosTheta" ] = fs_->make< TH1D >( "subjet112MassRatio_cutCosTheta", "subjet112MassRatio_cutCosTheta", 20, 0., 1. );
	histos1D_[ "subjet112MassRatio_cutCosTheta" ]->Sumw2();
	histos1D_[ "subjet212MassRatio_cutCosTheta" ] = fs_->make< TH1D >( "subjet212MassRatio_cutCosTheta", "subjet212MassRatio_cutCosTheta", 20, 0., 1. );
	histos1D_[ "subjet212MassRatio_cutCosTheta" ]->Sumw2();
	histos1D_[ "subjetPolAngle13412_cutCosTheta" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutCosTheta", "subjetPolAngle13412_cutCosTheta", 20, 0., 1. );
	histos1D_[ "subjetPolAngle13412_cutCosTheta" ]->Sumw2();
	histos1D_[ "subjetPolAngle31234_cutCosTheta" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutCosTheta", "subjetPolAngle31234_cutCosTheta", 20, 0., 1. );
	histos1D_[ "subjetPolAngle31234_cutCosTheta" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle13412_cutCosTheta" ] = fs_->make< TH1D >( "tmpSubjetPolAngle13412_cutCosTheta", "tmpSubjetPolAngle13412_cutCosTheta", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle13412_cutCosTheta" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle31234_cutCosTheta" ] = fs_->make< TH1D >( "tmpSubjetPolAngle31234_cutCosTheta", "tmpSubjetPolAngle31234_cutCosTheta", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle31234_cutCosTheta" ]->Sumw2();
	histos2D_[ "subjet12Mass_cutCosTheta" ] = fs_->make< TH2D >( "subjet12Mass_cutCosTheta", "subjet12Mass_cutCosTheta", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "subjet12Mass_cutCosTheta" ]->Sumw2();
	histos2D_[ "dijetCorr_cutCosTheta" ] = fs_->make< TH2D >( "dijetCorr_cutCosTheta", "dijetCorr_cutCosTheta", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorr_cutCosTheta" ]->Sumw2();
	histos2D_[ "dijetCorrPhi_cutCosTheta" ] = fs_->make< TH2D >( "dijetCorrPhi_cutCosTheta", "dijetCorrPhi_cutCosTheta", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorrPhi_cutCosTheta" ]->Sumw2();
	histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutCosTheta", "subjet112vs212MassRatio_cutCosTheta", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ]->Sumw2();
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutCosTheta", "subjet1JetvsSubjet2JetMassRatio_cutCosTheta", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ]->Sumw2();
	histos2D_[ "subjetPolAngle13412vs31234_cutCosTheta" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutCosTheta", "subjetPolAngle13412vs31234_cutCosTheta", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjetPolAngle13412vs31234_cutCosTheta" ]->Sumw2();
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutCosTheta" ] = fs_->make< TH2D >( "tmpSubjetPolAngle13412vs31234_cutCosTheta", "tmpSubjetPolAngle13412vs31234_cutCosTheta", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutCosTheta" ]->Sumw2();
	histos2D_[ "dalitz1234_cutCosTheta" ] = fs_->make< TH2D >( "dalitz1234_cutCosTheta", "dalitz1234_cutCosTheta", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz1234_cutCosTheta" ]->Sumw2();
	histos2D_[ "dalitz3412_cutCosTheta" ] = fs_->make< TH2D >( "dalitz3412_cutCosTheta", "dalitz3412_cutCosTheta", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz3412_cutCosTheta" ]->Sumw2();

	histos1D_[ "massAve_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAve_cutSubjetPtRatio", "massAve_cutSubjetPtRatio", 30, 0., 300. );
	histos1D_[ "massAve_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "massAveLowPU_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAveLowPU_cutSubjetPtRatio", "massAveLowPU_cutSubjetPtRatio", 30, 0., 300. );
	histos1D_[ "massAveLowPU_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "massAveMedPU_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAveMedPU_cutSubjetPtRatio", "massAveMedPU_cutSubjetPtRatio", 30, 0., 300. );
	histos1D_[ "massAveMedPU_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "massAveHighPU_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAveHighPU_cutSubjetPtRatio", "massAveHighPU_cutSubjetPtRatio", 30, 0., 300. );
	histos1D_[ "massAveHighPU_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1Tau21_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1Tau21_cutSubjetPtRatio", "jet1Tau21_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1Tau31_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1Tau31_cutSubjetPtRatio", "jet1Tau31_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1Tau32_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1Tau32_cutSubjetPtRatio", "jet1Tau32_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "jet1Tau32_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "subjetMass21Ratio_cutSubjetPtRatio" ] = fs_->make< TH1D >( "subjetMass21Ratio_cutSubjetPtRatio", "subjetMass21Ratio_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "subjetMass21Ratio_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "subjet112MassRatio_cutSubjetPtRatio" ] = fs_->make< TH1D >( "subjet112MassRatio_cutSubjetPtRatio", "subjet112MassRatio_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "subjet112MassRatio_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "subjet212MassRatio_cutSubjetPtRatio" ] = fs_->make< TH1D >( "subjet212MassRatio_cutSubjetPtRatio", "subjet212MassRatio_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "subjet212MassRatio_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "subjetPolAngle13412_cutSubjetPtRatio" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutSubjetPtRatio", "subjetPolAngle13412_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "subjetPolAngle13412_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "subjetPolAngle31234_cutSubjetPtRatio" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutSubjetPtRatio", "subjetPolAngle31234_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "subjetPolAngle31234_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle13412_cutSubjetPtRatio" ] = fs_->make< TH1D >( "tmpSubjetPolAngle13412_cutSubjetPtRatio", "tmpSubjetPolAngle13412_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle13412_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle31234_cutSubjetPtRatio" ] = fs_->make< TH1D >( "tmpSubjetPolAngle31234_cutSubjetPtRatio", "tmpSubjetPolAngle31234_cutSubjetPtRatio", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle31234_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "subjet12Mass_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjet12Mass_cutSubjetPtRatio", "subjet12Mass_cutSubjetPtRatio", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "subjet12Mass_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "dijetCorr_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dijetCorr_cutSubjetPtRatio", "dijetCorr_cutSubjetPtRatio", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorr_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "dijetCorrPhi_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dijetCorrPhi_cutSubjetPtRatio", "dijetCorrPhi_cutSubjetPtRatio", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorrPhi_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutSubjetPtRatio", "subjet112vs212MassRatio_cutSubjetPtRatio", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio", "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "subjetPolAngle13412vs31234_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutSubjetPtRatio", "subjetPolAngle13412vs31234_cutSubjetPtRatio", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjetPolAngle13412vs31234_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutSubjetPtRatio" ] = fs_->make< TH2D >( "tmpSubjetPolAngle13412vs31234_cutSubjetPtRatio", "tmpSubjetPolAngle13412vs31234_cutSubjetPtRatio", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "dalitz1234_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dalitz1234_cutSubjetPtRatio", "dalitz1234_cutSubjetPtRatio", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "dalitz3412_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dalitz3412_cutSubjetPtRatio", "dalitz3412_cutSubjetPtRatio", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Sumw2();

	histos1D_[ "massAve_cutTau31" ] = fs_->make< TH1D >( "massAve_cutTau31", "massAve_cutTau31", 30, 0., 300. );
	histos1D_[ "massAve_cutTau31" ]->Sumw2();
	histos1D_[ "subjetMass21Ratio_cutTau31" ] = fs_->make< TH1D >( "subjetMass21Ratio_cutTau31", "subjetMass21Ratio_cutTau31", 20, 0., 1. );
	histos1D_[ "subjetMass21Ratio_cutTau31" ]->Sumw2();
	histos1D_[ "subjet112MassRatio_cutTau31" ] = fs_->make< TH1D >( "subjet112MassRatio_cutTau31", "subjet112MassRatio_cutTau31", 20, 0., 1. );
	histos1D_[ "subjet112MassRatio_cutTau31" ]->Sumw2();
	histos1D_[ "subjet212MassRatio_cutTau31" ] = fs_->make< TH1D >( "subjet212MassRatio_cutTau31", "subjet212MassRatio_cutTau31", 20, 0., 1. );
	histos1D_[ "subjet212MassRatio_cutTau31" ]->Sumw2();
	histos1D_[ "subjetPolAngle13412_cutTau31" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutTau31", "subjetPolAngle13412_cutTau31", 20, 0., 1. );
	histos1D_[ "subjetPolAngle13412_cutTau31" ]->Sumw2();
	histos1D_[ "subjetPolAngle31234_cutTau31" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutTau31", "subjetPolAngle31234_cutTau31", 20, 0., 1. );
	histos1D_[ "subjetPolAngle31234_cutTau31" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle13412_cutTau31" ] = fs_->make< TH1D >( "tmpSubjetPolAngle13412_cutTau31", "tmpSubjetPolAngle13412_cutTau31", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle13412_cutTau31" ]->Sumw2();
	histos1D_[ "tmpSubjetPolAngle31234_cutTau31" ] = fs_->make< TH1D >( "tmpSubjetPolAngle31234_cutTau31", "tmpSubjetPolAngle31234_cutTau31", 20, 0., 1. );
	histos1D_[ "tmpSubjetPolAngle31234_cutTau31" ]->Sumw2();
	histos2D_[ "subjet12Mass_cutTau31" ] = fs_->make< TH2D >( "subjet12Mass_cutTau31", "subjet12Mass_cutTau31", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "subjet12Mass_cutTau31" ]->Sumw2();
	histos2D_[ "dijetCorr_cutTau31" ] = fs_->make< TH2D >( "dijetCorr_cutTau31", "dijetCorr_cutTau31", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorr_cutTau31" ]->Sumw2();
	histos2D_[ "dijetCorrPhi_cutTau31" ] = fs_->make< TH2D >( "dijetCorrPhi_cutTau31", "dijetCorrPhi_cutTau31", 14, -3.5, 3.5, 14, -3.5, 3.5 );
	histos2D_[ "dijetCorrPhi_cutTau31" ]->Sumw2();
	histos2D_[ "subjet112vs212MassRatio_cutTau31" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutTau31", "subjet112vs212MassRatio_cutTau31", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet112vs212MassRatio_cutTau31" ]->Sumw2();
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutTau31", "subjet1JetvsSubjet2JetMassRatio_cutTau31", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ]->Sumw2();
	histos2D_[ "subjetPolAngle13412vs31234_cutTau31" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutTau31", "subjetPolAngle13412vs31234_cutTau31", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjetPolAngle13412vs31234_cutTau31" ]->Sumw2();
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutTau31" ] = fs_->make< TH2D >( "tmpSubjetPolAngle13412vs31234_cutTau31", "tmpSubjetPolAngle13412vs31234_cutTau31", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "tmpSubjetPolAngle13412vs31234_cutTau31" ]->Sumw2();

	histos1D_[ "massAve_cutTau21" ] = fs_->make< TH1D >( "massAve_cutTau21", "massAve_cutTau21", 30, 0., 300. );
	histos1D_[ "massAve_cutTau21" ]->Sumw2();
	histos2D_[ "subjet12Mass_cutTau21" ] = fs_->make< TH2D >( "subjet12Mass_cutTau21", "subjet12Mass_cutTau21", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "subjet12Mass_cutTau21" ]->Sumw2();

	histos1D_[ "massAve_cutBtagAfterSubjetPtRatio" ] = fs_->make< TH1D >( "massAve_cutBtagAfterSubjetPtRatio", "massAve_cutBtagAfterSubjetPtRatio", 30, 0., 300. );
	histos1D_[ "massAve_cutBtagAfterSubjetPtRatio" ]->Sumw2();
	histos1D_[ "massAve_cutBtagAfterTau31" ] = fs_->make< TH1D >( "massAve_cutBtagAfterTau31", "massAve_cutBtagAfterTau31", 30, 0., 300. );
	histos1D_[ "massAve_cutBtagAfterTau31" ]->Sumw2();
	histos1D_[ "massAve_cutBtagAfterTau21" ] = fs_->make< TH1D >( "massAve_cutBtagAfterTau21", "massAve_cutBtagAfterTau21", 30, 0., 300. );
	histos1D_[ "massAve_cutBtagAfterTau21" ]->Sumw2();

	cutLabels.push_back("Processed");
	cutLabels.push_back("Trigger");
	cutLabels.push_back("HT");
	cutLabels.push_back("Asymmetry");
	cutLabels.push_back("CosTheta");
	cutLabels.push_back("SubjetPtRatio");
	cutLabels.push_back("btagAfterSubjetPtRatio");
	cutLabels.push_back("Tau31");
	cutLabels.push_back("btagAfterTau31");
	cutLabels.push_back("Tau21");
	cutLabels.push_back("btagAfterTau21");
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
