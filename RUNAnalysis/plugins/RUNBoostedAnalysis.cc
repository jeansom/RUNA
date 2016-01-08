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
#include <TH1D.h>
#include <TH2D.h>
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
#include "RUNA/RUNAnalysis/interface/PUReweighter.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNBoostedAnalysis : public EDAnalyzer {
   public:
      explicit RUNBoostedAnalysis(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
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
      PUReweighter PUWeight_;
      
      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      bool bjSample;
      bool mkTree;
      bool isData;
      string dataPUFile;
      string jecVersion;
      TString systematics;
      double scale;
      double cutAsymvalue;
      double cutCosThetavalue;
      double cutSubjetPtRatiovalue;
      double cutTau31value;
      double cutTau21value;
      double cutBtagvalue;
      double cutDEtavalue;

      vector<string> triggerPass;
      vector<JetCorrectorParameters> jetPar;
      FactorizedJetCorrector * jetJECAK8;
      vector<JetCorrectorParameters> massPar;
      FactorizedJetCorrector * massJECAK8;
      JetCorrectionUncertainty *jetCorrUnc;

      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;
      float AK4HT = 0, HT = 0, trimmedMass = -999, puWeight = -999, lumiWeight = -999, MET = -999,
	    jet1Pt = -999, jet1Eta = -999, jet1Phi = -999, jet1E = -999, jet1Mass = -999, jet1btagCSV = -9999,
	    jet2Pt = -999, jet2Eta = -999, jet2Phi = -999, jet2E = -999, jet2Mass = -999, jet2btagCSV = -9999,
	    subjet11Pt = -999, subjet11Eta = -999, subjet11Phi = -999, subjet11E = -999, 
	    subjet12Pt = -999, subjet12Eta = -999, subjet12Phi = -999, subjet12E = -999, 
	    subjet21Pt = -999, subjet21Eta = -999, subjet21Phi = -999, subjet21E = -999, 
	    subjet22Pt = -999, subjet22Eta = -999, subjet22Phi = -999, subjet22E = -999,
	    massAve = -9999, massAsym = -9999, jet1CosThetaStar = -9999, jet2CosThetaStar = -9999, deltaEtaDijet = -9999,
	    jet1Tau21 = -9999, jet1Tau31 = -9999, jet1Tau32 = -9999,
	    jet2Tau21 = -9999, jet2Tau31 = -9999, jet2Tau32 = -9999,
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
      EDGetTokenT<vector<float>> jetArea_;
      EDGetTokenT<vector<float>> jetGenPt_;
      EDGetTokenT<vector<float>> jetGenEta_;
      EDGetTokenT<vector<float>> jetGenPhi_;
      EDGetTokenT<vector<float>> jetGenE_;
      EDGetTokenT<vector<float>> metPt_;
      EDGetTokenT<int> NPV_;
      EDGetTokenT<int> trueNInt_;
      EDGetTokenT<vector<int>> bunchCross_;
      EDGetTokenT<vector<float>> rho_;
      EDGetTokenT<vector<int>> puNumInt_;
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
	jetArea_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetArea"))),
	jetGenPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenPt"))),
	jetGenEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenEta"))),
	jetGenPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenPhi"))),
	jetGenE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenE"))),
	metPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("metPt"))),
	NPV_(consumes<int>(iConfig.getParameter<InputTag>("NPV"))),
	trueNInt_(consumes<int>(iConfig.getParameter<InputTag>("trueNInt"))),
	bunchCross_(consumes<vector<int>>(iConfig.getParameter<InputTag>("bunchCross"))),
	rho_(consumes<vector<float>>(iConfig.getParameter<InputTag>("rho"))),
	puNumInt_(consumes<vector<int>>(iConfig.getParameter<InputTag>("puNumInt"))),
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
	muonEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("muonEnergy"))),
	// Subjets
	subjetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetPt"))),
	subjetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetEta"))),
	subjetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetPhi"))),
	subjetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetE"))),
	subjetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetMass")))
{
	scale 		= iConfig.getParameter<double>("scale");
	bjSample 	= iConfig.getParameter<bool>("bjSample");
	mkTree 		= iConfig.getParameter<bool>("mkTree");
	isData 		= iConfig.getParameter<bool>("isData");
	dataPUFile 	= iConfig.getParameter<string>("dataPUFile");
	jecVersion 	= iConfig.getParameter<string>("jecVersion");
	systematics 	= iConfig.getParameter<string>("systematics");
	triggerPass 	= iConfig.getParameter<vector<string>>("triggerPass");
	/*
	cutAK4HTvalue = iConfig.getParameter<double>("cutAK4HTvalue");
	cutjetAK4Ptvalue = iConfig.getParameter<double>("cutjetAK4Ptvalue");
	cutTrimmedMassvalue = iConfig.getParameter<double>("cutTrimmedMassvalue");
	*/
	cutAsymvalue 	= iConfig.getParameter<double>("cutAsymvalue");
	cutCosThetavalue = iConfig.getParameter<double>("cutCosThetavalue");
	cutSubjetPtRatiovalue = iConfig.getParameter<double>("cutSubjetPtRatiovalue");
	cutTau31value 	= iConfig.getParameter<double>("cutTau31value");
	cutTau21value 	= iConfig.getParameter<double>("cutTau21value");
	cutBtagvalue 	= iConfig.getParameter<double>("cutBtagvalue");
	cutDEtavalue 	= iConfig.getParameter<double>("cutDEtavalue");

	/////// JECs
	string prefix;
	if (isData) prefix = jecVersion + "_DATA_";
	else prefix = jecVersion + "_MC_";

	// all jet
	vector<string> jecAK8PayloadNames_;
	jecAK8PayloadNames_.push_back(prefix + "L1FastJet_AK8PFchs.txt");
	jecAK8PayloadNames_.push_back(prefix + "L2Relative_AK8PFchs.txt");
	jecAK8PayloadNames_.push_back(prefix + "L3Absolute_AK8PFchs.txt");
	if (isData) jecAK8PayloadNames_.push_back(prefix + "L2L3Residual_AK8PFchs.txt");

	for ( vector<string>::const_iterator payloadBegin = jecAK8PayloadNames_.begin(), payloadEnd = jecAK8PayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
		JetCorrectorParameters pars(*ipayload);
		jetPar.push_back(pars);
	}
	jetJECAK8 = new FactorizedJetCorrector(jetPar);

	// jet mass
	vector<string> massjecAK8PayloadNames_;
	massjecAK8PayloadNames_.push_back(prefix + "L2Relative_AK8PFchs.txt");
	massjecAK8PayloadNames_.push_back(prefix + "L3Absolute_AK8PFchs.txt");
	if (isData) massjecAK8PayloadNames_.push_back(prefix + "L2L3Residual_AK8PFchs.txt");

	for ( vector<string>::const_iterator payloadBegin = massjecAK8PayloadNames_.begin(), payloadEnd = massjecAK8PayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
		JetCorrectorParameters massPars(*ipayload);
		massPar.push_back(massPars);
	}
	massJECAK8 = new FactorizedJetCorrector(massPar);

	// jec uncertainty
	JetCorrectorParameters jecUncParam( prefix + "Uncertainty_AK8PFchs.txt");
	jetCorrUnc  = new JetCorrectionUncertainty( jecUncParam);
	////////////////////////////////////////////////////
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

	Handle<vector<float> > jetArea;
	iEvent.getByToken(jetArea_, jetArea);

	Handle<vector<float> > jetGenPt;
	iEvent.getByToken(jetGenPt_, jetGenPt);

	Handle<vector<float> > jetGenEta;
	iEvent.getByToken(jetGenEta_, jetGenEta);

	Handle<vector<float> > jetGenPhi;
	iEvent.getByToken(jetGenPhi_, jetGenPhi);

	Handle<vector<float> > jetGenE;
	iEvent.getByToken(jetGenE_, jetGenE);

	Handle<vector<float> > metPt;
	iEvent.getByToken(metPt_, metPt);

	Handle<int> NPV;
	iEvent.getByToken(NPV_, NPV);

	Handle<int> trueNInt;
	iEvent.getByToken(trueNInt_, trueNInt);

	Handle<vector<int>> bunchCross;
	iEvent.getByToken(bunchCross_, bunchCross);

	Handle<vector<float>> rho;
	iEvent.getByToken(rho_, rho);

	Handle<vector<int>> puNumInt;
	iEvent.getByToken(puNumInt_, puNumInt);

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

	bool ORTriggers = checkORListOfTriggerBits( triggerName, triggerBit, triggerPass );
	
	////////// PU Reweight
	if ( isData ) puWeight = 1;
	else puWeight = PUWeight_.getPUWeight( *trueNInt, *bunchCross );
	if (!mkTree) histos1D_[ "PUWeight" ]->Fill( puWeight );
	lumiWeight = scale;
	double totalWeight = puWeight * lumiWeight;
	////////////////////////////////////////////////////
	
	///////// AK4 jets to model PFHT trigger
	AK4HT = 0;
	for (size_t q = 0; q < jetAK4Pt->size(); q++) {

		if ( TMath::Abs( (*jetAK4Eta)[q] ) > 2.4 ) continue;
		if ( (*jetAK4Pt)[q] < 40.0 ) continue;
		AK4HT += (*jetAK4Pt)[q];
	}
	////////////////////////////////////////////////////

	/// Applying kinematic, trigger and jet ID
	cutmap["Processed"] += totalWeight;
	vector< myJet > JETS;
	vector< float > tmpTriggerMass;
	bool cutHT = 0;
	bool cutJetPt = 0;
	//bool bTagCSV = 0;
	int numberJets = 0;
	HT = 0;

	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		bool idL = jetID( (*jetEta)[i], (*jetE)[i], (*jecFactor)[i], (*neutralHadronEnergy)[i], (*neutralEmEnergy)[i], (*chargedHadronEnergy)[i], (*muonEnergy)[i], (*chargedEmEnergy)[i], (*chargedHadronMultiplicity)[i], (*neutralHadronMultiplicity)[i], (*chargedMultiplicity)[i] ); 

		if( (*jetPt)[i] < 50 ) continue; // just to reduce time

		TLorentzVector tmpJet, rawJet, corrJet, genJet, smearJet;
		tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );
		rawJet = tmpJet* (*jecFactor)[i] ;

		double JEC = corrections( rawJet, (*jetArea)[i], (*rho)[i] ,*NPV, jetJECAK8); 
		double sysJEC = 0;
		if ( !isData ) {
			if ( systematics.Contains("JESUp") ){
				double JESUp = uncertainty( rawJet, jetCorrUnc, true );
				sysJEC = ( + JESUp );
			} else if  ( systematics.Contains("JESDown") ){
				double JESDown = uncertainty( rawJet, jetCorrUnc, false );
				sysJEC = ( - JESDown );
			}
		} 
		corrJet = rawJet* ( JEC + sysJEC  );

		/*
			genJet.SetPtEtaPhiE( (*jetGenPt)[i], (*jetGenEta)[i], (*jetGenPhi)[i], (*jetGenE)[i]);
			smearjet = 
			} else if  ( systematics.Contains("JER") ){
				double smearFactor = getJER( (*jetEta)[i], 0 );
				double smearPt = ( (*jetPt)[i] - (*jetGenPt)[i]) * smearFactor;
				LogWarning("test") << smearFactor << " " << smearPt ;
				*/

		//LogWarning("jet") << i << " " << (*jetPt)[i] << " " << (*jetEta)[i] << " " << (*jetPhi)[i] << " " << (*jetMass)[i] << " " <<(*jetE)[i] << " " << (*jecFactor)[i];
		//LogWarning("rawjet") << i << " " << rawJet.Pt() << " " << rawJet.Eta() << " " << rawJet.Phi() << " " << rawJet.M() << " " << rawJet.E();
		//LogWarning("corrjet") << i << " " << corrJet.Pt() << " " << corrJet.Eta() << " " << corrJet.Phi() << " " << corrJet.M() << " " << corrJet.E() << " " << JEC;

		if( corrJet.Pt() > 150 && idL ) { 

			HT += corrJet.Pt();
			tmpTriggerMass.push_back( (*jetTrimmedMass)[i] );
			++numberJets;

			double massJEC = corrections( rawJet, (*jetArea)[i], (*rho)[i] ,*NPV, massJECAK8); 
			double corrMass = (*jetMass)[i] * ( massJEC + sysJEC  );

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
			//if ( (*jetCSV)[i] > 0.679 ) bTagCSV = 1; 	// CSVM
			//if ( (*jetCSVV1)[i] > 0.405 ) bTagCSV = 1; 	// CSVV1L
			//if ( (*jetCSVV1)[i] > 0.783 ) bTagCSV = 1; 	// CSVV1M
			
			double jec = 1. / ( rawJet.E() ); //(*jecFactor)[i] * (*jetE)[i] );
			if (!mkTree) {
				histos1D_[ "oldJetPt" ]->Fill( (*jetPt)[i], totalWeight );
				histos1D_[ "jetPt" ]->Fill( corrJet.Pt(), totalWeight );
				histos1D_[ "rawJetPt" ]->Fill( rawJet.Pt(), totalWeight );
				histos1D_[ "oldJetEta" ]->Fill( (*jetEta)[i], totalWeight );
				histos1D_[ "jetEta" ]->Fill( corrJet.Eta(), totalWeight );
				histos1D_[ "rawJetEta" ]->Fill( rawJet.Eta(), totalWeight );
				histos1D_[ "oldJetMass" ]->Fill( (*jetMass)[i], totalWeight );
				histos1D_[ "jetMass" ]->Fill( corrMass, totalWeight );
				histos1D_[ "rawJetMass" ]->Fill( rawJet.M(), totalWeight );
				histos1D_[ "neutralHadronEnergy" ]->Fill( (*neutralHadronEnergy)[i] * jec, totalWeight );
				histos1D_[ "neutralEmEnergy" ]->Fill( (*neutralEmEnergy)[i] * jec, totalWeight );
				histos1D_[ "chargedHadronEnergy" ]->Fill( (*chargedHadronEnergy)[i] * jec, totalWeight );
				histos1D_[ "chargedEmEnergy" ]->Fill( (*chargedEmEnergy)[i] * jec, totalWeight );
				histos1D_[ "numConst" ]->Fill( (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i], totalWeight );
				histos1D_[ "chargedMultiplicity" ]->Fill( (*chargedMultiplicity)[i] * jec, totalWeight );
			}

			myJet tmpJET;
			tmpJET.p4 = tmpJet;
			tmpJET.subjet0 = tmpSubjet0;
			tmpJET.subjet1 = tmpSubjet1;
			tmpJET.mass = corrMass;
			tmpJET.tau1 = (*jetTau1)[i];
			tmpJET.tau2 = (*jetTau2)[i];
			tmpJET.tau3 = (*jetTau3)[i];
			tmpJET.btagCSV = (*jetCSV)[i];
			tmpJET.nhf = (*neutralHadronEnergy)[i] * jec;
			tmpJET.nEMf = (*neutralEmEnergy)[i] * jec;
			tmpJET.chf = (*chargedHadronEnergy)[i] * jec;
			tmpJET.cEMf = (*chargedEmEnergy)[i] * jec;
			tmpJET.numConst = (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i];
			tmpJET.chm = (*chargedMultiplicity)[i] * jec;
			JETS.push_back( tmpJET );
	   
		}
	}

	numPV = *NPV;
	MET = (*metPt)[0];
	numJets = numberJets;
	//sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { return p1.mass > p2.mass; }); 
	//sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1.p4; tmpP2 = p2.p4;  return tmpP1.M() > tmpP2.M(); }); 
	if (!mkTree) {
		histos1D_[ "jetNum" ]->Fill( numJets, totalWeight );
		histos1D_[ "NPV_NOPUWeight" ]->Fill( numPV );
		histos1D_[ "NPV" ]->Fill( numPV, totalWeight );
		if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT, totalWeight );
	}
	if ( HT > 900. ) cutHT = 1;

	sort(tmpTriggerMass.begin(), tmpTriggerMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	if ( ( tmpTriggerMass.size()> 0 ) ) { //&& ( tmpTriggerMass[0] > cutTrimmedMassvalue) ){
		trimmedMass = tmpTriggerMass[0];
		if (!mkTree) {
			histos1D_[ "jetTrimmedMass" ]->Fill( tmpTriggerMass[0], totalWeight );
			if (HT > 0) histos2D_[ "jetTrimmedMassHT" ]->Fill( tmpTriggerMass[0], HT, totalWeight );
		}
	}
	tmpTriggerMass.clear();

	if ( ORTriggers ) {
		//LogWarning("fired") << HT << " " << trimmedMass;
		cutmap["Trigger"] += totalWeight; 

		if (!mkTree) {
			histos1D_[ "HT_cutTrigger" ]->Fill( HT, totalWeight );
			histos1D_[ "MET_cutTrigger" ]->Fill( MET, totalWeight );
			histos1D_[ "METHT_cutTrigger" ]->Fill( MET/HT, totalWeight );
			histos1D_[ "NPV_cutTrigger" ]->Fill( numPV, totalWeight );
			histos1D_[ "jetNum_cutTrigger" ]->Fill( numJets, totalWeight );
			histos2D_[ "jetTrimmedMassHT_cutTrigger" ]->Fill( trimmedMass, HT, totalWeight );

			int kdum = 0;
			for (size_t k = 0; k < JETS.size(); k++) {
				histos1D_[ "jetPt_cutTrigger" ]->Fill( JETS[k].p4.Pt(), totalWeight );
				histos1D_[ "jetEta_cutTrigger" ]->Fill( JETS[k].p4.Eta(), totalWeight );
				histos1D_[ "jetMass_cutTrigger" ]->Fill( JETS[k].mass, totalWeight );

				if ( (++kdum) == 1 ) {
					histos1D_[ "jet1Pt_cutTrigger" ]->Fill( JETS[0].p4.Pt(), totalWeight );
					histos1D_[ "jet1Mass_cutTrigger" ]->Fill( JETS[0].mass, totalWeight );
					histos1D_[ "jet1Eta_cutTrigger" ]->Fill( JETS[0].p4.Eta(), totalWeight );
				}
			 }
		}
		//////////////////////////////////////////////////////////////////////////////
		
		vector<double> dalitz1, dalitz2;
		vector<TLorentzVector> jet1SubjetsTLV, jet2SubjetsTLV;

		if ( JETS.size() > 1 ) {

			cutmap["Dijet"] += totalWeight;

			// Cut Pt
			if (( JETS[0].p4.Pt() > 500. ) && ( JETS[1].p4.Pt() > 450. ) ) cutJetPt = 1 ;

			// Mass average and asymmetry
			jet1Mass = JETS[0].mass;
			jet2Mass = JETS[1].mass;
			massAve = massAverage( jet1Mass, jet2Mass );
			massAsym = massAsymmetry( jet1Mass, jet2Mass );
			//////////////////////////////////////////////////////////////////////////
			
			// Btag
			jet1btagCSV = JETS[0].btagCSV;
			jet2btagCSV = JETS[1].btagCSV;

			// Dijet eta
			deltaEtaDijet = deltaValue( JETS[0].p4.Eta(), JETS[1].p4.Eta() );

			// Cos theta star
			jet1CosThetaStar = calculateCosThetaStar( JETS[0].p4, JETS[1].p4 ) ;
			jet2CosThetaStar = calculateCosThetaStar( JETS[1].p4, JETS[0].p4 ) ;

			// Nsubjetiness
			jet1Tau21 = JETS[0].tau2 / JETS[0].tau1;
			jet1Tau31 = JETS[0].tau3 / JETS[0].tau1;
			jet1Tau32 = JETS[0].tau3 / JETS[0].tau2;
			jet2Tau21 = JETS[1].tau2 / JETS[1].tau1;
			jet2Tau31 = JETS[1].tau3 / JETS[1].tau1;
			jet2Tau32 = JETS[1].tau3 / JETS[1].tau2;
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

			
				/*/ SUbjet Polarization angle & dalitz variables
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
				//////////////////////////////////////////////////////////////////////////////////////*/

			}

			///// Variables for tree
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

			if (!mkTree){

				histos1D_[ "HT_cutDijet" ]->Fill( HT, totalWeight );
				histos1D_[ "MET_cutDijet" ]->Fill( MET, totalWeight );
				histos1D_[ "METHT_cutDijet" ]->Fill( MET/HT, totalWeight );
				histos1D_[ "NPV_cutDijet" ]->Fill( numPV, totalWeight );
				histos1D_[ "jetNum_cutDijet" ]->Fill( numJets, totalWeight );
				histos1D_[ "jet1Pt_cutDijet" ]->Fill( JETS[0].p4.Pt(), totalWeight );
				histos1D_[ "jet1Eta_cutDijet" ]->Fill( JETS[0].p4.Eta(), totalWeight );
				histos1D_[ "jet1Mass_cutDijet" ]->Fill( JETS[0].mass, totalWeight );
				histos1D_[ "jet2Pt_cutDijet" ]->Fill( JETS[1].p4.Pt(), totalWeight );
				histos1D_[ "jet2Eta_cutDijet" ]->Fill( JETS[1].p4.Eta(), totalWeight );
				histos1D_[ "jet2Mass_cutDijet" ]->Fill( JETS[1].mass, totalWeight );

				histos1D_[ "massAsymmetry_cutDijet" ]->Fill( massAsym, totalWeight );
				histos1D_[ "massAve_cutDijet" ]->Fill( massAve, totalWeight );
				histos1D_[ "jet1CosThetaStar_cutDijet" ]->Fill( jet1CosThetaStar, totalWeight );
				histos1D_[ "jet2CosThetaStar_cutDijet" ]->Fill( jet2CosThetaStar, totalWeight );
				histos1D_[ "jet1Tau1_cutDijet" ]->Fill( JETS[0].tau1, totalWeight );
				histos1D_[ "jet1Tau2_cutDijet" ]->Fill( JETS[0].tau2, totalWeight );
				histos1D_[ "jet1Tau3_cutDijet" ]->Fill( JETS[0].tau3, totalWeight );
				histos1D_[ "jet1Tau21_cutDijet" ]->Fill( jet1Tau21, totalWeight );
				histos1D_[ "jet1Tau31_cutDijet" ]->Fill( jet1Tau31, totalWeight );
				histos1D_[ "jet1Tau32_cutDijet" ]->Fill( jet1Tau32, totalWeight );
				histos1D_[ "jet2Tau1_cutDijet" ]->Fill( JETS[1].tau1, totalWeight );
				histos1D_[ "jet2Tau2_cutDijet" ]->Fill( JETS[1].tau2, totalWeight );
				histos1D_[ "jet2Tau3_cutDijet" ]->Fill( JETS[1].tau3, totalWeight );
				histos1D_[ "jet2Tau21_cutDijet" ]->Fill( jet2Tau21, totalWeight );
				histos1D_[ "jet2Tau31_cutDijet" ]->Fill( jet2Tau31, totalWeight );
				histos1D_[ "jet2Tau32_cutDijet" ]->Fill( jet2Tau32, totalWeight );
				histos1D_[ "deltaEtaDijet_cutDijet" ]->Fill( deltaEtaDijet, totalWeight );
				histos1D_[ "jet1SubjetPtRatio_cutDijet" ]->Fill( jet1SubjetPtRatio, totalWeight );
				histos1D_[ "jet2SubjetPtRatio_cutDijet" ]->Fill( jet2SubjetPtRatio, totalWeight );
				histos1D_[ "subjetPtRatio_cutDijet" ]->Fill( jet1SubjetPtRatio, totalWeight );
				histos1D_[ "subjetPtRatio_cutDijet" ]->Fill( jet2SubjetPtRatio, totalWeight );

				histos2D_[ "jetTrimmedMassHT_cutDijet" ]->Fill( trimmedMass, HT, totalWeight );
				histos2D_[ "massAveHT_cutDijet" ]->Fill( massAve, HT, totalWeight );

				histos2D_[ "massAvevsJet1Mass_cutDijet" ]->Fill( massAve, jet1Mass, totalWeight );
				histos2D_[ "massAvevsJet2Mass_cutDijet" ]->Fill( massAve, jet2Mass, totalWeight );
				histos2D_[ "massAvevsMassAsym_cutDijet" ]->Fill( massAve, massAsym, totalWeight );
				histos2D_[ "massAvevsDEta_cutDijet" ]->Fill( massAve, deltaEtaDijet, totalWeight );
				histos2D_[ "massAvevsJet1CosThetaStar_cutDijet" ]->Fill( massAve, jet1CosThetaStar, totalWeight );
				histos2D_[ "massAvevsJet2CosThetaStar_cutDijet" ]->Fill( massAve, jet2CosThetaStar, totalWeight );
				histos2D_[ "massAvevsJet1Tau21_cutDijet" ]->Fill( massAve, jet1Tau21, totalWeight );
				histos2D_[ "massAvevsJet1Tau31_cutDijet" ]->Fill( massAve, jet1Tau31, totalWeight );
				histos2D_[ "massAvevsJet1Tau32_cutDijet" ]->Fill( massAve, jet1Tau32, totalWeight );
				histos2D_[ "massAvevsJet2Tau21_cutDijet" ]->Fill( massAve, jet1Tau21, totalWeight );
				histos2D_[ "massAvevsJet2Tau31_cutDijet" ]->Fill( massAve, jet1Tau31, totalWeight );
				histos2D_[ "massAvevsJet2Tau32_cutDijet" ]->Fill( massAve, jet1Tau32, totalWeight );
				histos2D_[ "massAvevsJet1SubjetPtRatio_cutDijet" ]->Fill( massAve, jet1SubjetPtRatio, totalWeight );
				histos2D_[ "massAvevsJet2SubjetPtRatio_cutDijet" ]->Fill( massAve, jet2SubjetPtRatio, totalWeight );
				histos2D_[ "jet1vs2Mass_cutDijet" ]->Fill( jet1Mass, jet2Mass, totalWeight );
				histos2D_[ "dijetCorr_cutDijet" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), totalWeight );
				histos2D_[ "dijetCorrPhi_cutDijet" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), totalWeight );
				/*
				histos1D_[ "subjetPolAngle13412_cutDijet" ]->Fill( cosPhi13412, totalWeight );
				histos1D_[ "subjetPolAngle31234_cutDijet" ]->Fill( cosPhi31234, totalWeight );
				histos1D_[ "mu1_cutDijet" ]->Fill( dalitz1[0], totalWeight );
				histos1D_[ "mu2_cutDijet" ]->Fill( dalitz1[1], totalWeight );
				histos1D_[ "mu3_cutDijet" ]->Fill( dalitz1[2], totalWeight );
				histos1D_[ "mu4_cutDijet" ]->Fill( dalitz2[0], totalWeight );
				histos1D_[ "mu5_cutDijet" ]->Fill( dalitz2[1], totalWeight );
				histos1D_[ "mu6_cutDijet" ]->Fill( dalitz2[2], totalWeight );
				histos2D_[ "subjetPolAngle13412vs31234_cutDijet" ]->Fill( cosPhi13412, cosPhi31234, totalWeight );
				histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutDijet" ]->Fill( cosPhi31234, jet2SubjetPtRatio, totalWeight );
				histos2D_[ "mu1234_cutDijet" ]->Fill( dalitz1[0], dalitz1[2], totalWeight );
				histos2D_[ "mu1234_cutDijet" ]->Fill( dalitz1[1], dalitz1[2], totalWeight );
				histos2D_[ "mu1234_cutDijet" ]->Fill( dalitz1[0], dalitz1[1], totalWeight );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX1, dalitz1[1], totalWeight );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX2, dalitz1[2], totalWeight );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX3, dalitz1[0], totalWeight );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX4, dalitz1[2], totalWeight );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX5, dalitz1[0], totalWeight );
				histos2D_[ "dalitz1234_cutDijet" ]->Fill( dalitzX6, dalitz1[1], totalWeight );
				histos2D_[ "mu3412_cutDijet" ]->Fill( dalitz2[0], dalitz2[2], totalWeight );
				histos2D_[ "mu3412_cutDijet" ]->Fill( dalitz2[1], dalitz2[2], totalWeight );
				histos2D_[ "mu3412_cutDijet" ]->Fill( dalitz2[0], dalitz2[1], totalWeight );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY1, dalitz2[1], totalWeight );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY2, dalitz2[2], totalWeight );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY3, dalitz2[0], totalWeight );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY4, dalitz2[2], totalWeight );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY5, dalitz2[0], totalWeight );
				histos2D_[ "dalitz3412_cutDijet" ]->Fill( dalitzY6, dalitz2[1], totalWeight );*/

			}

			if ( cutHT && cutJetPt ) {

				cutmap["HT"] += totalWeight;

				if ( mkTree ) {
					RUNAtree->Fill();

				} else {

					histos1D_[ "HT_cutHT" ]->Fill( HT, totalWeight );
					histos1D_[ "MET_cutHT" ]->Fill( MET, totalWeight );
					histos1D_[ "METHT_cutHT" ]->Fill( MET/HT, totalWeight );
					histos1D_[ "NPV_cutHT" ]->Fill( numPV, totalWeight );
					histos1D_[ "jetNum_cutHT" ]->Fill( numJets, totalWeight );
					histos1D_[ "jet1Pt_cutHT" ]->Fill( JETS[0].p4.Pt(), totalWeight );
					histos1D_[ "jet1Eta_cutHT" ]->Fill( JETS[0].p4.Eta(), totalWeight );
					histos1D_[ "jet1Mass_cutHT" ]->Fill( JETS[0].mass, totalWeight );
					histos1D_[ "jet2Pt_cutHT" ]->Fill( JETS[1].p4.Pt(), totalWeight );
					histos1D_[ "jet2Eta_cutHT" ]->Fill( JETS[1].p4.Eta(), totalWeight );
					histos1D_[ "jet2Mass_cutHT" ]->Fill( JETS[1].mass, totalWeight );
					for (size_t k = 0; k < JETS.size(); k++) {
						histos1D_[ "neutralHadronEnergy_cutHT" ]->Fill( JETS[k].nhf, totalWeight );
						histos1D_[ "neutralEmEnergy_cutHT" ]->Fill( JETS[k].nEMf, totalWeight );
						histos1D_[ "chargedHadronEnergy_cutHT" ]->Fill( JETS[k].chf, totalWeight );
						histos1D_[ "chargedEmEnergy_cutHT" ]->Fill( JETS[k].cEMf, totalWeight );
						histos1D_[ "numConst_cutHT" ]->Fill( JETS[k].numConst, totalWeight );
						histos1D_[ "chargedMultiplicity_cutHT" ]->Fill( JETS[k].chm, totalWeight );
					}

					histos1D_[ "massAsymmetry_cutHT" ]->Fill( massAsym, totalWeight );
					histos1D_[ "massAve_cutHT" ]->Fill( massAve, totalWeight );
					histos1D_[ "jet1CosThetaStar_cutHT" ]->Fill( jet1CosThetaStar, totalWeight );
					histos1D_[ "jet2CosThetaStar_cutHT" ]->Fill( jet2CosThetaStar, totalWeight );
					histos1D_[ "jet1Tau1_cutHT" ]->Fill( JETS[0].tau1, totalWeight );
					histos1D_[ "jet1Tau2_cutHT" ]->Fill( JETS[0].tau2, totalWeight );
					histos1D_[ "jet1Tau3_cutHT" ]->Fill( JETS[0].tau3, totalWeight );
					histos1D_[ "jet1Tau21_cutHT" ]->Fill( jet1Tau21, totalWeight );
					histos1D_[ "jet1Tau31_cutHT" ]->Fill( jet1Tau31, totalWeight );
					histos1D_[ "jet1Tau32_cutHT" ]->Fill( jet1Tau32, totalWeight );
					histos1D_[ "jet2Tau1_cutHT" ]->Fill( JETS[1].tau1, totalWeight );
					histos1D_[ "jet2Tau2_cutHT" ]->Fill( JETS[1].tau2, totalWeight );
					histos1D_[ "jet2Tau3_cutHT" ]->Fill( JETS[1].tau3, totalWeight );
					histos1D_[ "jet2Tau21_cutHT" ]->Fill( jet2Tau21, totalWeight );
					histos1D_[ "jet2Tau31_cutHT" ]->Fill( jet2Tau31, totalWeight );
					histos1D_[ "jet2Tau32_cutHT" ]->Fill( jet2Tau32, totalWeight );
					histos1D_[ "deltaEtaDijet_cutHT" ]->Fill( deltaEtaDijet, totalWeight );
					histos1D_[ "jet1SubjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, totalWeight );
					histos1D_[ "jet2SubjetPtRatio_cutHT" ]->Fill( jet2SubjetPtRatio, totalWeight );
					histos1D_[ "subjetPtRatio_cutHT" ]->Fill( jet1SubjetPtRatio, totalWeight );
					histos1D_[ "subjetPtRatio_cutHT" ]->Fill( jet2SubjetPtRatio, totalWeight );

					histos2D_[ "jetTrimmedMassHT_cutHT" ]->Fill( trimmedMass, HT, totalWeight );
					histos2D_[ "massAveHT_cutHT" ]->Fill( massAve, HT, totalWeight );

					histos2D_[ "massAvevsJet1Mass_cutHT" ]->Fill( massAve, jet1Mass, totalWeight );
					histos2D_[ "massAvevsJet2Mass_cutHT" ]->Fill( massAve, jet2Mass, totalWeight );
					histos2D_[ "massAvevsHT_cutHT" ]->Fill( massAve, massAsym, totalWeight );
					histos2D_[ "massAvevsDEta_cutHT" ]->Fill( massAve, deltaEtaDijet, totalWeight );
					histos2D_[ "massAvevsJet1CosThetaStar_cutHT" ]->Fill( massAve, jet1CosThetaStar, totalWeight );
					histos2D_[ "massAvevsJet2CosThetaStar_cutHT" ]->Fill( massAve, jet2CosThetaStar, totalWeight );
					histos2D_[ "massAvevsJet1Tau21_cutHT" ]->Fill( massAve, jet1Tau21, totalWeight );
					histos2D_[ "massAvevsJet1Tau31_cutHT" ]->Fill( massAve, jet1Tau31, totalWeight );
					histos2D_[ "massAvevsJet1Tau32_cutHT" ]->Fill( massAve, jet1Tau32, totalWeight );
					histos2D_[ "massAvevsJet2Tau21_cutHT" ]->Fill( massAve, jet1Tau21, totalWeight );
					histos2D_[ "massAvevsJet2Tau31_cutHT" ]->Fill( massAve, jet1Tau31, totalWeight );
					histos2D_[ "massAvevsJet2Tau32_cutHT" ]->Fill( massAve, jet1Tau32, totalWeight );
					histos2D_[ "massAvevsJet1SubjetPtRatio_cutHT" ]->Fill( massAve, jet1SubjetPtRatio, totalWeight );
					histos2D_[ "massAvevsJet2SubjetPtRatio_cutHT" ]->Fill( massAve, jet2SubjetPtRatio, totalWeight );
					histos2D_[ "jet1vs2Mass_cutHT" ]->Fill( jet1Mass, jet2Mass, totalWeight );
					histos2D_[ "dijetCorr_cutHT" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), totalWeight );
					histos2D_[ "dijetCorrPhi_cutHT" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), totalWeight );

					if(  ( jet1Tau21 < cutTau21value ) && ( jet2Tau21 < cutTau21value ) ){

						cutmap["Tau21"] += totalWeight;
						histos1D_[ "HT_cutTau21" ]->Fill( HT, totalWeight );
						histos1D_[ "NPV_cutTau21" ]->Fill( numPV, totalWeight );
						histos1D_[ "jetNum_cutTau21" ]->Fill( numJets, totalWeight );
						histos1D_[ "jet1Pt_cutTau21" ]->Fill( JETS[0].p4.Pt(), totalWeight );
						histos1D_[ "jet1Eta_cutTau21" ]->Fill( JETS[0].p4.Eta(), totalWeight );
						histos1D_[ "jet1Mass_cutTau21" ]->Fill( JETS[0].mass, totalWeight );
						histos1D_[ "jet2Pt_cutTau21" ]->Fill( JETS[1].p4.Pt(), totalWeight );
						histos1D_[ "jet2Eta_cutTau21" ]->Fill( JETS[1].p4.Eta(), totalWeight );
						histos1D_[ "jet2Mass_cutTau21" ]->Fill( JETS[1].mass, totalWeight );

						histos1D_[ "massAsymmetry_cutTau21" ]->Fill( massAsym, totalWeight );
						histos1D_[ "massAve_cutTau21" ]->Fill( massAve, totalWeight );
						histos1D_[ "jet1CosThetaStar_cutTau21" ]->Fill( jet1CosThetaStar, totalWeight );
						histos1D_[ "jet2CosThetaStar_cutTau21" ]->Fill( jet2CosThetaStar, totalWeight );
						histos1D_[ "jet1Tau1_cutTau21" ]->Fill( JETS[0].tau1, totalWeight );
						histos1D_[ "jet1Tau2_cutTau21" ]->Fill( JETS[0].tau2, totalWeight );
						histos1D_[ "jet1Tau3_cutTau21" ]->Fill( JETS[0].tau3, totalWeight );
						histos1D_[ "jet1Tau21_cutTau21" ]->Fill( jet1Tau21, totalWeight );
						histos1D_[ "jet1Tau31_cutTau21" ]->Fill( jet1Tau31, totalWeight );
						histos1D_[ "jet1Tau32_cutTau21" ]->Fill( jet1Tau32, totalWeight );
						histos1D_[ "jet2Tau1_cutTau21" ]->Fill( JETS[1].tau1, totalWeight );
						histos1D_[ "jet2Tau2_cutTau21" ]->Fill( JETS[1].tau2, totalWeight );
						histos1D_[ "jet2Tau3_cutTau21" ]->Fill( JETS[1].tau3, totalWeight );
						histos1D_[ "jet2Tau21_cutTau21" ]->Fill( jet2Tau21, totalWeight );
						histos1D_[ "jet2Tau31_cutTau21" ]->Fill( jet2Tau31, totalWeight );
						histos1D_[ "jet2Tau32_cutTau21" ]->Fill( jet2Tau32, totalWeight );
						histos1D_[ "deltaEtaDijet_cutTau21" ]->Fill( deltaEtaDijet, totalWeight );
						histos1D_[ "jet1SubjetPtRatio_cutTau21" ]->Fill( jet1SubjetPtRatio, totalWeight );
						histos1D_[ "jet2SubjetPtRatio_cutTau21" ]->Fill( jet2SubjetPtRatio, totalWeight );
						histos1D_[ "subjetPtRatio_cutTau21" ]->Fill( jet1SubjetPtRatio, totalWeight );
						histos1D_[ "subjetPtRatio_cutTau21" ]->Fill( jet2SubjetPtRatio, totalWeight );

						histos2D_[ "jetTrimmedMassHT_cutTau21" ]->Fill( trimmedMass, HT, totalWeight );
						histos2D_[ "massAveHT_cutTau21" ]->Fill( massAve, HT, totalWeight );

						histos2D_[ "massAvevsJet1Mass_cutTau21" ]->Fill( massAve, jet1Mass, totalWeight );
						histos2D_[ "massAvevsJet2Mass_cutTau21" ]->Fill( massAve, jet2Mass, totalWeight );
						histos2D_[ "massAvevsMassAsym_cutTau21" ]->Fill( massAve, massAsym, totalWeight );
						histos2D_[ "massAvevsDEta_cutTau21" ]->Fill( massAve, deltaEtaDijet, totalWeight );
						histos2D_[ "massAvevsJet1CosThetaStar_cutTau21" ]->Fill( massAve, jet1CosThetaStar, totalWeight );
						histos2D_[ "massAvevsJet2CosThetaStar_cutTau21" ]->Fill( massAve, jet2CosThetaStar, totalWeight );
						histos2D_[ "massAvevsJet1Tau21_cutTau21" ]->Fill( massAve, jet1Tau21, totalWeight );
						histos2D_[ "massAvevsJet1Tau31_cutTau21" ]->Fill( massAve, jet1Tau31, totalWeight );
						histos2D_[ "massAvevsJet1Tau32_cutTau21" ]->Fill( massAve, jet1Tau32, totalWeight );
						histos2D_[ "massAvevsJet2Tau21_cutTau21" ]->Fill( massAve, jet1Tau21, totalWeight );
						histos2D_[ "massAvevsJet2Tau31_cutTau21" ]->Fill( massAve, jet1Tau31, totalWeight );
						histos2D_[ "massAvevsJet2Tau32_cutTau21" ]->Fill( massAve, jet1Tau32, totalWeight );
						histos2D_[ "massAvevsJet1SubjetPtRatio_cutTau21" ]->Fill( massAve, jet1SubjetPtRatio, totalWeight );
						histos2D_[ "massAvevsJet2SubjetPtRatio_cutTau21" ]->Fill( massAve, jet2SubjetPtRatio, totalWeight );
						histos2D_[ "jet1vs2Mass_cutTau21" ]->Fill( jet1Mass, jet2Mass, totalWeight );
						histos2D_[ "dijetCorr_cutTau21" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), totalWeight );
						histos2D_[ "dijetCorrPhi_cutTau21" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), totalWeight );

						if(( TMath::Abs( jet1CosThetaStar ) < cutCosThetavalue ) && ( TMath::Abs( jet2CosThetaStar ) < cutCosThetavalue )){
						
							cutmap["CosTheta"] += totalWeight;
							histos1D_[ "HT_cutCosTheta" ]->Fill( HT, totalWeight );
							histos1D_[ "NPV_cutCosTheta" ]->Fill( numPV, totalWeight );
							histos1D_[ "jetNum_cutCosTheta" ]->Fill( numJets, totalWeight );
							histos1D_[ "jet1Pt_cutCosTheta" ]->Fill( JETS[0].p4.Pt(), totalWeight );
							histos1D_[ "jet1Eta_cutCosTheta" ]->Fill( JETS[0].p4.Eta(), totalWeight );
							histos1D_[ "jet1Mass_cutCosTheta" ]->Fill( JETS[0].mass, totalWeight );
							histos1D_[ "jet2Pt_cutCosTheta" ]->Fill( JETS[1].p4.Pt(), totalWeight );
							histos1D_[ "jet2Eta_cutCosTheta" ]->Fill( JETS[1].p4.Eta(), totalWeight );
							histos1D_[ "jet2Mass_cutCosTheta" ]->Fill( JETS[1].mass, totalWeight );

							histos1D_[ "massAsymmetry_cutCosTheta" ]->Fill( massAsym, totalWeight );
							histos1D_[ "massAve_cutCosTheta" ]->Fill( massAve, totalWeight );
							histos1D_[ "jet1CosThetaStar_cutCosTheta" ]->Fill( jet1CosThetaStar, totalWeight );
							histos1D_[ "jet2CosThetaStar_cutCosTheta" ]->Fill( jet2CosThetaStar, totalWeight );
							histos1D_[ "jet1Tau1_cutCosTheta" ]->Fill( JETS[0].tau1, totalWeight );
							histos1D_[ "jet1Tau2_cutCosTheta" ]->Fill( JETS[0].tau2, totalWeight );
							histos1D_[ "jet1Tau3_cutCosTheta" ]->Fill( JETS[0].tau3, totalWeight );
							histos1D_[ "jet1Tau21_cutCosTheta" ]->Fill( jet1Tau21, totalWeight );
							histos1D_[ "jet1Tau31_cutCosTheta" ]->Fill( jet1Tau31, totalWeight );
							histos1D_[ "jet1Tau32_cutCosTheta" ]->Fill( jet1Tau32, totalWeight );
							histos1D_[ "jet2Tau1_cutCosTheta" ]->Fill( JETS[1].tau1, totalWeight );
							histos1D_[ "jet2Tau2_cutCosTheta" ]->Fill( JETS[1].tau2, totalWeight );
							histos1D_[ "jet2Tau3_cutCosTheta" ]->Fill( JETS[1].tau3, totalWeight );
							histos1D_[ "jet2Tau21_cutCosTheta" ]->Fill( jet2Tau21, totalWeight );
							histos1D_[ "jet2Tau31_cutCosTheta" ]->Fill( jet2Tau31, totalWeight );
							histos1D_[ "jet2Tau32_cutCosTheta" ]->Fill( jet2Tau32, totalWeight );
							histos1D_[ "deltaEtaDijet_cutCosTheta" ]->Fill( deltaEtaDijet, totalWeight );
							histos1D_[ "jet1SubjetPtRatio_cutCosTheta" ]->Fill( jet1SubjetPtRatio, totalWeight );
							histos1D_[ "jet2SubjetPtRatio_cutCosTheta" ]->Fill( jet2SubjetPtRatio, totalWeight );
							histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet1SubjetPtRatio, totalWeight );
							histos1D_[ "subjetPtRatio_cutCosTheta" ]->Fill( jet2SubjetPtRatio, totalWeight );

							histos2D_[ "jetTrimmedMassHT_cutCosTheta" ]->Fill( trimmedMass, HT, totalWeight );
							histos2D_[ "massAveHT_cutCosTheta" ]->Fill( massAve, HT, totalWeight );

							histos2D_[ "massAvevsJet1Mass_cutCosTheta" ]->Fill( massAve, jet1Mass, totalWeight );
							histos2D_[ "massAvevsJet2Mass_cutCosTheta" ]->Fill( massAve, jet2Mass, totalWeight );
							histos2D_[ "massAvevsMassAsym_cutCosTheta" ]->Fill( massAve, massAsym, totalWeight );
							histos2D_[ "massAvevsDEta_cutCosTheta" ]->Fill( massAve, deltaEtaDijet, totalWeight );
							histos2D_[ "massAvevsJet1CosThetaStar_cutCosTheta" ]->Fill( massAve, jet1CosThetaStar, totalWeight );
							histos2D_[ "massAvevsJet2CosThetaStar_cutCosTheta" ]->Fill( massAve, jet2CosThetaStar, totalWeight );
							histos2D_[ "massAvevsJet1Tau21_cutCosTheta" ]->Fill( massAve, jet1Tau21, totalWeight );
							histos2D_[ "massAvevsJet1Tau31_cutCosTheta" ]->Fill( massAve, jet1Tau31, totalWeight );
							histos2D_[ "massAvevsJet1Tau32_cutCosTheta" ]->Fill( massAve, jet1Tau32, totalWeight );
							histos2D_[ "massAvevsJet2Tau21_cutCosTheta" ]->Fill( massAve, jet1Tau21, totalWeight );
							histos2D_[ "massAvevsJet2Tau31_cutCosTheta" ]->Fill( massAve, jet1Tau31, totalWeight );
							histos2D_[ "massAvevsJet2Tau32_cutCosTheta" ]->Fill( massAve, jet1Tau32, totalWeight );
							histos2D_[ "massAvevsJet1SubjetPtRatio_cutCosTheta" ]->Fill( massAve, jet1SubjetPtRatio, totalWeight );
							histos2D_[ "massAvevsJet2SubjetPtRatio_cutCosTheta" ]->Fill( massAve, jet2SubjetPtRatio, totalWeight );
							histos2D_[ "jet1vs2Mass_cutCosTheta" ]->Fill( jet1Mass, jet2Mass, totalWeight );
							histos2D_[ "dijetCorr_cutCosTheta" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), totalWeight );
							histos2D_[ "dijetCorrPhi_cutCosTheta" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), totalWeight );

							if( massAsym < cutAsymvalue ){
								cutmap["Asymmetry"] += totalWeight;

								histos1D_[ "HT_cutMassAsym" ]->Fill( HT, totalWeight );
								histos1D_[ "NPV_cutMassAsym" ]->Fill( numPV, totalWeight );
								histos1D_[ "jetNum_cutMassAsym" ]->Fill( numJets, totalWeight );
								histos1D_[ "jet1Pt_cutMassAsym" ]->Fill( JETS[0].p4.Pt(), totalWeight );
								histos1D_[ "jet1Eta_cutMassAsym" ]->Fill( JETS[0].p4.Eta(), totalWeight );
								histos1D_[ "jet1Mass_cutMassAsym" ]->Fill( JETS[0].mass, totalWeight );
								histos1D_[ "jet2Pt_cutMassAsym" ]->Fill( JETS[1].p4.Pt(), totalWeight );
								histos1D_[ "jet2Eta_cutMassAsym" ]->Fill( JETS[1].p4.Eta(), totalWeight );
								histos1D_[ "jet2Mass_cutMassAsym" ]->Fill( JETS[1].mass, totalWeight );

								histos1D_[ "massAsymmetry_cutMassAsym" ]->Fill( massAsym, totalWeight );
								histos1D_[ "massAve_cutMassAsym" ]->Fill( massAve, totalWeight );
								histos1D_[ "jet1CosThetaStar_cutMassAsym" ]->Fill( jet1CosThetaStar, totalWeight );
								histos1D_[ "jet2CosThetaStar_cutMassAsym" ]->Fill( jet2CosThetaStar, totalWeight );
								histos1D_[ "jet1Tau1_cutMassAsym" ]->Fill( JETS[0].tau1, totalWeight );
								histos1D_[ "jet1Tau2_cutMassAsym" ]->Fill( JETS[0].tau2, totalWeight );
								histos1D_[ "jet1Tau3_cutMassAsym" ]->Fill( JETS[0].tau3, totalWeight );
								histos1D_[ "jet1Tau21_cutMassAsym" ]->Fill( jet1Tau21, totalWeight );
								histos1D_[ "jet1Tau31_cutMassAsym" ]->Fill( jet1Tau31, totalWeight );
								histos1D_[ "jet1Tau32_cutMassAsym" ]->Fill( jet1Tau32, totalWeight );
								histos1D_[ "jet2Tau1_cutMassAsym" ]->Fill( JETS[1].tau1, totalWeight );
								histos1D_[ "jet2Tau2_cutMassAsym" ]->Fill( JETS[1].tau2, totalWeight );
								histos1D_[ "jet2Tau3_cutMassAsym" ]->Fill( JETS[1].tau3, totalWeight );
								histos1D_[ "jet2Tau21_cutMassAsym" ]->Fill( jet2Tau21, totalWeight );
								histos1D_[ "jet2Tau31_cutMassAsym" ]->Fill( jet2Tau31, totalWeight );
								histos1D_[ "jet2Tau32_cutMassAsym" ]->Fill( jet2Tau32, totalWeight );
								histos1D_[ "deltaEtaDijet_cutMassAsym" ]->Fill( deltaEtaDijet, totalWeight );
								histos1D_[ "jet1SubjetPtRatio_cutMassAsym" ]->Fill( jet1SubjetPtRatio, totalWeight );
								histos1D_[ "jet2SubjetPtRatio_cutMassAsym" ]->Fill( jet2SubjetPtRatio, totalWeight );
								histos1D_[ "subjetPtRatio_cutMassAsym" ]->Fill( jet1SubjetPtRatio, totalWeight );
								histos1D_[ "subjetPtRatio_cutMassAsym" ]->Fill( jet2SubjetPtRatio, totalWeight );

								histos2D_[ "jetTrimmedMassHT_cutMassAsym" ]->Fill( trimmedMass, HT, totalWeight );
								histos2D_[ "massAveHT_cutMassAsym" ]->Fill( massAve, HT, totalWeight );

								histos2D_[ "massAvevsJet1Mass_cutMassAsym" ]->Fill( massAve, jet1Mass, totalWeight );
								histos2D_[ "massAvevsJet2Mass_cutMassAsym" ]->Fill( massAve, jet2Mass, totalWeight );
								histos2D_[ "massAvevsMassAsym_cutMassAsym" ]->Fill( massAve, massAsym, totalWeight );
								histos2D_[ "massAvevsDEta_cutMassAsym" ]->Fill( massAve, deltaEtaDijet, totalWeight );
								histos2D_[ "massAvevsJet1CosThetaStar_cutMassAsym" ]->Fill( massAve, jet1CosThetaStar, totalWeight );
								histos2D_[ "massAvevsJet2CosThetaStar_cutMassAsym" ]->Fill( massAve, jet2CosThetaStar, totalWeight );
								histos2D_[ "massAvevsJet1Tau21_cutMassAsym" ]->Fill( massAve, jet1Tau21, totalWeight );
								histos2D_[ "massAvevsJet1Tau31_cutMassAsym" ]->Fill( massAve, jet1Tau31, totalWeight );
								histos2D_[ "massAvevsJet1Tau32_cutMassAsym" ]->Fill( massAve, jet1Tau32, totalWeight );
								histos2D_[ "massAvevsJet2Tau21_cutMassAsym" ]->Fill( massAve, jet1Tau21, totalWeight );
								histos2D_[ "massAvevsJet2Tau31_cutMassAsym" ]->Fill( massAve, jet1Tau31, totalWeight );
								histos2D_[ "massAvevsJet2Tau32_cutMassAsym" ]->Fill( massAve, jet1Tau32, totalWeight );
								histos2D_[ "massAvevsJet1SubjetPtRatio_cutMassAsym" ]->Fill( massAve, jet1SubjetPtRatio, totalWeight );
								histos2D_[ "massAvevsJet2SubjetPtRatio_cutMassAsym" ]->Fill( massAve, jet2SubjetPtRatio, totalWeight );
								histos2D_[ "jet1vs2Mass_cutMassAsym" ]->Fill( jet1Mass, jet2Mass, totalWeight );
								histos2D_[ "dijetCorr_cutMassAsym" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), totalWeight );
								histos2D_[ "dijetCorrPhi_cutMassAsym" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), totalWeight );
							
								if( ( deltaEtaDijet  > cutDEtavalue ) ){

									cutmap["DEta"] += totalWeight;
									histos1D_[ "HT_cutDEta" ]->Fill( HT, totalWeight );
									histos1D_[ "NPV_cutDEta" ]->Fill( numPV, totalWeight );
									histos1D_[ "jetNum_cutDEta" ]->Fill( numJets, totalWeight );
									histos1D_[ "jet1Pt_cutDEta" ]->Fill( JETS[0].p4.Pt(), totalWeight );
									histos1D_[ "jet1Eta_cutDEta" ]->Fill( JETS[0].p4.Eta(), totalWeight );
									histos1D_[ "jet1Mass_cutDEta" ]->Fill( JETS[0].mass, totalWeight );
									histos1D_[ "jet2Pt_cutDEta" ]->Fill( JETS[1].p4.Pt(), totalWeight );
									histos1D_[ "jet2Eta_cutDEta" ]->Fill( JETS[1].p4.Eta(), totalWeight );
									histos1D_[ "jet2Mass_cutDEta" ]->Fill( JETS[1].mass, totalWeight );

									histos1D_[ "massAsymmetry_cutDEta" ]->Fill( massAsym, totalWeight );
									histos1D_[ "massAve_cutDEta" ]->Fill( massAve, totalWeight );
									histos1D_[ "massAve_cutDEta_1GeVBin" ]->Fill( massAve, totalWeight );
									histos1D_[ "jet1CosThetaStar_cutDEta" ]->Fill( jet1CosThetaStar, totalWeight );
									histos1D_[ "jet2CosThetaStar_cutDEta" ]->Fill( jet2CosThetaStar, totalWeight );
									histos1D_[ "jet1Tau1_cutDEta" ]->Fill( JETS[0].tau1, totalWeight );
									histos1D_[ "jet1Tau2_cutDEta" ]->Fill( JETS[0].tau2, totalWeight );
									histos1D_[ "jet1Tau3_cutDEta" ]->Fill( JETS[0].tau3, totalWeight );
									histos1D_[ "jet1Tau21_cutDEta" ]->Fill( jet1Tau21, totalWeight );
									histos1D_[ "jet1Tau31_cutDEta" ]->Fill( jet1Tau31, totalWeight );
									histos1D_[ "jet1Tau32_cutDEta" ]->Fill( jet1Tau32, totalWeight );
									histos1D_[ "jet2Tau1_cutDEta" ]->Fill( JETS[1].tau1, totalWeight );
									histos1D_[ "jet2Tau2_cutDEta" ]->Fill( JETS[1].tau2, totalWeight );
									histos1D_[ "jet2Tau3_cutDEta" ]->Fill( JETS[1].tau3, totalWeight );
									histos1D_[ "jet2Tau21_cutDEta" ]->Fill( jet2Tau21, totalWeight );
									histos1D_[ "jet2Tau31_cutDEta" ]->Fill( jet2Tau31, totalWeight );
									histos1D_[ "jet2Tau32_cutDEta" ]->Fill( jet2Tau32, totalWeight );
									histos1D_[ "deltaEtaDijet_cutDEta" ]->Fill( deltaEtaDijet, totalWeight );
									histos1D_[ "jet1SubjetPtRatio_cutDEta" ]->Fill( jet1SubjetPtRatio, totalWeight );
									histos1D_[ "jet2SubjetPtRatio_cutDEta" ]->Fill( jet2SubjetPtRatio, totalWeight );
									histos1D_[ "subjetPtRatio_cutDEta" ]->Fill( jet1SubjetPtRatio, totalWeight );
									histos1D_[ "subjetPtRatio_cutDEta" ]->Fill( jet2SubjetPtRatio, totalWeight );

									histos2D_[ "jetTrimmedMassHT_cutDEta" ]->Fill( trimmedMass, HT, totalWeight );
									histos2D_[ "massAveHT_cutDEta" ]->Fill( massAve, HT, totalWeight );

									histos2D_[ "massAvevsJet1Mass_cutDEta" ]->Fill( massAve, jet1Mass, totalWeight );
									histos2D_[ "massAvevsJet2Mass_cutDEta" ]->Fill( massAve, jet2Mass, totalWeight );
									histos2D_[ "massAvevsMassAsym_cutDEta" ]->Fill( massAve, massAsym, totalWeight );
									histos2D_[ "massAvevsDEta_cutDEta" ]->Fill( massAve, deltaEtaDijet, totalWeight );
									histos2D_[ "massAvevsJet1CosThetaStar_cutDEta" ]->Fill( massAve, jet1CosThetaStar, totalWeight );
									histos2D_[ "massAvevsJet2CosThetaStar_cutDEta" ]->Fill( massAve, jet2CosThetaStar, totalWeight );
									histos2D_[ "massAvevsJet1Tau21_cutDEta" ]->Fill( massAve, jet1Tau21, totalWeight );
									histos2D_[ "massAvevsJet1Tau31_cutDEta" ]->Fill( massAve, jet1Tau31, totalWeight );
									histos2D_[ "massAvevsJet1Tau32_cutDEta" ]->Fill( massAve, jet1Tau32, totalWeight );
									histos2D_[ "massAvevsJet2Tau21_cutDEta" ]->Fill( massAve, jet1Tau21, totalWeight );
									histos2D_[ "massAvevsJet2Tau31_cutDEta" ]->Fill( massAve, jet1Tau31, totalWeight );
									histos2D_[ "massAvevsJet2Tau32_cutDEta" ]->Fill( massAve, jet1Tau32, totalWeight );
									histos2D_[ "massAvevsJet1SubjetPtRatio_cutDEta" ]->Fill( massAve, jet1SubjetPtRatio, totalWeight );
									histos2D_[ "massAvevsJet2SubjetPtRatio_cutDEta" ]->Fill( massAve, jet2SubjetPtRatio, totalWeight );
									histos2D_[ "jet1vs2Mass_cutDEta" ]->Fill( jet1Mass, jet2Mass, totalWeight );
									histos2D_[ "dijetCorr_cutDEta" ]->Fill( JETS[0].p4.Eta(), JETS[1].p4.Eta(), totalWeight );
									histos2D_[ "dijetCorrPhi_cutDEta" ]->Fill( JETS[0].p4.Phi(), JETS[1].p4.Phi(), totalWeight );
								}
							}
						}
						
						if ((( TMath::Abs( jet1CosThetaStar ) < cutCosThetavalue ) && ( TMath::Abs( jet2CosThetaStar ) < cutCosThetavalue ) ) && ( massAsym < cutAsymvalue ) ) histos1D_[ "massAve_cutMassAsym_A" ]->Fill( massAve, totalWeight );
						if ((( TMath::Abs( jet1CosThetaStar ) < cutCosThetavalue ) && ( TMath::Abs( jet2CosThetaStar ) < cutCosThetavalue ) ) && ( massAsym > cutAsymvalue ) ) histos1D_[ "massAve_cutMassAsym_B" ]->Fill( massAve, totalWeight ); 
						if ((( TMath::Abs( jet1CosThetaStar ) > cutCosThetavalue ) && ( TMath::Abs( jet2CosThetaStar ) > cutCosThetavalue ) ) && ( massAsym < cutAsymvalue ) ) histos1D_[ "massAve_cutMassAsym_D" ]->Fill( massAve, totalWeight );
						if ((( TMath::Abs( jet1CosThetaStar ) > cutCosThetavalue ) && ( TMath::Abs( jet2CosThetaStar ) > cutCosThetavalue ) ) && ( massAsym > cutAsymvalue ) ) histos1D_[ "massAve_cutMassAsym_C" ]->Fill( massAve, totalWeight );
					}
				}
			}
		}
	}
	JETS.clear();
}


