// -*- C++ -*-
//
// Package:    RUNA/Ntuples
// Class:      RUNTriggerEfficiency
// 
/**\class RUNTriggerEfficiency RUNTriggerEfficiency.cc Ntuples/Ntuples/plugins/RUNTriggerEfficiency.cc

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
class RUNTriggerEfficiency : public EDAnalyzer {
   public:
      explicit RUNTriggerEfficiency(const ParameterSet&);
      ~RUNTriggerEfficiency();

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
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;

      bool bjSample;
      TString HLTtriggerOne;
      TString HLTtriggerTwo;
      double scale;
      /*double cutTrimmedMassvalue;
      double cutHTvalue;*/
      double cutjetPtvalue;
      double cutAsymvalue;
      double cutCosThetavalue;
      double cutSubjetPtRatiovalue;
      double cutTau31value;
      double cutTau21value;

      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;

      EDGetTokenT<vector<float>> ak4jetPt_;
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
RUNTriggerEfficiency::RUNTriggerEfficiency(const ParameterSet& iConfig):
//	getterOfProducts_(ProcessMatch(*), this) {
//	triggerBits_(consumes<TriggerResults>(iConfig.getParameter<InputTag>("bits"))),
	ak4jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("ak4jetPt"))),
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
	HLTtriggerOne = iConfig.getParameter<string>("HLTtriggerOne");
	HLTtriggerTwo = iConfig.getParameter<string>("HLTtriggerTwo");
	cutjetPtvalue = iConfig.getParameter<double>("cutjetPtvalue");
	cutAsymvalue = iConfig.getParameter<double>("cutAsymvalue");
	cutCosThetavalue = iConfig.getParameter<double>("cutCosThetavalue");
	cutSubjetPtRatiovalue = iConfig.getParameter<double>("cutSubjetPtRatiovalue");
	cutTau31value = iConfig.getParameter<double>("cutTau31value");
	cutTau21value = iConfig.getParameter<double>("cutTau21value");
}


