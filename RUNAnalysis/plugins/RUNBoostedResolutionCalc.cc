// -*- C++ -*-
//
// Package:    Ntuples/Ntuples
// Class:      RUNBoostedResolutionCalc
// 
/**\class RUNBoostedResolutionCalc RUNBoostedResolutionCalc.cc Ntuples/Ntuples/plugins/RUNBoostedResolutionCalc.cc

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
class RUNBoostedResolutionCalc : public EDAnalyzer {
   public:
      explicit RUNBoostedResolutionCalc(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
      ~RUNBoostedResolutionCalc();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(const Run&, const EventSetup&) override;
      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      string PUMethod;
      //PUReweighter PUWeight_;
      int lhaPdfId ;
      
      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      bool bjSample;
      bool isData;
      double scale;
      double cutTau21;
      double cutTau31;
      double cutMassAsym;
      double cutDeltaEtaDijet;
      string dataPUFile;
      string jecVersion;
      TString systematics;

      //vector<string> triggerPass;
      vector<JetCorrectorParameters> jetPar;
      FactorizedJetCorrector * jetJECAK8;
      vector<JetCorrectorParameters> massPar;
      FactorizedJetCorrector * massJECAK8;
      JetCorrectionUncertainty *jetCorrUnc;

      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;
      float AK4HT = 0, HT = 0, trimmedMass = -999, puWeight = -999, genWeight = -999, lumiWeight = -999, MET = -999,
	    jet1Pt = -999, jet1Eta = -999, jet1Phi = -999, jet1E = -999, jet1btagCSVv2 = -9999, jet1btagCMVAv2 = -9999, jet1btagDoubleB = -9999,
	    jet2Pt = -999, jet2Eta = -999, jet2Phi = -999, jet2E = -999, jet2btagCSVv2 = -9999, jet2btagCMVAv2 = -9999, jet2btagDoubleB = -9999,
	    massAve = -9999, massAsym = -9999, 
	    jet1PrunedMass = -9999, jet2PrunedMass = -9999,
	    jet1SoftDropMass = -9999, jet2SoftDropMass = -9999,
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
      EDGetTokenT<vector<float>> jetTau1_;
      EDGetTokenT<vector<float>> jetTau2_;
      EDGetTokenT<vector<float>> jetTau3_;
      EDGetTokenT<vector<float>> jetCSVv2_;
      EDGetTokenT<vector<float>> jetCMVAv2_;
      EDGetTokenT<vector<float>> jetDoubleB_;
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
      //EDGetTokenT<vector<float>> triggerBit_;
      //EDGetTokenT<vector<string>> triggerName_;

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

      // GenInfo
      EDGetTokenT<vector<float>> genPartID_; 
      EDGetTokenT<vector<float>> genPartPt_; 
      EDGetTokenT<vector<float>> genPartPhi_; 
      EDGetTokenT<vector<float>> genPartEta_; 
      EDGetTokenT<vector<float>> genPartE_; 
      EDGetTokenT<vector<float>> genPartStatus_; 
      EDGetTokenT<vector<float>> genPartMom0ID_; 
      EDGetTokenT<vector<float>> genPartMom1ID_; 

};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNBoostedResolutionCalc::RUNBoostedResolutionCalc(const ParameterSet& iConfig):
	jetAK4Pt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4Pt"))),
	jetAK4Eta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4Eta"))),
	jetAK4Phi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4Phi"))),
	jetAK4E_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK4E"))),
	jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPt"))),
	jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetEta"))),
	jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPhi"))),
	jetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetE"))),
	jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
	jetTau1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau1"))),
	jetTau2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau2"))),
	jetTau3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau3"))),
	jetCSVv2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVv2"))),
	jetCMVAv2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCMVAv2"))),
	jetDoubleB_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetDoubleB"))),
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
	//triggerBit_(consumes<vector<float>>(iConfig.getParameter<InputTag>("triggerBit"))),
	//triggerName_(consumes<vector<string>>(iConfig.getParameter<InputTag>("triggerName"))),
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
	genPartID_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartID"))),
	genPartPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartPt"))),
	genPartPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartPhi"))),
	genPartEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartEta"))),
	genPartE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartE"))),
	genPartStatus_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartStatus"))),
	genPartMom0ID_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartMom0ID"))),
	genPartMom1ID_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPartMom1ID")))
{
	consumes<LHERunInfoProduct,edm::InRun> (edm::InputTag("externalLHEProducer"));
	scale 		= iConfig.getParameter<double>("scale");
	cutTau21 		= iConfig.getParameter<double>("cutTau21");
	cutTau31 		= iConfig.getParameter<double>("cutTau31");
	cutMassAsym 		= iConfig.getParameter<double>("cutMassAsym");
	cutDeltaEtaDijet 		= iConfig.getParameter<double>("cutDeltaEtaDijet");
	bjSample 	= iConfig.getParameter<bool>("bjSample");
	isData 		= iConfig.getParameter<bool>("isData");
	dataPUFile 	= iConfig.getParameter<string>("dataPUFile");
	PUMethod 	= iConfig.getParameter<string>("PUMethod");
	jecVersion 	= iConfig.getParameter<string>("jecVersion");
	systematics 	= iConfig.getParameter<string>("systematics");
	//triggerPass 	= iConfig.getParameter<vector<string>>("triggerPass");

	/////// JECs
	string prefix;
	if (isData) prefix = jecVersion + "_DATA_";
	else prefix = jecVersion + "_MC_";

	// all jet
	vector<string> jecAK8PayloadNames_;
	jecAK8PayloadNames_.push_back(prefix + "L1FastJet_AK8PF"+PUMethod+".txt");
	jecAK8PayloadNames_.push_back(prefix + "L2Relative_AK8PF"+PUMethod+".txt");
	jecAK8PayloadNames_.push_back(prefix + "L3Absolute_AK8PF"+PUMethod+".txt");
	if (isData) jecAK8PayloadNames_.push_back(prefix + "L2L3Residual_AK8PF"+PUMethod+".txt");

	for ( vector<string>::const_iterator payloadBegin = jecAK8PayloadNames_.begin(), payloadEnd = jecAK8PayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
		JetCorrectorParameters pars(*ipayload);
		jetPar.push_back(pars);
	}
	jetJECAK8 = new FactorizedJetCorrector(jetPar);

	// jet mass
	vector<string> massjecAK8PayloadNames_;
	massjecAK8PayloadNames_.push_back(prefix + "L2Relative_AK8PF"+PUMethod+".txt");
	massjecAK8PayloadNames_.push_back(prefix + "L3Absolute_AK8PF"+PUMethod+".txt");
	if (isData) massjecAK8PayloadNames_.push_back(prefix + "L2L3Residual_AK8PF"+PUMethod+".txt");

	for ( vector<string>::const_iterator payloadBegin = massjecAK8PayloadNames_.begin(), payloadEnd = massjecAK8PayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
		JetCorrectorParameters massPars(*ipayload);
		massPar.push_back(massPars);
	}
	massJECAK8 = new FactorizedJetCorrector(massPar);

	// jec uncertainty
	JetCorrectorParameters jecUncParam( prefix + "Uncertainty_AK8PF"+PUMethod+".txt");
	jetCorrUnc  = new JetCorrectionUncertainty( jecUncParam );
	////////////////////////////////////////////////////
}


RUNBoostedResolutionCalc::~RUNBoostedResolutionCalc()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNBoostedResolutionCalc::analyze(const Event& iEvent, const EventSetup& iSetup) {


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

	Handle<vector<float> > jetTau1;
	iEvent.getByToken(jetTau1_, jetTau1);

	Handle<vector<float> > jetTau2;
	iEvent.getByToken(jetTau2_, jetTau2);

	Handle<vector<float> > jetTau3;
	iEvent.getByToken(jetTau3_, jetTau3);

	Handle<vector<float> > jetCSVv2;
	iEvent.getByToken(jetCSVv2_, jetCSVv2);

	Handle<vector<float> > jetCMVAv2;
	iEvent.getByToken(jetCMVAv2_, jetCMVAv2);

	Handle<vector<float> > jetDoubleB;
	iEvent.getByToken(jetDoubleB_, jetDoubleB);

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

	/*// Trigger
	Handle<vector<float> > triggerBit;
	iEvent.getByToken(triggerBit_, triggerBit);

	Handle<vector<string> > triggerName;
	iEvent.getByToken(triggerName_, triggerName);
	*/

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

	//// GenInfo
	Handle<vector<float> > genPartID;
	iEvent.getByToken(genPartID_, genPartID);

	Handle<vector<float> > genPartPt;
	iEvent.getByToken(genPartPt_, genPartPt);

	Handle<vector<float> > genPartPhi;
	iEvent.getByToken(genPartPhi_, genPartPhi);

	Handle<vector<float> > genPartEta;
	iEvent.getByToken(genPartEta_, genPartEta);

	Handle<vector<float> > genPartE;
	iEvent.getByToken(genPartE_, genPartE);

	Handle<vector<float> > genPartStatus;
	iEvent.getByToken(genPartStatus_, genPartStatus);

	Handle<vector<float> > genPartMom0ID;
	iEvent.getByToken(genPartMom0ID_, genPartMom0ID);

	Handle<vector<float> > genPartMom1ID;
	iEvent.getByToken(genPartMom1ID_, genPartMom1ID);

	vector<TLorentzVector> boostedStops;
	vector<TLorentzVector> dauStop1, dauStop2;
	if ( !isData ) {

		TLorentzVector tmpStopDau;
		for (size_t p = 0; p < genPartID->size(); p++) {
			if ( ( (*genPartMom0ID)[p] == 1000002 ) && ( (*genPartStatus)[p] == 23 )  ) { 
				tmpStopDau.SetPtEtaPhiE( (*genPartPt)[p], (*genPartEta)[p], (*genPartPhi)[p], (*genPartE)[p] ); 
				dauStop1.push_back( tmpStopDau );
				//LogWarning("test") << p << " " <<  (*genPartID)[p] << " " << (*genPartMom0ID)[p] << " " << (*genPartStatus)[p] ;
			}
			if ( ( (*genPartMom0ID)[p] == -1000002 ) && ( (*genPartStatus)[p] == 23 )  ) { 
				tmpStopDau.SetPtEtaPhiE( (*genPartPt)[p], (*genPartEta)[p], (*genPartPhi)[p], (*genPartE)[p] ); 
				dauStop2.push_back( tmpStopDau );
				//LogWarning("test") << p << " " <<  (*genPartID)[p] << " " << (*genPartMom0ID)[p] << " " << (*genPartStatus)[p] ;
			}
		}
		/*if ( dauStop1.size() > 1 ){
			double deltaRStop1 = dauStop1[0].DeltaR( dauStop1[1] );
			if ( deltaRStop1 < 0.7 ) boostedStops.push_back( ( dauStop1[0] + dauStop1[1] ) ); 
			//LogWarning( "test" ) << deltaRStop1 << " " << ( dauStop1[0] + dauStop1[1] ).M();
		}
		if ( dauStop2.size() > 1 ){
			double deltaRStop2 = dauStop2[0].DeltaR( dauStop2[1] );
			if ( deltaRStop2 < 0.7 ) boostedStops.push_back( ( dauStop2[0] + dauStop2[1] ) ); 
		}*/

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

	//if ( boostedStops.size() == 2 ) { 
	if ( ( dauStop1.size() == 2 ) && ( dauStop2.size() == 2 ) ) { 
	       //LogWarning("test") << boostedStops.size();

		////////// Check trigger fired
		//bool ORTriggers = checkORListOfTriggerBits( triggerName, triggerBit, triggerPass );
		////////////////////////////////////////////////////
		
		////////// PU Reweight
		//if ( isData ) puWeight = 1;
		//else puWeight = PUWeight_.getPUWeight( *trueNInt, *bunchCross );
		puWeight = 1;
		lumiWeight = scale;
		double totalWeight = puWeight * lumiWeight;
		////////////////////////////////////////////////////
		

		/// Applying kinematic, trigger and jet ID
		cutmap["Processed"] += 1;
		vector< myJet > JETS;
		vector< float > tmpTriggerMass;
		bool cutHT = 0;
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
			corrJet = rawJet* ( JEC + sysJEC  );

			if( corrJet.Pt() > 150 && idL ) { 

				HT += corrJet.Pt();
				++numberJets;

				double massJEC = corrections( rawJet, (*jetArea)[i], (*rho)[i] ,*NPV, massJECAK8); 
				double corrMass = (*jetMass)[i] * ( massJEC + sysJEC  );

				myJet tmpJET;
				tmpJET.p4 = tmpJet;
				tmpJET.mass = corrMass;
				tmpJET.tau1 = (*jetTau1)[i];
				tmpJET.tau2 = (*jetTau2)[i];
				tmpJET.tau3 = (*jetTau3)[i];
				tmpJET.btagCSVv2 = (*jetCSVv2)[i];
				tmpJET.btagCMVAv2 = (*jetCMVAv2)[i];
				tmpJET.btagDoubleB = (*jetDoubleB)[i];
				JETS.push_back( tmpJET );
		   
			}
		}

		if ( HT > 900. ) cutHT = 1;


		//if ( ORTriggers ) {
		if ( JETS.size() > 1 ) {
			bool matched = false;
			double tmpDeltaRJet0Dau00 = JETS[0].p4.DeltaR( dauStop1[0] );
			double tmpDeltaRJet0Dau01 = JETS[0].p4.DeltaR( dauStop1[1] );
			if ( ( tmpDeltaRJet0Dau00 < 0.7 ) && ( tmpDeltaRJet0Dau01 < 0.7 ) ) {
				double tmpDeltaRJet1Dau10 = JETS[1].p4.DeltaR( dauStop2[0] );
				double tmpDeltaRJet1Dau11 = JETS[1].p4.DeltaR( dauStop2[1] );
				if ( ( tmpDeltaRJet1Dau10 < 0.7 ) && ( tmpDeltaRJet1Dau11 < 0.7 ) ) {
					matched = true;
				}
			}
			double tmpDeltaRJet1Dau00 = JETS[1].p4.DeltaR( dauStop1[0] );
			double tmpDeltaRJet1Dau01 = JETS[1].p4.DeltaR( dauStop1[1] );
			if ( ( tmpDeltaRJet1Dau00 < 0.7 ) && ( tmpDeltaRJet1Dau01 < 0.7 ) ) {
				double tmpDeltaRJet0Dau10 = JETS[0].p4.DeltaR( dauStop2[0] );
				double tmpDeltaRJet0Dau11 = JETS[0].p4.DeltaR( dauStop2[1] );
				if ( ( tmpDeltaRJet0Dau10 < 0.7 ) && ( tmpDeltaRJet0Dau11 < 0.7 ) ) {
					matched = true;
				}
			}



			//double deltaRJet1 = boostedStops[0].DeltaR( JETS[0].p4 );
			//double deltaRJet2 = boostedStops[1].DeltaR( JETS[1].p4 );

			//if ( ( deltaRJet1 < 0.7 ) && ( deltaRJet2 < 0.7 ) ) {
			if ( matched ) {

				// Mass average and asymmetry
				massAve = massAverage( JETS[0].mass, JETS[1].mass );
				massAsym = massAsymmetry( JETS[0].mass, JETS[1].mass );
				//////////////////////////////////////////////////////////////////////////
				
				/*/ Btag
				jet1btagCSVv2 = JETS[0].btagCSVv2;
				jet2btagCSVv2 = JETS[1].btagCSVv2;
				jet1btagCMVAv2 = JETS[0].btagCMVAv2;
				jet2btagCMVAv2 = JETS[1].btagCMVAv2;
				jet1btagDoubleB = JETS[0].btagDoubleB;
				jet2btagDoubleB = JETS[1].btagDoubleB;
				*/

				// Dijet eta
				deltaEtaDijet = deltaValue( JETS[0].p4.Eta(), JETS[1].p4.Eta() );

				// Cos theta star
				//jet1CosThetaStar = calculateCosThetaStar( JETS[0].p4, JETS[1].p4 ) ;
				//jet2CosThetaStar = calculateCosThetaStar( JETS[1].p4, JETS[0].p4 ) ;

				// Nsubjetiness
				jet1Tau21 = JETS[0].tau2 / JETS[0].tau1;
				jet1Tau31 = JETS[0].tau3 / JETS[0].tau1;
				//jet1Tau32 = JETS[0].tau3 / JETS[0].tau2;
				jet2Tau21 = JETS[1].tau2 / JETS[1].tau1;
				jet2Tau31 = JETS[1].tau3 / JETS[1].tau1;
				//jet2Tau32 = JETS[1].tau3 / JETS[1].tau2;
				////////////////////////////////////////////////////////////////////////////////

				if ( cutHT ) {
					histos1D_[ "massAve_cutHT" ]->Fill( massAve, totalWeight );
					histos1D_[ "prunedMassAsym_cutHT" ]->Fill( massAsym, totalWeight );
					histos1D_[ "jet1Tau21_cutHT" ]->Fill( jet1Tau21, totalWeight );
					histos1D_[ "jet2Tau21_cutHT" ]->Fill( jet2Tau21, totalWeight );
					histos1D_[ "jet1Tau31_cutHT" ]->Fill( jet1Tau31, totalWeight );
					histos1D_[ "jet2Tau31_cutHT" ]->Fill( jet2Tau31, totalWeight );
					histos1D_[ "deltaEtaDijet_cutHT" ]->Fill( deltaEtaDijet, totalWeight );
					if ( ( jet1Tau21 < cutTau21 ) && ( jet2Tau21 < cutTau21  ) ) {
						histos1D_[ "massAve_cutTau21" ]->Fill( massAve, totalWeight );
						if ( ( jet1Tau31 < cutTau31 ) && ( jet2Tau31 < cutTau31  ) ) {
							histos1D_[ "massAve_cutTau31" ]->Fill( massAve, totalWeight );
							if ( massAsym < cutMassAsym) {
								histos1D_[ "massAve_cutMassAsym" ]->Fill( massAve, totalWeight );
								if ( deltaEtaDijet < cutDeltaEtaDijet ) {
									histos1D_[ "massAve_cutDeltaEtaDijet" ]->Fill( massAve, totalWeight );
									histos1D_[ "prunedMassAsym_cutDeltaEtaDijet" ]->Fill( massAsym, totalWeight );
									histos1D_[ "jet1Tau21_cutDeltaEtaDijet" ]->Fill( jet1Tau21, totalWeight );
									histos1D_[ "jet2Tau21_cutDeltaEtaDijet" ]->Fill( jet2Tau21, totalWeight );
									histos1D_[ "jet1Tau31_cutDeltaEtaDijet" ]->Fill( jet1Tau31, totalWeight );
									histos1D_[ "jet2Tau31_cutDeltaEtaDijet" ]->Fill( jet2Tau31, totalWeight );
									histos1D_[ "deltaEtaDijet_cutDeltaEtaDijet" ]->Fill( deltaEtaDijet, totalWeight );
								}
							}
						}
					}
				}
			}
		}
		JETS.clear();
	}

}