// ------------ method called once each job just before starting event loop  ------------
void RUNBoostedAnalysis::beginJob() {

	// Calculate PUWeight
	if ( !isData ) PUWeight_.generateWeights( dataPUFile );

	if (mkTree) {
		RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
		RUNAtree->Branch( "run", &run, "run/I" );
		RUNAtree->Branch( "lumi", &lumi, "lumi/I" );
		RUNAtree->Branch( "event", &event, "event/I" );
		RUNAtree->Branch( "numJets", &numJets, "numJets/I" );
		RUNAtree->Branch( "numPV", &numPV, "numPV/I" );
		RUNAtree->Branch( "puWeight", &puWeight, "puWeight/F" );
		RUNAtree->Branch( "lumiWeight", &lumiWeight, "lumiWeight/F" );
		RUNAtree->Branch( "HT", &HT, "HT/F" );
		RUNAtree->Branch( "AK4HT", &AK4HT, "AK4HT/F" );
		RUNAtree->Branch( "trimmedMass", &trimmedMass, "trimmedMass/F" );
		RUNAtree->Branch( "jet1Pt", &jet1Pt, "jet1Pt/F" );
		RUNAtree->Branch( "jet1Eta", &jet1Eta, "jet1Eta/F" );
		RUNAtree->Branch( "jet1Phi", &jet1Phi, "jet1Phi/F" );
		RUNAtree->Branch( "jet1E", &jet1E, "jet1E/F" );
		RUNAtree->Branch( "jet1btagCSV", &jet1btagCSV, "jet1btagCSV/F" );
		RUNAtree->Branch( "jet1Mass", &jet1Mass, "jet1Mass/F" );
		RUNAtree->Branch( "jet2Pt", &jet2Pt, "jet2Pt/F" );
		RUNAtree->Branch( "jet2Eta", &jet2Eta, "jet2Eta/F" );
		RUNAtree->Branch( "jet2Phi", &jet2Phi, "jet2Phi/F" );
		RUNAtree->Branch( "jet2E", &jet2E, "jet2E/F" );
		RUNAtree->Branch( "jet2btagCSV", &jet2btagCSV, "jet2btagCSV/F" );
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
		RUNAtree->Branch( "deltaEtaDijet", &deltaEtaDijet, "deltaEtaDijet/F" );
		RUNAtree->Branch( "jet1CosThetaStar", &jet1CosThetaStar, "jet1CosThetaStar/F" );
		RUNAtree->Branch( "jet2CosThetaStar", &jet2CosThetaStar, "jet2CosThetaStar/F" );
		RUNAtree->Branch( "jet1Tau21", &jet1Tau21, "jet1Tau21/F" );
		RUNAtree->Branch( "jet1Tau31", &jet1Tau31, "jet1Tau31/F" );
		RUNAtree->Branch( "jet1Tau32", &jet1Tau32, "jet1Tau32/F" );	
		RUNAtree->Branch( "jet2Tau21", &jet2Tau21, "jet2Tau21/F" );
		RUNAtree->Branch( "jet2Tau31", &jet2Tau31, "jet2Tau31/F" );
		RUNAtree->Branch( "jet2Tau32", &jet2Tau32, "jet2Tau32/F" );	
		RUNAtree->Branch( "jet1SubjetPtRatio", &jet1SubjetPtRatio, "jet1SubjetPtRatio/F" );
		RUNAtree->Branch( "jet2SubjetPtRatio", &jet2SubjetPtRatio, "jet2SubjetPtRatio/F" );
		RUNAtree->Branch( "cosPhi13412", &cosPhi13412, "cosPhi13412/F" );
		RUNAtree->Branch( "cosPhi31234", &cosPhi31234, "cosPhi31234/F" );

	} else { 

		histos1D_[ "oldJetPt" ] = fs_->make< TH1D >( "oldJetPt", "oldJetPt", 100, 0., 1000. );
		histos1D_[ "oldJetPt" ]->Sumw2();
		histos1D_[ "jetPt" ] = fs_->make< TH1D >( "jetPt", "jetPt", 100, 0., 1000. );
		histos1D_[ "jetPt" ]->Sumw2();
		histos1D_[ "rawJetPt" ] = fs_->make< TH1D >( "rawJetPt", "rawJetPt", 100, 0., 1000. );
		histos1D_[ "rawJetPt" ]->Sumw2();
		histos1D_[ "oldJetEta" ] = fs_->make< TH1D >( "oldJetEta", "oldJetEta", 100, -5., 5. );
		histos1D_[ "oldJetEta" ]->Sumw2();
		histos1D_[ "jetEta" ] = fs_->make< TH1D >( "jetEta", "jetEta", 100, -5., 5. );
		histos1D_[ "jetEta" ]->Sumw2();
		histos1D_[ "rawJetEta" ] = fs_->make< TH1D >( "rawJetEta", "rawJetEta", 100, -5., 5. );
		histos1D_[ "rawJetEta" ]->Sumw2();
		histos1D_[ "oldJetMass" ] = fs_->make< TH1D >( "oldJetMass", "oldJetMass", 60, 0., 600. );
		histos1D_[ "oldJetMass" ]->Sumw2();
		histos1D_[ "jetMass" ] = fs_->make< TH1D >( "jetMass", "jetMass", 60, 0., 600. );
		histos1D_[ "jetMass" ]->Sumw2();
		histos1D_[ "rawJetMass" ] = fs_->make< TH1D >( "rawJetMass", "rawJetMass", 60, 0., 600. );
		histos1D_[ "rawJetMass" ]->Sumw2();
		histos1D_[ "jetNum" ] = fs_->make< TH1D >( "jetNum", "jetNum", 10, 0., 10. );
		histos1D_[ "jetNum" ]->Sumw2();
		histos1D_[ "jetTrimmedMass" ] = fs_->make< TH1D >( "jetTrimmedMass", "jetTrimmedMass", 60, 0., 600. );
		histos1D_[ "jetTrimmedMass" ]->Sumw2();
		histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 500, 0., 5000. );
		histos1D_[ "HT" ]->Sumw2();
		histos1D_[ "NPV_NOPUWeight" ] = fs_->make< TH1D >( "NPV_NOPUWeight", "NPV_NOPUWeight", 80, 0., 80. );
		histos1D_[ "NPV_NOPUWeight" ]->Sumw2();
		histos1D_[ "NPV" ] = fs_->make< TH1D >( "NPV", "NPV", 80, 0., 80. );
		histos1D_[ "NPV" ]->Sumw2();
		histos1D_[ "PUWeight" ] = fs_->make< TH1D >( "PUWeight", "PUWeight", 50, 0., 5. );
		histos1D_[ "PUWeight" ]->Sumw2();
		histos2D_[ "jetTrimmedMassHT" ] = fs_->make< TH2D >( "jetTrimmedMassHT", "jetTrimmedMassHT", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT" ]->Sumw2();
		histos1D_[ "neutralHadronEnergy" ] = fs_->make< TH1D >( "neutralHadronEnergy", "neutralHadronEnergy", 50, 0., 1. );
		histos1D_[ "neutralHadronEnergy" ]->Sumw2();
		histos1D_[ "neutralEmEnergy" ] = fs_->make< TH1D >( "neutralEmEnergy", "neutralEmEnergy", 50, 0., 1. );
		histos1D_[ "neutralEmEnergy" ]->Sumw2();
		histos1D_[ "chargedHadronEnergy" ] = fs_->make< TH1D >( "chargedHadronEnergy", "chargedHadronEnergy", 50, 0., 1. );
		histos1D_[ "chargedHadronEnergy" ]->Sumw2();
		histos1D_[ "chargedEmEnergy" ] = fs_->make< TH1D >( "chargedEmEnergy", "chargedEmEnergy", 50, 0., 1. );
		histos1D_[ "chargedEmEnergy" ]->Sumw2();
		histos1D_[ "chargedMultiplicity" ] = fs_->make< TH1D >( "chargedMultiplicity", "chargedMultiplicity", 50, 0., 1. );
		histos1D_[ "chargedMultiplicity" ]->Sumw2();
		histos1D_[ "numConst" ] = fs_->make< TH1D >( "numConst", "numConst", 100, 0., 100. );
		histos1D_[ "numConst" ]->Sumw2();

		histos1D_[ "HT_cutTrigger" ] = fs_->make< TH1D >( "HT_cutTrigger", "HT_cutTrigger", 500, 0., 5000. );
		histos1D_[ "HT_cutTrigger" ]->Sumw2();
		histos1D_[ "MET_cutTrigger" ] = fs_->make< TH1D >( "MET_cutTrigger", "MET_cutTrigger", 20, 0., 200. );
		histos1D_[ "MET_cutTrigger" ]->Sumw2();
		histos1D_[ "METHT_cutTrigger" ] = fs_->make< TH1D >( "METHT_cutTrigger", "METHT_cutTrigger", 50, 0., 1. );
		histos1D_[ "METHT_cutTrigger" ]->Sumw2();
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
		histos2D_[ "jetTrimmedMassHT_cutTrigger" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutTrigger", "jetTrimmedMassHT_cutTrigger", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT_cutTrigger" ]->Sumw2();

		histos1D_[ "HT_cutDijet" ] = fs_->make< TH1D >( "HT_cutDijet", "HT_cutDijet", 500, 0., 5000. );
		histos1D_[ "HT_cutDijet" ]->Sumw2();
		histos1D_[ "NPV_cutDijet" ] = fs_->make< TH1D >( "NPV_cutDijet", "NPV_cutDijet", 80, 0., 80. );
		histos1D_[ "NPV_cutDijet" ]->Sumw2();
		histos1D_[ "jetNum_cutDijet" ] = fs_->make< TH1D >( "jetNum_cutDijet", "jetNum_cutDijet", 10, 0., 10. );
		histos1D_[ "jetNum_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Pt_cutDijet" ] = fs_->make< TH1D >( "jet1Pt_cutDijet", "jet1Pt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Eta_cutDijet" ] = fs_->make< TH1D >( "jet1Eta_cutDijet", "jet1Eta_cutDijet", 100, -5., 5. );
		histos1D_[ "jet1Eta_cutDijet" ]->Sumw2();
		histos1D_[ "jet1Mass_cutDijet" ] = fs_->make< TH1D >( "jet1Mass_cutDijet", "jet1Mass_cutDijet", 60, 0., 600. );
		histos1D_[ "jet1Mass_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Pt_cutDijet" ] = fs_->make< TH1D >( "jet2Pt_cutDijet", "jet2Pt_cutDijet", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Eta_cutDijet" ] = fs_->make< TH1D >( "jet2Eta_cutDijet", "jet2Eta_cutDijet", 100, -5., 5. );
		histos1D_[ "jet2Eta_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Mass_cutDijet" ] = fs_->make< TH1D >( "jet2Mass_cutDijet", "jet2Mass_cutDijet", 60, 0., 600. );
		histos1D_[ "jet2Mass_cutDijet" ]->Sumw2();
		histos1D_[ "MET_cutDijet" ] = fs_->make< TH1D >( "MET_cutDijet", "MET_cutDijet", 20, 0., 200. );
		histos1D_[ "MET_cutDijet" ]->Sumw2();
		histos1D_[ "METHT_cutDijet" ] = fs_->make< TH1D >( "METHT_cutDijet", "METHT_cutDijet", 50, 0., 1. );
		histos1D_[ "METHT_cutDijet" ]->Sumw2();

		histos1D_[ "massAsymmetry_cutDijet" ] = fs_->make< TH1D >( "massAsymmetry_cutDijet", "massAsymmetry_cutDijet", 20, 0., 1. );
		histos1D_[ "massAsymmetry_cutDijet" ]->Sumw2();
		histos1D_[ "massAve_cutDijet" ] = fs_->make< TH1D >( "massAve_cutDijet", "massAve_cutDijet", 60, 0., 600. );
		histos1D_[ "massAve_cutDijet" ]->Sumw2();
		histos1D_[ "jet1CosThetaStar_cutDijet" ] = fs_->make< TH1D >( "jet1CosThetaStar_cutDijet", "jet1CosThetaStar_cutDijet", 20, 0., 1. );
		histos1D_[ "jet1CosThetaStar_cutDijet" ]->Sumw2();
		histos1D_[ "jet2CosThetaStar_cutDijet" ] = fs_->make< TH1D >( "jet2CosThetaStar_cutDijet", "jet2CosThetaStar_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2CosThetaStar_cutDijet" ]->Sumw2();
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
		histos1D_[ "jet2Tau1_cutDijet" ] = fs_->make< TH1D >( "jet2Tau1_cutDijet", "jet2Tau1_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Tau1_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Tau2_cutDijet" ] = fs_->make< TH1D >( "jet2Tau2_cutDijet", "jet2Tau2_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Tau2_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Tau3_cutDijet" ] = fs_->make< TH1D >( "jet2Tau3_cutDijet", "jet2Tau3_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Tau3_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Tau21_cutDijet" ] = fs_->make< TH1D >( "jet2Tau21_cutDijet", "jet2Tau21_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Tau21_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Tau31_cutDijet" ] = fs_->make< TH1D >( "jet2Tau31_cutDijet", "jet2Tau31_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Tau31_cutDijet" ]->Sumw2();
		histos1D_[ "jet2Tau32_cutDijet" ] = fs_->make< TH1D >( "jet2Tau32_cutDijet", "jet2Tau32_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2Tau32_cutDijet" ]->Sumw2();
		histos1D_[ "deltaEtaDijet_cutDijet" ] = fs_->make< TH1D >( "deltaEtaDijet_cutDijet", "deltaEtaDijet_cutDijet", 50, 0., 5. );
		histos1D_[ "deltaEtaDijet_cutDijet" ]->Sumw2();
		histos1D_[ "jet1SubjetPtRatio_cutDijet" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutDijet", "jet1SubjetPtRatio_cutDijet", 20, 0, 1.);
		histos1D_[ "jet1SubjetPtRatio_cutDijet" ]->Sumw2();
		histos1D_[ "jet2SubjetPtRatio_cutDijet" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutDijet", "jet2SubjetPtRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "jet2SubjetPtRatio_cutDijet" ]->Sumw2();
		histos1D_[ "subjetPtRatio_cutDijet" ] = fs_->make< TH1D >( "subjetPtRatio_cutDijet", "subjetPtRatio_cutDijet", 20, 0., 1. );
		histos1D_[ "subjetPtRatio_cutDijet" ]->Sumw2();

		histos2D_[ "jetTrimmedMassHT_cutDijet" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutDijet", "jetTrimmedMassHT_cutDijet", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT_cutDijet" ]->Sumw2();
		histos2D_[ "massAveHT_cutDijet" ] = fs_->make< TH2D >( "massAveHT_cutDijet", "massAveHT_cutDijet", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "massAveHT_cutDijet" ]->Sumw2();

		histos2D_[ "massAvevsJet1Mass_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutDijet", "massAvevsJet1Mass_cutDijet", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet1Mass_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet2Mass_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutDijet", "massAvevsJet2Mass_cutDijet", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet2Mass_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsMassAsym_cutDijet" ] = fs_->make< TH2D >( "massAvevsMassAsym_cutDijet", "massAvevsMassAsym_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsMassAsym_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsDEta_cutDijet" ] = fs_->make< TH2D >( "massAvevsDEta_cutDijet", "massAvevsDEta_cutDijet", 60, 0., 600., 50, 0., 5. );
		histos2D_[ "massAvevsDEta_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet1CosThetaStar_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet1CosThetaStar_cutDijet", "massAvevsJet1CosThetaStar_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1CosThetaStar_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet2CosThetaStar_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet2CosThetaStar_cutDijet", "massAvevsJet2CosThetaStar_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2CosThetaStar_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau21_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet1Tau21_cutDijet", "massAvevsJet1Tau21_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau21_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau31_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet1Tau31_cutDijet", "massAvevsJet1Tau31_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau31_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau32_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet1Tau32_cutDijet", "massAvevsJet1Tau32_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau32_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau21_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet2Tau21_cutDijet", "massAvevsJet2Tau21_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau21_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau31_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet2Tau31_cutDijet", "massAvevsJet2Tau31_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau31_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau32_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet2Tau32_cutDijet", "massAvevsJet2Tau32_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau32_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet1SubjetPtRatio_cutDijet", "massAvevsJet1SubjetPtRatio_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutDijet" ]->Sumw2();
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutDijet" ] = fs_->make< TH2D >( "massAvevsJet2SubjetPtRatio_cutDijet", "massAvevsJet2SubjetPtRatio_cutDijet", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutDijet" ]->Sumw2();

		histos2D_[ "jet1vs2Mass_cutDijet" ] = fs_->make< TH2D >( "jet1vs2Mass_cutDijet", "jet1vs2Mass_cutDijet", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "jet1vs2Mass_cutDijet" ]->Sumw2();
		histos2D_[ "dijetCorr_cutDijet" ] = fs_->make< TH2D >( "dijetCorr_cutDijet", "dijetCorr_cutDijet", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutDijet" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutDijet" ] = fs_->make< TH2D >( "dijetCorrPhi_cutDijet", "dijetCorrPhi_cutDijet", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutDijet" ]->Sumw2();

		histos1D_[ "subjetPolAngle13412_cutDijet" ] = fs_->make< TH1D >( "subjetPolAngle13412_cutDijet", "subjetPolAngle13412_cutDijet", 100, 0., 1. );
		histos1D_[ "subjetPolAngle13412_cutDijet" ]->Sumw2();
		histos1D_[ "subjetPolAngle31234_cutDijet" ] = fs_->make< TH1D >( "subjetPolAngle31234_cutDijet", "subjetPolAngle31234_cutDijet", 100, 0., 1. );
		histos1D_[ "subjetPolAngle31234_cutDijet" ]->Sumw2();
		histos1D_[ "mu1_cutDijet" ] = fs_->make< TH1D >( "mu1_cutDijet", "mu1_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu1_cutDijet" ]->Sumw2();
		histos1D_[ "mu2_cutDijet" ] = fs_->make< TH1D >( "mu2_cutDijet", "mu2_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu2_cutDijet" ]->Sumw2();
		histos1D_[ "mu3_cutDijet" ] = fs_->make< TH1D >( "mu3_cutDijet", "mu3_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu3_cutDijet" ]->Sumw2();
		histos1D_[ "mu4_cutDijet" ] = fs_->make< TH1D >( "mu4_cutDijet", "mu4_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu4_cutDijet" ]->Sumw2();
		histos1D_[ "mu5_cutDijet" ] = fs_->make< TH1D >( "mu5_cutDijet", "mu5_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu5_cutDijet" ]->Sumw2();
		histos1D_[ "mu6_cutDijet" ] = fs_->make< TH1D >( "mu6_cutDijet", "mu6_cutDijet", 150, 0., 1.5 );
		histos1D_[ "mu6_cutDijet" ]->Sumw2();
		histos2D_[ "subjetPolAngle13412vs31234_cutDijet" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234_cutDijet", "subjetPolAngle13412vs31234_cutDijet", 100, 0., 1., 100, 0., 1. );
		histos2D_[ "subjetPolAngle13412vs31234_cutDijet" ]->Sumw2();
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutDijet" ] = fs_->make< TH2D >( "subjetPolAngle31234vsSubjetPtRatio_cutDijet", "subjetPolAngle31234vsSubjetPtRatio_cutDijet", 100, 0., 1., 20, 0., 1. );
		histos2D_[ "subjetPolAngle31234vsSubjetPtRatio_cutDijet" ]->Sumw2();
		histos2D_[ "mu1234_cutDijet" ] = fs_->make< TH2D >( "mu1234_cutDijet", "mu1234_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu1234_cutDijet" ]->Sumw2();
		histos2D_[ "dalitz1234_cutDijet" ] = fs_->make< TH2D >( "dalitz1234_cutDijet", "dalitz1234_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz1234_cutDijet" ]->Sumw2();
		histos2D_[ "mu3412_cutDijet" ] = fs_->make< TH2D >( "mu3412_cutDijet", "mu3412_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "mu3412_cutDijet" ]->Sumw2();
		histos2D_[ "dalitz3412_cutDijet" ] = fs_->make< TH2D >( "dalitz3412_cutDijet", "dalitz3412_cutDijet", 150, 0., 1.5, 150, 0., 1.5 );
		histos2D_[ "dalitz3412_cutDijet" ]->Sumw2();

		histos1D_[ "HT_cutHT" ] = fs_->make< TH1D >( "HT_cutHT", "HT_cutHT", 500, 0., 5000. );
		histos1D_[ "HT_cutHT" ]->Sumw2();
		histos1D_[ "NPV_cutHT" ] = fs_->make< TH1D >( "NPV_cutHT", "NPV_cutHT", 80, 0., 80. );
		histos1D_[ "NPV_cutHT" ]->Sumw2();
		histos1D_[ "jetNum_cutHT" ] = fs_->make< TH1D >( "jetNum_cutHT", "jetNum_cutHT", 10, 0., 10. );
		histos1D_[ "jetNum_cutHT" ]->Sumw2();
		histos1D_[ "jet1Pt_cutHT" ] = fs_->make< TH1D >( "jet1Pt_cutHT", "jet1Pt_cutHT", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutHT" ]->Sumw2();
		histos1D_[ "jet1Eta_cutHT" ] = fs_->make< TH1D >( "jet1Eta_cutHT", "jet1Eta_cutHT", 100, -5., 5. );
		histos1D_[ "jet1Eta_cutHT" ]->Sumw2();
		histos1D_[ "jet1Mass_cutHT" ] = fs_->make< TH1D >( "jet1Mass_cutHT", "jet1Mass_cutHT", 60, 0., 600. );
		histos1D_[ "jet1Mass_cutHT" ]->Sumw2();
		histos1D_[ "jet2Pt_cutHT" ] = fs_->make< TH1D >( "jet2Pt_cutHT", "jet2Pt_cutHT", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutHT" ]->Sumw2();
		histos1D_[ "jet2Eta_cutHT" ] = fs_->make< TH1D >( "jet2Eta_cutHT", "jet2Eta_cutHT", 100, -5., 5. );
		histos1D_[ "jet2Eta_cutHT" ]->Sumw2();
		histos1D_[ "jet2Mass_cutHT" ] = fs_->make< TH1D >( "jet2Mass_cutHT", "jet2Mass_cutHT", 60, 0., 600. );
		histos1D_[ "jet2Mass_cutHT" ]->Sumw2();
		histos1D_[ "neutralHadronEnergy_cutHT" ] = fs_->make< TH1D >( "neutralHadronEnergy_cutHT", "neutralHadronEnergy", 50, 0., 1. );
		histos1D_[ "neutralHadronEnergy_cutHT" ]->Sumw2();
		histos1D_[ "neutralEmEnergy_cutHT" ] = fs_->make< TH1D >( "neutralEmEnergy_cutHT", "neutralEmEnergy", 50, 0., 1. );
		histos1D_[ "neutralEmEnergy_cutHT" ]->Sumw2();
		histos1D_[ "chargedHadronEnergy_cutHT" ] = fs_->make< TH1D >( "chargedHadronEnergy_cutHT", "chargedHadronEnergy", 50, 0., 1. );
		histos1D_[ "chargedHadronEnergy_cutHT" ]->Sumw2();
		histos1D_[ "chargedEmEnergy_cutHT" ] = fs_->make< TH1D >( "chargedEmEnergy_cutHT", "chargedEmEnergy", 50, 0., 1. );
		histos1D_[ "chargedEmEnergy_cutHT" ]->Sumw2();
		histos1D_[ "chargedMultiplicity_cutHT" ] = fs_->make< TH1D >( "chargedMultiplicity_cutHT", "chargedMultiplicity", 50, 0., 1. );
		histos1D_[ "chargedMultiplicity_cutHT" ]->Sumw2();
		histos1D_[ "numConst_cutHT" ] = fs_->make< TH1D >( "numConst_cutHT", "numConst", 100, 0., 100. );
		histos1D_[ "numConst_cutHT" ]->Sumw2();
		histos1D_[ "MET_cutHT" ] = fs_->make< TH1D >( "MET_cutHT", "MET_cutHT", 20, 0., 200. );
		histos1D_[ "MET_cutHT" ]->Sumw2();
		histos1D_[ "METHT_cutHT" ] = fs_->make< TH1D >( "METHT_cutHT", "METHT_cutHT", 50, 0., 1. );
		histos1D_[ "METHT_cutHT" ]->Sumw2();

		histos1D_[ "massAsymmetry_cutHT" ] = fs_->make< TH1D >( "massAsymmetry_cutHT", "massAsymmetry_cutHT", 20, 0., 1. );
		histos1D_[ "massAsymmetry_cutHT" ]->Sumw2();
		histos1D_[ "massAve_cutHT" ] = fs_->make< TH1D >( "massAve_cutHT", "massAve_cutHT", 60, 0., 600. );
		histos1D_[ "massAve_cutHT" ]->Sumw2();
		histos1D_[ "jet1CosThetaStar_cutHT" ] = fs_->make< TH1D >( "jet1CosThetaStar_cutHT", "jet1CosThetaStar_cutHT", 20, 0., 1. );
		histos1D_[ "jet1CosThetaStar_cutHT" ]->Sumw2();
		histos1D_[ "jet2CosThetaStar_cutHT" ] = fs_->make< TH1D >( "jet2CosThetaStar_cutHT", "jet2CosThetaStar_cutHT", 20, 0., 1. );
		histos1D_[ "jet2CosThetaStar_cutHT" ]->Sumw2();
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
		histos1D_[ "jet2Tau1_cutHT" ] = fs_->make< TH1D >( "jet2Tau1_cutHT", "jet2Tau1_cutHT", 20, 0., 1. );
		histos1D_[ "jet2Tau1_cutHT" ]->Sumw2();
		histos1D_[ "jet2Tau2_cutHT" ] = fs_->make< TH1D >( "jet2Tau2_cutHT", "jet2Tau2_cutHT", 20, 0., 1. );
		histos1D_[ "jet2Tau2_cutHT" ]->Sumw2();
		histos1D_[ "jet2Tau3_cutHT" ] = fs_->make< TH1D >( "jet2Tau3_cutHT", "jet2Tau3_cutHT", 20, 0., 1. );
		histos1D_[ "jet2Tau3_cutHT" ]->Sumw2();
		histos1D_[ "jet2Tau21_cutHT" ] = fs_->make< TH1D >( "jet2Tau21_cutHT", "jet2Tau21_cutHT", 20, 0., 1. );
		histos1D_[ "jet2Tau21_cutHT" ]->Sumw2();
		histos1D_[ "jet2Tau31_cutHT" ] = fs_->make< TH1D >( "jet2Tau31_cutHT", "jet2Tau31_cutHT", 20, 0., 1. );
		histos1D_[ "jet2Tau31_cutHT" ]->Sumw2();
		histos1D_[ "jet2Tau32_cutHT" ] = fs_->make< TH1D >( "jet2Tau32_cutHT", "jet2Tau32_cutHT", 20, 0., 1. );
		histos1D_[ "jet2Tau32_cutHT" ]->Sumw2();
		histos1D_[ "deltaEtaDijet_cutHT" ] = fs_->make< TH1D >( "deltaEtaDijet_cutHT", "deltaEtaDijet_cutHT", 50, 0., 5. );
		histos1D_[ "deltaEtaDijet_cutHT" ]->Sumw2();
		histos1D_[ "jet1SubjetPtRatio_cutHT" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutHT", "jet1SubjetPtRatio_cutHT", 20, 0, 1.);
		histos1D_[ "jet1SubjetPtRatio_cutHT" ]->Sumw2();
		histos1D_[ "jet2SubjetPtRatio_cutHT" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutHT", "jet2SubjetPtRatio_cutHT", 20, 0., 1. );
		histos1D_[ "jet2SubjetPtRatio_cutHT" ]->Sumw2();
		histos1D_[ "subjetPtRatio_cutHT" ] = fs_->make< TH1D >( "subjetPtRatio_cutHT", "subjetPtRatio_cutHT", 20, 0., 1. );
		histos1D_[ "subjetPtRatio_cutHT" ]->Sumw2();

		histos2D_[ "jetTrimmedMassHT_cutHT" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutHT", "jetTrimmedMassHT_cutHT", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT_cutHT" ]->Sumw2();
		histos2D_[ "massAveHT_cutHT" ] = fs_->make< TH2D >( "massAveHT_cutHT", "massAveHT_cutHT", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "massAveHT_cutHT" ]->Sumw2();

		histos2D_[ "massAvevsJet1Mass_cutHT" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutHT", "massAvevsJet1Mass_cutHT", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet1Mass_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet2Mass_cutHT" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutHT", "massAvevsJet2Mass_cutHT", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet2Mass_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsHT_cutHT" ] = fs_->make< TH2D >( "massAvevsHT_cutHT", "massAvevsHT_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsHT_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsDEta_cutHT" ] = fs_->make< TH2D >( "massAvevsDEta_cutHT", "massAvevsDEta_cutHT", 60, 0., 600., 50, 0., 5. );
		histos2D_[ "massAvevsDEta_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet1CosThetaStar_cutHT" ] = fs_->make< TH2D >( "massAvevsJet1CosThetaStar_cutHT", "massAvevsJet1CosThetaStar_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1CosThetaStar_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet2CosThetaStar_cutHT" ] = fs_->make< TH2D >( "massAvevsJet2CosThetaStar_cutHT", "massAvevsJet2CosThetaStar_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2CosThetaStar_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau21_cutHT" ] = fs_->make< TH2D >( "massAvevsJet1Tau21_cutHT", "massAvevsJet1Tau21_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau21_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau31_cutHT" ] = fs_->make< TH2D >( "massAvevsJet1Tau31_cutHT", "massAvevsJet1Tau31_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau31_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau32_cutHT" ] = fs_->make< TH2D >( "massAvevsJet1Tau32_cutHT", "massAvevsJet1Tau32_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau32_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau21_cutHT" ] = fs_->make< TH2D >( "massAvevsJet2Tau21_cutHT", "massAvevsJet2Tau21_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau21_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau31_cutHT" ] = fs_->make< TH2D >( "massAvevsJet2Tau31_cutHT", "massAvevsJet2Tau31_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau31_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau32_cutHT" ] = fs_->make< TH2D >( "massAvevsJet2Tau32_cutHT", "massAvevsJet2Tau32_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau32_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutHT" ] = fs_->make< TH2D >( "massAvevsJet1SubjetPtRatio_cutHT", "massAvevsJet1SubjetPtRatio_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutHT" ]->Sumw2();
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutHT" ] = fs_->make< TH2D >( "massAvevsJet2SubjetPtRatio_cutHT", "massAvevsJet2SubjetPtRatio_cutHT", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutHT" ]->Sumw2();
		histos2D_[ "jet1vs2Mass_cutHT" ] = fs_->make< TH2D >( "jet1vs2Mass_cutHT", "jet1vs2Mass_cutHT", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "jet1vs2Mass_cutHT" ]->Sumw2();
		histos2D_[ "dijetCorr_cutHT" ] = fs_->make< TH2D >( "dijetCorr_cutHT", "dijetCorr_cutHT", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutHT" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutHT" ] = fs_->make< TH2D >( "dijetCorrPhi_cutHT", "dijetCorrPhi_cutHT", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutHT" ]->Sumw2();

		histos1D_[ "HT_cutTau21" ] = fs_->make< TH1D >( "HT_cutTau21", "HT_cutTau21", 500, 0., 5000. );
		histos1D_[ "HT_cutTau21" ]->Sumw2();
		histos1D_[ "NPV_cutTau21" ] = fs_->make< TH1D >( "NPV_cutTau21", "NPV_cutTau21", 80, 0., 80. );
		histos1D_[ "NPV_cutTau21" ]->Sumw2();
		histos1D_[ "jetNum_cutTau21" ] = fs_->make< TH1D >( "jetNum_cutTau21", "jetNum_cutTau21", 10, 0., 10. );
		histos1D_[ "jetNum_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Pt_cutTau21" ] = fs_->make< TH1D >( "jet1Pt_cutTau21", "jet1Pt_cutTau21", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Eta_cutTau21" ] = fs_->make< TH1D >( "jet1Eta_cutTau21", "jet1Eta_cutTau21", 100, -5., 5. );
		histos1D_[ "jet1Eta_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Mass_cutTau21" ] = fs_->make< TH1D >( "jet1Mass_cutTau21", "jet1Mass_cutTau21", 60, 0., 600. );
		histos1D_[ "jet1Mass_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Pt_cutTau21" ] = fs_->make< TH1D >( "jet2Pt_cutTau21", "jet2Pt_cutTau21", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Eta_cutTau21" ] = fs_->make< TH1D >( "jet2Eta_cutTau21", "jet2Eta_cutTau21", 100, -5., 5. );
		histos1D_[ "jet2Eta_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Mass_cutTau21" ] = fs_->make< TH1D >( "jet2Mass_cutTau21", "jet2Mass_cutTau21", 60, 0., 600. );
		histos1D_[ "jet2Mass_cutTau21" ]->Sumw2();

		histos1D_[ "massAsymmetry_cutTau21" ] = fs_->make< TH1D >( "massAsymmetry_cutTau21", "massAsymmetry_cutTau21", 20, 0., 1. );
		histos1D_[ "massAsymmetry_cutTau21" ]->Sumw2();
		histos1D_[ "massAve_cutTau21" ] = fs_->make< TH1D >( "massAve_cutTau21", "massAve_cutTau21", 60, 0., 600. );
		histos1D_[ "massAve_cutTau21" ]->Sumw2();
		histos1D_[ "jet1CosThetaStar_cutTau21" ] = fs_->make< TH1D >( "jet1CosThetaStar_cutTau21", "jet1CosThetaStar_cutTau21", 20, 0., 1. );
		histos1D_[ "jet1CosThetaStar_cutTau21" ]->Sumw2();
		histos1D_[ "jet2CosThetaStar_cutTau21" ] = fs_->make< TH1D >( "jet2CosThetaStar_cutTau21", "jet2CosThetaStar_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2CosThetaStar_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Tau1_cutTau21" ] = fs_->make< TH1D >( "jet1Tau1_cutTau21", "jet1Tau1_cutTau21", 20, 0., 1. );
		histos1D_[ "jet1Tau1_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Tau2_cutTau21" ] = fs_->make< TH1D >( "jet1Tau2_cutTau21", "jet1Tau2_cutTau21", 20, 0., 1. );
		histos1D_[ "jet1Tau2_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Tau3_cutTau21" ] = fs_->make< TH1D >( "jet1Tau3_cutTau21", "jet1Tau3_cutTau21", 20, 0., 1. );
		histos1D_[ "jet1Tau3_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Tau21_cutTau21" ] = fs_->make< TH1D >( "jet1Tau21_cutTau21", "jet1Tau21_cutTau21", 20, 0., 1. );
		histos1D_[ "jet1Tau21_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Tau31_cutTau21" ] = fs_->make< TH1D >( "jet1Tau31_cutTau21", "jet1Tau31_cutTau21", 20, 0., 1. );
		histos1D_[ "jet1Tau31_cutTau21" ]->Sumw2();
		histos1D_[ "jet1Tau32_cutTau21" ] = fs_->make< TH1D >( "jet1Tau32_cutTau21", "jet1Tau32_cutTau21", 20, 0., 1. );
		histos1D_[ "jet1Tau32_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Tau1_cutTau21" ] = fs_->make< TH1D >( "jet2Tau1_cutTau21", "jet2Tau1_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2Tau1_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Tau2_cutTau21" ] = fs_->make< TH1D >( "jet2Tau2_cutTau21", "jet2Tau2_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2Tau2_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Tau3_cutTau21" ] = fs_->make< TH1D >( "jet2Tau3_cutTau21", "jet2Tau3_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2Tau3_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Tau21_cutTau21" ] = fs_->make< TH1D >( "jet2Tau21_cutTau21", "jet2Tau21_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2Tau21_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Tau31_cutTau21" ] = fs_->make< TH1D >( "jet2Tau31_cutTau21", "jet2Tau31_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2Tau31_cutTau21" ]->Sumw2();
		histos1D_[ "jet2Tau32_cutTau21" ] = fs_->make< TH1D >( "jet2Tau32_cutTau21", "jet2Tau32_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2Tau32_cutTau21" ]->Sumw2();
		histos1D_[ "deltaEtaDijet_cutTau21" ] = fs_->make< TH1D >( "deltaEtaDijet_cutTau21", "deltaEtaDijet_cutTau21", 50, 0., 5. );
		histos1D_[ "deltaEtaDijet_cutTau21" ]->Sumw2();
		histos1D_[ "jet1SubjetPtRatio_cutTau21" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutTau21", "jet1SubjetPtRatio_cutTau21", 20, 0, 1.);
		histos1D_[ "jet1SubjetPtRatio_cutTau21" ]->Sumw2();
		histos1D_[ "jet2SubjetPtRatio_cutTau21" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutTau21", "jet2SubjetPtRatio_cutTau21", 20, 0., 1. );
		histos1D_[ "jet2SubjetPtRatio_cutTau21" ]->Sumw2();
		histos1D_[ "subjetPtRatio_cutTau21" ] = fs_->make< TH1D >( "subjetPtRatio_cutTau21", "subjetPtRatio_cutTau21", 20, 0., 1. );
		histos1D_[ "subjetPtRatio_cutTau21" ]->Sumw2();

		histos2D_[ "jetTrimmedMassHT_cutTau21" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutTau21", "jetTrimmedMassHT_cutTau21", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT_cutTau21" ]->Sumw2();
		histos2D_[ "massAveHT_cutTau21" ] = fs_->make< TH2D >( "massAveHT_cutTau21", "massAveHT_cutTau21", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "massAveHT_cutTau21" ]->Sumw2();

		histos2D_[ "massAvevsJet1Mass_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutTau21", "massAvevsJet1Mass_cutTau21", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet1Mass_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet2Mass_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutTau21", "massAvevsJet2Mass_cutTau21", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet2Mass_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsMassAsym_cutTau21" ] = fs_->make< TH2D >( "massAvevsMassAsym_cutTau21", "massAvevsMassAsym_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsMassAsym_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsDEta_cutTau21" ] = fs_->make< TH2D >( "massAvevsDEta_cutTau21", "massAvevsDEta_cutTau21", 60, 0., 600., 50, 0., 5. );
		histos2D_[ "massAvevsDEta_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet1CosThetaStar_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet1CosThetaStar_cutTau21", "massAvevsJet1CosThetaStar_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1CosThetaStar_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet2CosThetaStar_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet2CosThetaStar_cutTau21", "massAvevsJet2CosThetaStar_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2CosThetaStar_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau21_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet1Tau21_cutTau21", "massAvevsJet1Tau21_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau21_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau31_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet1Tau31_cutTau21", "massAvevsJet1Tau31_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau31_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau32_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet1Tau32_cutTau21", "massAvevsJet1Tau32_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau32_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau21_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet2Tau21_cutTau21", "massAvevsJet2Tau21_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau21_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau31_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet2Tau31_cutTau21", "massAvevsJet2Tau31_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau31_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau32_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet2Tau32_cutTau21", "massAvevsJet2Tau32_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau32_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet1SubjetPtRatio_cutTau21", "massAvevsJet1SubjetPtRatio_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutTau21" ]->Sumw2();
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutTau21" ] = fs_->make< TH2D >( "massAvevsJet2SubjetPtRatio_cutTau21", "massAvevsJet2SubjetPtRatio_cutTau21", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutTau21" ]->Sumw2();
		histos2D_[ "jet1vs2Mass_cutTau21" ] = fs_->make< TH2D >( "jet1vs2Mass_cutTau21", "jet1vs2Mass_cutTau21", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "jet1vs2Mass_cutTau21" ]->Sumw2();
		histos2D_[ "dijetCorr_cutTau21" ] = fs_->make< TH2D >( "dijetCorr_cutTau21", "dijetCorr_cutTau21", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutTau21" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutTau21" ] = fs_->make< TH2D >( "dijetCorrPhi_cutTau21", "dijetCorrPhi_cutTau21", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutTau21" ]->Sumw2();



		histos1D_[ "HT_cutCosTheta" ] = fs_->make< TH1D >( "HT_cutCosTheta", "HT_cutCosTheta", 500, 0., 5000. );
		histos1D_[ "HT_cutCosTheta" ]->Sumw2();
		histos1D_[ "NPV_cutCosTheta" ] = fs_->make< TH1D >( "NPV_cutCosTheta", "NPV_cutCosTheta", 80, 0., 80. );
		histos1D_[ "NPV_cutCosTheta" ]->Sumw2();
		histos1D_[ "jetNum_cutCosTheta" ] = fs_->make< TH1D >( "jetNum_cutCosTheta", "jetNum_cutCosTheta", 10, 0., 10. );
		histos1D_[ "jetNum_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Pt_cutCosTheta" ] = fs_->make< TH1D >( "jet1Pt_cutCosTheta", "jet1Pt_cutCosTheta", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Eta_cutCosTheta" ] = fs_->make< TH1D >( "jet1Eta_cutCosTheta", "jet1Eta_cutCosTheta", 100, -5., 5. );
		histos1D_[ "jet1Eta_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Mass_cutCosTheta" ] = fs_->make< TH1D >( "jet1Mass_cutCosTheta", "jet1Mass_cutCosTheta", 60, 0., 600. );
		histos1D_[ "jet1Mass_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Pt_cutCosTheta" ] = fs_->make< TH1D >( "jet2Pt_cutCosTheta", "jet2Pt_cutCosTheta", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Eta_cutCosTheta" ] = fs_->make< TH1D >( "jet2Eta_cutCosTheta", "jet2Eta_cutCosTheta", 100, -5., 5. );
		histos1D_[ "jet2Eta_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Mass_cutCosTheta" ] = fs_->make< TH1D >( "jet2Mass_cutCosTheta", "jet2Mass_cutCosTheta", 60, 0., 600. );
		histos1D_[ "jet2Mass_cutCosTheta" ]->Sumw2();

		histos1D_[ "massAsymmetry_cutCosTheta" ] = fs_->make< TH1D >( "massAsymmetry_cutCosTheta", "massAsymmetry_cutCosTheta", 20, 0., 1. );
		histos1D_[ "massAsymmetry_cutCosTheta" ]->Sumw2();
		histos1D_[ "massAve_cutCosTheta" ] = fs_->make< TH1D >( "massAve_cutCosTheta", "massAve_cutCosTheta", 60, 0., 600. );
		histos1D_[ "massAve_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1CosThetaStar_cutCosTheta" ] = fs_->make< TH1D >( "jet1CosThetaStar_cutCosTheta", "jet1CosThetaStar_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet1CosThetaStar_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2CosThetaStar_cutCosTheta" ] = fs_->make< TH1D >( "jet2CosThetaStar_cutCosTheta", "jet2CosThetaStar_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2CosThetaStar_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Tau1_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau1_cutCosTheta", "jet1Tau1_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet1Tau1_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Tau2_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau2_cutCosTheta", "jet1Tau2_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet1Tau2_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Tau3_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau3_cutCosTheta", "jet1Tau3_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet1Tau3_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Tau21_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau21_cutCosTheta", "jet1Tau21_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet1Tau21_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Tau31_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau31_cutCosTheta", "jet1Tau31_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet1Tau31_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1Tau32_cutCosTheta" ] = fs_->make< TH1D >( "jet1Tau32_cutCosTheta", "jet1Tau32_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet1Tau32_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Tau1_cutCosTheta" ] = fs_->make< TH1D >( "jet2Tau1_cutCosTheta", "jet2Tau1_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2Tau1_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Tau2_cutCosTheta" ] = fs_->make< TH1D >( "jet2Tau2_cutCosTheta", "jet2Tau2_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2Tau2_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Tau3_cutCosTheta" ] = fs_->make< TH1D >( "jet2Tau3_cutCosTheta", "jet2Tau3_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2Tau3_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Tau21_cutCosTheta" ] = fs_->make< TH1D >( "jet2Tau21_cutCosTheta", "jet2Tau21_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2Tau21_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Tau31_cutCosTheta" ] = fs_->make< TH1D >( "jet2Tau31_cutCosTheta", "jet2Tau31_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2Tau31_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Tau32_cutCosTheta" ] = fs_->make< TH1D >( "jet2Tau32_cutCosTheta", "jet2Tau32_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2Tau32_cutCosTheta" ]->Sumw2();
		histos1D_[ "deltaEtaDijet_cutCosTheta" ] = fs_->make< TH1D >( "deltaEtaDijet_cutCosTheta", "deltaEtaDijet_cutCosTheta", 50, 0., 5. );
		histos1D_[ "deltaEtaDijet_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1SubjetPtRatio_cutCosTheta" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutCosTheta", "jet1SubjetPtRatio_cutCosTheta", 20, 0, 1.);
		histos1D_[ "jet1SubjetPtRatio_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2SubjetPtRatio_cutCosTheta" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutCosTheta", "jet2SubjetPtRatio_cutCosTheta", 20, 0., 1. );
		histos1D_[ "jet2SubjetPtRatio_cutCosTheta" ]->Sumw2();
		histos1D_[ "subjetPtRatio_cutCosTheta" ] = fs_->make< TH1D >( "subjetPtRatio_cutCosTheta", "subjetPtRatio_cutCosTheta", 20, 0., 1. );
		histos1D_[ "subjetPtRatio_cutCosTheta" ]->Sumw2();

		histos2D_[ "jetTrimmedMassHT_cutCosTheta" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutCosTheta", "jetTrimmedMassHT_cutCosTheta", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAveHT_cutCosTheta" ] = fs_->make< TH2D >( "massAveHT_cutCosTheta", "massAveHT_cutCosTheta", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "massAveHT_cutCosTheta" ]->Sumw2();

		histos2D_[ "massAvevsJet1Mass_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutCosTheta", "massAvevsJet1Mass_cutCosTheta", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet1Mass_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Mass_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutCosTheta", "massAvevsJet2Mass_cutCosTheta", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet2Mass_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsMassAsym_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsMassAsym_cutCosTheta", "massAvevsMassAsym_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsMassAsym_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsDEta_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsDEta_cutCosTheta", "massAvevsDEta_cutCosTheta", 60, 0., 600., 50, 0., 5. );
		histos2D_[ "massAvevsDEta_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet1CosThetaStar_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet1CosThetaStar_cutCosTheta", "massAvevsJet1CosThetaStar_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1CosThetaStar_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet2CosThetaStar_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet2CosThetaStar_cutCosTheta", "massAvevsJet2CosThetaStar_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2CosThetaStar_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau21_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet1Tau21_cutCosTheta", "massAvevsJet1Tau21_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau21_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau31_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet1Tau31_cutCosTheta", "massAvevsJet1Tau31_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau31_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau32_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet1Tau32_cutCosTheta", "massAvevsJet1Tau32_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau32_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau21_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet2Tau21_cutCosTheta", "massAvevsJet2Tau21_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau21_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau31_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet2Tau31_cutCosTheta", "massAvevsJet2Tau31_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau31_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau32_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet2Tau32_cutCosTheta", "massAvevsJet2Tau32_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau32_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet1SubjetPtRatio_cutCosTheta", "massAvevsJet1SubjetPtRatio_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutCosTheta" ]->Sumw2();
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutCosTheta" ] = fs_->make< TH2D >( "massAvevsJet2SubjetPtRatio_cutCosTheta", "massAvevsJet2SubjetPtRatio_cutCosTheta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutCosTheta" ]->Sumw2();
		histos2D_[ "jet1vs2Mass_cutCosTheta" ] = fs_->make< TH2D >( "jet1vs2Mass_cutCosTheta", "jet1vs2Mass_cutCosTheta", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "jet1vs2Mass_cutCosTheta" ]->Sumw2();
		histos2D_[ "dijetCorr_cutCosTheta" ] = fs_->make< TH2D >( "dijetCorr_cutCosTheta", "dijetCorr_cutCosTheta", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutCosTheta" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutCosTheta" ] = fs_->make< TH2D >( "dijetCorrPhi_cutCosTheta", "dijetCorrPhi_cutCosTheta", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutCosTheta" ]->Sumw2();


		histos1D_[ "HT_cutMassAsym" ] = fs_->make< TH1D >( "HT_cutMassAsym", "HT_cutMassAsym", 500, 0., 5000. );
		histos1D_[ "HT_cutMassAsym" ]->Sumw2();
		histos1D_[ "NPV_cutMassAsym" ] = fs_->make< TH1D >( "NPV_cutMassAsym", "NPV_cutMassAsym", 80, 0., 80. );
		histos1D_[ "NPV_cutMassAsym" ]->Sumw2();
		histos1D_[ "jetNum_cutMassAsym" ] = fs_->make< TH1D >( "jetNum_cutMassAsym", "jetNum_cutMassAsym", 10, 0., 10. );
		histos1D_[ "jetNum_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Pt_cutMassAsym" ] = fs_->make< TH1D >( "jet1Pt_cutMassAsym", "jet1Pt_cutMassAsym", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Eta_cutMassAsym" ] = fs_->make< TH1D >( "jet1Eta_cutMassAsym", "jet1Eta_cutMassAsym", 100, -5., 5. );
		histos1D_[ "jet1Eta_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Mass_cutMassAsym" ] = fs_->make< TH1D >( "jet1Mass_cutMassAsym", "jet1Mass_cutMassAsym", 60, 0., 600. );
		histos1D_[ "jet1Mass_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Pt_cutMassAsym" ] = fs_->make< TH1D >( "jet2Pt_cutMassAsym", "jet2Pt_cutMassAsym", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Eta_cutMassAsym" ] = fs_->make< TH1D >( "jet2Eta_cutMassAsym", "jet2Eta_cutMassAsym", 100, -5., 5. );
		histos1D_[ "jet2Eta_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Mass_cutMassAsym" ] = fs_->make< TH1D >( "jet2Mass_cutMassAsym", "jet2Mass_cutMassAsym", 60, 0., 600. );
		histos1D_[ "jet2Mass_cutMassAsym" ]->Sumw2();

		histos1D_[ "massAsymmetry_cutMassAsym" ] = fs_->make< TH1D >( "massAsymmetry_cutMassAsym", "massAsymmetry_cutMassAsym", 20, 0., 1. );
		histos1D_[ "massAsymmetry_cutMassAsym" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym" ] = fs_->make< TH1D >( "massAve_cutMassAsym", "massAve_cutMassAsym", 60, 0., 600. );
		histos1D_[ "massAve_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1CosThetaStar_cutMassAsym" ] = fs_->make< TH1D >( "jet1CosThetaStar_cutMassAsym", "jet1CosThetaStar_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet1CosThetaStar_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2CosThetaStar_cutMassAsym" ] = fs_->make< TH1D >( "jet2CosThetaStar_cutMassAsym", "jet2CosThetaStar_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2CosThetaStar_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Tau1_cutMassAsym" ] = fs_->make< TH1D >( "jet1Tau1_cutMassAsym", "jet1Tau1_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet1Tau1_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Tau2_cutMassAsym" ] = fs_->make< TH1D >( "jet1Tau2_cutMassAsym", "jet1Tau2_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet1Tau2_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Tau3_cutMassAsym" ] = fs_->make< TH1D >( "jet1Tau3_cutMassAsym", "jet1Tau3_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet1Tau3_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Tau21_cutMassAsym" ] = fs_->make< TH1D >( "jet1Tau21_cutMassAsym", "jet1Tau21_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet1Tau21_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Tau31_cutMassAsym" ] = fs_->make< TH1D >( "jet1Tau31_cutMassAsym", "jet1Tau31_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet1Tau31_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1Tau32_cutMassAsym" ] = fs_->make< TH1D >( "jet1Tau32_cutMassAsym", "jet1Tau32_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet1Tau32_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Tau1_cutMassAsym" ] = fs_->make< TH1D >( "jet2Tau1_cutMassAsym", "jet2Tau1_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2Tau1_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Tau2_cutMassAsym" ] = fs_->make< TH1D >( "jet2Tau2_cutMassAsym", "jet2Tau2_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2Tau2_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Tau3_cutMassAsym" ] = fs_->make< TH1D >( "jet2Tau3_cutMassAsym", "jet2Tau3_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2Tau3_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Tau21_cutMassAsym" ] = fs_->make< TH1D >( "jet2Tau21_cutMassAsym", "jet2Tau21_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2Tau21_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Tau31_cutMassAsym" ] = fs_->make< TH1D >( "jet2Tau31_cutMassAsym", "jet2Tau31_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2Tau31_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2Tau32_cutMassAsym" ] = fs_->make< TH1D >( "jet2Tau32_cutMassAsym", "jet2Tau32_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2Tau32_cutMassAsym" ]->Sumw2();
		histos1D_[ "deltaEtaDijet_cutMassAsym" ] = fs_->make< TH1D >( "deltaEtaDijet_cutMassAsym", "deltaEtaDijet_cutMassAsym", 50, 0., 5. );
		histos1D_[ "deltaEtaDijet_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet1SubjetPtRatio_cutMassAsym" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutMassAsym", "jet1SubjetPtRatio_cutMassAsym", 20, 0, 1.);
		histos1D_[ "jet1SubjetPtRatio_cutMassAsym" ]->Sumw2();
		histos1D_[ "jet2SubjetPtRatio_cutMassAsym" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutMassAsym", "jet2SubjetPtRatio_cutMassAsym", 20, 0., 1. );
		histos1D_[ "jet2SubjetPtRatio_cutMassAsym" ]->Sumw2();
		histos1D_[ "subjetPtRatio_cutMassAsym" ] = fs_->make< TH1D >( "subjetPtRatio_cutMassAsym", "subjetPtRatio_cutMassAsym", 20, 0., 1. );
		histos1D_[ "subjetPtRatio_cutMassAsym" ]->Sumw2();

		histos2D_[ "jetTrimmedMassHT_cutMassAsym" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutMassAsym", "jetTrimmedMassHT_cutMassAsym", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAveHT_cutMassAsym" ] = fs_->make< TH2D >( "massAveHT_cutMassAsym", "massAveHT_cutMassAsym", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "massAveHT_cutMassAsym" ]->Sumw2();

		histos2D_[ "massAvevsJet1Mass_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutMassAsym", "massAvevsJet1Mass_cutMassAsym", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet1Mass_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet2Mass_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutMassAsym", "massAvevsJet2Mass_cutMassAsym", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet2Mass_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsMassAsym_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsMassAsym_cutMassAsym", "massAvevsMassAsym_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsMassAsym_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsDEta_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsDEta_cutMassAsym", "massAvevsDEta_cutMassAsym", 60, 0., 600., 50, 0., 5. );
		histos2D_[ "massAvevsDEta_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet1CosThetaStar_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet1CosThetaStar_cutMassAsym", "massAvevsJet1CosThetaStar_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1CosThetaStar_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet2CosThetaStar_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet2CosThetaStar_cutMassAsym", "massAvevsJet2CosThetaStar_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2CosThetaStar_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau21_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet1Tau21_cutMassAsym", "massAvevsJet1Tau21_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau21_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau31_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet1Tau31_cutMassAsym", "massAvevsJet1Tau31_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau31_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau32_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet1Tau32_cutMassAsym", "massAvevsJet1Tau32_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau32_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau21_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet2Tau21_cutMassAsym", "massAvevsJet2Tau21_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau21_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau31_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet2Tau31_cutMassAsym", "massAvevsJet2Tau31_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau31_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau32_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet2Tau32_cutMassAsym", "massAvevsJet2Tau32_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau32_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet1SubjetPtRatio_cutMassAsym", "massAvevsJet1SubjetPtRatio_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutMassAsym" ]->Sumw2();
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutMassAsym" ] = fs_->make< TH2D >( "massAvevsJet2SubjetPtRatio_cutMassAsym", "massAvevsJet2SubjetPtRatio_cutMassAsym", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutMassAsym" ]->Sumw2();
		histos2D_[ "jet1vs2Mass_cutMassAsym" ] = fs_->make< TH2D >( "jet1vs2Mass_cutMassAsym", "jet1vs2Mass_cutMassAsym", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "jet1vs2Mass_cutMassAsym" ]->Sumw2();
		histos2D_[ "dijetCorr_cutMassAsym" ] = fs_->make< TH2D >( "dijetCorr_cutMassAsym", "dijetCorr_cutMassAsym", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutMassAsym" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutMassAsym" ] = fs_->make< TH2D >( "dijetCorrPhi_cutMassAsym", "dijetCorrPhi_cutMassAsym", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutMassAsym" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym_A" ] = fs_->make< TH1D >( "massAve_cutMassAsym_A", "massAve_cutMassAsym_A", 60, 0., 600. );
		histos1D_[ "massAve_cutMassAsym_A" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym_B" ] = fs_->make< TH1D >( "massAve_cutMassAsym_B", "massAve_cutMassAsym_B", 60, 0., 600. );
		histos1D_[ "massAve_cutMassAsym_B" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym_C" ] = fs_->make< TH1D >( "massAve_cutMassAsym_C", "massAve_cutMassAsym_C", 60, 0., 600. );
		histos1D_[ "massAve_cutMassAsym_C" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym_D" ] = fs_->make< TH1D >( "massAve_cutMassAsym_D", "massAve_cutMassAsym_D", 60, 0., 600. );
		histos1D_[ "massAve_cutMassAsym_D" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym_Bkg" ] = fs_->make< TH1D >( "massAve_cutMassAsym_Bkg", "massAve_cutMassAsym_Bkg", 60, 0., 600. );
		histos1D_[ "massAve_cutMassAsym_BD" ] = fs_->make< TH1D >( "massAve_cutMassAsym_BD", "massAve_cutMassAsym_BD", 60, 0., 600. );



		histos1D_[ "HT_cutDEta" ] = fs_->make< TH1D >( "HT_cutDEta", "HT_cutDEta", 500, 0., 5000. );
		histos1D_[ "HT_cutDEta" ]->Sumw2();
		histos1D_[ "NPV_cutDEta" ] = fs_->make< TH1D >( "NPV_cutDEta", "NPV_cutDEta", 80, 0., 80. );
		histos1D_[ "NPV_cutDEta" ]->Sumw2();
		histos1D_[ "jetNum_cutDEta" ] = fs_->make< TH1D >( "jetNum_cutDEta", "jetNum_cutDEta", 10, 0., 10. );
		histos1D_[ "jetNum_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Pt_cutDEta" ] = fs_->make< TH1D >( "jet1Pt_cutDEta", "jet1Pt_cutDEta", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Eta_cutDEta" ] = fs_->make< TH1D >( "jet1Eta_cutDEta", "jet1Eta_cutDEta", 100, -5., 5. );
		histos1D_[ "jet1Eta_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Mass_cutDEta" ] = fs_->make< TH1D >( "jet1Mass_cutDEta", "jet1Mass_cutDEta", 60, 0., 600. );
		histos1D_[ "jet1Mass_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Pt_cutDEta" ] = fs_->make< TH1D >( "jet2Pt_cutDEta", "jet2Pt_cutDEta", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Eta_cutDEta" ] = fs_->make< TH1D >( "jet2Eta_cutDEta", "jet2Eta_cutDEta", 100, -5., 5. );
		histos1D_[ "jet2Eta_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Mass_cutDEta" ] = fs_->make< TH1D >( "jet2Mass_cutDEta", "jet2Mass_cutDEta", 60, 0., 600. );
		histos1D_[ "jet2Mass_cutDEta" ]->Sumw2();

		histos1D_[ "massAsymmetry_cutDEta" ] = fs_->make< TH1D >( "massAsymmetry_cutDEta", "massAsymmetry_cutDEta", 20, 0., 1. );
		histos1D_[ "massAsymmetry_cutDEta" ]->Sumw2();
		histos1D_[ "massAve_cutDEta" ] = fs_->make< TH1D >( "massAve_cutDEta", "massAve_cutDEta", 60, 0., 600. );
		histos1D_[ "massAve_cutDEta" ]->Sumw2();
		histos1D_[ "massAve_cutDEta_1GeVBin" ] = fs_->make< TH1D >( "massAve_cutDEta_1GeVBin", "massAve_cutDEta_1GeVBin", 600, 0., 600. );
		histos1D_[ "massAve_cutDEta_1GeVBin" ]->Sumw2();
		histos1D_[ "jet1CosThetaStar_cutDEta" ] = fs_->make< TH1D >( "jet1CosThetaStar_cutDEta", "jet1CosThetaStar_cutDEta", 20, 0., 1. );
		histos1D_[ "jet1CosThetaStar_cutDEta" ]->Sumw2();
		histos1D_[ "jet2CosThetaStar_cutDEta" ] = fs_->make< TH1D >( "jet2CosThetaStar_cutDEta", "jet2CosThetaStar_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2CosThetaStar_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Tau1_cutDEta" ] = fs_->make< TH1D >( "jet1Tau1_cutDEta", "jet1Tau1_cutDEta", 20, 0., 1. );
		histos1D_[ "jet1Tau1_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Tau2_cutDEta" ] = fs_->make< TH1D >( "jet1Tau2_cutDEta", "jet1Tau2_cutDEta", 20, 0., 1. );
		histos1D_[ "jet1Tau2_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Tau3_cutDEta" ] = fs_->make< TH1D >( "jet1Tau3_cutDEta", "jet1Tau3_cutDEta", 20, 0., 1. );
		histos1D_[ "jet1Tau3_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Tau21_cutDEta" ] = fs_->make< TH1D >( "jet1Tau21_cutDEta", "jet1Tau21_cutDEta", 20, 0., 1. );
		histos1D_[ "jet1Tau21_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Tau31_cutDEta" ] = fs_->make< TH1D >( "jet1Tau31_cutDEta", "jet1Tau31_cutDEta", 20, 0., 1. );
		histos1D_[ "jet1Tau31_cutDEta" ]->Sumw2();
		histos1D_[ "jet1Tau32_cutDEta" ] = fs_->make< TH1D >( "jet1Tau32_cutDEta", "jet1Tau32_cutDEta", 20, 0., 1. );
		histos1D_[ "jet1Tau32_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Tau1_cutDEta" ] = fs_->make< TH1D >( "jet2Tau1_cutDEta", "jet2Tau1_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2Tau1_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Tau2_cutDEta" ] = fs_->make< TH1D >( "jet2Tau2_cutDEta", "jet2Tau2_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2Tau2_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Tau3_cutDEta" ] = fs_->make< TH1D >( "jet2Tau3_cutDEta", "jet2Tau3_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2Tau3_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Tau21_cutDEta" ] = fs_->make< TH1D >( "jet2Tau21_cutDEta", "jet2Tau21_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2Tau21_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Tau31_cutDEta" ] = fs_->make< TH1D >( "jet2Tau31_cutDEta", "jet2Tau31_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2Tau31_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Tau32_cutDEta" ] = fs_->make< TH1D >( "jet2Tau32_cutDEta", "jet2Tau32_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2Tau32_cutDEta" ]->Sumw2();
		histos1D_[ "deltaEtaDijet_cutDEta" ] = fs_->make< TH1D >( "deltaEtaDijet_cutDEta", "deltaEtaDijet_cutDEta", 50, 0., 5. );
		histos1D_[ "deltaEtaDijet_cutDEta" ]->Sumw2();
		histos1D_[ "jet1SubjetPtRatio_cutDEta" ] = fs_->make< TH1D >( "jet1SubjetPtRatio_cutDEta", "jet1SubjetPtRatio_cutDEta", 20, 0, 1.);
		histos1D_[ "jet1SubjetPtRatio_cutDEta" ]->Sumw2();
		histos1D_[ "jet2SubjetPtRatio_cutDEta" ] = fs_->make< TH1D >( "jet2SubjetPtRatio_cutDEta", "jet2SubjetPtRatio_cutDEta", 20, 0., 1. );
		histos1D_[ "jet2SubjetPtRatio_cutDEta" ]->Sumw2();
		histos1D_[ "subjetPtRatio_cutDEta" ] = fs_->make< TH1D >( "subjetPtRatio_cutDEta", "subjetPtRatio_cutDEta", 20, 0., 1. );
		histos1D_[ "subjetPtRatio_cutDEta" ]->Sumw2();

		histos2D_[ "jetTrimmedMassHT_cutDEta" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutDEta", "jetTrimmedMassHT_cutDEta", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "jetTrimmedMassHT_cutDEta" ]->Sumw2();
		histos2D_[ "massAveHT_cutDEta" ] = fs_->make< TH2D >( "massAveHT_cutDEta", "massAveHT_cutDEta", 30, 0., 300., 500, 0., 5000. );
		histos2D_[ "massAveHT_cutDEta" ]->Sumw2();

		histos2D_[ "massAvevsJet1Mass_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet1Mass_cutDEta", "massAvevsJet1Mass_cutDEta", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet1Mass_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Mass_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet2Mass_cutDEta", "massAvevsJet2Mass_cutDEta", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "massAvevsJet2Mass_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsMassAsym_cutDEta" ] = fs_->make< TH2D >( "massAvevsMassAsym_cutDEta", "massAvevsMassAsym_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsMassAsym_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsDEta_cutDEta" ] = fs_->make< TH2D >( "massAvevsDEta_cutDEta", "massAvevsDEta_cutDEta", 60, 0., 600., 50, 0., 5. );
		histos2D_[ "massAvevsDEta_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet1CosThetaStar_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet1CosThetaStar_cutDEta", "massAvevsJet1CosThetaStar_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1CosThetaStar_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet2CosThetaStar_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet2CosThetaStar_cutDEta", "massAvevsJet2CosThetaStar_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2CosThetaStar_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau21_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet1Tau21_cutDEta", "massAvevsJet1Tau21_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau21_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau31_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet1Tau31_cutDEta", "massAvevsJet1Tau31_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau31_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet1Tau32_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet1Tau32_cutDEta", "massAvevsJet1Tau32_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1Tau32_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau21_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet2Tau21_cutDEta", "massAvevsJet2Tau21_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau21_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau31_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet2Tau31_cutDEta", "massAvevsJet2Tau31_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau31_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet2Tau32_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet2Tau32_cutDEta", "massAvevsJet2Tau32_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2Tau32_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet1SubjetPtRatio_cutDEta", "massAvevsJet1SubjetPtRatio_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet1SubjetPtRatio_cutDEta" ]->Sumw2();
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutDEta" ] = fs_->make< TH2D >( "massAvevsJet2SubjetPtRatio_cutDEta", "massAvevsJet2SubjetPtRatio_cutDEta", 60, 0., 600., 20, 0., 1. );
		histos2D_[ "massAvevsJet2SubjetPtRatio_cutDEta" ]->Sumw2();
		histos2D_[ "jet1vs2Mass_cutDEta" ] = fs_->make< TH2D >( "jet1vs2Mass_cutDEta", "jet1vs2Mass_cutDEta", 60, 0., 600., 30, 0., 300. );
		histos2D_[ "jet1vs2Mass_cutDEta" ]->Sumw2();
		histos2D_[ "dijetCorr_cutDEta" ] = fs_->make< TH2D >( "dijetCorr_cutDEta", "dijetCorr_cutDEta", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorr_cutDEta" ]->Sumw2();
		histos2D_[ "dijetCorrPhi_cutDEta" ] = fs_->make< TH2D >( "dijetCorrPhi_cutDEta", "dijetCorrPhi_cutDEta", 56, -3.5, 3.5, 56, -3.5, 3.5 );
		histos2D_[ "dijetCorrPhi_cutDEta" ]->Sumw2();

	}

	cutLabels.push_back("Processed");
	cutLabels.push_back("Trigger");
	cutLabels.push_back("Dijet");
	cutLabels.push_back("HT");
	cutLabels.push_back("Tau21");
	cutLabels.push_back("CosTheta");
	cutLabels.push_back("Asymmetry");
	cutLabels.push_back("DEta");
	cutLabels.push_back("btag");
	histos1D_[ "hcutflow" ] = fs_->make< TH1D >("cutflow","cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflow" ]->Sumw2();
	for( const string &ivec : cutLabels ) cutmap[ ivec ] = 0;

}

// ------------ method called once each job just after ending the event loop  ------------
void RUNBoostedAnalysis::endJob() {

	int ibin = 1;
	for( const string &ivec : cutLabels ) {
		histos1D_["hcutflow"]->SetBinContent( ibin, cutmap[ ivec ] );
		histos1D_["hcutflow"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		ibin++;
	}

	if ( !mkTree ) {
		histos1D_[ "massAve_cutMassAsym_BD" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym_BD" ]->Multiply( histos1D_[ "massAve_cutMassAsym_B" ],  histos1D_[ "massAve_cutMassAsym_D" ], 1, 1, "" );
		histos1D_[ "massAve_cutMassAsym_Bkg" ]->Sumw2();
		histos1D_[ "massAve_cutMassAsym_Bkg" ]->Divide( histos1D_[ "massAve_cutMassAsym_BD" ],  histos1D_[ "massAve_cutMassAsym_C" ], 1, 1, "" );
	}

}

void RUNBoostedAnalysis::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutAsymvalue", 1);
	desc.add<double>("cutCosThetavalue", 1);
	desc.add<double>("cutSubjetPtRatiovalue", 1);
	desc.add<double>("cutTau31value", 1);
	desc.add<double>("cutTau21value", 1);
	desc.add<double>("cutDEtavalue", 1);
	desc.add<double>("cutBtagvalue", 1);
	desc.add<double>("scale", 1);
	desc.add<bool>("bjSample", false);
	desc.add<bool>("mkTree", false);
	desc.add<bool>("isData", false);
	desc.add<string>("dataPUFile", "supportFiles/PileupData2015D_JSON_10-23-2015.root");
	desc.add<string>("jecVersion", "supportFiles/Summer15_25nsV6");
	desc.add<string>("systematics", "None");
	vector<string> HLTPass;
	HLTPass.push_back("HLT_AK8PFHT700_TrimR0p1PT0p03Mass50");
	desc.add<vector<string>>("triggerPass",	HLTPass);

	desc.add<InputTag>("Lumi", 	InputTag("eventInfo:evtInfoLumiBlock"));
	desc.add<InputTag>("Run", 	InputTag("eventInfo:evtInfoRunNumber"));
	desc.add<InputTag>("Event", 	InputTag("eventInfo:evtInfoEventNumber"));
	desc.add<InputTag>("bunchCross", 	InputTag("eventUserData:puBX"));
	desc.add<InputTag>("rho", 	InputTag("vertexInfo:rho"));
	desc.add<InputTag>("puNumInt", 	InputTag("eventUserData:puNInt"));
	desc.add<InputTag>("trueNInt", 	InputTag("eventUserData:puNtrueInt"));
	desc.add<InputTag>("NPV", 	InputTag("eventUserData:npv"));
	desc.add<InputTag>("jetAK4Pt", 	InputTag("jetsAK4:jetAK4Pt"));
	desc.add<InputTag>("jetAK4Eta", 	InputTag("jetsAK4:jetAK4Eta"));
	desc.add<InputTag>("jetAK4Phi", 	InputTag("jetsAK4:jetAK4Phi"));
	desc.add<InputTag>("jetAK4E", 	InputTag("jetsAK4:jetAK4E"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK8:jetAK8Pt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK8:jetAK8Eta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK8:jetAK8Phi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK8:jetAK8E"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK8:jetAK8Mass"));
	desc.add<InputTag>("jetTrimmedMass", 	InputTag("jetsAK8:jetAK8trimmedMass"));
	desc.add<InputTag>("jetTau1", 	InputTag("jetsAK8:jetAK8tau1"));
	desc.add<InputTag>("jetTau2", 	InputTag("jetsAK8:jetAK8tau2"));
	desc.add<InputTag>("jetTau3", 	InputTag("jetsAK8:jetAK8tau3"));
	desc.add<InputTag>("jetNSubjets", 	InputTag("jetsAK8:jetAK8nSubjets"));
	desc.add<InputTag>("jetSubjetIndex0", 	InputTag("jetsAK8:jetAK8vSubjetIndex0"));
	desc.add<InputTag>("jetSubjetIndex1", 	InputTag("jetsAK8:jetAK8vSubjetIndex1"));
	desc.add<InputTag>("jetSubjetIndex2", 	InputTag("jetsAK8:jetAK8vSubjetIndex2"));
	desc.add<InputTag>("jetSubjetIndex3", 	InputTag("jetsAK8:jetAK8vSubjetIndex3"));
	desc.add<InputTag>("jetKeys", 	InputTag("jetKeysAK8"));
	desc.add<InputTag>("jetCSV", 	InputTag("jetsAK8:jetAK8CSV"));
	desc.add<InputTag>("jetCSVV1", 	InputTag("jetsAK8:jetAK8CSVV1"));
	desc.add<InputTag>("jetArea", 	InputTag("jetsAK8:jetAK8jetArea"));
	desc.add<InputTag>("jetGenPt", 	InputTag("jetsAK8:jetAK8GenJetPt"));
	desc.add<InputTag>("jetGenEta", 	InputTag("jetsAK8:jetAK8GenJetEta"));
	desc.add<InputTag>("jetGenPhi", 	InputTag("jetsAK8:jetAK8GenJetPhi"));
	desc.add<InputTag>("jetGenE", 	InputTag("jetsAK8:jetAK8GenJetE"));
	desc.add<InputTag>("metPt", 	InputTag("met:metPt"));
	// JetID
	desc.add<InputTag>("jecFactor", 		InputTag("jetsAK8:jetAK8jecFactor0"));
	desc.add<InputTag>("neutralHadronEnergy", 	InputTag("jetsAK8:jetAK8neutralHadronEnergy"));
	desc.add<InputTag>("neutralEmEnergy", 		InputTag("jetsAK8:jetAK8neutralEmEnergy"));
	desc.add<InputTag>("chargedEmEnergy", 		InputTag("jetsAK8:jetAK8chargedEmEnergy"));
	desc.add<InputTag>("muonEnergy", 		InputTag("jetsAK8:jetAK8MuonEnergy"));
	desc.add<InputTag>("chargedHadronEnergy", 	InputTag("jetsAK8:jetAK8chargedHadronEnergy"));
	desc.add<InputTag>("chargedHadronMultiplicity",	InputTag("jetsAK8:jetAK8ChargedHadronMultiplicity"));
	desc.add<InputTag>("neutralHadronMultiplicity",	InputTag("jetsAK8:jetAK8neutralHadronMultiplicity"));
	desc.add<InputTag>("chargedMultiplicity", 	InputTag("jetsAK8:jetAK8chargedMultiplicity"));
	// Trigger
	desc.add<InputTag>("triggerBit",		InputTag("TriggerUserData:triggerBitTree"));
	desc.add<InputTag>("triggerName",		InputTag("TriggerUserData:triggerNameTree"));
	// Subjets
	desc.add<InputTag>("subjetPt", 	InputTag("subjetsAK8:subjetAK8Pt"));
	desc.add<InputTag>("subjetEta", 	InputTag("subjetsAK8:subjetAK8Eta"));
	desc.add<InputTag>("subjetPhi", 	InputTag("subjetsAK8:subjetAK8Phi"));
	desc.add<InputTag>("subjetE", 	InputTag("subjetsAK8:subjetAK8E"));
	desc.add<InputTag>("subjetMass", 	InputTag("subjetsAK8:subjetAK8Mass"));
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNBoostedAnalysis);
