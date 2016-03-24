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

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"

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
      virtual void beginRun(const Run&, const EventSetup&) override;

      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      PUReweighter PUWeight_;
      int lhaPdfId ;
      
      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      bool bjSample;
      bool isData;
      string dataPUFile;
      string jecVersion;
      TString systematics;

      vector<string> triggerPass;
      vector<JetCorrectorParameters> jetPar;
      FactorizedJetCorrector * jetJECAK8;
      vector<JetCorrectorParameters> massPar;
      FactorizedJetCorrector * massJECAK8;
      JetCorrectionUncertainty *jetCorrUnc;

      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;
      float AK4HT = 0, HT = 0, trimmedMass = -999, puWeight = -999, genWeight = -999, MET = -999,
	    jet1Pt = -999, jet1Eta = -999, jet1Phi = -999, jet1E = -999, jet1btagCSV = -9999,
	    jet2Pt = -999, jet2Eta = -999, jet2Phi = -999, jet2E = -999, jet2btagCSV = -9999,
	    subjet11Pt = -999, subjet11Eta = -999, subjet11Phi = -999, subjet11E = -999, 
	    subjet12Pt = -999, subjet12Eta = -999, subjet12Phi = -999, subjet12E = -999, 
	    subjet21Pt = -999, subjet21Eta = -999, subjet21Phi = -999, subjet21E = -999, 
	    subjet22Pt = -999, subjet22Eta = -999, subjet22Phi = -999, subjet22E = -999,
	    massAve = -9999, massAsym = -9999, 
	    trimmedMassAve = -9999, trimmedMassAsym = -9999, 
	    prunedMassAve = -9999, prunedMassAsym = -9999, 
	    filteredMassAve = -9999, filteredMassAsym = -9999, 
	    softDropMassAve = -9999, softDropMassAsym = -9999, 
	    jet1CosThetaStar = -9999, jet2CosThetaStar = -9999, deltaEtaDijet = -9999,
	    jet1Tau21 = -9999, jet1Tau31 = -9999, jet1Tau32 = -9999,
	    jet2Tau21 = -9999, jet2Tau31 = -9999, jet2Tau32 = -9999,
	    jet1SubjetPtRatio = -999, jet2SubjetPtRatio = -999, jet1SubjetMass21Ratio = -999, jet1Subjet112MassRatio = -999, jet1Subjet1JetMassRatio = - 999, jet1Subjet212MassRatio = - 999, jet1Subjet2JetMassRatio = - 999,
	    jet2SubjetMass21Ratio = -999, jet2Subjet112MassRatio = -999, jet2Subjet1JetMassRatio = - 999, jet2Subjet212MassRatio = - 999, jet2Subjet2JetMassRatio = - 999, 
	    cosPhi13412 = -9999, cosPhi31234 = -9999,
	    dalitzY1 = -9999, dalitzY2 = -9999, dalitzY3 = -9999, dalitzY4 = -9999, dalitzY5 = -9999, dalitzY6 = -9999, 
	    dalitzX1 = -9999, dalitzX2 = -9999, dalitzX3 = -9999, dalitzX4 = -9999, dalitzX5 = -9999, dalitzX6 = -9999;
      vector<float> scaleWeights, pdfWeights, alphaWeights;

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
      EDGetTokenT<vector<float>> jetPrunedMass_;
      EDGetTokenT<vector<float>> jetFilteredMass_;
      EDGetTokenT<vector<float>> jetSoftDropMass_;
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
      EDGetTokenT<GenEventInfoProduct> generator_;
      EDGetTokenT<LHEEventProduct> extLHEProducer_;

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
	jetPrunedMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPrunedMass"))),
	jetFilteredMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetFilteredMass"))),
	jetSoftDropMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSoftDropMass"))),
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
	generator_(consumes<GenEventInfoProduct>(iConfig.getParameter<InputTag>("generator"))),
	extLHEProducer_(consumes<LHEEventProduct>(iConfig.getParameter<InputTag>("extLHEProducer"))),
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
	consumes<LHERunInfoProduct,edm::InRun> (edm::InputTag("externalLHEProducer"));
	bjSample 	= iConfig.getParameter<bool>("bjSample");
	isData 		= iConfig.getParameter<bool>("isData");
	dataPUFile 	= iConfig.getParameter<string>("dataPUFile");
	jecVersion 	= iConfig.getParameter<string>("jecVersion");
	systematics 	= iConfig.getParameter<string>("systematics");
	triggerPass 	= iConfig.getParameter<vector<string>>("triggerPass");

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
	jetCorrUnc  = new JetCorrectionUncertainty( jecUncParam );
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

	Handle<vector<float> > jetPrunedMass;
	iEvent.getByToken(jetPrunedMass_, jetPrunedMass);

	Handle<vector<float> > jetFilteredMass;
	iEvent.getByToken(jetFilteredMass_, jetFilteredMass);

	Handle<vector<float> > jetSoftDropMass;
	iEvent.getByToken(jetSoftDropMass_, jetSoftDropMass);

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

	if ( !isData ) {

		// all this section is based on https://github.com/jkarancs/B2GTTrees/blob/master/plugins/B2GEdmExtraVarProducer.cc#L215-L281
		/////////// GEN weight
		Handle<GenEventInfoProduct> genEvtInfo; 
		iEvent.getByToken( generator_, genEvtInfo );
		genWeight = genEvtInfo->weight();	
		//vector<double> evtWeights = genEvtInfo->weights();

		/////////// LHE weight
		Handle<LHEEventProduct> lheEvtInfo;
		iEvent.getByToken( extLHEProducer_, lheEvtInfo );
		// This function will return all the weights from the lheEvtInfo (scaleWeights, pdfWeights, alphaWeights)
		//getWeights( lheEvtInfo, lhaPdfId, scaleWeights, pdfWeights, alphaWeights );
		////////////////////////////////////////////////////
	}

	////////// Check trigger fired
	bool ORTriggers = checkORListOfTriggerBits( triggerName, triggerBit, triggerPass );
	////////////////////////////////////////////////////
	
	////////// PU Reweight
	if ( isData ) puWeight = 1;
	else puWeight = PUWeight_.getPUWeight( *trueNInt, *bunchCross );
	histos1D_[ "PUWeight" ]->Fill( puWeight );
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
	cutmap["Processed"] += 1;
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

		if( corrJet.Pt() > 150 && idL ) { 

			HT += corrJet.Pt();
			tmpTriggerMass.push_back( (*jetTrimmedMass)[i] );
			++numberJets;

			double massJEC = corrections( rawJet, (*jetArea)[i], (*rho)[i] ,*NPV, massJECAK8); 
			double corrMass = (*jetMass)[i] * ( massJEC + sysJEC  );
			double corrTrimmedMass = (*jetTrimmedMass)[i] * ( massJEC + sysJEC  );
			double corrPrunedMass = (*jetPrunedMass)[i] * ( massJEC + sysJEC  );
			double corrSoftDropMass = (*jetSoftDropMass)[i] * ( massJEC + sysJEC  );
			double corrFilteredMass = (*jetFilteredMass)[i] * ( massJEC + sysJEC  );

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
			histos1D_[ "oldJetPt" ]->Fill( (*jetPt)[i], puWeight );
			histos1D_[ "jetPt" ]->Fill( corrJet.Pt(), puWeight );
			histos1D_[ "rawJetPt" ]->Fill( rawJet.Pt(), puWeight );
			histos1D_[ "oldJetEta" ]->Fill( (*jetEta)[i], puWeight );
			histos1D_[ "jetEta" ]->Fill( corrJet.Eta(), puWeight );
			histos1D_[ "rawJetEta" ]->Fill( rawJet.Eta(), puWeight );
			histos1D_[ "oldJetMass" ]->Fill( (*jetMass)[i], puWeight );
			histos1D_[ "jetMass" ]->Fill( corrMass, puWeight );
			histos1D_[ "jetTrimmedMass" ]->Fill( corrTrimmedMass, puWeight );
			histos1D_[ "jetPrunedMass" ]->Fill( corrPrunedMass, puWeight );
			histos1D_[ "jetFilteredMass" ]->Fill( corrFilteredMass, puWeight );
			histos1D_[ "jetSoftDropMass" ]->Fill( corrSoftDropMass, puWeight );
			histos1D_[ "rawJetMass" ]->Fill( rawJet.M(), puWeight );
			histos1D_[ "neutralHadronEnergy" ]->Fill( (*neutralHadronEnergy)[i] * jec, puWeight );
			histos1D_[ "neutralEmEnergy" ]->Fill( (*neutralEmEnergy)[i] * jec, puWeight );
			histos1D_[ "chargedHadronEnergy" ]->Fill( (*chargedHadronEnergy)[i] * jec, puWeight );
			histos1D_[ "chargedEmEnergy" ]->Fill( (*chargedEmEnergy)[i] * jec, puWeight );
			histos1D_[ "numConst" ]->Fill( (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i], puWeight );
			histos1D_[ "chargedMultiplicity" ]->Fill( (*chargedMultiplicity)[i] * jec, puWeight );

			myJet tmpJET;
			tmpJET.p4 = tmpJet;
			tmpJET.subjet0 = tmpSubjet0;
			tmpJET.subjet1 = tmpSubjet1;
			tmpJET.mass = corrMass;
			tmpJET.trimmedMass = corrTrimmedMass;
			tmpJET.prunedMass = corrPrunedMass;
			tmpJET.filteredMass = corrFilteredMass;
			tmpJET.softDropMass = corrSoftDropMass;
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
	histos1D_[ "jetNum" ]->Fill( numJets, puWeight );
	histos1D_[ "NPV_NOPUWeight" ]->Fill( numPV );
	histos1D_[ "NPV" ]->Fill( numPV, puWeight );
	if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT, puWeight );
	if ( HT > 900. ) cutHT = 1;

	sort(tmpTriggerMass.begin(), tmpTriggerMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	if ( ( tmpTriggerMass.size()> 0 ) ) { //&& ( tmpTriggerMass[0] > cutTrimmedMassvalue) ){
		trimmedMass = tmpTriggerMass[0];
		if (HT > 0) histos2D_[ "jetTrimmedMassHT" ]->Fill( tmpTriggerMass[0], HT, puWeight );
	}
	tmpTriggerMass.clear();

	if ( ORTriggers ) {
		//LogWarning("fired") << HT << " " << trimmedMass;
		cutmap["Trigger"] += 1; 

		histos1D_[ "HT_cutTrigger" ]->Fill( HT, puWeight );
		histos1D_[ "MET_cutTrigger" ]->Fill( MET, puWeight );
		histos1D_[ "METHT_cutTrigger" ]->Fill( MET/HT, puWeight );
		histos1D_[ "NPV_cutTrigger" ]->Fill( numPV, puWeight );
		histos1D_[ "jetNum_cutTrigger" ]->Fill( numJets, puWeight );
		histos2D_[ "jetTrimmedMassHT_cutTrigger" ]->Fill( trimmedMass, HT, puWeight );

		int kdum = 0;
		for (size_t k = 0; k < JETS.size(); k++) {
			histos1D_[ "jetPt_cutTrigger" ]->Fill( JETS[k].p4.Pt(), puWeight );
			histos1D_[ "jetEta_cutTrigger" ]->Fill( JETS[k].p4.Eta(), puWeight );
			histos1D_[ "jetMass_cutTrigger" ]->Fill( JETS[k].mass, puWeight );

			if ( (++kdum) == 1 ) {
				histos1D_[ "jet1Pt_cutTrigger" ]->Fill( JETS[0].p4.Pt(), puWeight );
				histos1D_[ "jet1Mass_cutTrigger" ]->Fill( JETS[0].mass, puWeight );
				histos1D_[ "jet1Eta_cutTrigger" ]->Fill( JETS[0].p4.Eta(), puWeight );
			}
		 }
		//////////////////////////////////////////////////////////////////////////////
		
		vector<double> dalitz1, dalitz2;
		vector<TLorentzVector> jet1SubjetsTLV, jet2SubjetsTLV;

		if ( JETS.size() > 1 ) {

			cutmap["Dijet"] += 1;
			
			histos1D_[ "HT_cutDijet" ]->Fill( HT, puWeight );
			histos1D_[ "MET_cutDijet" ]->Fill( MET, puWeight );
			histos1D_[ "METHT_cutDijet" ]->Fill( MET/HT, puWeight );
			histos1D_[ "NPV_cutDijet" ]->Fill( numPV, puWeight );
			histos1D_[ "jetNum_cutDijet" ]->Fill( numJets, puWeight );
			histos1D_[ "jet1Pt_cutDijet" ]->Fill( JETS[0].p4.Pt(), puWeight );
			histos1D_[ "jet1Eta_cutDijet" ]->Fill( JETS[0].p4.Eta(), puWeight );
			histos1D_[ "jet1Mass_cutDijet" ]->Fill( JETS[0].mass, puWeight );
			histos1D_[ "jet2Pt_cutDijet" ]->Fill( JETS[1].p4.Pt(), puWeight );
			histos1D_[ "jet2Eta_cutDijet" ]->Fill( JETS[1].p4.Eta(), puWeight );
			histos1D_[ "jet2Mass_cutDijet" ]->Fill( JETS[1].mass, puWeight );
			for (size_t k = 0; k < JETS.size(); k++) {
				histos1D_[ "neutralHadronEnergy_cutDijet" ]->Fill( JETS[k].nhf, puWeight );
				histos1D_[ "neutralEmEnergy_cutDijet" ]->Fill( JETS[k].nEMf, puWeight );
				histos1D_[ "chargedHadronEnergy_cutDijet" ]->Fill( JETS[k].chf, puWeight );
				histos1D_[ "chargedEmEnergy_cutDijet" ]->Fill( JETS[k].cEMf, puWeight );
				histos1D_[ "numConst_cutDijet" ]->Fill( JETS[k].numConst, puWeight );
				histos1D_[ "chargedMultiplicity_cutDijet" ]->Fill( JETS[k].chm, puWeight );
			}

			// Cut Pt
			if (( JETS[0].p4.Pt() > 500. ) && ( JETS[1].p4.Pt() > 450. ) ) cutJetPt = 1 ;

			if ( cutHT && cutJetPt ) {

				cutmap["HT"] += 1;

				// Mass average and asymmetry
				massAve = massAverage( JETS[0].mass, JETS[1].mass );
				massAsym = massAsymmetry( JETS[0].mass, JETS[1].mass );
				trimmedMassAve = massAverage( JETS[0].trimmedMass, JETS[1].trimmedMass );
				trimmedMassAsym = massAsymmetry( JETS[0].trimmedMass, JETS[1].trimmedMass );
				prunedMassAve = massAverage( JETS[0].prunedMass, JETS[1].prunedMass );
				prunedMassAsym = massAsymmetry( JETS[0].prunedMass, JETS[1].prunedMass );
				filteredMassAve = massAverage( JETS[0].filteredMass, JETS[1].filteredMass );
				filteredMassAsym = massAsymmetry( JETS[0].filteredMass, JETS[1].filteredMass );
				softDropMassAve = massAverage( JETS[0].softDropMass, JETS[1].softDropMass );
				softDropMassAsym = massAsymmetry( JETS[0].softDropMass, JETS[1].softDropMass );
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
				/*
				if( ( jet1SubjetsTLV.size() > 0 ) && ( jet2SubjetsTLV.size() > 0 ) ) {

					// Subjet Pt ratio, subjet mass ratio 
					//LogWarning("subjet0") <<  jet1SubjetsTLV[0].Pt() << " " <<  jet1SubjetsTLV[1].Pt();
					jet1SubjetPtRatio = min( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() ) / max( jet1SubjetsTLV[0].Pt(), jet1SubjetsTLV[1].Pt() );
					jet1SubjetMass21Ratio =  jet1SubjetsTLV[1].M() / jet1SubjetsTLV[0].M() ;
					jet1Subjet112MassRatio = jet1SubjetsTLV[0].M() / ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] ).M();
					jet1Subjet1JetMassRatio = jet1SubjetsTLV[0].M() /JETS[0].mass;
					jet1Subjet212MassRatio = jet1SubjetsTLV[1].M() / ( jet1SubjetsTLV[0] + jet1SubjetsTLV[1] ).M();
					jet1Subjet2JetMassRatio = jet1SubjetsTLV[1].M() /JETS[0].mass;

					jet2SubjetPtRatio = min( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() ) / max( jet2SubjetsTLV[0].Pt(), jet2SubjetsTLV[1].Pt() );
					jet2SubjetMass21Ratio =  jet2SubjetsTLV[1].M()/jet2SubjetsTLV[0].M();
					jet2Subjet112MassRatio = jet2SubjetsTLV[0].M()/ ( jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M();
					jet2Subjet1JetMassRatio = jet2SubjetsTLV[0].M()/JETS[1].mass;
					jet2Subjet212MassRatio = jet2SubjetsTLV[1].M()/ ( jet2SubjetsTLV[0] + jet2SubjetsTLV[1] ).M();
					jet2Subjet2JetMassRatio = jet2SubjetsTLV[1].M()/JETS[1].mass;
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

				}*/

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

				RUNAtree->Fill();  
				histos1D_[ "HT_cutEffTrigger" ]->Fill( HT, puWeight );
				histos1D_[ "MET_cutEffTrigger" ]->Fill( MET, puWeight );
				histos1D_[ "METHT_cutEffTrigger" ]->Fill( MET/HT, puWeight );
				histos1D_[ "NPV_cutEffTrigger" ]->Fill( numPV, puWeight );
				histos1D_[ "jetNum_cutEffTrigger" ]->Fill( numJets, puWeight );
				histos1D_[ "jet1Pt_cutEffTrigger" ]->Fill( JETS[0].p4.Pt(), puWeight );
				histos1D_[ "jet1Eta_cutEffTrigger" ]->Fill( JETS[0].p4.Eta(), puWeight );
				histos1D_[ "jet2Pt_cutEffTrigger" ]->Fill( JETS[1].p4.Pt(), puWeight );
				histos1D_[ "jet2Eta_cutEffTrigger" ]->Fill( JETS[1].p4.Eta(), puWeight );

			}
		}
	}
	JETS.clear();
	scaleWeights.clear();
	pdfWeights.clear();
	alphaWeights.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNBoostedAnalysis::beginJob() {

	// Calculate PUWeight
	if ( !isData ) PUWeight_.generateWeights( dataPUFile );

	RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
	RUNAtree->Branch( "run", &run, "run/I" );
	RUNAtree->Branch( "lumi", &lumi, "lumi/I" );
	RUNAtree->Branch( "event", &event, "event/I" );
	RUNAtree->Branch( "numJets", &numJets, "numJets/I" );
	RUNAtree->Branch( "numPV", &numPV, "numPV/I" );
	RUNAtree->Branch( "puWeight", &puWeight, "puWeight/F" );
	RUNAtree->Branch( "genWeight", &genWeight, "genWeight/F" );
	RUNAtree->Branch( "HT", &HT, "HT/F" );
	RUNAtree->Branch( "AK4HT", &AK4HT, "AK4HT/F" );
	RUNAtree->Branch( "trimmedMass", &trimmedMass, "trimmedMass/F" );
	RUNAtree->Branch( "jet1Pt", &jet1Pt, "jet1Pt/F" );
	RUNAtree->Branch( "jet1Eta", &jet1Eta, "jet1Eta/F" );
	RUNAtree->Branch( "jet1Phi", &jet1Phi, "jet1Phi/F" );
	RUNAtree->Branch( "jet1E", &jet1E, "jet1E/F" );
	RUNAtree->Branch( "jet1btagCSV", &jet1btagCSV, "jet1btagCSV/F" );
	RUNAtree->Branch( "jet2Pt", &jet2Pt, "jet2Pt/F" );
	RUNAtree->Branch( "jet2Eta", &jet2Eta, "jet2Eta/F" );
	RUNAtree->Branch( "jet2Phi", &jet2Phi, "jet2Phi/F" );
	RUNAtree->Branch( "jet2E", &jet2E, "jet2E/F" );
	RUNAtree->Branch( "jet2btagCSV", &jet2btagCSV, "jet2btagCSV/F" );
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
	RUNAtree->Branch( "trimmedMassAve", &trimmedMassAve, "trimmedMassAve/F" );
	RUNAtree->Branch( "trimmedMassAsym", &trimmedMassAsym, "trimmedMassAsym/F" );
	RUNAtree->Branch( "prunedMassAve", &prunedMassAve, "prunedMassAve/F" );
	RUNAtree->Branch( "prunedMassAsym", &prunedMassAsym, "prunedMassAsym/F" );
	RUNAtree->Branch( "filteredMassAve", &filteredMassAve, "filteredMassAve/F" );
	RUNAtree->Branch( "filteredMassAsym", &filteredMassAsym, "filteredMassAsym/F" );
	RUNAtree->Branch( "softDropMassAve", &softDropMassAve, "softDropMassAve/F" );
	RUNAtree->Branch( "softDropMassAsym", &softDropMassAsym, "softDropMassAsym/F" );
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
	RUNAtree->Branch( "scaleWeights", &scaleWeights );
	RUNAtree->Branch( "pdfWeights", &pdfWeights );
	RUNAtree->Branch( "alphaWeights", &alphaWeights );


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
	histos1D_[ "oldJetMass" ] = fs_->make< TH1D >( "oldJetMass", "oldJetMass", 600, 0., 600. );
	histos1D_[ "oldJetMass" ]->Sumw2();
	histos1D_[ "jetMass" ] = fs_->make< TH1D >( "jetMass", "jetMass", 600, 0., 600. );
	histos1D_[ "jetMass" ]->Sumw2();
	histos1D_[ "rawJetMass" ] = fs_->make< TH1D >( "rawJetMass", "rawJetMass", 600, 0., 600. );
	histos1D_[ "rawJetMass" ]->Sumw2();
	histos1D_[ "jetNum" ] = fs_->make< TH1D >( "jetNum", "jetNum", 10, 0., 10. );
	histos1D_[ "jetNum" ]->Sumw2();
	histos1D_[ "jetTrimmedMass" ] = fs_->make< TH1D >( "jetTrimmedMass", "jetTrimmedMass", 600, 0., 600. );
	histos1D_[ "jetTrimmedMass" ]->Sumw2();
	histos1D_[ "jetPrunedMass" ] = fs_->make< TH1D >( "jetPrunedMass", "jetPrunedMass", 600, 0., 600. );
	histos1D_[ "jetPrunedMass" ]->Sumw2();
	histos1D_[ "jetFilteredMass" ] = fs_->make< TH1D >( "jetFilteredMass", "jetFilteredMass", 600, 0., 600. );
	histos1D_[ "jetFilteredMass" ]->Sumw2();
	histos1D_[ "jetSoftDropMass" ] = fs_->make< TH1D >( "jetSoftDropMass", "jetSoftDropMass", 600, 0., 600. );
	histos1D_[ "jetSoftDropMass" ]->Sumw2();
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
	histos1D_[ "jetMass_cutTrigger" ] = fs_->make< TH1D >( "jetMass_cutTrigger", "jetMass_cutTrigger", 600, 0., 600. );
	histos1D_[ "jetMass_cutTrigger" ]->Sumw2();
	histos1D_[ "jet1Pt_cutTrigger" ] = fs_->make< TH1D >( "jet1Pt_cutTrigger", "jet1Pt_cutTrigger", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutTrigger" ]->Sumw2();
	histos1D_[ "jet1Eta_cutTrigger" ] = fs_->make< TH1D >( "jet1Eta_cutTrigger", "jet1Eta_cutTrigger", 100, -5., 5. );
	histos1D_[ "jet1Eta_cutTrigger" ]->Sumw2();
	histos1D_[ "jet1Mass_cutTrigger" ] = fs_->make< TH1D >( "jet1Mass_cutTrigger", "jet1Mass_cutTrigger", 600, 0., 600. );
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
	histos1D_[ "jet1Mass_cutDijet" ] = fs_->make< TH1D >( "jet1Mass_cutDijet", "jet1Mass_cutDijet", 600, 0., 600. );
	histos1D_[ "jet1Mass_cutDijet" ]->Sumw2();
	histos1D_[ "jet2Pt_cutDijet" ] = fs_->make< TH1D >( "jet2Pt_cutDijet", "jet2Pt_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cutDijet" ]->Sumw2();
	histos1D_[ "jet2Eta_cutDijet" ] = fs_->make< TH1D >( "jet2Eta_cutDijet", "jet2Eta_cutDijet", 100, -5., 5. );
	histos1D_[ "jet2Eta_cutDijet" ]->Sumw2();
	histos1D_[ "jet2Mass_cutDijet" ] = fs_->make< TH1D >( "jet2Mass_cutDijet", "jet2Mass_cutDijet", 600, 0., 600. );
	histos1D_[ "jet2Mass_cutDijet" ]->Sumw2();
	histos1D_[ "neutralHadronEnergy_cutDijet" ] = fs_->make< TH1D >( "neutralHadronEnergy_cutDijet", "neutralHadronEnergy", 50, 0., 1. );
	histos1D_[ "neutralHadronEnergy_cutDijet" ]->Sumw2();
	histos1D_[ "neutralEmEnergy_cutDijet" ] = fs_->make< TH1D >( "neutralEmEnergy_cutDijet", "neutralEmEnergy", 50, 0., 1. );
	histos1D_[ "neutralEmEnergy_cutDijet" ]->Sumw2();
	histos1D_[ "chargedHadronEnergy_cutDijet" ] = fs_->make< TH1D >( "chargedHadronEnergy_cutDijet", "chargedHadronEnergy", 50, 0., 1. );
	histos1D_[ "chargedHadronEnergy_cutDijet" ]->Sumw2();
	histos1D_[ "chargedEmEnergy_cutDijet" ] = fs_->make< TH1D >( "chargedEmEnergy_cutDijet", "chargedEmEnergy", 50, 0., 1. );
	histos1D_[ "chargedEmEnergy_cutDijet" ]->Sumw2();
	histos1D_[ "chargedMultiplicity_cutDijet" ] = fs_->make< TH1D >( "chargedMultiplicity_cutDijet", "chargedMultiplicity", 50, 0., 1. );
	histos1D_[ "chargedMultiplicity_cutDijet" ]->Sumw2();
	histos1D_[ "numConst_cutDijet" ] = fs_->make< TH1D >( "numConst_cutDijet", "numConst", 100, 0., 100. );
	histos1D_[ "numConst_cutDijet" ]->Sumw2();
	histos1D_[ "MET_cutDijet" ] = fs_->make< TH1D >( "MET_cutDijet", "MET_cutDijet", 20, 0., 200. );
	histos1D_[ "MET_cutDijet" ]->Sumw2();
	histos1D_[ "METHT_cutDijet" ] = fs_->make< TH1D >( "METHT_cutDijet", "METHT_cutDijet", 50, 0., 1. );
	histos1D_[ "METHT_cutDijet" ]->Sumw2();


	histos1D_[ "HT_cutEffTrigger" ] = fs_->make< TH1D >( "HT_cutEffTrigger", "HT_cutEffTrigger", 500, 0., 5000. );
	histos1D_[ "HT_cutEffTrigger" ]->Sumw2();
	histos1D_[ "NPV_cutEffTrigger" ] = fs_->make< TH1D >( "NPV_cutEffTrigger", "NPV_cutEffTrigger", 80, 0., 80. );
	histos1D_[ "NPV_cutEffTrigger" ]->Sumw2();
	histos1D_[ "jetNum_cutEffTrigger" ] = fs_->make< TH1D >( "jetNum_cutEffTrigger", "jetNum_cutEffTrigger", 10, 0., 10. );
	histos1D_[ "jetNum_cutEffTrigger" ]->Sumw2();
	histos1D_[ "jet1Pt_cutEffTrigger" ] = fs_->make< TH1D >( "jet1Pt_cutEffTrigger", "jet1Pt_cutEffTrigger", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutEffTrigger" ]->Sumw2();
	histos1D_[ "jet1Eta_cutEffTrigger" ] = fs_->make< TH1D >( "jet1Eta_cutEffTrigger", "jet1Eta_cutEffTrigger", 100, -5., 5. );
	histos1D_[ "jet1Eta_cutEffTrigger" ]->Sumw2();
	histos1D_[ "jet2Pt_cutEffTrigger" ] = fs_->make< TH1D >( "jet2Pt_cutEffTrigger", "jet2Pt_cutEffTrigger", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cutEffTrigger" ]->Sumw2();
	histos1D_[ "jet2Eta_cutEffTrigger" ] = fs_->make< TH1D >( "jet2Eta_cutEffTrigger", "jet2Eta_cutEffTrigger", 100, -5., 5. );
	histos1D_[ "jet2Eta_cutEffTrigger" ]->Sumw2();
	histos1D_[ "MET_cutEffTrigger" ] = fs_->make< TH1D >( "MET_cutEffTrigger", "MET_cutEffTrigger", 20, 0., 200. );
	histos1D_[ "MET_cutEffTrigger" ]->Sumw2();
	histos1D_[ "METHT_cutEffTrigger" ] = fs_->make< TH1D >( "METHT_cutEffTrigger", "METHT_cutEffTrigger", 50, 0., 1. );
	histos1D_[ "METHT_cutEffTrigger" ]->Sumw2();


	cutLabels.push_back("Processed");
	cutLabels.push_back("Trigger");
	cutLabels.push_back("Dijet");
	cutLabels.push_back("HT");
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

}

void RUNBoostedAnalysis::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutBtagvalue", 1);
	desc.add<bool>("bjSample", false);
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
	desc.add<InputTag>("generator", 	InputTag("generator"));
	desc.add<InputTag>("extLHEProducer", 	InputTag("externalLHEProducer"));
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
	desc.add<InputTag>("jetPrunedMass", 	InputTag("jetsAK8:jetAK8prunedMass"));
	desc.add<InputTag>("jetFilteredMass", 	InputTag("jetsAK8:jetAK8filteredMass"));
	desc.add<InputTag>("jetSoftDropMass", 	InputTag("jetsAK8:jetAK8softDropMass"));
	desc.add<InputTag>("jetTau1", 	InputTag("jetsAK8:jetAK8tau1"));
	desc.add<InputTag>("jetTau2", 	InputTag("jetsAK8:jetAK8tau2"));
	desc.add<InputTag>("jetTau3", 	InputTag("jetsAK8:jetAK8tau3"));
	desc.add<InputTag>("jetNSubjets", 	InputTag("jetsAK8:jetAK8nSubjets"));
	desc.add<InputTag>("jetSubjetIndex0", 	InputTag("jetsAK8:jetAK8vSubjetIndex0"));
	desc.add<InputTag>("jetSubjetIndex1", 	InputTag("jetsAK8:jetAK8vSubjetIndex1"));
	desc.add<InputTag>("jetSubjetIndex2", 	InputTag("jetsAK8:jetAK8vSubjetIndex2"));
	desc.add<InputTag>("jetSubjetIndex3", 	InputTag("jetsAK8:jetAK8vSubjetIndex3"));
	desc.add<InputTag>("jetKeys", 	InputTag("jetKeysAK8"));
	desc.add<InputTag>("jetCSV", 	InputTag("jetsAK8:jetAK8CSVv2"));
	desc.add<InputTag>("jetArea", 	InputTag("jetsAK8:jetAK8jetArea"));
	desc.add<InputTag>("jetGenPt", 	InputTag("jetsAK8:jetAK8GenJetPt"));
	desc.add<InputTag>("jetGenEta", 	InputTag("jetsAK8:jetAK8GenJetEta"));
	desc.add<InputTag>("jetGenPhi", 	InputTag("jetsAK8:jetAK8GenJetPhi"));
	desc.add<InputTag>("jetGenE", 	InputTag("jetsAK8:jetAK8GenJetE"));
	desc.add<InputTag>("metPt", 	InputTag("metFull:metFullPt"));
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
      
void RUNBoostedAnalysis::beginRun(const Run& iRun, const EventSetup& iSetup){

	/* Weights from scale variations, PDFs etc. are stored in the relative product. 
	 * Notice that to be used they need to be renormalized to the central event weight
	 * at LHE level which may be different from genEvtInfo->weight()
	 */
	if (!isData) {
		Handle<LHERunInfoProduct> lheRunInfo;
		iRun.getByLabel( "externalLHEProducer", lheRunInfo );

		if (lheRunInfo.isValid()) {
			// Check which PDF set was used
			lhaPdfId = lheRunInfo->heprup().PDFSUP.first;
			std::cout<<"LHE: LHA PDF ID = "<<lhaPdfId<< "\nLHE:   --> For more info about the sets, check: https://lhapdf.hepforge.org/pdfsets.html"<<std::endl;

			// Check headers
			LHERunInfoProduct lheRunInfoProduct = *(lheRunInfo.product());
			typedef std::vector<LHERunInfoProduct::Header>::const_iterator headers_const_iterator;
			size_t iHead = 0;
			for (headers_const_iterator header=lheRunInfoProduct.headers_begin(); header!=lheRunInfoProduct.headers_end(); header++){
				if (header->tag()=="initrwgt") {
					//std::cout<<"LHE: "<<iHead<<" "<<header->tag()<<std::endl;
					for (auto line : header->lines()) {
						//std::cout<<"LHE: "<<line;
						// Fix buggy powheg samples
						if (lhaPdfId==-1 && line.find("weight id=\"2001\"")!=std::string::npos) {
						if (line.find("PDF set = 260001")!=std::string::npos) lhaPdfId = 260000;
						else if (line.find("PDF set = 260401")!=std::string::npos) lhaPdfId = 260400;
						}
					}
				}
				iHead++;
			}
		}
	}
}


//define this as a plug-in
DEFINE_FWK_MODULE(RUNBoostedAnalysis);
