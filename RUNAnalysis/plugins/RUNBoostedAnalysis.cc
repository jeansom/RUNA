// -*- C++ -*-
//
// Package:    Ntuples/Ntuples
// Class:      RUNBoostedAnalysis
// 
/**\class RUNBoostedAnalysis RUNBoostedAnalysis.cc Ntuples/Ntuples/plugins/RUNBoostedAnalysis.cc

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
class RUNBoostedAnalysis : public EDAnalyzer {
   public:
      explicit RUNBoostedAnalysis(const ParameterSet&);
      ~RUNBoostedAnalysis();

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
      map< string, double > cutmap;

      bool bjSample;
      bool mkTree;
      double scale;
      double cutAK4HTvalue;
      double cutjetAK4Ptvalue;
      double cutTrimmedMassvalue;
      double cutHTvalue;
      double cutjetPtvalue;
      double cutAsymvalue;
      double cutCosThetavalue;
      double cutSubjetPtRatiovalue;
      double cutTau31value;
      double cutTau21value;

      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;
      float AK4HT = 0, HT = 0, trimmedMass = -999, 
	    jet1Pt = -999, jet1Eta = -999, jet1Phi = -999, jet1E = -999, jet1Mass = -999, 
	    jet2Pt = -999, jet2Eta = -999, jet2Phi = -999, jet2E = -999, jet2Mass = -999,
	    subjet11Pt = -999, subjet11Eta = -999, subjet11Phi = -999, subjet11E = -999, 
	    subjet12Pt = -999, subjet12Eta = -999, subjet12Phi = -999, subjet12E = -999, 
	    subjet21Pt = -999, subjet21Eta = -999, subjet21Phi = -999, subjet21E = -999, 
	    subjet22Pt = -999, subjet22Eta = -999, subjet22Phi = -999, subjet22E = -999,
	    massAve = -9999, massAsym = -9999, cosThetaStar = -9999,
	    jet1Tau21 = -9999, jet1Tau31 = -9999, jet1Tau32 = -9999,
	    jet1SubjetPtRatio = -999, jet2SubjetPtRatio = -999, jet1SubjetMass21Ratio = -999, jet1Subjet112MassRatio = -999, jet1Subjet1JetMassRatio = - 999, jet1Subjet212MassRatio = - 999, jet1Subjet2JetMassRatio = - 999,
	    jet2SubjetMass21Ratio = -999, jet2Subjet112MassRatio = -999, jet2Subjet1JetMassRatio = - 999, jet2Subjet212MassRatio = - 999, jet2Subjet2JetMassRatio = - 999, 
	    cosPhi13412 = -9999, cosPhi31234 = -9999,
	    dalitzY1 = -9999, dalitzY2 = -9999, dalitzY3 = -9999, dalitzY4 = -9999, dalitzY5 = -9999, dalitzY6 = -9999, 
	    dalitzX1 = -9999, dalitzX2 = -9999, dalitzX3 = -9999, dalitzX4 = -9999, dalitzX5 = -9999, dalitzX6 = -9999;

      EDGetTokenT<vector<float>> jetAK4Pt_;
      EDGetTokenT<vector<float>> jetAK4Eta_;
      EDGetTokenT<vector<float>> jetAK4Phi_;
      EDGetTokenT<vector<float>> jetAK4E_;
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
RUNBoostedAnalysis::RUNBoostedAnalysis(const ParameterSet& iConfig):
//	getterOfProducts_(ProcessMatch(*), this) {
//	triggerBits_(consumes<TriggerResults>(iConfig.getParameter<InputTag>("bits"))),
	jetAK4Pt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4Pt"))),
	jetAK4Eta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4Eta"))),
	jetAK4Phi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4Phi"))),
	jetAK4E_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4E"))),
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
	mkTree = iConfig.getParameter<bool>("mkTree");
	cutAK4HTvalue = iConfig.getParameter<double>("cutAK4HTvalue");
	cutjetAK4Ptvalue = iConfig.getParameter<double>("cutjetAK4Ptvalue");
	cutTrimmedMassvalue = iConfig.getParameter<double>("cutTrimmedMassvalue");
	cutHTvalue = iConfig.getParameter<double>("cutHTvalue");
	cutjetPtvalue = iConfig.getParameter<double>("cutjetPtvalue");
	cutAsymvalue = iConfig.getParameter<double>("cutAsymvalue");
	cutCosThetavalue = iConfig.getParameter<double>("cutCosThetavalue");
	cutSubjetPtRatiovalue = iConfig.getParameter<double>("cutSubjetPtRatiovalue");
	cutTau31value = iConfig.getParameter<double>("cutTau31value");
	cutTau21value = iConfig.getParameter<double>("cutTau21value");
}


RUNBoostedAnalysis::~RUNBoostedAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNBoostedAnalysis::analyze(const Event& iEvent, const EventSetup& iSetup) {


	/*vector<Handle< vector<float> > > handles;
	getterOfProducts_.fillHandles(event, handles);
	*/

	Handle<vector<float> > jetAK4Pt;
	iEvent.getByToken(jetAK4Pt_, jetAK4Pt);

	Handle<vector<float> > jetAK4Eta;
	iEvent.getByToken(jetAK4Eta_, jetAK4Eta);

	Handle<vector<float> > jetAK4Phi;
	iEvent.getByToken(jetAK4Phi_, jetAK4Phi);

	Handle<vector<float> > jetAK4E;
	iEvent.getByToken(jetAK4E_, jetAK4E);

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


	///////// AK4 jets to model PFHT trigger
	bool cutAK4HT = 0;
	AK4HT = 0;
	for (size_t q = 0; q < jetAK4Pt->size(); q++) {

		if ( TMath::Abs( (*jetAK4Eta)[q] ) > 2.4 ) continue;
		if ( (*jetAK4Pt)[q] < cutjetAK4Ptvalue ) continue;
		AK4HT += (*jetAK4Pt)[q];
	}
	if ( AK4HT > cutAK4HTvalue ) cutAK4HT = 1;
	////////////////////////////////////////////////////

	/// Applying kinematic, trigger and jet ID
	cutmap["Processed"] += 1;
	vector< JETtype > JETS;
	vector< float > tmpTriggerMass;
	double rawHT = 0;
	bool cutHT = 0;
	bool cutMass = 0;
	bool bTagCSV = 0;
	numJets = 0;
	HT = 0;

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
	   
			histos1D_[ "jetPt" ]->Fill( (*jetPt)[i], scale  );
			histos1D_[ "jetEta" ]->Fill( (*jetEta)[i], scale  );
			histos1D_[ "jetMass" ]->Fill( (*jetMass)[i], scale  );
		}
	}

	numPV = *NPV;
	//sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1.p4; tmpP2 = p2.p4;  return tmpP1.M() > tmpP2.M(); }); 
	histos1D_[ "jetNum" ]->Fill( numJets, scale );
	histos1D_[ "NPV" ]->Fill( numPV, scale );
	if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT, scale  );
	if ( rawHT > 0 ) histos1D_[ "rawHT" ]->Fill( rawHT, scale  );
	if ( HT > cutHTvalue ) cutHT = 1;

	sort(tmpTriggerMass.begin(), tmpTriggerMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	if ( ( tmpTriggerMass.size()> 0 ) && ( tmpTriggerMass[0] > cutTrimmedMassvalue) ){
		cutMass = 1;
		trimmedMass = tmpTriggerMass[0];
		histos1D_[ "jetTrimmedMass" ]->Fill( tmpTriggerMass[0], scale  );
	}
	tmpTriggerMass.clear();

	if ( cutMass && cutHT && cutAK4HT ) {

		cutmap["Trigger"] += 1; 
		histos1D_[ "HT_cutTrigger" ]->Fill( HT, scale  );
		histos1D_[ "NPV_cutTrigger" ]->Fill( numPV, scale );
		histos1D_[ "jetNum_cutTrigger" ]->Fill( numJets, scale );
		histos1D_[ "jet1Pt_cutTrigger" ]->Fill( JETS[0].p4.Pt(), scale  );
		histos1D_[ "jet1Mass_cutTrigger" ]->Fill( JETS[0].mass, scale );
		histos1D_[ "jet1Eta_cutTrigger" ]->Fill( JETS[0].p4.Eta(), scale  );

		for (size_t k = 0; k < JETS.size(); k++) {
			histos1D_[ "jetPt_cutTrigger" ]->Fill( JETS[k].p4.Pt(), scale  );
			histos1D_[ "jetEta_cutTrigger" ]->Fill( JETS[k].p4.Eta(), scale  );
			histos1D_[ "jetMass_cutTrigger" ]->Fill( JETS[k].mass, scale );
		 }
		//////////////////////////////////////////////////////////////////////////////
						
		vector<double> dalitz1, dalitz2;
		vector<TLorentzVector> jet1SubjetsTLV, jet2SubjetsTLV;

		if ( numJets > 1 ) {

			cutmap["Dijet"] += 1;

			// Mass average and asymmetry
			jet1Mass = JETS[0].mass;
			jet2Mass = JETS[1].mass;
			massAve = ( jet1Mass + jet2Mass ) / 2.0;
			massAsym = abs( jet1Mass - jet2Mass ) / ( jet1Mass + jet2Mass );
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
			cosThetaStar = TMath::Abs( ( tmpJet1.Px() * tmpCM.Px() +  tmpJet1.Py() * tmpCM.Py() + tmpJet1.Pz() * tmpCM.Pz() ) / (tmpJet1.E() * tmpCM.E() ) ) ;
			//LogWarning("cos theta") << cosThetaStar ;
			/////////////////////////////////////////////////////////////////////////////////


			// Nsubjetiness
			jet1Tau21 = JETS[0].tau2 / JETS[0].tau1;
			jet1Tau31 = JETS[0].tau3 / JETS[0].tau1;
			jet1Tau32 = JETS[0].tau3 / JETS[0].tau2;
			////////////////////////////////////////////////////////////////////////////////


			// Subjet variables
			jet1SubjetsTLV.push_back( JETS[0].subjet0 );
			jet1SubjetsTLV.push_back( JETS[0].subjet1 );
			//LogWarning("subjet0") <<  jet1SubjetsTLV[0].M() << " " <<  jet1SubjetsTLV[1].M();
			sort(jet1SubjetsTLV.begin(), jet1SubjetsTLV.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.M() > p2.M(); }); 
			//LogWarning("subjet0") <<  jet1SubjetsTLV[0].M() << " " <<  jet1SubjetsTLV[1].M();
			jet2SubjetsTLV.push_back( JETS[1].subjet0 );
			jet2SubjetsTLV.push_back( JETS[1].subjet1 );
			sort(jet2SubjetsTLV.begin(), jet2SubjetsTLV.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.M() > p2.M(); }); 

			if( ( jet1SubjetsTLV.size() > 0 ) && ( jet2SubjetsTLV.size() > 0 ) ) {

				// Subjet Pt ratio, subjet mass ratio 
				//LogWarning("subjet0") <<  jet1SubjetsTLV[0].Pt() << " " <<  jet1SubjetsTLV[1].Pt();
				jet1SubjetPtRatio = min( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() ) / max( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() );
				jet1SubjetMass21Ratio =  jet1SubjetsTLV[1].M() / jet1SubjetsTLV[0].M() ;
				jet1Subjet112MassRatio = jet1SubjetsTLV[0].M() / ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] ).M();
				jet1Subjet1JetMassRatio = jet1SubjetsTLV[0].M() /jet1Mass;
				jet1Subjet212MassRatio = jet1SubjetsTLV[1].M() / ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] ).M();
				jet1Subjet2JetMassRatio = jet1SubjetsTLV[1].M() /jet1Mass;

				jet2SubjetPtRatio = min( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() ) / max( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() );
				jet2SubjetMass21Ratio =  jet2SubjetsTLV[1].M()/jet2SubjetsTLV[0].M();
				jet2Subjet112MassRatio = jet2SubjetsTLV[0].M()/ ( jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M();
				jet2Subjet1JetMassRatio = jet2SubjetsTLV[0].M()/jet2Mass;
				jet2Subjet212MassRatio = jet2SubjetsTLV[1].M()/ ( jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M();
				jet2Subjet2JetMassRatio = jet2SubjetsTLV[1].M()/jet2Mass;
				//////////////////////////////////////////////////////////////////////////////////

			
				// SUbjet Polarization angle & dalitz variables
				double m1 = jet1SubjetsTLV[0].M();
				double m2 = jet1SubjetsTLV[1].M();
				double m3 = jet2SubjetsTLV[0].M();
				double m4 = jet2SubjetsTLV[1].M();

				double m12 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] ).M() ;
				double m34 = ( jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				double m134 = ( jet1SubjetsTLV[0] + jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				double m123 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] + jet2SubjetsTLV[0] ).M() ;
				double m124 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] + jet2SubjetsTLV[1] ).M() ;
				double m234 = ( jet1SubjetsTLV[1] + jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				double m1234 = ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] + jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M() ;
				
				// subjet polarization angles
				double tmpX1 = pow(m1234,2) * ( ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2) ) ;
				double tmpX2 = pow(m12,2) * ( pow(m134,2) - pow(m34,2) - pow(m1,2) );
				double tmpX3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
				double tmpX4 = ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2);
				double tmpX5 = pow(m12,2) * pow(m1,2);
				double tmpx1 = tmpX1 - (tmpX2/2);
				double tmpx2 = tmpX3 * ( pow(tmpX4,2) - tmpX5 );
				cosPhi13412 = TMath::Abs( tmpx1 / TMath::Sqrt( tmpx2 ) );

				double tmpY1 = pow(m1234,2) * ( ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2) ) ;
				double tmpY2 = pow(m34,2) * ( pow(m123,2) - pow(m12,2) - pow(m3,2) );
				double tmpY3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
				double tmpY4 = ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2);
				double tmpY5 = pow(m34,2) * pow(m3,2);
				double tmpy1 = tmpY1 - (tmpY2/2);
				double tmpy2 = tmpY3 * ( pow(tmpY4,2) - tmpY5 );
				cosPhi31234 = TMath::Abs( tmpy1 / TMath::Sqrt( tmpy2 ) );

				// dalitz
				double tmptilde1 = pow( m1, 2 ) + pow( m2, 2) + pow( m34, 2 ) + pow( m1234, 2);
				double mtilde12 = pow( m12, 2 ) / tmptilde1;
				double mtilde134 = pow( m134, 2 ) / tmptilde1;
				double mtilde234 = pow( m234, 2 ) / tmptilde1;
				//double tmpMtilde = mtilde12 + mtilde134 + mtilde234;
				//LogWarning("dalitz0") << tmpMtilde << " " << mtilde12 << " " << mtilde134 << " " <<  mtilde234;
				dalitz1.push_back( mtilde12 );
				dalitz1.push_back( mtilde134 );
				dalitz1.push_back( mtilde234 );
				sort( dalitz1.begin(), dalitz1.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
				//LogWarning("dalitz1") << dalitz1[0] << " " << dalitz1[1] << " " << dalitz1[2];

				dalitzX1 = ( dalitz1[1] + ( 2 * dalitz1[0] ) ) / TMath::Sqrt(3);
				//LogWarning("X1") << dalitzX1 << " " << dalitz1[1] ;
				dalitzX2 = ( dalitz1[2] + ( 2 * dalitz1[0] ) ) / TMath::Sqrt(3);
				//LogWarning("X2") << dalitzX2 << " " << dalitz1[2] ;
				dalitzX3 = ( dalitz1[0] + ( 2 * dalitz1[1] ) ) / TMath::Sqrt(3);
				//LogWarning("X3") << dalitzX3 << " " << dalitz1[0] ;
				dalitzX4 = ( dalitz1[2] + ( 2 * dalitz1[1] ) ) / TMath::Sqrt(3);
				//LogWarning("X4") << dalitzX4 << " " << dalitz1[2] ;
				dalitzX5 = ( dalitz1[0] + ( 2 * dalitz1[2] ) ) / TMath::Sqrt(3);
				//LogWarning("X5") << dalitzX5 << " " << dalitz1[0] ;
				dalitzX6 = ( dalitz1[1] + ( 2 * dalitz1[2] ) ) / TMath::Sqrt(3);
				//LogWarning("X6") << dalitzX6 << " " << dalitz1[1] ;


				double tmptilde2 = pow( m3, 2 ) + pow( m4, 2) + pow( m12, 2 ) + pow( m1234, 2);
				double mtilde34 = pow( m34, 2 ) / tmptilde2;
				double mtilde123 = pow( m123, 2 ) / tmptilde2;
				double mtilde124 = pow( m124, 2 ) / tmptilde2;
				dalitz2.push_back( mtilde34 );
				dalitz2.push_back( mtilde123 );
				dalitz2.push_back( mtilde124 );
				sort( dalitz2.begin(), dalitz2.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 

				dalitzY1 = ( dalitz2[1] + ( 2 * dalitz2[0] ) ) / TMath::Sqrt(3);
				dalitzY2 = ( dalitz2[2] + ( 2 * dalitz2[0] ) ) / TMath::Sqrt(3);
				dalitzY3 = ( dalitz2[0] + ( 2 * dalitz2[1] ) ) / TMath::Sqrt(3);
				dalitzY4 = ( dalitz2[2] + ( 2 * dalitz2[1] ) ) / TMath::Sqrt(3);
				dalitzY5 = ( dalitz2[0] + ( 2 * dalitz2[2] ) ) / TMath::Sqrt(3);
				dalitzY6 = ( dalitz2[1] + ( 2 * dalitz2[2] ) ) / TMath::Sqrt(3);
				///////////////////////////////////////////////////////////////////////////////////////

			}

			///// Variables for tree
			if ( mkTree ) {
				event		= *ievent;
				run		= *Run;
				lumi		= *Lumi;
				jet1Pt 		= JETS[0].p4.Pt();
				jet1Eta 	= JETS[0].p4.Eta();
				jet1Phi 	= JETS[0].p4.Phi();
				jet1E 		= JETS[0].p4.E();
				jet2Pt 		= JETS[1].p4.Pt();
				jet2Eta 	= JETS[1].p4.Eta();
				jet2Phi 	= JETS[1].p4.Phi();
				jet2E 		= JETS[1].p4.E();
				subjet11Pt	= jet1SubjetsTLV[0].Pt();
				subjet11Eta	= jet1SubjetsTLV[0].Eta();
				subjet11Phi	= jet1SubjetsTLV[0].Phi();
				subjet11E	= jet1SubjetsTLV[0].E();
				subjet12Pt	= jet1SubjetsTLV[1].Pt();
				subjet12Eta	= jet1SubjetsTLV[1].Eta();
				subjet12Phi	= jet1SubjetsTLV[1].Phi();
				subjet12E	= jet1SubjetsTLV[1].E();
				subjet21Pt	= jet2SubjetsTLV[0].Pt();
				subjet21Eta	= jet2SubjetsTLV[0].Eta();
				subjet21Phi	= jet2SubjetsTLV[0].Phi();
				subjet21E	= jet2SubjetsTLV[0].E();
				subjet22Pt	= jet2SubjetsTLV[1].Pt();
				subjet22Eta	= jet2SubjetsTLV[1].Eta();
				subjet22Phi	= jet2SubjetsTLV[1].Phi();
				subjet22E	= jet2SubjetsTLV[1].E();
				RUNAtree->Fill();

			} else {

				histos1D_[ "HT_cutDijet" ]->Fill( HT, scale  );
				histos1D_[ "NPV_cutDijet" ]->Fill( numPV, scale );
				histos1D_[ "jetNum_cutDijet" ]->Fill( numJets, scale );
				histos1D_[ "jet1Pt_cutDijet" ]->Fill( JETS[0].p4.Pt(), scale  );
				histos1D_[ "jet1Eta_cutDijet" ]->Fill( JETS[0].p4.Eta(), scale  );
				histos1D_[ "jet1Mass_cutDijet" ]->Fill( JETS[0].mass, scale );
				for (size_t k = 0; k < JETS.size(); k++) {
					histos1D_[ "jetPt_cutDijet" ]->Fill( JETS[k].p4.Pt(), scale  );
					histos1D_[ "jetEta_cutDijet" ]->Fill( JETS[k].p4.Eta(), scale  );
					histos1D_[ "jetMass_cutDijet" ]->Fill( JETS[k].mass, scale );
				 }

				histos1D_[ "massAsymmetry_cutDijet" ]->Fill( massAsym, scale  );
				histos1D_[ "massAve_cutDijet" ]->Fill( massAve, scale  );
				histos2D_[ "massAvevsJet1Mass_cutDijet" ]->Fill( massAve, jet1Mass, scale );
				histos2D_[ "massAvevsJet2Mass_cutDijet" ]->Fill( massAve, jet2Mass, scale );
				histos2D_[ "jet1vs2Mass_cutDijet" ]->Fill( jet1Mass, jet2Mass, scale );

				histos1D_[ "cosThetaStar_cutDijet" ]->Fill( cosThetaStar, scale  );
				histos1D_[ "jet1Tau1_cutDijet" ]->Fill( JETS[0].tau1, scale );
				histos1D_[ "jet1Tau2_cutDijet" ]->Fill( JETS[0].tau2, scale );
				histos1D_[ "jet1Tau3_cutDijet" ]->Fill( JETS[0].tau3, scale );
				histos1D_[ "jet1Tau21_cutDijet" ]->Fill( jet1Tau21, scale );
				histos1D_[ "jet1Tau31_cutDijet" ]->Fill( jet1Tau31, scale );
				histos1D_[ "jet1Tau32_cutDijet" ]->Fill( jet1Tau32, scale );
				histos2D_[ "dijetCorr_cutDijet" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), scale );
				histos2D_[ "dijetCorrPhi_cutDijet" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), scale );

				histos1D_[ "jet1Subjet1Pt_cutDijet" ]->Fill( jet1SubjetsTLV[0].Pt(), scale );
				histos1D_[ "jet1Subjet2Pt_cutDijet" ]->Fill( jet1SubjetsTLV[1].Pt(), scale );
				histos1D_[ "jet1SubjetPtRatio_cutDijet" ]->Fill( jet1SubjetPtRatio, scale );
				histos1D_[ "jet1Subjet1Mass_cutDijet" ]->Fill( jet1SubjetsTLV[0].M(), scale );
				histos1D_[ "jet1Subjet2Mass_cutDijet" ]->Fill( jet1SubjetsTLV[1].M(), scale );
				histos1D_[ "jet1SubjetMass21Ratio_cutDijet" ]->Fill( jet1SubjetMass21Ratio, scale );
				histos1D_[ "jet1Subjet112MassRatio_cutDijet" ]->Fill( jet1Subjet112MassRatio, scale );
				histos1D_[ "jet1Subjet1JetMassRatio_cutDijet" ]->Fill( jet1Subjet1JetMassRatio, scale );
				histos1D_[ "jet1Subjet212MassRatio_cutDijet" ]->Fill( jet1Subjet212MassRatio, scale );
				histos1D_[ "jet1Subjet2JetMassRatio_cutDijet" ]->Fill( jet1Subjet2JetMassRatio, scale );
				histos2D_[ "jet1Subjet12Mass_cutDijet" ]->Fill( jet1SubjetsTLV[0].M(), jet1SubjetsTLV[1].M(), scale );
				histos2D_[ "jet1Subjet112vs212MassRatio_cutDijet" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio, scale );
				histos2D_[ "jet1Subjet1JetvsSubjet2JetMassRatio_cutDijet" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio, scale );

				histos1D_[ "jet2Subjet1Pt_cutDijet" ]->Fill( jet2SubjetsTLV[0].Pt(), scale );
				histos1D_[ "jet2Subjet2Pt_cutDijet" ]->Fill( jet2SubjetsTLV[1].Pt(), scale );
				histos1D_[ "jet2SubjetPtRatio_cutDijet" ]->Fill( jet2SubjetPtRatio, scale );
				histos1D_[ "jet2Subjet1Mass_cutDijet" ]->Fill( jet2SubjetsTLV[0].M(), scale );
				histos1D_[ "jet2Subjet2Mass_cutDijet" ]->Fill( jet2SubjetsTLV[1].M(), scale );
				histos1D_[ "jet2SubjetMass21Ratio_cutDijet" ]->Fill( jet2SubjetMass21Ratio, scale );
				histos1D_[ "jet2Subjet112MassRatio_cutDijet" ]->Fill( jet2Subjet112MassRatio, scale );
				histos1D_[ "jet2Subjet1JetMassRatio_cutDijet" ]->Fill( jet2Subjet1JetMassRatio, scale );
				histos1D_[ "jet2Subjet212MassRatio_cutDijet" ]->Fill( jet2Subjet212MassRatio, scale );
				histos1D_[ "jet2Subjet2JetMassRatio_cutDijet" ]->Fill( jet2Subjet2JetMassRatio, scale );
				histos2D_[ "jet2Subjet12Mass_cutDijet" ]->Fill( jet2SubjetsTLV[0].M(), jet2SubjetsTLV[1].M(), scale );
				histos2D_[ "jet2Subjet112vs212MassRatio_cutDijet" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio, scale );
				histos2D_[ "jet2Subjet1JetvsSubjet2JetMassRatio_cutDijet" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio, scale );

				histos1D_[ "subjetPtRatio_cutDijet" ]->Fill( jet1SubjetPtRatio, scale );
				histos1D_[ "subjetPtRatio_cutDijet" ]->Fill( jet2SubjetPtRatio, scale );
				histos1D_[ "subjetMass21Ratio_cutDijet" ]->Fill( jet1SubjetMass21Ratio, scale );
				histos1D_[ "subjetMass21Ratio_cutDijet" ]->Fill( jet2SubjetMass21Ratio, scale );
				histos1D_[ "subjet112MassRatio_cutDijet" ]->Fill( jet1Subjet112MassRatio, scale );
				histos1D_[ "subjet112MassRatio_cutDijet" ]->Fill( jet2Subjet112MassRatio, scale );
				histos1D_[ "subjet212MassRatio_cutDijet" ]->Fill( jet1Subjet212MassRatio, scale );
				histos1D_[ "subjet212MassRatio_cutDijet" ]->Fill( jet2Subjet212MassRatio, scale );
				histos2D_[ "subjet12Mass_cutDijet" ]->Fill( jet1SubjetsTLV[0].M(), jet1SubjetsTLV[1].M(), scale );
				histos2D_[ "subjet12Mass_cutDijet" ]->Fill( jet2SubjetsTLV[0].M(), jet2SubjetsTLV[1].M(), scale );
				histos2D_[ "subjet112vs212MassRatio_cutDijet" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio, scale );
				histos2D_[ "subjet112vs212MassRatio_cutDijet" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio, scale );
				histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutDijet" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio, scale );
				histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutDijet" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio, scale );

				histos1D_[ "subjetPolAngle13412_cutDijet" ]->Fill( cosPhi13412, scale );
				histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutDijet" ]->Fill( cosPhi13412, jet1SubjetPtRatio, scale );
				histos1D_[ "subjetPolAngle31234_cutDijet" ]->Fill( cosPhi31234, scale );
				histos2D_[ "subjetPolAngle13412vs31234_cutDijet" ]->Fill( cosPhi13412, cosPhi31234, scale );
				histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutDijet" ]->Fill( cosPhi31234, jet2SubjetPtRatio, scale );
				histos1D_[ "mu1_cutDijet" ]->Fill( dalitz1[0], scale );
				histos1D_[ "mu2_cutDijet" ]->Fill( dalitz1[1], scale );
				histos1D_[ "mu3_cutDijet" ]->Fill( dalitz1[2], scale );
				histos2D_[ "mu1234_cutDijet" ]->Fill( dalitz1[0], dalitz1[2], scale );
				histos2D_[ "mu1234_cutDijet" ]->Fill( dalitz1[1], dalitz1[2], scale );
				histos2D_[ "mu1234_cutDijet" ]->Fill( dalitz1[0], dalitz1[1], scale );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX1, dalitz1[1], scale );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX2, dalitz1[2], scale );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX3, dalitz1[0], scale );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX4, dalitz1[2], scale );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX5, dalitz1[0], scale );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX6, dalitz1[1], scale );

				histos1D_[ "mu4_cutDijet" ]->Fill( dalitz2[0], scale );
				histos1D_[ "mu5_cutDijet" ]->Fill( dalitz2[1], scale );
				histos1D_[ "mu6_cutDijet" ]->Fill( dalitz2[2], scale );
				histos2D_[ "mu3412_cutDijet" ]->Fill( dalitz2[0], dalitz2[2], scale );
				histos2D_[ "mu3412_cutDijet" ]->Fill( dalitz2[1], dalitz2[2], scale );
				histos2D_[ "mu3412_cutDijet" ]->Fill( dalitz2[0], dalitz2[1], scale );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY1, dalitz2[1], scale );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY2, dalitz2[2], scale );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY3, dalitz2[0], scale );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY4, dalitz2[2], scale );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY5, dalitz2[0], scale );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY6, dalitz2[1], scale );

				if( massAsym < cutAsymvalue ){
					cutmap["Asymmetry"] += 1;
					histos1D_[ "massAve_cutAsym" ]->Fill( massAve, scale  );
					histos1D_[ "cosThetaStar_cutAsym" ]->Fill( cosThetaStar, scale  );
					histos1D_[ "jet1Tau21_cutAsym" ]->Fill( jet1Tau21, scale  );
					histos1D_[ "jet1Tau31_cutAsym" ]->Fill( jet1Tau31, scale  );
					histos1D_[ "jet1Tau32_cutAsym" ]->Fill( jet1Tau32, scale  );
					histos1D_[ "subjetPtRatio_cutAsym" ]->Fill( jet1SubjetPtRatio, scale );
					histos1D_[ "subjetPtRatio_cutAsym" ]->Fill( jet2SubjetPtRatio, scale );
					histos1D_[ "subjetMass21Ratio_cutAsym" ]->Fill( jet1SubjetMass21Ratio, scale );
					histos1D_[ "subjetMass21Ratio_cutAsym" ]->Fill( jet2SubjetMass21Ratio, scale );
					histos1D_[ "subjet112MassRatio_cutAsym" ]->Fill( jet1Subjet112MassRatio, scale );
					histos1D_[ "subjet112MassRatio_cutAsym" ]->Fill( jet2Subjet112MassRatio, scale );
					histos1D_[ "subjet212MassRatio_cutAsym" ]->Fill( jet1Subjet212MassRatio, scale );
					histos1D_[ "subjet212MassRatio_cutAsym" ]->Fill( jet2Subjet212MassRatio, scale );
					histos1D_[ "subjetPolAngle13412_cutAsym" ]->Fill( cosPhi13412, scale );
					histos1D_[ "subjetPolAngle31234_cutAsym" ]->Fill( cosPhi31234, scale );
					histos2D_[ "dijetCorr_cutAsym" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), scale );
					histos2D_[ "dijetCorrPhi_cutAsym" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), scale );
					histos2D_[ "subjet12Mass_cutAsym" ]->Fill( jet1SubjetsTLV[0].M(), jet1SubjetsTLV[1].M(), scale );
					histos2D_[ "subjet12Mass_cutAsym" ]->Fill( jet2SubjetsTLV[0].M(), jet2SubjetsTLV[1].M(), scale );
					histos2D_[ "subjet112vs212MassRatio_cutAsym" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio, scale );
					histos2D_[ "subjet112vs212MassRatio_cutAsym" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio, scale );
					histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio, scale );
					histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio, scale );
					histos2D_[ "subjetPolAngle13412vs31234_cutAsym" ]->Fill( cosPhi13412, cosPhi31234, scale );
					histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutAsym" ]->Fill( cosPhi13412, jet1SubjetPtRatio, scale );
					histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutAsym" ]->Fill( cosPhi31234, jet2SubjetPtRatio, scale );
					histos2D_[ "mu1234_cutAsym" ]->Fill( dalitz1[0], dalitz1[2], scale );
					histos2D_[ "mu1234_cutAsym" ]->Fill( dalitz1[1], dalitz1[2], scale );
					histos2D_[ "mu1234_cutAsym" ]->Fill( dalitz1[0], dalitz1[1], scale );
					histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzX1, dalitz1[1], scale );
					histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzX2, dalitz1[2], scale );
					histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzX3, dalitz1[0], scale );
					histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzX4, dalitz1[2], scale );
					histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzX5, dalitz1[0], scale );
					histos2D_[ "dalitz1234_cutAsym" ]->Fill( dalitzX6, dalitz1[1], scale );
					histos2D_[ "mu3412_cutAsym" ]->Fill( dalitz2[0], dalitz2[2], scale );
					histos2D_[ "mu3412_cutAsym" ]->Fill( dalitz2[1], dalitz2[2], scale );
					histos2D_[ "mu3412_cutAsym" ]->Fill( dalitz2[0], dalitz2[1], scale );
					histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY1, dalitz2[1], scale );
					histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY2, dalitz2[2], scale );
					histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY3, dalitz2[0], scale );
					histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY4, dalitz2[2], scale );
					histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY5, dalitz2[0], scale );
					histos2D_[ "dalitz3412_cutAsym" ]->Fill( dalitzY6, dalitz2[1], scale );

					//if( TMath::Abs( cosThetaStar ) < 0.3 ){
					if( TMath::Abs( cosThetaStar ) < cutCosThetavalue ){
						cutmap["CosTheta"] += 1;
						histos1D_[ "massAve_cutCosTheta" ]->Fill( massAve, scale  );
						histos1D_[ "jet1Tau21_cutCosTheta" ]->Fill( jet1Tau21, scale  );
						histos1D_[ "jet1Tau31_cutCosTheta" ]->Fill( jet1Tau31, scale  );
						histos1D_[ "jet1Tau32_cutCosTheta" ]->Fill( jet1Tau32, scale  );
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
						histos1D_[ "subjetPolAngle13412_cutCosTheta" ]->Fill( cosPhi13412, scale );
						histos1D_[ "subjetPolAngle31234_cutCosTheta" ]->Fill( cosPhi31234, scale );
						histos2D_[ "dijetCorr_cutCosTheta" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), scale );
						histos2D_[ "dijetCorrPhi_cutCosTheta" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), scale );
						histos2D_[ "subjet12Mass_cutCosTheta" ]->Fill( jet1SubjetsTLV[0].M(), jet1SubjetsTLV[1].M(), scale );
						histos2D_[ "subjet12Mass_cutCosTheta" ]->Fill( jet2SubjetsTLV[0].M(), jet2SubjetsTLV[1].M(), scale );
						histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio, scale );
						histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio, scale );
						histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio, scale );
						histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio, scale );
						histos2D_[ "subjetPolAngle13412vs31234_cutCosTheta" ]->Fill( cosPhi13412, cosPhi31234, scale );
						histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutCosTheta" ]->Fill( cosPhi13412, jet1SubjetPtRatio, scale );
						histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutCosTheta" ]->Fill( cosPhi31234, jet2SubjetPtRatio, scale );
						histos2D_[ "mu1234_cutCosTheta" ]->Fill( dalitz1[0], dalitz1[2], scale );
						histos2D_[ "mu1234_cutCosTheta" ]->Fill( dalitz1[1], dalitz1[2], scale );
						histos2D_[ "mu1234_cutCosTheta" ]->Fill( dalitz1[0], dalitz1[1], scale );
						histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzX1, dalitz1[1], scale );
						histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzX2, dalitz1[2], scale );
						histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzX3, dalitz1[0], scale );
						histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzX4, dalitz1[2], scale );
						histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzX5, dalitz1[0], scale );
						histos2D_[ "dalitz1234_cutCosTheta" ]->Fill( dalitzX6, dalitz1[1], scale );
						histos2D_[ "mu3412_cutCosTheta" ]->Fill( dalitz2[0], dalitz2[2], scale );
						histos2D_[ "mu3412_cutCosTheta" ]->Fill( dalitz2[1], dalitz2[2], scale );
						histos2D_[ "mu3412_cutCosTheta" ]->Fill( dalitz2[0], dalitz2[1], scale );
						histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY1, dalitz2[1], scale );
						histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY2, dalitz2[2], scale );
						histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY3, dalitz2[0], scale );
						histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY4, dalitz2[2], scale );
						histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY5, dalitz2[0], scale );
						histos2D_[ "dalitz3412_cutCosTheta" ]->Fill( dalitzY6, dalitz2[1], scale );

						if( ( jet1SubjetPtRatio > cutSubjetPtRatiovalue ) && ( jet2SubjetPtRatio > cutSubjetPtRatiovalue ) ){
						//if( ( jet1SubjetPtRatio > 0.3 ) && ( jet2SubjetPtRatio > 0.3 ) ){
							cutmap["SubjetPtRatio"] += 1;
							//massAveForFit = massAve;
							histos1D_[ "massAve_cutSubjetPtRatio" ]->Fill( massAve, scale  );
							histos1D_[ "jet1Tau21_cutSubjetPtRatio" ]->Fill( jet1Tau21, scale  );
							histos1D_[ "jet1Tau31_cutSubjetPtRatio" ]->Fill( jet1Tau31, scale  );
							histos1D_[ "jet1Tau32_cutSubjetPtRatio" ]->Fill( jet1Tau32, scale  );
							histos1D_[ "subjetMass21Ratio_cutSubjetPtRatio" ]->Fill( jet1SubjetMass21Ratio, scale );
							histos1D_[ "subjetMass21Ratio_cutSubjetPtRatio" ]->Fill( jet2SubjetMass21Ratio, scale );
							histos1D_[ "subjet112MassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet112MassRatio, scale );
							histos1D_[ "subjet112MassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet112MassRatio, scale );
							histos1D_[ "subjet212MassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet212MassRatio, scale );
							histos1D_[ "subjet212MassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet212MassRatio, scale );
							histos1D_[ "subjetPolAngle13412_cutSubjetPtRatio" ]->Fill( cosPhi13412, scale );
							histos1D_[ "subjetPolAngle31234_cutSubjetPtRatio" ]->Fill( cosPhi31234, scale );
							histos2D_[ "dijetCorr_cutSubjetPtRatio" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), scale );
							histos2D_[ "dijetCorrPhi_cutSubjetPtRatio" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), scale );
							histos2D_[ "subjet12Mass_cutSubjetPtRatio" ]->Fill( jet1SubjetsTLV[0].M(), jet1SubjetsTLV[1].M(), scale );
							histos2D_[ "subjet12Mass_cutSubjetPtRatio" ]->Fill( jet2SubjetsTLV[0].M(), jet2SubjetsTLV[1].M(), scale );
							histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio, scale );
							histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio, scale );
							histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio, scale );
							histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio, scale );
							histos2D_[ "subjetPolAngle13412vs31234_cutSubjetPtRatio" ]->Fill( cosPhi13412, cosPhi31234, scale );
							histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutSubjetPtRatio" ]->Fill( cosPhi13412, jet1SubjetPtRatio, scale );
							histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutSubjetPtRatio" ]->Fill( cosPhi31234, jet2SubjetPtRatio, scale );
							histos2D_[ "mu1234_cutSubjetPtRatio" ]->Fill( dalitz1[0], dalitz1[2], scale );
							histos2D_[ "mu1234_cutSubjetPtRatio" ]->Fill( dalitz1[1], dalitz1[2], scale );
							histos2D_[ "mu1234_cutSubjetPtRatio" ]->Fill( dalitz1[0], dalitz1[1], scale );
							histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzX1, dalitz1[1], scale );
							histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzX2, dalitz1[2], scale );
							histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzX3, dalitz1[0], scale );
							histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzX4, dalitz1[2], scale );
							histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzX5, dalitz1[0], scale );
							histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Fill( dalitzX6, dalitz1[1], scale );
							histos2D_[ "mu3412_cutSubjetPtRatio" ]->Fill( dalitz2[0], dalitz2[2], scale );
							histos2D_[ "mu3412_cutSubjetPtRatio" ]->Fill( dalitz2[1], dalitz2[2], scale );
							histos2D_[ "mu3412_cutSubjetPtRatio" ]->Fill( dalitz2[0], dalitz2[1], scale );
							histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY1, dalitz2[1], scale );
							histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY2, dalitz2[2], scale );
							histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY3, dalitz2[0], scale );
							histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY4, dalitz2[2], scale );
							histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY5, dalitz2[0], scale );
							histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Fill( dalitzY6, dalitz2[1], scale );

							if ( JETS[0].btagCSV || JETS[1].btagCSV ){
								//LogWarning("btag") <<JETS[0].btagCSV << " " << JETS[1].btagCSV;
								//cutmap["btagAfterSubjetPtRatio"] += 1;
								histos1D_[ "massAve_cutBtagAfterSubjetPtRatio" ]->Fill( massAve, scale  );
							}
						}

						if( jet1Tau31 < cutTau31value ){
						//if(  jet1Tau31 < 0.5 ){
							cutmap["Tau31"] += 1;
							histos1D_[ "massAve_cutTau31" ]->Fill( massAve, scale  );
							histos1D_[ "subjetMass21Ratio_cutTau31" ]->Fill( jet1SubjetMass21Ratio, scale );
							histos1D_[ "subjetMass21Ratio_cutTau31" ]->Fill( jet2SubjetMass21Ratio, scale );
							histos1D_[ "subjet112MassRatio_cutTau31" ]->Fill( jet1Subjet112MassRatio, scale );
							histos1D_[ "subjet112MassRatio_cutTau31" ]->Fill( jet2Subjet112MassRatio, scale );
							histos1D_[ "subjet212MassRatio_cutTau31" ]->Fill( jet1Subjet212MassRatio, scale );
							histos1D_[ "subjet212MassRatio_cutTau31" ]->Fill( jet2Subjet212MassRatio, scale );
							histos1D_[ "subjetPolAngle13412_cutTau31" ]->Fill( cosPhi13412, scale );
							histos1D_[ "subjetPolAngle31234_cutTau31" ]->Fill( cosPhi31234, scale );
							histos2D_[ "dijetCorr_cutTau31" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), scale );
							histos2D_[ "dijetCorrPhi_cutTau31" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), scale );
							histos2D_[ "subjet12Mass_cutTau31" ]->Fill( jet1SubjetsTLV[0].M(), jet1SubjetsTLV[1].M(), scale );
							histos2D_[ "subjet12Mass_cutTau31" ]->Fill( jet2SubjetsTLV[0].M(), jet2SubjetsTLV[1].M(), scale );
							histos2D_[ "subjet112vs212MassRatio_cutTau31" ]->Fill( jet1Subjet112MassRatio, jet1Subjet212MassRatio, scale );
							histos2D_[ "subjet112vs212MassRatio_cutTau31" ]->Fill( jet2Subjet112MassRatio, jet2Subjet212MassRatio, scale );
							histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ]->Fill( jet1Subjet1JetMassRatio, jet1Subjet2JetMassRatio, scale );
							histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ]->Fill( jet2Subjet1JetMassRatio, jet2Subjet2JetMassRatio, scale );
							histos2D_[ "subjetPolAngle13412vs31234_cutTau31" ]->Fill( cosPhi13412, cosPhi31234, scale );

							if ( JETS[0].btagCSV || JETS[1].btagCSV ){
								//LogWarning("btag") <<JETS[0].btagCSV << " " << JETS[1].btagCSV;
								//cutmap["btagAfterTau31"] += 1;
								histos1D_[ "massAve_cutBtagAfterTau31" ]->Fill( massAve, scale  );
							}
						}

						//if(  jet1Tau21 < 0.6 ){
						if(  jet1Tau21 < cutTau21value ){
							cutmap["Tau21"] += 1;
							histos1D_[ "massAve_cutTau21" ]->Fill( massAve, scale  );
							histos2D_[ "subjet12Mass_cutTau21" ]->Fill( jet1SubjetsTLV[0].M(), jet1SubjetsTLV[1].M(), scale );
							histos2D_[ "subjet12Mass_cutTau21" ]->Fill( jet2SubjetsTLV[0].M(), jet2SubjetsTLV[1].M(), scale );
							if ( JETS[0].btagCSV || JETS[1].btagCSV ){
								//LogWarning("btag") <<JETS[0].btagCSV << " " << JETS[1].btagCSV;
								//cutmap["btagAfterTau21"] += 1;
								histos1D_[ "massAve_cutBtagAfterTau21" ]->Fill( massAve, scale  );
							}
						} 
					}
				}
			}
		}
	}
	JETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNBoostedAnalysis::beginJob() {

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
	histos1D_[ "jetMass" ] = fs_->make< TH1D >( "jetMass", "jetMass", 60, 0., 600. );
	histos1D_[ "jetMass" ]->Sumw2();
	histos1D_[ "jetTrimmedMass" ] = fs_->make< TH1D >( "jetTrimmedMass", "jetTrimmedMass", 60, 0., 600. );
	histos1D_[ "jetTrimmedMass" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 150, 0., 1500. );
	histos1D_[ "HT" ]->Sumw2();
	histos1D_[ "NPV" ] = fs_->make< TH1D >( "NPV", "NPV", 80, 0., 80. );
	histos1D_[ "NPV" ]->Sumw2();

	histos1D_[ "HT_cutTrigger" ] = fs_->make< TH1D >( "HT_cutTrigger", "HT_cutTrigger", 150, 0., 1500. );
	histos1D_[ "HT_cutTrigger" ]->Sumw2();
	histos1D_[ "NPV_cutTrigger" ] = fs_->make< TH1D >( "NPV_cutTrigger", "NPV_cutTrigger", 80, 0., 80. );
	histos1D_[ "NPV_cutTrigger" ]->Sumw2();
	histos1D_[ "jetPt_cutTrigger" ] = fs_->make< TH1D >( "jetPt_cutTrigger", "jetPt_cutTrigger", 100, 0., 1000. );
	histos1D_[ "jetPt_cutTrigger" ]->Sumw2();
	histos1D_[ "jetEta_cutTrigger" ] = fs_->make< TH1D >( "jetEta_cutTrigger", "jetEta_cutTrigger", 100, -5., 5. );
	histos1D_[ "jetEta_cutTrigger" ]->Sumw2();
	histos1D_[ "jetNum_cutTrigger" ] = fs_->make< TH1D >( "jetNum_cutTrigger", "jetNum_cutTrigger", 10, 0., 10. );
	histos1D_[ "jetNum_cutTrigger" ]->Sumw2();
	histos1D_[ "jetMass_cutTrigger" ] = fs_->make< TH1D >( "jetMass_cutTrigger", "jetMass_cutTrigger", 60, 0., 600. );
	histos1D_[ "jetMass_cutTrigger" ]->Sumw2();
	histos1D_[ "jet1Pt_cutTrigger" ] = fs_->make< TH1D >( "jet1Pt_cutTrigger", "jet1Pt_cutTrigger", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutTrigger" ]->Sumw2();
	histos1D_[ "jet1Eta_cutTrigger" ] = fs_->make< TH1D >( "jet1Eta_cutTrigger", "jet1Eta_cutTrigger", 100, -5., 5. );
	histos1D_[ "jet1Eta_cutTrigger" ]->Sumw2();
	histos1D_[ "jet1Mass_cutTrigger" ] = fs_->make< TH1D >( "jet1Mass_cutTrigger", "jet1Mass_cutTrigger", 60, 0., 600. );
	histos1D_[ "jet1Mass_cutTrigger" ]->Sumw2();

	if (mkTree) {
		RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
		RUNAtree->Branch( "run", &run, "run/I" );
		RUNAtree->Branch( "lumi", &lumi, "lumi/I" );
		RUNAtree->Branch( "event", &event, "event/I" );
		RUNAtree->Branch( "scale", &scale, "scale/F" );
		RUNAtree->Branch( "numJets", &numJets, "numJets/I" );
		RUNAtree->Branch( "numPV", &numPV, "numPV/I" );
		RUNAtree->Branch( "HT", &HT, "HT/F" );
		RUNAtree->Branch( "AK4HT", &AK4HT, "AK4HT/F" );
		RUNAtree->Branch( "trimmedMass", &trimmedMass, "trimmedMass/F" );
		RUNAtree->Branch( "jet1Pt", &jet1Pt, "jet1Pt/F" );
		RUNAtree->Branch( "jet1Eta", &jet1Eta, "jet1Eta/F" );
		RUNAtree->Branch( "jet1Phi", &jet1Phi, "jet1Phi/F" );
		RUNAtree->Branch( "jet1E", &jet1E, "jet1E/F" );
		RUNAtree->Branch( "jet1Mass", &jet1Mass, "jet1Mass/F" );
		RUNAtree->Branch( "jet2Pt", &jet2Pt, "jet2Pt/F" );
		RUNAtree->Branch( "jet2Eta", &jet2Eta, "jet2Eta/F" );
		RUNAtree->Branch( "jet2Phi", &jet2Phi, "jet2Phi/F" );
		RUNAtree->Branch( "jet2E", &jet2E, "jet2E/F" );
		RUNAtree->Branch( "jet2Mass", &jet2Mass, "jet2Mass/F" );
		RUNAtree->Branch( "subjet11Pt", &subjet11Pt, "subjet11Pt/F" );
		RUNAtree->Branch( "subjet11Eta", &subjet11Eta, "subjet11Eta/F" );
		RUNAtree->Branch( "subjet11Phi", &subjet11Phi, "subjet11Phi/F" );
		RUNAtree->Branch( "subjet11E", &subjet11E, "subjet11E/F" );
		RUNAtree->Branch( "subjet12Pt", &subjet12Pt, "subjet12Pt/F" );
		RUNAtree->Branch( "subjet12Eta", &subjet12Eta, "subjet12Eta/F" );
		RUNAtree->Branch( "subjet12Phi", &subjet12Phi, "subjet12Phi/F" );
		RUNAtree->Branch( "subjet12E", &subjet12E, "subjet12E/F" );
		RUNAtree->Branch( "subjet21Pt", &subjet21Pt, "subjet21Pt/F" );
		RUNAtree->Branch( "subjet21Eta", &subjet21Eta, "subjet21Eta/F" );
		RUNAtree->Branch( "subjet21Phi", &subjet21Phi, "subjet21Phi/F" );
		RUNAtree->Branch( "subjet21E", &subjet21E, "subjet21E/F" );
		RUNAtree->Branch( "subjet22Pt", &subjet22Pt, "subjet22Pt/F" );
		RUNAtree->Branch( "subjet22Eta", &subjet22Eta, "subjet22Eta/F" );
		RUNAtree->Branch( "subjet22Phi", &subjet22Phi, "subjet22Phi/F" );
		RUNAtree->Branch( "subjet22E", &subjet22E, "subjet22E/F" );
		RUNAtree->Branch( "massAve", &massAve, "massAve/F" );
		RUNAtree->Branch( "massAsym", &massAsym, "massAsym/F" );
		RUNAtree->Branch( "cosThetaStar", &cosThetaStar, "cosThetaStar/F" );
		RUNAtree->Branch( "jet1Tau21", &jet1Tau21, "jet1Tau21/F" );
		RUNAtree->Branch( "jet1Tau31", &jet1Tau31, "jet1Tau31/F" );
		RUNAtree->Branch( "jet1Tau32", &jet1Tau32, "jet1Tau32/F" );
		RUNAtree->Branch( "jet1SubjetPtRatio", &jet1SubjetPtRatio, "jet1SubjetPtRatio/F" );
		RUNAtree->Branch( "jet2SubjetPtRatio", &jet2SubjetPtRatio, "jet2SubjetPtRatio/F" );
		RUNAtree->Branch( "cosPhi13412", &cosPhi13412, "cosPhi13412/F" );
		RUNAtree->Branch( "cosPhi31234", &cosPhi31234, "cosPhi31234/F" );

	} else { 

		histos1D_[ "HT_cutDijet" ] = fs_->make< TH1D >( "HT_cutDijet", "HT_cutDijet", 150, 0., 1500. );
		histos1D_[ "HT_cutDijet" ]->Sumw2();
		histos1D_[ "NPV_cutDijet" ] = fs_->make< TH1D >( "NPV_cutDijet", "NPV_cutDijet", 80, 0., 80. );
		histos1D_[ "NPV_cutDijet" ]->Sumw2();
		histos1D_[ "jetNum_cutDijet" ] = fs_->make< TH1D >( "jetNum_cutDijet", "jetNum_cutDijet", 10, 0., 10. );
		histos1D_[ "jetNum_cutDijet" ]->Sumw2();
		histos1D_[ "jetPt_cutDijet" ] = fs_->make< TH1D >( "jetPt_cutDijet", "jetPt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jetPt_cutDijet" ]->Sumw2();
		histos1D_[ "jetEta_cutDijet" ] = fs_->make< TH1D >( "jetEta_cutDijet", "jetEta_cutDijet", 100, -5., 5. );
		histos1D_[ "jetEta_cutDijet" ]->Sumw2();
		histos1D_[ "jetMass_cutDijet" ] = fs_->make< TH1D >( "jetMass_cutDijet", "jetMass_cutDijet", 60, 0., 600. );
		histos1D_[ "jetMass_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Pt_cutDijet" ] = fs_->make< TH1D >( "jet1Pt_cutDijet", "jet1Pt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Eta_cutDijet" ] = fs_->make< TH1D >( "jet1Eta_cutDijet", "jet1Eta_cutDijet", 100, -5., 5. );
		histos1D_[ "jet1Eta_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Mass_cutDijet" ] = fs_->make< TH1D >( "jet1Mass_cutDijet", "jet1Mass_cutDijet", 60, 0., 600. );
		histos1D_[ "jet1Mass_cutDijet" ]->Sumw2();

		histos1D_[ "massAsymmetry_cutDijet" ] = fs_->make< TH1D >( "massAsymmetry_cutDijet", "massAsymmetry_cutDijet", 20, 0., 1. );
		histos1D_[ "massAsymmetry_cutDijet" ]->Sumw2();
		histos1D_[ "massAve_cutDijet" ] = fs_->make< TH1D >( "massAve_cutDijet", "massAve_cutDijet", 60, 0., 600. );
		histos1D_[ "massAve_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet1Mass_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutDijet", "massAvevsJet1Mass_cutDijet", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet1Mass_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet2Mass_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutDijet", "massAvevsJet2Mass_cutDijet", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet2Mass_cutDijet" ]->Sumw2();
		histos2D_[ "jet1vs2Mass_cutDijet" ] = fs_->make< TH2D >( "jet1vs2Mass_cutDijet", "jet1vs2Mass_cutDijet", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "jet1vs2Mass_cutDijet" ]->Sumw2();
		histos1D_[ "cosThetaStar_cutDijet" ] = fs_->make< TH1D >( "cosThetaStar_cutDijet", "cosThetaStar_cutDijet", 20, 0., 1. );
		histos1D_[ "cosThetaStar_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Tau1_cutDijet" ] = fs_->make< TH1D >( "jet1Tau1_cutDijet", "jet1Tau1_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Tau1_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Tau2_cutDijet" ] = fs_->make< TH1D >( "jet1Tau2_cutDijet", "jet1Tau2_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Tau2_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Tau3_cutDijet" ] = fs_->make< TH1D >( "jet1Tau3_cutDijet", "jet1Tau3_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Tau3_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Tau21_cutDijet" ] = fs_->make< TH1D >( "jet1Tau21_cutDijet", "jet1Tau21_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Tau21_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Tau31_cutDijet" ] = fs_->make< TH1D >( "jet1Tau31_cutDijet", "jet1Tau31_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Tau31_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Tau32_cutDijet" ] = fs_->make< TH1D >( "jet1Tau32_cutDijet", "jet1Tau32_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Tau32_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet1Pt_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet1Pt_cutDijet", "jet1Subjet1Pt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jet1Subjet1Pt_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet2Pt_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet2Pt_cutDijet", "jet1Subjet2Pt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jet1Subjet2Pt_cutDijet" ]->Sumw2();
		histos1D_[ "jet1SubjetPtRatio_cutDijet" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutDijet", "jet1SubjetPtRatio_cutDijet", 20, 0, 1.);
		histos1D_[ "jet1SubjetPtRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet1SubjetMass21Ratio_cutDijet" ] = fs_->make< TH1D >( "jet1SubjetMass21Ratio_cutDijet", "jet1SubjetMass21Ratio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1SubjetMass21Ratio_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet112MassRatio_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet112MassRatio_cutDijet", "jet1Subjet112MassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Subjet112MassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet1JetMassRatio_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet1JetMassRatio_cutDijet", "jet1Subjet1JetMassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Subjet1JetMassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet212MassRatio_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet212MassRatio_cutDijet", "jet1Subjet212MassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Subjet212MassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet2JetMassRatio_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet2JetMassRatio_cutDijet", "jet1Subjet2JetMassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1Subjet2JetMassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet1Mass_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet1Mass_cutDijet", "jet1Subjet1Mass_cutDijet", 20, 0., 100. );
		histos1D_[ "jet1Subjet1Mass_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Subjet2Mass_cutDijet" ] = fs_->make< TH1D >( "jet1Subjet2Mass_cutDijet", "jet1Subjet2Mass_cutDijet", 20, 0., 100. );
		histos1D_[ "jet1Subjet2Mass_cutDijet" ]->Sumw2();
		histos2D_[ "jet1Subjet12Mass_cutDijet" ] = fs_->make< TH2D >( "jet1Subjet12Mass_cutDijet", "jet1Subjet12Mass_cutDijet", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "jet1Subjet12Mass_cutDijet" ]->Sumw2();
		histos2D_[ "jet1Subjet112vs212MassRatio_cutDijet" ] = fs_->make< TH2D >( "jet1Subjet112vs212MassRatio_cutDijet", "jet1Subjet112vs212MassRatio_cutDijet", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "jet1Subjet112vs212MassRatio_cutDijet" ]->Sumw2();
		histos2D_[ "jet1Subjet1JetvsSubjet2JetMassRatio_cutDijet" ] = fs_->make< TH2D >( "jet1Subjet1JetvsSubjet2JetMassRatio_cutDijet", "jet1Subjet1JetvsSubjet2JetMassRatio_cutDijet", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "jet1Subjet1JetvsSubjet2JetMassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet1Pt_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet1Pt_cutDijet", "jet2Subjet1Pt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jet2Subjet1Pt_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet2Pt_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet2Pt_cutDijet", "jet2Subjet2Pt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jet2Subjet2Pt_cutDijet" ]->Sumw2();
		histos1D_[ "jet2SubjetPtRatio_cutDijet" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutDijet", "jet2SubjetPtRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2SubjetPtRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2SubjetMass21Ratio_cutDijet" ] = fs_->make< TH1D >( "jet2SubjetMass21Ratio_cutDijet", "jet2SubjetMass21Ratio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2SubjetMass21Ratio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet112MassRatio_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet112MassRatio_cutDijet", "jet2Subjet112MassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Subjet112MassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet1JetMassRatio_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet1JetMassRatio_cutDijet", "jet2Subjet1JetMassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Subjet1JetMassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet212MassRatio_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet212MassRatio_cutDijet", "jet2Subjet212MassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Subjet212MassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet2JetMassRatio_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet2JetMassRatio_cutDijet", "jet2Subjet2JetMassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Subjet2JetMassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet1Mass_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet1Mass_cutDijet", "jet2Subjet1Mass_cutDijet", 20, 0., 100.);
		histos1D_[ "jet2Subjet1Mass_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Subjet2Mass_cutDijet" ] = fs_->make< TH1D >( "jet2Subjet2Mass_cutDijet", "jet2Subjet2Mass_cutDijet", 20, 0., 100. );
		histos1D_[ "jet2Subjet2Mass_cutDijet" ]->Sumw2();
		histos2D_[ "jet2Subjet12Mass_cutDijet" ] = fs_->make< TH2D >( "jet2Subjet12Mass_cutDijet", "jet2Subjet12Mass_cutDijet", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "jet2Subjet12Mass_cutDijet" ]->Sumw2();
		histos2D_[ "jet2Subjet112vs212MassRatio_cutDijet" ] = fs_->make< TH2D >( "jet2Subjet112vs212MassRatio_cutDijet", "jet2Subjet112vs212MassRatio_cutDijet", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "jet2Subjet112vs212MassRatio_cutDijet" ]->Sumw2();
		histos2D_[ "jet2Subjet1JetvsSubjet2JetMassRatio_cutDijet" ] = fs_->make< TH2D >( "jet2Subjet1JetvsSubjet2JetMassRatio_cutDijet", "jet2Subjet1JetvsSubjet2JetMassRatio_cutDijet", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "jet2Subjet1JetvsSubjet2JetMassRatio_cutDijet" ]->Sumw2();

		histos1D_[ "subjetPtRatio_cutDijet" ] = fs_->make< TH1D >( "subjetPtRatio_cutDijet", "subjetPtRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "subjetPtRatio_cutDijet" ]->Sumw2();
		histos1D_[ "subjetMass21Ratio_cutDijet" ] = fs_->make< TH1D >( "subjetMass21Ratio_cutDijet", "subjetMass21Ratio_cutDijet", 20, 0., 1. );
		histos1D_[ "subjetMass21Ratio_cutDijet" ]->Sumw2();
		histos1D_[ "subjet112MassRatio_cutDijet" ] = fs_->make< TH1D >( "subjet112MassRatio_cutDijet", "subjet112MassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "subjet112MassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "subjet212MassRatio_cutDijet" ] = fs_->make< TH1D >( "subjet212MassRatio_cutDijet", "subjet212MassRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "subjet212MassRatio_cutDijet" ]->Sumw2();
		histos2D_[ "subjet12Mass_cutDijet" ] = fs_->make< TH2D >( "subjet12Mass_cutDijet", "subjet12Mass_cutDijet", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "subjet12Mass_cutDijet" ]->Sumw2();
		histos2D_[ "dijetCorr_cutDijet" ] = fs_->make< TH2D >( "dijetCorr_cutDijet", "dijetCorr_cutDijet", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutDijet" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutDijet" ] = fs_->make< TH2D >( "dijetCorrPhi_cutDijet", "dijetCorrPhi_cutDijet", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutDijet" ]->Sumw2();
		histos2D_[ "subjet112vs212MassRatio_cutDijet" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutDijet", "subjet112vs212MassRatio_cutDijet", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet112vs212MassRatio_cutDijet" ]->Sumw2();
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutDijet" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutDijet", "subjet1JetvsSubjet2JetMassRatio_cutDijet", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutDijet" ]->Sumw2();
		histos1D_[ "subjetPolAngle13412_cutDijet" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutDijet", "subjetPolAngle13412_cutDijet", 100, 0., 1. );
		histos1D_[ "subjetPolAngle13412_cutDijet" ]->Sumw2();
		histos1D_[ "subjetPolAngle31234_cutDijet" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutDijet", "subjetPolAngle31234_cutDijet", 100, 0., 1. );
		histos1D_[ "subjetPolAngle31234_cutDijet" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vs31234_cutDijet" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutDijet", "subjetPolAngle13412vs31234_cutDijet", 100, 0., 1., 100, 0., 1. );
		histos2D_[ "subjetPolAngle13412vs31234_cutDijet" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutDijet" ] = fs_->make< TH2D >( "subjetPolAngle13412vsSubjetPtRatio_cutDijet", "subjetPolAngle13412vsSubjetPtRatio_cutDijet", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutDijet" ]->Sumw2();
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutDijet" ] = fs_->make< TH2D >( "subjetPolAngle31234vsSubjetPtRatio_cutDijet", "subjetPolAngle31234vsSubjetPtRatio_cutDijet", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutDijet" ]->Sumw2();
		histos1D_[ "mu1_cutDijet" ] = fs_->make< TH1D >( "mu1_cutDijet", "mu1_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu1_cutDijet" ]->Sumw2();
		histos1D_[ "mu2_cutDijet" ] = fs_->make< TH1D >( "mu2_cutDijet", "mu2_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu2_cutDijet" ]->Sumw2();
		histos1D_[ "mu3_cutDijet" ] = fs_->make< TH1D >( "mu3_cutDijet", "mu3_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu3_cutDijet" ]->Sumw2();
		histos2D_[ "mu1234_cutDijet" ] = fs_->make< TH2D >( "mu1234_cutDijet", "mu1234_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu1234_cutDijet" ]->Sumw2();
		histos2D_[ "dalitz1234_cutDijet" ] = fs_->make< TH2D >( "dalitz1234_cutDijet", "dalitz1234_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz1234_cutDijet" ]->Sumw2();
		histos1D_[ "mu4_cutDijet" ] = fs_->make< TH1D >( "mu4_cutDijet", "mu4_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu4_cutDijet" ]->Sumw2();
		histos1D_[ "mu5_cutDijet" ] = fs_->make< TH1D >( "mu5_cutDijet", "mu5_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu5_cutDijet" ]->Sumw2();
		histos1D_[ "mu6_cutDijet" ] = fs_->make< TH1D >( "mu6_cutDijet", "mu6_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu6_cutDijet" ]->Sumw2();
		histos2D_[ "mu3412_cutDijet" ] = fs_->make< TH2D >( "mu3412_cutDijet", "mu3412_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu3412_cutDijet" ]->Sumw2();
		histos2D_[ "dalitz3412_cutDijet" ] = fs_->make< TH2D >( "dalitz3412_cutDijet", "dalitz3412_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz3412_cutDijet" ]->Sumw2();

		histos1D_[ "massAve_cutAsym" ] = fs_->make< TH1D >( "massAve_cutAsym", "massAve_cutAsym", 60, 0., 600. );
		histos1D_[ "massAve_cutAsym" ]->Sumw2();
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
		histos1D_[ "subjetPolAngle13412_cutAsym" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutAsym", "subjetPolAngle13412_cutAsym", 100, 0., 1. );
		histos1D_[ "subjetPolAngle13412_cutAsym" ]->Sumw2();
		histos1D_[ "subjetPolAngle31234_cutAsym" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutAsym", "subjetPolAngle31234_cutAsym", 100, 0., 1. );
		histos1D_[ "subjetPolAngle31234_cutAsym" ]->Sumw2();
		histos2D_[ "subjet12Mass_cutAsym" ] = fs_->make< TH2D >( "subjet12Mass_cutAsym", "subjet12Mass_cutAsym", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "subjet12Mass_cutAsym" ]->Sumw2();
		histos2D_[ "dijetCorr_cutAsym" ] = fs_->make< TH2D >( "dijetCorr_cutAsym", "dijetCorr_cutAsym", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutAsym" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutAsym" ] = fs_->make< TH2D >( "dijetCorrPhi_cutAsym", "dijetCorrPhi_cutAsym", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutAsym" ]->Sumw2();
		histos2D_[ "subjet112vs212MassRatio_cutAsym" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutAsym", "subjet112vs212MassRatio_cutAsym", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet112vs212MassRatio_cutAsym" ]->Sumw2();
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutAsym", "subjet1JetvsSubjet2JetMassRatio_cutAsym", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutAsym" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vs31234_cutAsym" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutAsym", "subjetPolAngle13412vs31234_cutAsym", 100, 0., 1., 100, 0., 1. );
		histos2D_[ "subjetPolAngle13412vs31234_cutAsym" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutAsym" ] = fs_->make< TH2D >( "subjetPolAngle13412vsSubjetPtRatio_cutAsym", "subjetPolAngle13412vsSubjetPtRatio_cutAsym", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutAsym" ]->Sumw2();
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutAsym" ] = fs_->make< TH2D >( "subjetPolAngle31234vsSubjetPtRatio_cutAsym", "subjetPolAngle31234vsSubjetPtRatio_cutAsym", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutAsym" ]->Sumw2();
		histos2D_[ "mu1234_cutAsym" ] = fs_->make< TH2D >( "mu1234_cutAsym", "mu1234_cutAsym", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu1234_cutAsym" ]->Sumw2();
		histos2D_[ "mu3412_cutAsym" ] = fs_->make< TH2D >( "mu3412_cutAsym", "mu3412_cutAsym", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu3412_cutAsym" ]->Sumw2();
		histos2D_[ "dalitz1234_cutAsym" ] = fs_->make< TH2D >( "dalitz1234_cutAsym", "dalitz1234_cutAsym", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz1234_cutAsym" ]->Sumw2();
		histos2D_[ "dalitz3412_cutAsym" ] = fs_->make< TH2D >( "dalitz3412_cutAsym", "dalitz3412_cutAsym", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz3412_cutAsym" ]->Sumw2();

		histos1D_[ "massAve_cutCosTheta" ] = fs_->make< TH1D >( "massAve_cutCosTheta", "massAve_cutCosTheta", 60, 0., 600. );
		histos1D_[ "massAve_cutCosTheta" ]->Sumw2();
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
		histos1D_[ "subjetPolAngle13412_cutCosTheta" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutCosTheta", "subjetPolAngle13412_cutCosTheta", 100, 0., 1. );
		histos1D_[ "subjetPolAngle13412_cutCosTheta" ]->Sumw2();
		histos1D_[ "subjetPolAngle31234_cutCosTheta" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutCosTheta", "subjetPolAngle31234_cutCosTheta", 100, 0., 1. );
		histos1D_[ "subjetPolAngle31234_cutCosTheta" ]->Sumw2();
		histos2D_[ "subjet12Mass_cutCosTheta" ] = fs_->make< TH2D >( "subjet12Mass_cutCosTheta", "subjet12Mass_cutCosTheta", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "subjet12Mass_cutCosTheta" ]->Sumw2();
		histos2D_[ "dijetCorr_cutCosTheta" ] = fs_->make< TH2D >( "dijetCorr_cutCosTheta", "dijetCorr_cutCosTheta", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutCosTheta" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutCosTheta" ] = fs_->make< TH2D >( "dijetCorrPhi_cutCosTheta", "dijetCorrPhi_cutCosTheta", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutCosTheta" ]->Sumw2();
		histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutCosTheta", "subjet112vs212MassRatio_cutCosTheta", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet112vs212MassRatio_cutCosTheta" ]->Sumw2();
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutCosTheta", "subjet1JetvsSubjet2JetMassRatio_cutCosTheta", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutCosTheta" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vs31234_cutCosTheta" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutCosTheta", "subjetPolAngle13412vs31234_cutCosTheta", 100, 0., 1., 100, 0., 1. );
		histos2D_[ "subjetPolAngle13412vs31234_cutCosTheta" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutCosTheta" ] = fs_->make< TH2D >( "subjetPolAngle13412vsSubjetPtRatio_cutCosTheta", "subjetPolAngle13412vsSubjetPtRatio_cutCosTheta", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutCosTheta" ]->Sumw2();
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutCosTheta" ] = fs_->make< TH2D >( "subjetPolAngle31234vsSubjetPtRatio_cutCosTheta", "subjetPolAngle31234vsSubjetPtRatio_cutCosTheta", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutCosTheta" ]->Sumw2();
		histos2D_[ "mu1234_cutCosTheta" ] = fs_->make< TH2D >( "mu1234_cutCosTheta", "mu1234_cutCosTheta", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu1234_cutCosTheta" ]->Sumw2();
		histos2D_[ "mu3412_cutCosTheta" ] = fs_->make< TH2D >( "mu3412_cutCosTheta", "mu3412_cutCosTheta", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu3412_cutCosTheta" ]->Sumw2();
		histos2D_[ "dalitz1234_cutCosTheta" ] = fs_->make< TH2D >( "dalitz1234_cutCosTheta", "dalitz1234_cutCosTheta", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz1234_cutCosTheta" ]->Sumw2();
		histos2D_[ "dalitz3412_cutCosTheta" ] = fs_->make< TH2D >( "dalitz3412_cutCosTheta", "dalitz3412_cutCosTheta", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz3412_cutCosTheta" ]->Sumw2();

		histos1D_[ "massAve_cutSubjetPtRatio" ] = fs_->make< TH1D >( "massAve_cutSubjetPtRatio", "massAve_cutSubjetPtRatio", 60, 0., 600. );
		histos1D_[ "massAve_cutSubjetPtRatio" ]->Sumw2();
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
		histos1D_[ "subjetPolAngle13412_cutSubjetPtRatio" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutSubjetPtRatio", "subjetPolAngle13412_cutSubjetPtRatio", 100, 0., 1. );
		histos1D_[ "subjetPolAngle13412_cutSubjetPtRatio" ]->Sumw2();
		histos1D_[ "subjetPolAngle31234_cutSubjetPtRatio" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutSubjetPtRatio", "subjetPolAngle31234_cutSubjetPtRatio", 100, 0., 1. );
		histos1D_[ "subjetPolAngle31234_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "subjet12Mass_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjet12Mass_cutSubjetPtRatio", "subjet12Mass_cutSubjetPtRatio", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "subjet12Mass_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "dijetCorr_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dijetCorr_cutSubjetPtRatio", "dijetCorr_cutSubjetPtRatio", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dijetCorrPhi_cutSubjetPtRatio", "dijetCorrPhi_cutSubjetPtRatio", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutSubjetPtRatio", "subjet112vs212MassRatio_cutSubjetPtRatio", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet112vs212MassRatio_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio", "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vs31234_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutSubjetPtRatio", "subjetPolAngle13412vs31234_cutSubjetPtRatio", 100, 0., 1., 100, 0., 1. );
		histos2D_[ "subjetPolAngle13412vs31234_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjetPolAngle13412vsSubjetPtRatio_cutSubjetPtRatio", "subjetPolAngle13412vsSubjetPtRatio_cutSubjetPtRatio", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle13412vsSubjetPtRatio_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutSubjetPtRatio" ] = fs_->make< TH2D >( "subjetPolAngle31234vsSubjetPtRatio_cutSubjetPtRatio", "subjetPolAngle31234vsSubjetPtRatio_cutSubjetPtRatio", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "mu1234_cutSubjetPtRatio" ] = fs_->make< TH2D >( "mu1234_cutSubjetPtRatio", "mu1234_cutSubjetPtRatio", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu1234_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "mu3412_cutSubjetPtRatio" ] = fs_->make< TH2D >( "mu3412_cutSubjetPtRatio", "mu3412_cutSubjetPtRatio", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu3412_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "dalitz1234_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dalitz1234_cutSubjetPtRatio", "dalitz1234_cutSubjetPtRatio", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz1234_cutSubjetPtRatio" ]->Sumw2();
		histos2D_[ "dalitz3412_cutSubjetPtRatio" ] = fs_->make< TH2D >( "dalitz3412_cutSubjetPtRatio", "dalitz3412_cutSubjetPtRatio", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz3412_cutSubjetPtRatio" ]->Sumw2();

		histos1D_[ "massAve_cutTau31" ] = fs_->make< TH1D >( "massAve_cutTau31", "massAve_cutTau31", 60, 0., 600. );
		histos1D_[ "massAve_cutTau31" ]->Sumw2();
		histos1D_[ "subjetMass21Ratio_cutTau31" ] = fs_->make< TH1D >( "subjetMass21Ratio_cutTau31", "subjetMass21Ratio_cutTau31", 20, 0., 1. );
		histos1D_[ "subjetMass21Ratio_cutTau31" ]->Sumw2();
		histos1D_[ "subjet112MassRatio_cutTau31" ] = fs_->make< TH1D >( "subjet112MassRatio_cutTau31", "subjet112MassRatio_cutTau31", 20, 0., 1. );
		histos1D_[ "subjet112MassRatio_cutTau31" ]->Sumw2();
		histos1D_[ "subjet212MassRatio_cutTau31" ] = fs_->make< TH1D >( "subjet212MassRatio_cutTau31", "subjet212MassRatio_cutTau31", 20, 0., 1. );
		histos1D_[ "subjet212MassRatio_cutTau31" ]->Sumw2();
		histos1D_[ "subjetPolAngle13412_cutTau31" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutTau31", "subjetPolAngle13412_cutTau31", 100, 0., 1. );
		histos1D_[ "subjetPolAngle13412_cutTau31" ]->Sumw2();
		histos1D_[ "subjetPolAngle31234_cutTau31" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutTau31", "subjetPolAngle31234_cutTau31", 100, 0., 1. );
		histos1D_[ "subjetPolAngle31234_cutTau31" ]->Sumw2();
		histos2D_[ "subjet12Mass_cutTau31" ] = fs_->make< TH2D >( "subjet12Mass_cutTau31", "subjet12Mass_cutTau31", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "subjet12Mass_cutTau31" ]->Sumw2();
		histos2D_[ "dijetCorr_cutTau31" ] = fs_->make< TH2D >( "dijetCorr_cutTau31", "dijetCorr_cutTau31", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutTau31" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutTau31" ] = fs_->make< TH2D >( "dijetCorrPhi_cutTau31", "dijetCorrPhi_cutTau31", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutTau31" ]->Sumw2();
		histos2D_[ "subjet112vs212MassRatio_cutTau31" ] = fs_->make< TH2D >( "subjet112vs212MassRatio_cutTau31", "subjet112vs212MassRatio_cutTau31", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet112vs212MassRatio_cutTau31" ]->Sumw2();
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ] = fs_->make< TH2D >( "subjet1JetvsSubjet2JetMassRatio_cutTau31", "subjet1JetvsSubjet2JetMassRatio_cutTau31", 20, 0., 1., 20, 0., 1. );
		histos2D_[ "subjet1JetvsSubjet2JetMassRatio_cutTau31" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vs31234_cutTau31" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutTau31", "subjetPolAngle13412vs31234_cutTau31", 100, 0., 1., 100, 0., 1. );
		histos2D_[ "subjetPolAngle13412vs31234_cutTau31" ]->Sumw2();

		histos1D_[ "massAve_cutTau21" ] = fs_->make< TH1D >( "massAve_cutTau21", "massAve_cutTau21", 60, 0., 600. );
		histos1D_[ "massAve_cutTau21" ]->Sumw2();
		histos2D_[ "subjet12Mass_cutTau21" ] = fs_->make< TH2D >( "subjet12Mass_cutTau21", "subjet12Mass_cutTau21", 20, 0., 100., 20, 0., 100. );
		histos2D_[ "subjet12Mass_cutTau21" ]->Sumw2();

		histos1D_[ "massAve_cutBtagAfterSubjetPtRatio" ] = fs_->make< TH1D >( "massAve_cutBtagAfterSubjetPtRatio", "massAve_cutBtagAfterSubjetPtRatio", 60, 0., 600. );
		histos1D_[ "massAve_cutBtagAfterSubjetPtRatio" ]->Sumw2();
		histos1D_[ "massAve_cutBtagAfterTau31" ] = fs_->make< TH1D >( "massAve_cutBtagAfterTau31", "massAve_cutBtagAfterTau31", 60, 0., 600. );
		histos1D_[ "massAve_cutBtagAfterTau31" ]->Sumw2();
		histos1D_[ "massAve_cutBtagAfterTau21" ] = fs_->make< TH1D >( "massAve_cutBtagAfterTau21", "massAve_cutBtagAfterTau21", 60, 0., 600. );
		histos1D_[ "massAve_cutBtagAfterTau21" ]->Sumw2();

		cutLabels.push_back("Processed");
		cutLabels.push_back("Trigger");
		cutLabels.push_back("Dijet");
		cutLabels.push_back("Asymmetry");
		cutLabels.push_back("CosTheta");
		cutLabels.push_back("SubjetPtRatio");
		cutLabels.push_back("btagAfterSubjetPtRatio");
		//cutLabels.push_back("Tau31");
		//cutLabels.push_back("btagAfterTau31");
		//cutLabels.push_back("Tau21");
		//cutLabels.push_back("btagAfterTau21");
		histos1D_[ "hcutflow" ] = fs_->make< TH1D >("cutflow","cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
		histos1D_[ "hcutflow" ]->Sumw2();
		histos1D_[ "hcutflowSimple" ] = fs_->make< TH1D >("cutflowSimple","simple cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
		histos1D_[ "hcutflowSimple" ]->Sumw2();
		for( const string &ivec : cutLabels ) cutmap[ ivec ] = 0;

	}
}

// ------------ method called once each job just after ending the event loop  ------------
void RUNBoostedAnalysis::endJob() {

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
DEFINE_FWK_MODULE(RUNBoostedAnalysis);