// ------------ method called once each job just before starting event loop  ------------
void RUNBoostedResolutionCalc::beginJob() {


	histos1D_[ "massAve_cutHT" ] = fs_->make< TH1D >( "massAve_cutHT", "massAve_cutHT", 600, 0., 600. );
	histos1D_[ "massAve_cutHT" ]->Sumw2();

	histos1D_[ "prunedMassAsym_cutHT" ] = fs_->make< TH1D >( "prunedMassAsym_cutHT", "prunedMassAsym_cutHT", 20, 0., 1. );
	histos1D_[ "prunedMassAsym_cutHT" ]->Sumw2();

	histos1D_[ "jet1Tau21_cutHT" ] = fs_->make< TH1D >( "jet1Tau21_cutHT", "jet1Tau21_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutHT" ]->Sumw2();

	histos1D_[ "jet2Tau21_cutHT" ] = fs_->make< TH1D >( "jet2Tau21_cutHT", "jet2Tau21_cutHT", 20, 0., 1. );
	histos1D_[ "jet2Tau21_cutHT" ]->Sumw2();

	histos1D_[ "jet1Tau31_cutHT" ] = fs_->make< TH1D >( "jet1Tau31_cutHT", "jet1Tau31_cutHT", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutHT" ]->Sumw2();

	histos1D_[ "jet2Tau31_cutHT" ] = fs_->make< TH1D >( "jet2Tau31_cutHT", "jet2Tau31_cutHT", 20, 0., 1. );
	histos1D_[ "jet2Tau31_cutHT" ]->Sumw2();

	histos1D_[ "deltaEtaDijet_cutHT" ] = fs_->make< TH1D >( "deltaEtaDijet_cutHT", "deltaEtaDijet_cutHT", 100, 0., 5. );
	histos1D_[ "deltaEtaDijet_cutHT" ]->Sumw2();


	histos1D_[ "massAve_cutTau21" ] = fs_->make< TH1D >( "massAve_cutTau21", "massAve_cutTau21", 600, 0., 600. );
	histos1D_[ "massAve_cutTau21" ]->Sumw2();

	histos1D_[ "massAve_cutTau31" ] = fs_->make< TH1D >( "massAve_cutTau31", "massAve_cutTau31", 600, 0., 600. );
	histos1D_[ "massAve_cutTau31" ]->Sumw2();

	histos1D_[ "massAve_cutMassAsym" ] = fs_->make< TH1D >( "massAve_cutMassAsym", "massAve_cutMassAsym", 600, 0., 600. );
	histos1D_[ "massAve_cutMassAsym" ]->Sumw2();

	histos1D_[ "massAve_cutDeltaEtaDijet" ] = fs_->make< TH1D >( "massAve_cutDeltaEtaDijet", "massAve_cutDeltaEtaDijet", 600, 0., 600. );
	histos1D_[ "massAve_cutDeltaEtaDijet" ]->Sumw2();

	histos1D_[ "prunedMassAsym_cutDeltaEtaDijet" ] = fs_->make< TH1D >( "prunedMassAsym_cutDeltaEtaDijet", "prunedMassAsym_cutDeltaEtaDijet", 20, 0., 1. );
	histos1D_[ "prunedMassAsym_cutDeltaEtaDijet" ]->Sumw2();

	histos1D_[ "jet1Tau21_cutDeltaEtaDijet" ] = fs_->make< TH1D >( "jet1Tau21_cutDeltaEtaDijet", "jet1Tau21_cutDeltaEtaDijet", 20, 0., 1. );
	histos1D_[ "jet1Tau21_cutDeltaEtaDijet" ]->Sumw2();

	histos1D_[ "jet2Tau21_cutDeltaEtaDijet" ] = fs_->make< TH1D >( "jet2Tau21_cutDeltaEtaDijet", "jet2Tau21_cutDeltaEtaDijet", 20, 0., 1. );
	histos1D_[ "jet2Tau21_cutDeltaEtaDijet" ]->Sumw2();

	histos1D_[ "jet1Tau31_cutDeltaEtaDijet" ] = fs_->make< TH1D >( "jet1Tau31_cutDeltaEtaDijet", "jet1Tau31_cutDeltaEtaDijet", 20, 0., 1. );
	histos1D_[ "jet1Tau31_cutDeltaEtaDijet" ]->Sumw2();

	histos1D_[ "jet2Tau31_cutDeltaEtaDijet" ] = fs_->make< TH1D >( "jet2Tau31_cutDeltaEtaDijet", "jet2Tau31_cutDeltaEtaDijet", 20, 0., 1. );
	histos1D_[ "jet2Tau31_cutDeltaEtaDijet" ]->Sumw2();

	histos1D_[ "deltaEtaDijet_cutDeltaEtaDijet" ] = fs_->make< TH1D >( "deltaEtaDijet_cutDeltaEtaDijet", "deltaEtaDijet_cutDeltaEtaDijet", 100, 0., 5. );
	histos1D_[ "deltaEtaDijet_cutDeltaEtaDijet" ]->Sumw2();

}

// ------------ method called once each job just after ending the event loop  ------------
void RUNBoostedResolutionCalc::endJob() {

}

void RUNBoostedResolutionCalc::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutTau21", 1);
	desc.add<double>("cutTau31", 1);
	desc.add<double>("cutMassAsym", 1);
	desc.add<double>("cutDeltaEtaDijet", 1);
	desc.add<bool>("bjSample", false);
	desc.add<bool>("isData", false);
	desc.add<string>("dataPUFile", "supportFiles/PileupData2015D_JSON_10-23-2015.root");
	desc.add<string>("jecVersion", "supportFiles/Summer15_25nsV6");
	desc.add<string>("systematics", "None");
	desc.add<string>("PUMethod", "chs");
	desc.add<double>("scale", 1);
	//vector<string> HLTPass;
	//HLTPass.push_back("HLT_AK8PFHT700_TrimR0p1PT0p03Mass50");
	//desc.add<vector<string>>("triggerPass",	HLTPass);

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
	desc.add<InputTag>("jetAK4Pt", 	InputTag("jetsAK4CHS:jetAK4CHSPt"));
	desc.add<InputTag>("jetAK4Eta", 	InputTag("jetsAK4CHS:jetAK4CHSEta"));
	desc.add<InputTag>("jetAK4Phi", 	InputTag("jetsAK4CHS:jetAK4CHSPhi"));
	desc.add<InputTag>("jetAK4E", 	InputTag("jetsAK4CHS:jetAK4CHSE"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK8CHS:jetAK8CHSPt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK8CHS:jetAK8CHSEta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK8CHS:jetAK8CHSPhi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK8CHS:jetAK8CHSE"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK8CHS:jetAK8CHSprunedMass"));
	desc.add<InputTag>("jetTau1", 	InputTag("jetsAK8CHS:jetAK8CHStau1"));
	desc.add<InputTag>("jetTau2", 	InputTag("jetsAK8CHS:jetAK8CHStau2"));
	desc.add<InputTag>("jetTau3", 	InputTag("jetsAK8CHS:jetAK8CHStau3"));
	desc.add<InputTag>("jetCSVv2", 	InputTag("jetsAK8CHS:jetAK8CHSCSVv2"));
	desc.add<InputTag>("jetCMVAv2", 	InputTag("jetsAK8CHS:jetAK8CHSCMVAv2"));
	desc.add<InputTag>("jetDoubleB", 	InputTag("jetsAK8CHS:jetAK8CHSDoubleBAK8"));
	desc.add<InputTag>("jetArea", 	InputTag("jetsAK8CHS:jetAK8CHSjetArea"));
	desc.add<InputTag>("jetGenPt", 	InputTag("jetsAK8CHS:jetAK8CHSGenJetPt"));
	desc.add<InputTag>("jetGenEta", 	InputTag("jetsAK8CHS:jetAK8CHSGenJetEta"));
	desc.add<InputTag>("jetGenPhi", 	InputTag("jetsAK8CHS:jetAK8CHSGenJetPhi"));
	desc.add<InputTag>("jetGenE", 	InputTag("jetsAK8CHS:jetAK8CHSGenJetE"));
	desc.add<InputTag>("metPt", 	InputTag("metFull:metFullPt"));
	// JetID
	desc.add<InputTag>("jecFactor", 		InputTag("jetsAK8CHS:jetAK8CHSjecFactor0"));
	desc.add<InputTag>("neutralHadronEnergy", 	InputTag("jetsAK8CHS:jetAK8CHSneutralHadronEnergy"));
	desc.add<InputTag>("neutralEmEnergy", 		InputTag("jetsAK8CHS:jetAK8CHSneutralEmEnergy"));
	desc.add<InputTag>("chargedEmEnergy", 		InputTag("jetsAK8CHS:jetAK8CHSchargedEmEnergy"));
	desc.add<InputTag>("muonEnergy", 		InputTag("jetsAK8CHS:jetAK8CHSMuonEnergy"));
	desc.add<InputTag>("chargedHadronEnergy", 	InputTag("jetsAK8CHS:jetAK8CHSchargedHadronEnergy"));
	desc.add<InputTag>("chargedHadronMultiplicity",	InputTag("jetsAK8CHS:jetAK8CHSChargedHadronMultiplicity"));
	desc.add<InputTag>("neutralHadronMultiplicity",	InputTag("jetsAK8CHS:jetAK8CHSneutralHadronMultiplicity"));
	desc.add<InputTag>("chargedMultiplicity", 	InputTag("jetsAK8CHS:jetAK8CHSchargedMultiplicity"));
	// Trigger
	//desc.add<InputTag>("triggerBit",		InputTag("TriggerUserData:triggerBitTree"));
	//desc.add<InputTag>("triggerName",		InputTag("TriggerUserData:triggerNameTree"));
	// GenInfo
	desc.add<InputTag>("genPartID",		InputTag("genPart:genPartID"));
	desc.add<InputTag>("genPartPt",		InputTag("genPart:genPartPt"));
	desc.add<InputTag>("genPartPhi",		InputTag("genPart:genPartPhi"));
	desc.add<InputTag>("genPartEta",		InputTag("genPart:genPartEta"));
	desc.add<InputTag>("genPartE",		InputTag("genPart:genPartE"));
	desc.add<InputTag>("genPartStatus",		InputTag("genPart:genPartStatus"));
	desc.add<InputTag>("genPartMom0ID",		InputTag("genPart:genPartMom0ID"));
	desc.add<InputTag>("genPartMom1ID",		InputTag("genPart:genPartMom1ID"));
	descriptions.addDefault(desc);
}
      


//define this as a plug-in
DEFINE_FWK_MODULE(RUNBoostedResolutionCalc);