RUNTriggerEfficiency::~RUNTriggerEfficiency()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNTriggerEfficiency::analyze(const Event& iEvent, const EventSetup& iSetup) {


	/*vector<Handle< vector<float> > > handles;
	getterOfProducts_.fillHandles(event, handles);
	*/

	Handle<vector<float> > ak4jetPt;
	iEvent.getByToken(ak4jetPt_, ak4jetPt);

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

	float triggerFiredOne = 0;
	float triggerFiredTwo = 0;
	for (size_t t = 0; t < triggerName->size(); t++) {
		//LogWarning("triggerbit") << (*triggerName)[t] << " " <<  (*triggerBit)[t];
		if ( TString( (*triggerName)[t] ).Contains( HLTtriggerOne ) ) {
			triggerFiredOne = (*triggerBit)[t];
			//LogWarning("triggerbit") << (*triggerName)[t] << " " <<  (*triggerBit)[t];
		}
		if ( TString( (*triggerName)[t] ).Contains( HLTtriggerTwo ) ) triggerFiredTwo = (*triggerBit)[t];
	}
	if ( HLTtriggerTwo.Contains( "NOTRIGGER" ) ) triggerFiredTwo = 1;
	if ( HLTtriggerOne.Contains( "NOTRIGGER" ) ) triggerFiredOne = 1;
	//LogWarning("BITS") << triggerFiredOne << " " << triggerFiredTwo;

	/// Applying kinematic, trigger and jet ID
	vector< JETtype > JETS;
	vector< float > tmpTriggerMass;
	bool bTagCSV = 0;
	float HT = 0;

	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		tmpTriggerMass.push_back( (*jetTrimmedMass)[i] );

		double jec = 1. / ( (*jecFactor)[i] * (*jetE)[i] );
		double nhf = (*neutralHadronEnergy)[i] * jec;
		double nEMf = (*neutralEmEnergy)[i] * jec;
		double cEMf = (*chargeEmEnergy)[i] * jec;
		double muf = (*muonEnergy)[i] * jec;
		//int npr = (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i] ;  //// REMEMBER TO INCLUDE # of constituents
		bool idL = ( (nhf<0.99) && (nEMf<0.99) && (muf<0.8) && (cEMf<0.9) );
		//if( !idL ) LogWarning("jetID") << (*jetPt)[i] << " " << jec << " " << nhf << " " << nEMf << " " << muf << " " << cEMf;

		if( (*jetPt)[i] > cutjetPtvalue  && idL ) { 
			//LogWarning("jetInfo") << i << " " << (*jetPt)[i] << " " << (*jetEta)[i] << " " << (*jetPhi)[i] << " " << (*jetMass)[i];

			HT += (*jetPt)[i];
			++numJets;

			TLorentzVector tmpJet;
			tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

			/// Vector of zeros
			TLorentzVector tmpSubjet0, tmpSubjet1, tmpZeros;
			tmpZeros.SetPtEtaPhiE( 0, 0, 0, 0 );

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
	   
		}
	}

	sort(tmpTriggerMass.begin(), tmpTriggerMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	float trimmedMass = -999;
	if ( ( tmpTriggerMass.size()> 0 ) ) trimmedMass = tmpTriggerMass[0];
	tmpTriggerMass.clear();

	//// test ak4 
	float ak4HT = 0;
	for (size_t i = 0; i < ak4jetPt->size(); i++) ak4HT += (*ak4jetPt)[i];
	///////////////////

	bool cutMassAsym = 0;
	bool cutCosTheta = 0;
	bool cutSubjetPtRatio= 0;

	if ( triggerFiredOne ) {

		vector<TLorentzVector> jet1SubjetsTLV, jet2SubjetsTLV;

		//if ( numJets > 1 ) {
		if ( JETS.size() > 1 ) {

			// Mass average and asymmetry
			float jet1Mass = JETS[0].mass;
			float jet2Mass = JETS[1].mass;
			float massAve = ( jet1Mass + jet2Mass ) / 2.0;
			float massAsym = abs( jet1Mass - jet2Mass ) / ( jet1Mass + jet2Mass );
			//////////////////////////////////////////////////////////////////////////

			// Cos theta star
			TLorentzVector tmpJet1, tmpJet2, tmpCM;
			tmpJet1 = JETS[0].p4;
			tmpJet2 = JETS[1].p4;
			tmpCM = tmpJet1 + tmpJet2;
			//LogWarning("Jets") << tmpJet1.Eta() << " " << tmpJet2.Eta() << " " << tmpCM.Eta();
			tmpJet1.Boost( -tmpCM.BoostVector() );
			tmpJet2.Boost( -tmpCM.BoostVector() );
			//LogWarning("JetsBoost") << tmpJet1.Eta() << " " << tmpJet2.Eta();
			float cosThetaStar = TMath::Abs( ( tmpJet1.Px() * tmpCM.Px() +  tmpJet1.Py() * tmpCM.Py() + tmpJet1.Pz() * tmpCM.Pz() ) / (tmpJet1.E() * tmpCM.E() ) ) ;
			//LogWarning("cos theta") << cosThetaStar ;
			/////////////////////////////////////////////////////////////////////////////////

			/*/ Nsubjetiness
			jet1Tau21 = JETS[0].tau2 / JETS[0].tau1;
			jet1Tau31 = JETS[0].tau3 / JETS[0].tau1;
			jet1Tau32 = JETS[0].tau3 / JETS[0].tau2;
			///////////////////////////////////////////////////////////////////////////////*/

			// Subjet variables
			jet1SubjetsTLV.push_back( JETS[0].subjet0 );
			jet1SubjetsTLV.push_back( JETS[0].subjet1 );
			//LogWarning("subjet0") <<  jet1SubjetsTLV[0].M() << " " <<  jet1SubjetsTLV[1].M();
			sort(jet1SubjetsTLV.begin(), jet1SubjetsTLV.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.M() > p2.M(); }); 
			//LogWarning("subjet0") <<  jet1SubjetsTLV[0].M() << " " <<  jet1SubjetsTLV[1].M();
			jet2SubjetsTLV.push_back( JETS[1].subjet0 );
			jet2SubjetsTLV.push_back( JETS[1].subjet1 );
			sort(jet2SubjetsTLV.begin(), jet2SubjetsTLV.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.M() > p2.M(); }); 
			
			float jet1SubjetPtRatio = 0;
			float jet2SubjetPtRatio = 0;
			if( ( jet1SubjetsTLV.size() > 0 ) && ( jet2SubjetsTLV.size() > 0 ) ) {
				jet1SubjetPtRatio = min( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() ) / max( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() );
				jet2SubjetPtRatio = min( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() ) / max( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() );
			}


			if( massAsym < cutAsymvalue ) cutMassAsym = 1;
			if( TMath::Abs( cosThetaStar ) < cutCosThetavalue ) cutCosTheta = 1;
			if( ( jet1SubjetPtRatio > cutSubjetPtRatiovalue ) && ( jet2SubjetPtRatio > cutSubjetPtRatiovalue ) ) cutSubjetPtRatio = 1;

			histos1D_[ "massAveDenom_cutDijet" ]->Fill( massAve, scale  );
			histos1D_[ "trimmedMassDenom_cutDijet" ]->Fill( trimmedMass, scale  );
			histos1D_[ "jet1MassDenom_cutDijet" ]->Fill( jet1Mass, scale  );
			histos1D_[ "jet1PtDenom_cutDijet" ]->Fill( JETS[0].p4.Pt() , scale  );
			histos1D_[ "HTDenom_cutDijet" ]->Fill( HT, scale  );
			histos1D_[ "ak4HTDenom_cutDijet" ]->Fill( ak4HT, scale  );
			histos2D_[ "jetMassHTDenom_cutDijet" ]->Fill( trimmedMass, HT, scale );

			if ( triggerFiredTwo ){
				histos1D_[ "massAvePassing_cutDijet" ]->Fill( massAve, scale  );
				histos1D_[ "trimmedMassPassing_cutDijet" ]->Fill( trimmedMass, scale  );
				histos1D_[ "jet1MassPassing_cutDijet" ]->Fill( jet1Mass, scale  );
				histos1D_[ "jet1PtPassing_cutDijet" ]->Fill( JETS[0].p4.Pt() , scale  );
				histos1D_[ "HTPassing_cutDijet" ]->Fill( HT, scale  );
				histos1D_[ "ak4HTPassing_cutDijet" ]->Fill( ak4HT, scale  );
				histos2D_[ "jetMassHTPassing_cutDijet" ]->Fill( trimmedMass, HT, scale );
			}

			if ( cutMassAsym ) {
				histos1D_[ "massAveDenom_cutMassAsym" ]->Fill( massAve, scale  );
				histos1D_[ "trimmedMassDenom_cutMassAsym" ]->Fill( trimmedMass, scale  );
				histos1D_[ "jet1MassDenom_cutMassAsym" ]->Fill( jet1Mass, scale  );
				histos1D_[ "jet1PtDenom_cutMassAsym" ]->Fill( JETS[0].p4.Pt() , scale  );
				histos1D_[ "HTDenom_cutMassAsym" ]->Fill( HT, scale  );
				histos1D_[ "ak4HTDenom_cutMassAsym" ]->Fill( ak4HT, scale  );
				histos2D_[ "jetMassHTDenom_cutMassAsym" ]->Fill( trimmedMass, HT, scale );

				if ( triggerFiredTwo ){
					histos1D_[ "massAvePassing_cutMassAsym" ]->Fill( massAve, scale  );
					histos1D_[ "trimmedMassPassing_cutMassAsym" ]->Fill( trimmedMass, scale  );
					histos1D_[ "jet1MassPassing_cutMassAsym" ]->Fill( jet1Mass, scale  );
					histos1D_[ "jet1PtPassing_cutMassAsym" ]->Fill( JETS[0].p4.Pt() , scale  );
					histos1D_[ "HTPassing_cutMassAsym" ]->Fill( HT, scale  );
					histos1D_[ "ak4HTPassing_cutMassAsym" ]->Fill( ak4HT, scale  );
					histos2D_[ "jetMassHTPassing_cutMassAsym" ]->Fill( trimmedMass, HT, scale );
				}

				if ( cutCosTheta ) {
					histos1D_[ "massAveDenom_cutCosTheta" ]->Fill( massAve, scale  );
					histos1D_[ "trimmedMassDenom_cutCosTheta" ]->Fill( trimmedMass, scale  );
					histos1D_[ "jet1MassDenom_cutCosTheta" ]->Fill( jet1Mass, scale  );
					histos1D_[ "jet1PtDenom_cutCosTheta" ]->Fill( JETS[0].p4.Pt() , scale  );
					histos1D_[ "HTDenom_cutCosTheta" ]->Fill( HT, scale  );
					histos1D_[ "ak4HTDenom_cutCosTheta" ]->Fill( ak4HT, scale  );
					histos2D_[ "jetMassHTDenom_cutCosTheta" ]->Fill( trimmedMass, HT, scale );

					if ( triggerFiredTwo ){
						histos1D_[ "massAvePassing_cutCosTheta" ]->Fill( massAve, scale  );
						histos1D_[ "trimmedMassPassing_cutCosTheta" ]->Fill( trimmedMass, scale  );
						histos1D_[ "jet1MassPassing_cutCosTheta" ]->Fill( jet1Mass, scale  );
						histos1D_[ "jet1PtPassing_cutCosTheta" ]->Fill( JETS[0].p4.Pt() , scale  );
						histos1D_[ "HTPassing_cutCosTheta" ]->Fill( HT, scale  );
						histos1D_[ "ak4HTPassing_cutCosTheta" ]->Fill( ak4HT, scale  );
						histos2D_[ "jetMassHTPassing_cutCosTheta" ]->Fill( trimmedMass, HT, scale );
					}

					if ( cutSubjetPtRatio ) {
						histos1D_[ "massAveDenom_cutSubjetPtRatio" ]->Fill( massAve, scale  );
						histos1D_[ "trimmedMassDenom_cutSubjetPtRatio" ]->Fill( trimmedMass, scale  );
						histos1D_[ "jet1MassDenom_cutSubjetPtRatio" ]->Fill( jet1Mass, scale  );
						histos1D_[ "jet1PtDenom_cutSubjetPtRatio" ]->Fill( JETS[0].p4.Pt() , scale  );
						histos1D_[ "HTDenom_cutSubjetPtRatio" ]->Fill( HT, scale  );
						histos1D_[ "ak4HTDenom_cutSubjetPtRatio" ]->Fill( ak4HT, scale  );
						histos2D_[ "jetMassHTDenom_cutSubjetPtRatio" ]->Fill( trimmedMass, HT, scale );

						if ( triggerFiredTwo ){
							histos1D_[ "massAvePassing_cutSubjetPtRatio" ]->Fill( massAve, scale  );
							histos1D_[ "trimmedMassPassing_cutSubjetPtRatio" ]->Fill( trimmedMass, scale  );
							histos1D_[ "jet1MassPassing_cutSubjetPtRatio" ]->Fill( jet1Mass, scale  );
							histos1D_[ "jet1PtPassing_cutSubjetPtRatio" ]->Fill( JETS[0].p4.Pt() , scale  );
							histos1D_[ "HTPassing_cutSubjetPtRatio" ]->Fill( HT, scale  );
							histos1D_[ "ak4HTPassing_cutSubjetPtRatio" ]->Fill( ak4HT, scale  );
							histos2D_[ "jetMassHTPassing_cutSubjetPtRatio" ]->Fill( trimmedMass, HT, scale );
						}
					}
				}
			}
		}
	}
	JETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNTriggerEfficiency::beginJob() {

	histos1D_[ "ak4HTDenom_cutDijet" ] = fs_->make< TH1D >( "ak4HTDenom_cutDijet", "ak4HTDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutDijet" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutDijet" ] = fs_->make< TH1D >( "ak4HTPassing_cutDijet", "ak4HTPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutDijet" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutDijet" ] = fs_->make< TH1D >( "ak4HTEfficiency_cutDijet", "ak4HTEfficiency_cutDijet", 150, 0., 1500. );
	histos1D_[ "ak4HTEfficiency_cutDijet" ]->SetYTitle( "Efficiency_cutDijet" );

	histos1D_[ "ak4HTDenom_cutMassAsym" ] = fs_->make< TH1D >( "ak4HTDenom_cutMassAsym", "ak4HTDenom_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutMassAsym" ] = fs_->make< TH1D >( "ak4HTPassing_cutMassAsym", "ak4HTPassing_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutMassAsym" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutMassAsym" ] = fs_->make< TH1D >( "ak4HTEfficiency_cutMassAsym", "ak4HTEfficiency_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "ak4HTEfficiency_cutMassAsym" ]->SetYTitle( "Efficiency_cutMassAsym" );

	histos1D_[ "ak4HTDenom_cutCosTheta" ] = fs_->make< TH1D >( "ak4HTDenom_cutCosTheta", "ak4HTDenom_cutCosTheta", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutCosTheta" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutCosTheta" ] = fs_->make< TH1D >( "ak4HTPassing_cutCosTheta", "ak4HTPassing_cutCosTheta", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutCosTheta" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutCosTheta" ] = fs_->make< TH1D >( "ak4HTEfficiency_cutCosTheta", "ak4HTEfficiency_cutCosTheta", 150, 0., 1500. );
	histos1D_[ "ak4HTEfficiency_cutCosTheta" ]->SetYTitle( "Efficiency_cutCosTheta" );

	histos1D_[ "ak4HTDenom_cutSubjetPtRatio" ] = fs_->make< TH1D >( "ak4HTDenom_cutSubjetPtRatio", "ak4HTDenom_cutSubjetPtRatio", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutSubjetPtRatio" ] = fs_->make< TH1D >( "ak4HTPassing_cutSubjetPtRatio", "ak4HTPassing_cutSubjetPtRatio", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutSubjetPtRatio" ] = fs_->make< TH1D >( "ak4HTEfficiency_cutSubjetPtRatio", "ak4HTEfficiency_cutSubjetPtRatio", 150, 0., 1500. );
	histos1D_[ "ak4HTEfficiency_cutSubjetPtRatio" ]->SetYTitle( "Efficiency_cutSubjetPtRatio" );

	histos1D_[ "HTDenom_cutDijet" ] = fs_->make< TH1D >( "HTDenom_cutDijet", "HTDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutDijet" ]->Sumw2();
	histos1D_[ "HTPassing_cutDijet" ] = fs_->make< TH1D >( "HTPassing_cutDijet", "HTPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutDijet" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutDijet" ] = fs_->make< TH1D >( "HTEfficiency_cutDijet", "HTEfficiency_cutDijet", 150, 0., 1500. );
	histos1D_[ "HTEfficiency_cutDijet" ]->SetYTitle( "Efficiency_cutDijet" );

	histos1D_[ "HTDenom_cutMassAsym" ] = fs_->make< TH1D >( "HTDenom_cutMassAsym", "HTDenom_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "HTPassing_cutMassAsym" ] = fs_->make< TH1D >( "HTPassing_cutMassAsym", "HTPassing_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutMassAsym" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutMassAsym" ] = fs_->make< TH1D >( "HTEfficiency_cutMassAsym", "HTEfficiency_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "HTEfficiency_cutMassAsym" ]->SetYTitle( "Efficiency_cutMassAsym" );

	histos1D_[ "HTDenom_cutCosTheta" ] = fs_->make< TH1D >( "HTDenom_cutCosTheta", "HTDenom_cutCosTheta", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutCosTheta" ]->Sumw2();
	histos1D_[ "HTPassing_cutCosTheta" ] = fs_->make< TH1D >( "HTPassing_cutCosTheta", "HTPassing_cutCosTheta", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutCosTheta" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutCosTheta" ] = fs_->make< TH1D >( "HTEfficiency_cutCosTheta", "HTEfficiency_cutCosTheta", 150, 0., 1500. );
	histos1D_[ "HTEfficiency_cutCosTheta" ]->SetYTitle( "Efficiency_cutCosTheta" );

	histos1D_[ "HTDenom_cutSubjetPtRatio" ] = fs_->make< TH1D >( "HTDenom_cutSubjetPtRatio", "HTDenom_cutSubjetPtRatio", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "HTPassing_cutSubjetPtRatio" ] = fs_->make< TH1D >( "HTPassing_cutSubjetPtRatio", "HTPassing_cutSubjetPtRatio", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutSubjetPtRatio" ] = fs_->make< TH1D >( "HTEfficiency_cutSubjetPtRatio", "HTEfficiency_cutSubjetPtRatio", 150, 0., 1500. );
	histos1D_[ "HTEfficiency_cutSubjetPtRatio" ]->SetYTitle( "Efficiency_cutSubjetPtRatio" );

	histos1D_[ "trimmedMassDenom_cutDijet" ] = fs_->make< TH1D >( "trimmedMassDenom_cutDijet", "trimmedMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutDijet" ] = fs_->make< TH1D >( "trimmedMassPassing_cutDijet", "trimmedMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutDijet" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutDijet" ] = fs_->make< TH1D >( "trimmedMassEfficiency_cutDijet", "trimmedMassEfficiency_cutDijet", 60, 0., 600. );
	histos1D_[ "trimmedMassEfficiency_cutDijet" ]->SetYTitle( "Efficiency_cutDijet" );

	histos1D_[ "trimmedMassDenom_cutMassAsym" ] = fs_->make< TH1D >( "trimmedMassDenom_cutMassAsym", "trimmedMassDenom_cutMassAsym", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutMassAsym" ] = fs_->make< TH1D >( "trimmedMassPassing_cutMassAsym", "trimmedMassPassing_cutMassAsym", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutMassAsym" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutMassAsym" ] = fs_->make< TH1D >( "trimmedMassEfficiency_cutMassAsym", "trimmedMassEfficiency_cutMassAsym", 60, 0., 600. );
	histos1D_[ "trimmedMassEfficiency_cutMassAsym" ]->SetYTitle( "Efficiency_cutMassAsym" );

	histos1D_[ "trimmedMassDenom_cutCosTheta" ] = fs_->make< TH1D >( "trimmedMassDenom_cutCosTheta", "trimmedMassDenom_cutCosTheta", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutCosTheta" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutCosTheta" ] = fs_->make< TH1D >( "trimmedMassPassing_cutCosTheta", "trimmedMassPassing_cutCosTheta", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutCosTheta" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutCosTheta" ] = fs_->make< TH1D >( "trimmedMassEfficiency_cutCosTheta", "trimmedMassEfficiency_cutCosTheta", 60, 0., 600. );
	histos1D_[ "trimmedMassEfficiency_cutCosTheta" ]->SetYTitle( "Efficiency_cutCosTheta" );

	histos1D_[ "trimmedMassDenom_cutSubjetPtRatio" ] = fs_->make< TH1D >( "trimmedMassDenom_cutSubjetPtRatio", "trimmedMassDenom_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutSubjetPtRatio" ] = fs_->make< TH1D >( "trimmedMassPassing_cutSubjetPtRatio", "trimmedMassPassing_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutSubjetPtRatio" ] = fs_->make< TH1D >( "trimmedMassEfficiency_cutSubjetPtRatio", "trimmedMassEfficiency_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "trimmedMassEfficiency_cutSubjetPtRatio" ]->SetYTitle( "Efficiency_cutSubjetPtRatio" );

	histos1D_[ "massAveDenom_cutDijet" ] = fs_->make< TH1D >( "massAveDenom_cutDijet", "massAveDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "massAveDenom_cutDijet" ]->Sumw2();
	histos1D_[ "massAvePassing_cutDijet" ] = fs_->make< TH1D >( "massAvePassing_cutDijet", "massAvePassing_cutDijet", 60, 0., 600. );
	histos1D_[ "massAvePassing_cutDijet" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutDijet" ] = fs_->make< TH1D >( "massAveEfficiency_cutDijet", "massAveEfficiency_cutDijet", 60, 0., 600. );
	histos1D_[ "massAveEfficiency_cutDijet" ]->SetYTitle( "Efficiency_cutDijet" );

	histos1D_[ "massAveDenom_cutMassAsym" ] = fs_->make< TH1D >( "massAveDenom_cutMassAsym", "massAveDenom_cutMassAsym", 60, 0., 600. );
	histos1D_[ "massAveDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "massAvePassing_cutMassAsym" ] = fs_->make< TH1D >( "massAvePassing_cutMassAsym", "massAvePassing_cutMassAsym", 60, 0., 600. );
	histos1D_[ "massAvePassing_cutMassAsym" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutMassAsym" ] = fs_->make< TH1D >( "massAveEfficiency_cutMassAsym", "massAveEfficiency_cutMassAsym", 60, 0., 600. );
	histos1D_[ "massAveEfficiency_cutMassAsym" ]->SetYTitle( "Efficiency_cutMassAsym" );

	histos1D_[ "massAveDenom_cutCosTheta" ] = fs_->make< TH1D >( "massAveDenom_cutCosTheta", "massAveDenom_cutCosTheta", 60, 0., 600. );
	histos1D_[ "massAveDenom_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAvePassing_cutCosTheta" ] = fs_->make< TH1D >( "massAvePassing_cutCosTheta", "massAvePassing_cutCosTheta", 60, 0., 600. );
	histos1D_[ "massAvePassing_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutCosTheta" ] = fs_->make< TH1D >( "massAveEfficiency_cutCosTheta", "massAveEfficiency_cutCosTheta", 60, 0., 600. );
	histos1D_[ "massAveEfficiency_cutCosTheta" ]->SetYTitle( "Efficiency_cutCosTheta" );

	histos1D_[ "massAveDenom_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAveDenom_cutSubjetPtRatio", "massAveDenom_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "massAveDenom_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "massAvePassing_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAvePassing_cutSubjetPtRatio", "massAvePassing_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "massAvePassing_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAveEfficiency_cutSubjetPtRatio", "massAveEfficiency_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "massAveEfficiency_cutSubjetPtRatio" ]->SetYTitle( "Efficiency_cutSubjetPtRatio" );

	histos1D_[ "jet1PtDenom_cutDijet" ] = fs_->make< TH1D >( "jet1PtDenom_cutDijet", "jet1PtDenom_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutDijet" ] = fs_->make< TH1D >( "jet1PtPassing_cutDijet", "jet1PtPassing_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cutDijet" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutDijet" ] = fs_->make< TH1D >( "jet1PtEfficiency_cutDijet", "jet1PtEfficiency_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet1PtEfficiency_cutDijet" ]->SetYTitle( "Efficiency_cutDijet" );

	histos1D_[ "jet1PtDenom_cutMassAsym" ] = fs_->make< TH1D >( "jet1PtDenom_cutMassAsym", "jet1PtDenom_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutMassAsym" ] = fs_->make< TH1D >( "jet1PtPassing_cutMassAsym", "jet1PtPassing_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutMassAsym" ] = fs_->make< TH1D >( "jet1PtEfficiency_cutMassAsym", "jet1PtEfficiency_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet1PtEfficiency_cutMassAsym" ]->SetYTitle( "Efficiency_cutMassAsym" );

	histos1D_[ "jet1PtDenom_cutCosTheta" ] = fs_->make< TH1D >( "jet1PtDenom_cutCosTheta", "jet1PtDenom_cutCosTheta", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutCosTheta" ] = fs_->make< TH1D >( "jet1PtPassing_cutCosTheta", "jet1PtPassing_cutCosTheta", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutCosTheta" ] = fs_->make< TH1D >( "jet1PtEfficiency_cutCosTheta", "jet1PtEfficiency_cutCosTheta", 100, 0., 1000. );
	histos1D_[ "jet1PtEfficiency_cutCosTheta" ]->SetYTitle( "Efficiency_cutCosTheta" );

	histos1D_[ "jet1PtDenom_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1PtDenom_cutSubjetPtRatio", "jet1PtDenom_cutSubjetPtRatio", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1PtPassing_cutSubjetPtRatio", "jet1PtPassing_cutSubjetPtRatio", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1PtEfficiency_cutSubjetPtRatio", "jet1PtEfficiency_cutSubjetPtRatio", 100, 0., 1000. );
	histos1D_[ "jet1PtEfficiency_cutSubjetPtRatio" ]->SetYTitle( "Efficiency_cutSubjetPtRatio" );

	histos1D_[ "jet1MassDenom_cutDijet" ] = fs_->make< TH1D >( "jet1MassDenom_cutDijet", "jet1MassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutDijet" ] = fs_->make< TH1D >( "jet1MassPassing_cutDijet", "jet1MassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutDijet" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutDijet" ] = fs_->make< TH1D >( "jet1MassEfficiency_cutDijet", "jet1MassEfficiency_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1MassEfficiency_cutDijet" ]->SetYTitle( "Efficiency_cutDijet" );

	histos1D_[ "jet1MassDenom_cutMassAsym" ] = fs_->make< TH1D >( "jet1MassDenom_cutMassAsym", "jet1MassDenom_cutMassAsym", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutMassAsym" ] = fs_->make< TH1D >( "jet1MassPassing_cutMassAsym", "jet1MassPassing_cutMassAsym", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutMassAsym" ] = fs_->make< TH1D >( "jet1MassEfficiency_cutMassAsym", "jet1MassEfficiency_cutMassAsym", 60, 0., 600. );
	histos1D_[ "jet1MassEfficiency_cutMassAsym" ]->SetYTitle( "Efficiency_cutMassAsym" );

	histos1D_[ "jet1MassDenom_cutCosTheta" ] = fs_->make< TH1D >( "jet1MassDenom_cutCosTheta", "jet1MassDenom_cutCosTheta", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutCosTheta" ] = fs_->make< TH1D >( "jet1MassPassing_cutCosTheta", "jet1MassPassing_cutCosTheta", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutCosTheta" ] = fs_->make< TH1D >( "jet1MassEfficiency_cutCosTheta", "jet1MassEfficiency_cutCosTheta", 60, 0., 600. );
	histos1D_[ "jet1MassEfficiency_cutCosTheta" ]->SetYTitle( "Efficiency_cutCosTheta" );

	histos1D_[ "jet1MassDenom_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1MassDenom_cutSubjetPtRatio", "jet1MassDenom_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1MassPassing_cutSubjetPtRatio", "jet1MassPassing_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutSubjetPtRatio" ] = fs_->make< TH1D >( "jet1MassEfficiency_cutSubjetPtRatio", "jet1MassEfficiency_cutSubjetPtRatio", 60, 0., 600. );
	histos1D_[ "jet1MassEfficiency_cutSubjetPtRatio" ]->SetYTitle( "Efficiency_cutSubjetPtRatio" );

	histos2D_[ "jetMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jetMassHTDenom_cutDijet", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTDenom_cutDijet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTDenom_cutDijet" ]->Sumw2();

	histos2D_[ "jetMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jetMassHTPassing_cutDijet", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTPassing_cutDijet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jetMassHTEfficiency_cutDijet" ] = fs_->make< TH2D >( "jetMassHTEfficiency_cutDijet", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTEfficiency_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTEfficiency_cutDijet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );

	histos2D_[ "jetMassHTDenom_cutMassAsym" ] = fs_->make< TH2D >( "jetMassHTDenom_cutMassAsym", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTDenom_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTDenom_cutMassAsym" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTDenom_cutMassAsym" ]->Sumw2();

	histos2D_[ "jetMassHTPassing_cutMassAsym" ] = fs_->make< TH2D >( "jetMassHTPassing_cutMassAsym", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTPassing_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTPassing_cutMassAsym" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTPassing_cutMassAsym" ]->Sumw2();

	histos2D_[ "jetMassHTEfficiency_cutMassAsym" ] = fs_->make< TH2D >( "jetMassHTEfficiency_cutMassAsym", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTEfficiency_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTEfficiency_cutMassAsym" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );

	histos2D_[ "jetMassHTDenom_cutCosTheta" ] = fs_->make< TH2D >( "jetMassHTDenom_cutCosTheta", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTDenom_cutCosTheta" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTDenom_cutCosTheta" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTDenom_cutCosTheta" ]->Sumw2();

	histos2D_[ "jetMassHTPassing_cutCosTheta" ] = fs_->make< TH2D >( "jetMassHTPassing_cutCosTheta", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTPassing_cutCosTheta" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTPassing_cutCosTheta" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTPassing_cutCosTheta" ]->Sumw2();

	histos2D_[ "jetMassHTEfficiency_cutCosTheta" ] = fs_->make< TH2D >( "jetMassHTEfficiency_cutCosTheta", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTEfficiency_cutCosTheta" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTEfficiency_cutCosTheta" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );

	histos2D_[ "jetMassHTDenom_cutSubjetPtRatio" ] = fs_->make< TH2D >( "jetMassHTDenom_cutSubjetPtRatio", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTDenom_cutSubjetPtRatio" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTDenom_cutSubjetPtRatio" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTDenom_cutSubjetPtRatio" ]->Sumw2();

	histos2D_[ "jetMassHTPassing_cutSubjetPtRatio" ] = fs_->make< TH2D >( "jetMassHTPassing_cutSubjetPtRatio", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTPassing_cutSubjetPtRatio" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTPassing_cutSubjetPtRatio" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetMassHTPassing_cutSubjetPtRatio" ]->Sumw2();

	histos2D_[ "jetMassHTEfficiency_cutSubjetPtRatio" ] = fs_->make< TH2D >( "jetMassHTEfficiency_cutSubjetPtRatio", "HT vs Leading Jet Mass", 16, 0., 400. , 20, 0., 2000);
	histos2D_[ "jetMassHTEfficiency_cutSubjetPtRatio" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTEfficiency_cutSubjetPtRatio" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );

}

// ------------ method called once each job just after ending the event loop  ------------
void RUNTriggerEfficiency::endJob() {

	histos1D_[ "HTEfficiency_cutDijet" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutDijet" ]->Divide(histos1D_[ "HTPassing_cutDijet" ],histos1D_[ "HTDenom_cutDijet" ],1,1,"B");

	histos1D_[ "HTEfficiency_cutMassAsym" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutMassAsym" ]->Divide(histos1D_[ "HTPassing_cutMassAsym" ],histos1D_[ "HTDenom_cutMassAsym" ],1,1,"B");

	histos1D_[ "HTEfficiency_cutCosTheta" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutCosTheta" ]->Divide(histos1D_[ "HTPassing_cutCosTheta" ],histos1D_[ "HTDenom_cutCosTheta" ],1,1,"B");

	histos1D_[ "HTEfficiency_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "HTEfficiency_cutSubjetPtRatio" ]->Divide(histos1D_[ "HTPassing_cutSubjetPtRatio" ],histos1D_[ "HTDenom_cutSubjetPtRatio" ],1,1,"B");

	histos1D_[ "ak4HTEfficiency_cutDijet" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutDijet" ]->Divide(histos1D_[ "ak4HTPassing_cutDijet" ],histos1D_[ "ak4HTDenom_cutDijet" ],1,1,"B");

	histos1D_[ "ak4HTEfficiency_cutMassAsym" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutMassAsym" ]->Divide(histos1D_[ "ak4HTPassing_cutMassAsym" ],histos1D_[ "ak4HTDenom_cutMassAsym" ],1,1,"B");

	histos1D_[ "ak4HTEfficiency_cutCosTheta" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutCosTheta" ]->Divide(histos1D_[ "ak4HTPassing_cutCosTheta" ],histos1D_[ "ak4HTDenom_cutCosTheta" ],1,1,"B");

	histos1D_[ "ak4HTEfficiency_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "ak4HTEfficiency_cutSubjetPtRatio" ]->Divide(histos1D_[ "ak4HTPassing_cutSubjetPtRatio" ],histos1D_[ "ak4HTDenom_cutSubjetPtRatio" ],1,1,"B");

	histos1D_[ "trimmedMassEfficiency_cutDijet" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutDijet" ]->Divide(histos1D_[ "trimmedMassPassing_cutDijet" ],histos1D_[ "trimmedMassDenom_cutDijet" ],1,1,"B");

	histos1D_[ "trimmedMassEfficiency_cutMassAsym" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutMassAsym" ]->Divide(histos1D_[ "trimmedMassPassing_cutMassAsym" ],histos1D_[ "trimmedMassDenom_cutMassAsym" ],1,1,"B");

	histos1D_[ "trimmedMassEfficiency_cutCosTheta" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutCosTheta" ]->Divide(histos1D_[ "trimmedMassPassing_cutCosTheta" ],histos1D_[ "trimmedMassDenom_cutCosTheta" ],1,1,"B");

	histos1D_[ "trimmedMassEfficiency_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "trimmedMassEfficiency_cutSubjetPtRatio" ]->Divide(histos1D_[ "trimmedMassPassing_cutSubjetPtRatio" ],histos1D_[ "trimmedMassDenom_cutSubjetPtRatio" ],1,1,"B");
	         
	histos1D_[ "massAveEfficiency_cutDijet" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutDijet" ]->Divide(histos1D_[ "massAvePassing_cutDijet" ],histos1D_[ "massAveDenom_cutDijet" ],1,1,"B");
	         
	histos1D_[ "massAveEfficiency_cutMassAsym" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutMassAsym" ]->Divide(histos1D_[ "massAvePassing_cutMassAsym" ],histos1D_[ "massAveDenom_cutMassAsym" ],1,1,"B");
	         
	histos1D_[ "massAveEfficiency_cutCosTheta" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutCosTheta" ]->Divide(histos1D_[ "massAvePassing_cutCosTheta" ],histos1D_[ "massAveDenom_cutCosTheta" ],1,1,"B");
	         
	histos1D_[ "massAveEfficiency_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "massAveEfficiency_cutSubjetPtRatio" ]->Divide(histos1D_[ "massAvePassing_cutSubjetPtRatio" ],histos1D_[ "massAveDenom_cutSubjetPtRatio" ],1,1,"B");
	         
	histos1D_[ "jet1PtEfficiency_cutDijet" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutDijet" ]->Divide(histos1D_[ "jet1PtPassing_cutDijet" ],histos1D_[ "jet1PtDenom_cutDijet" ],1,1,"B");
	         
	histos1D_[ "jet1PtEfficiency_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutMassAsym" ]->Divide(histos1D_[ "jet1PtPassing_cutMassAsym" ],histos1D_[ "jet1PtDenom_cutMassAsym" ],1,1,"B");
	         
	histos1D_[ "jet1PtEfficiency_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutCosTheta" ]->Divide(histos1D_[ "jet1PtPassing_cutCosTheta" ],histos1D_[ "jet1PtDenom_cutCosTheta" ],1,1,"B");
	         
	histos1D_[ "jet1PtEfficiency_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1PtEfficiency_cutSubjetPtRatio" ]->Divide(histos1D_[ "jet1PtPassing_cutSubjetPtRatio" ],histos1D_[ "jet1PtDenom_cutSubjetPtRatio" ],1,1,"B");
	         
	histos1D_[ "jet1MassEfficiency_cutDijet" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutDijet" ]->Divide(histos1D_[ "jet1MassPassing_cutDijet" ],histos1D_[ "jet1MassDenom_cutDijet" ],1,1,"B");
	         
	histos1D_[ "jet1MassEfficiency_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutMassAsym" ]->Divide(histos1D_[ "jet1MassPassing_cutMassAsym" ],histos1D_[ "jet1MassDenom_cutMassAsym" ],1,1,"B");
	         
	histos1D_[ "jet1MassEfficiency_cutCosTheta" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutCosTheta" ]->Divide(histos1D_[ "jet1MassPassing_cutCosTheta" ],histos1D_[ "jet1MassDenom_cutCosTheta" ],1,1,"B");
	         
	histos1D_[ "jet1MassEfficiency_cutSubjetPtRatio" ]->Sumw2();
	histos1D_[ "jet1MassEfficiency_cutSubjetPtRatio" ]->Divide(histos1D_[ "jet1MassPassing_cutSubjetPtRatio" ],histos1D_[ "jet1MassDenom_cutSubjetPtRatio" ],1,1,"B");

	histos2D_[ "jetMassHTEfficiency_cutDijet" ]->Sumw2();
	histos2D_[ "jetMassHTEfficiency_cutDijet" ]->Divide(histos2D_[ "jetMassHTPassing_cutDijet" ],histos2D_[ "jetMassHTDenom_cutDijet" ],1,1,"B");

	histos2D_[ "jetMassHTEfficiency_cutCosTheta" ]->Sumw2();
	histos2D_[ "jetMassHTEfficiency_cutCosTheta" ]->Divide(histos2D_[ "jetMassHTPassing_cutCosTheta" ],histos2D_[ "jetMassHTDenom_cutCosTheta" ],1,1,"B");

	histos2D_[ "jetMassHTEfficiency_cutMassAsym" ]->Sumw2();
	histos2D_[ "jetMassHTEfficiency_cutMassAsym" ]->Divide(histos2D_[ "jetMassHTPassing_cutMassAsym" ],histos2D_[ "jetMassHTDenom_cutMassAsym" ],1,1,"B");

	histos2D_[ "jetMassHTEfficiency_cutSubjetPtRatio" ]->Sumw2();
	histos2D_[ "jetMassHTEfficiency_cutSubjetPtRatio" ]->Divide(histos2D_[ "jetMassHTPassing_cutSubjetPtRatio" ],histos2D_[ "jetMassHTDenom_cutSubjetPtRatio" ],1,1,"B");
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNTriggerEfficiency);
