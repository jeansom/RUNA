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

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNAnalysis : public EDAnalyzer {
   public:
      explicit RUNAnalysis(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
      ~RUNAnalysis();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;
      virtual void clearVariables();

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
      double scale;
      bool mkTree;
      TString HLTtriggerOne;
      TString HLTtriggerTwo;
      double cutMassRes;
      double cutDelta;
      double cutEtaBand;
      double cutJetPt;
      double cutHT;

      vector<float> *jetsPt = new std::vector<float>();
      vector<float> *jetsEta = new std::vector<float>();
      vector<float> *jetsPhi = new std::vector<float>();
      vector<float> *jetsE = new std::vector<float>();

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
RUNAnalysis::RUNAnalysis(const ParameterSet& iConfig):
//	getterOfProducts_(ProcessMatch(*), this) {
//	triggerBits_(consumes<TriggerResults>(iConfig.getParameter<InputTag>("bits"))),
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
	scale 		= iConfig.getParameter<double>("scale");
	bjSample 	= iConfig.getParameter<bool>("bjSample");
	cutMassRes      = iConfig.getParameter<double>     ("cutMassRes");
	cutDelta        = iConfig.getParameter<double>     ("cutDelta");
	cutEtaBand      = iConfig.getParameter<double>     ("cutEtaBand");
	cutJetPt	= iConfig.getParameter<double>     ("cutJetPt");
	cutHT 		= iConfig.getParameter<double>("cutHT");
	HLTtriggerOne 	= iConfig.getParameter<string>("HLTtriggerOne");
	HLTtriggerTwo 	= iConfig.getParameter<string>("HLTtriggerTwo");
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


	bool triggerFiredOne = checkTriggerBits( triggerName, triggerBit, HLTtriggerOne  );
	bool triggerFiredTwo = checkTriggerBits( triggerName, triggerBit, HLTtriggerTwo  );
	
	cutmap["Processed"] += 1;

	int numPV = *NPV;
	//vector< JETtype > JETS;
	vector< TLorentzVector > JETS;
	vector< float > tmpTriggerMass;
	int numJets = 0;
	double HT = 0;
	double rawHT = 0;
	//bool bTagCSV = 0;
	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		rawHT += (*jetPt)[i];
		histos1D_[ "rawJetPt" ]->Fill( (*jetPt)[i], scale  );

		bool idL = loosejetID( (*jetE)[i], (*jecFactor)[i], (*neutralHadronEnergy)[i], (*neutralEmEnergy)[i], (*chargedHadronEnergy)[i], (*chargedEmEnergy)[i], (*chargedHadronMultiplicity)[i], (*neutralHadronMultiplicity)[i], (*chargedMultiplicity)[i] ); 

		if( ( (*jetPt)[i] > cutJetPt ) && idL ) { 

			HT += (*jetPt)[i];
			++numJets;

			TLorentzVector tmpJet;
			tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

			//if ( (*jetCSV)[i] > 0.244 ) bTagCSV = 1; 	// CSVL
			//if ( (*jetCSV)[i] > 0.679 ) bTagCSV = 1; 	// CSVM
			//if ( (*jetCSVV1)[i] > 0.405 ) bTagCSV = 1; 	// CSVV1L
			//if ( (*jetCSVV1)[i] > 0.783 ) bTagCSV = 1; 	// CSVV1M

			/*JETtype tmpJET;
			tmpJET = tmpJet;
			tmpJET.mass = (*jetMass)[i];
			tmpJET.btagCSV = bTagCSV;
			JETS.push_back( tmpJET );
			*/
			JETS.push_back( tmpJet );
	   
			histos1D_[ "jetPt" ]->Fill( (*jetPt)[i], scale  );
			histos1D_[ "jetEta" ]->Fill( (*jetEta)[i], scale  );
			histos1D_[ "jetMass" ]->Fill( (*jetMass)[i], scale  );
		}
	}

	//sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1; tmpP2 = p2;  return tmpP1.M() > tmpP2.M(); }); 
	histos1D_[ "jetNum" ]->Fill( numJets, scale );
	histos1D_[ "NPV" ]->Fill( numPV, scale );
	if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT, scale  );
	if ( rawHT > 0 ) histos1D_[ "rawHT" ]->Fill( rawHT, scale  );

	clearVariables();

	if ( triggerFiredOne && triggerFiredTwo ) {
		
		cutmap["Trigger"] += 1;
		histos1D_[ "HT_triggerCuts" ]->Fill( HT, scale  );
		histos1D_[ "NPV_triggerCuts" ]->Fill( numPV, scale );
		histos1D_[ "jetNum_triggerCuts" ]->Fill( numJets, scale );

		if( ( numJets == 4 ) && ( HT > cutHT ) ){
	
			vector<double> tmpDijetR;
			double dR12 = JETS[0].DeltaR( JETS[1] );
			double dR34 = JETS[2].DeltaR( JETS[3] );
			double dijetR1234 = abs( dR12 - 1 )  + abs( dR34 - 1 );
			tmpDijetR.push_back( dijetR1234 );

			double dR13 = JETS[0].DeltaR( JETS[2] );
			double dR24 = JETS[1].DeltaR( JETS[3] );
			double dijetR1324 = abs( dR13 - 1 )  + abs( dR24 - 1 );
			tmpDijetR.push_back( dijetR1324 );

			double dR14 = JETS[0].DeltaR( JETS[3] );
			double dR23 = JETS[1].DeltaR( JETS[2] );
			double dijetR1423 = abs( dR14 - 1 )  + abs( dR23 - 1 );
			tmpDijetR.push_back( dijetR1423 );

			//LogWarning("test") << min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin()  << " " << dijetR1234 << " " << dijetR1324 << " " << dijetR1423 ;
			int minDeltaR = min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin();
			TLorentzVector j1, j2, j3, j4;

			if( minDeltaR == 0 ){
				j1 = JETS[0];
				j2 = JETS[1];
				j3 = JETS[2];
				j4 = JETS[3];
			} else if ( minDeltaR == 1 ) {
				j1 = JETS[0];
				j2 = JETS[2];
				j3 = JETS[1];
				j4 = JETS[3];
			} else if ( minDeltaR == 2 ) {
				j1 = JETS[0];
				j2 = JETS[3];
				j3 = JETS[1];
				j4 = JETS[2];
			}


			double mass1 = ( j1 + j2 ).M();
			double mass2 = ( j3 + j4 ).M();
			double avgMass = ( mass1 + mass2 ) / 2;
			double delta1 = ( j1.Pt() + j2.Pt() ) - avgMass;
			double delta2 = ( j3.Pt() + j4.Pt() ) - avgMass;
			double massRes = TMath::Abs( mass1 - mass2 ) / avgMass;
			double eta1 = ( j1 + j2 ).Eta();
			double eta2 = ( j3 + j4 ).Eta();

			histos1D_[ "jet4Pt_best" ]->Fill( j4.Pt(), scale );
			histos1D_[ "massAve_best" ]->Fill( avgMass, scale );
			histos1D_[ "massRes_best" ]->Fill( massRes, scale );
			histos1D_[ "deltaEta_best" ]->Fill( TMath::Abs( eta1 - eta2 ), scale );
			histos1D_[ "minDeltaR_best" ]->Fill( minDeltaR, scale  );
			histos1D_[ "HT_best" ]->Fill( HT );
			histos2D_[ "deltavsMassAve_best" ]->Fill( avgMass, delta1, scale  );
			histos2D_[ "deltavsMassAve_best" ]->Fill( avgMass, delta2, scale  );

			bool passcutsdR   = false;
			if ( massRes < cutMassRes && 
					delta1  > cutDelta   && 
					delta2  > cutDelta   &&
					fabs(eta1 - eta2) <  cutEtaBand)
				passcutsdR = true;

			/*vector<double> dalitz1, dalitz2;
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
			
			double m1 = j1.M();
			double m2 = j2.M();
			double m3 = j3.M();
			double m4 = j4.M();

			double m12 = ( j1 + j2 ).M() ;
			double m34 = ( j3 + j4 ).M() ;
			double m134 = ( j1 + j3 + j4 ).M() ;
			double m123 = ( j1 + j2 + j3 ).M() ;
			double m124 = ( j1 + j2 + j4 ).M() ;
			double m234 = ( j2 + j3 + j4 ).M() ;
			double m1234 = ( j1 + j2 + j3 + j4 ).M() ;
			
			double tmpX1 = pow(m1234,2) * ( ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2) ) ;
			double tmpX2 = pow(m12,2) * ( pow(m134,2) - pow(m34,2) - pow(m1,2) );
			double tmpX3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
			double tmpX4 = ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2);
			double tmpX5 = pow(m12,2) * pow(m1,2);
			double tmpx1 = tmpX1 - (tmpX2/2);
			double tmpx2 = tmpX3 * ( pow(tmpX4,2) - tmpX5 );
			double cosPhi13412 = TMath::Abs( tmpx1 / TMath::Sqrt( tmpx2 ) );
			histos1D_[ "polAngle13412_best" ]->Fill( cosPhi13412 );

			double tmpY1 = pow(m1234,2) * ( ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2) ) ;
			double tmpY2 = pow(m34,2) * ( pow(m123,2) - pow(m12,2) - pow(m3,2) );
			double tmpY3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
			double tmpY4 = ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2);
			double tmpY5 = pow(m34,2) * pow(m3,2);
			double tmpy1 = tmpY1 - (tmpY2/2);
			double tmpy2 = tmpY3 * ( pow(tmpY4,2) - tmpY5 );
			double cosPhi31234 = TMath::Abs( tmpy1 / TMath::Sqrt( tmpy2 ) );
			histos1D_[ "polAngle31234_best" ]->Fill( cosPhi31234 );
			histos2D_[ "polAngle13412vs31234_best" ]->Fill( cosPhi13412, cosPhi31234, scale );

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
			histos1D_[ "mu1_best" ]->Fill( dalitz1[0], scale );
			histos1D_[ "mu2_best" ]->Fill( dalitz1[1], scale );
			histos1D_[ "mu3_best" ]->Fill( dalitz1[2], scale );
			histos2D_[ "mu1234_best" ]->Fill( dalitz1[0], dalitz1[2], scale );
			histos2D_[ "mu1234_best" ]->Fill( dalitz1[1], dalitz1[2], scale );
			histos2D_[ "mu1234_best" ]->Fill( dalitz1[0], dalitz1[1], scale );

			dalitzX1 = ( dalitz1[1] + ( 2 * dalitz1[0] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz1234_best" ]->Fill( dalitzX1, dalitz1[1], scale );
			//LogWarning("X1") << dalitzX1 << " " << dalitz1[1] ;
			dalitzX2 = ( dalitz1[2] + ( 2 * dalitz1[0] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz1234_best" ]->Fill( dalitzX2, dalitz1[2], scale );
			//LogWarning("X2") << dalitzX2 << " " << dalitz1[2] ;
			dalitzX3 = ( dalitz1[0] + ( 2 * dalitz1[1] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz1234_best" ]->Fill( dalitzX3, dalitz1[0], scale );
			//LogWarning("X3") << dalitzX3 << " " << dalitz1[0] ;
			dalitzX4 = ( dalitz1[2] + ( 2 * dalitz1[1] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz1234_best" ]->Fill( dalitzX4, dalitz1[2], scale );
			//LogWarning("X4") << dalitzX4 << " " << dalitz1[2] ;
			dalitzX5 = ( dalitz1[0] + ( 2 * dalitz1[2] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz1234_best" ]->Fill( dalitzX5, dalitz1[0], scale );
			//LogWarning("X5") << dalitzX5 << " " << dalitz1[0] ;
			dalitzX6 = ( dalitz1[1] + ( 2 * dalitz1[2] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz1234_best" ]->Fill( dalitzX6, dalitz1[1], scale );
			//LogWarning("X6") << dalitzX6 << " " << dalitz1[1] ;


			double tmptilde2 = pow( m3, 2 ) + pow( m4, 2) + pow( m12, 2 ) + pow( m1234, 2);
			double mtilde34 = pow( m34, 2 ) / tmptilde2;
			double mtilde123 = pow( m123, 2 ) / tmptilde2;
			double mtilde124 = pow( m124, 2 ) / tmptilde2;
			dalitz2.push_back( mtilde34 );
			dalitz2.push_back( mtilde123 );
			dalitz2.push_back( mtilde124 );
			sort( dalitz2.begin(), dalitz2.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
			histos1D_[ "mu4_best" ]->Fill( dalitz2[0], scale );
			histos1D_[ "mu5_best" ]->Fill( dalitz2[1], scale );
			histos1D_[ "mu6_best" ]->Fill( dalitz2[2], scale );
			histos2D_[ "mu3412_best" ]->Fill( dalitz2[0], dalitz2[2], scale );
			histos2D_[ "mu3412_best" ]->Fill( dalitz2[1], dalitz2[2], scale );
			histos2D_[ "mu3412_best" ]->Fill( dalitz2[0], dalitz2[1], scale );

			dalitzY1 = ( dalitz2[1] + ( 2 * dalitz2[0] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz3412_best" ]->Fill( dalitzY1, dalitz2[1], scale );
			dalitzY2 = ( dalitz2[2] + ( 2 * dalitz2[0] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz3412_best" ]->Fill( dalitzY2, dalitz2[2], scale );
			dalitzY3 = ( dalitz2[0] + ( 2 * dalitz2[1] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz3412_best" ]->Fill( dalitzY3, dalitz2[0], scale );
			dalitzY4 = ( dalitz2[2] + ( 2 * dalitz2[1] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz3412_best" ]->Fill( dalitzY4, dalitz2[2], scale );
			dalitzY5 = ( dalitz2[0] + ( 2 * dalitz2[2] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz3412_best" ]->Fill( dalitzY5, dalitz2[0], scale );
			dalitzY6 = ( dalitz2[1] + ( 2 * dalitz2[2] ) ) / TMath::Sqrt(3);
			histos2D_[ "dalitz3412_best" ]->Fill( dalitzY6, dalitz2[1], scale );
			*/

			if ( passcutsdR ) {

				histos1D_[ "jet4Pt_allCuts" ]->Fill( j4.Pt(), scale );
				histos1D_[ "massAve_allCuts" ]->Fill( avgMass, scale );
				histos1D_[ "massRes_allCuts" ]->Fill( massRes, scale );
				histos1D_[ "deltaEta_allCuts" ]->Fill( TMath::Abs( eta1 - eta2 ), scale );
				histos1D_[ "minDeltaR_allCuts" ]->Fill( minDeltaR, scale  );
				histos1D_[ "HT_allCuts" ]->Fill( HT );
				histos2D_[ "deltavsMassAve_allCuts" ]->Fill( avgMass, delta1, scale  );
				histos2D_[ "deltavsMassAve_allCuts" ]->Fill( avgMass, delta2, scale  );

				/*histos1D_[ "polAngle13412_allCuts" ]->Fill( cosPhi13412 );
				histos1D_[ "polAngle31234_allCuts" ]->Fill( cosPhi31234 );
				histos2D_[ "polAngle13412vs31234_allCuts" ]->Fill( cosPhi13412, cosPhi31234, scale );

				histos1D_[ "mu1_allCuts" ]->Fill( dalitz1[0], scale );
				histos1D_[ "mu2_allCuts" ]->Fill( dalitz1[1], scale );
				histos1D_[ "mu3_allCuts" ]->Fill( dalitz1[2], scale );
				histos2D_[ "mu1234_allCuts" ]->Fill( dalitz1[0], dalitz1[2], scale );
				histos2D_[ "mu1234_allCuts" ]->Fill( dalitz1[1], dalitz1[2], scale );
				histos2D_[ "mu1234_allCuts" ]->Fill( dalitz1[0], dalitz1[1], scale );

				histos2D_[ "dalitz1234_allCuts" ]->Fill( dalitzX1, dalitz1[1], scale );
				histos2D_[ "dalitz1234_allCuts" ]->Fill( dalitzX2, dalitz1[2], scale );
				histos2D_[ "dalitz1234_allCuts" ]->Fill( dalitzX3, dalitz1[0], scale );
				histos2D_[ "dalitz1234_allCuts" ]->Fill( dalitzX4, dalitz1[2], scale );
				histos2D_[ "dalitz1234_allCuts" ]->Fill( dalitzX5, dalitz1[0], scale );
				histos2D_[ "dalitz1234_allCuts" ]->Fill( dalitzX6, dalitz1[1], scale );

				histos1D_[ "mu4_allCuts" ]->Fill( dalitz2[0], scale );
				histos1D_[ "mu5_allCuts" ]->Fill( dalitz2[1], scale );
				histos1D_[ "mu6_allCuts" ]->Fill( dalitz2[2], scale );
				histos2D_[ "mu3412_allCuts" ]->Fill( dalitz2[0], dalitz2[2], scale );
				histos2D_[ "mu3412_allCuts" ]->Fill( dalitz2[1], dalitz2[2], scale );
				histos2D_[ "mu3412_allCuts" ]->Fill( dalitz2[0], dalitz2[1], scale );

				histos2D_[ "dalitz3412_allCuts" ]->Fill( dalitzY1, dalitz2[1], scale );
				histos2D_[ "dalitz3412_allCuts" ]->Fill( dalitzY2, dalitz2[2], scale );
				histos2D_[ "dalitz3412_allCuts" ]->Fill( dalitzY3, dalitz2[0], scale );
				histos2D_[ "dalitz3412_allCuts" ]->Fill( dalitzY4, dalitz2[2], scale );
				histos2D_[ "dalitz3412_allCuts" ]->Fill( dalitzY5, dalitz2[0], scale );
				histos2D_[ "dalitz3412_allCuts" ]->Fill( dalitzY6, dalitz2[1], scale );*/
			}

		}
	}
	JETS.clear();
}


// ------------ method called once each job just before starting event loop  ------------
void RUNAnalysis::beginJob() {

	RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
	RUNAtree->Branch( "jetsPt", "vector<float>", &jetsPt);
	RUNAtree->Branch( "jetsEta", "vector<float>", &jetsEta);
	RUNAtree->Branch( "jetsPhi", "vector<float>", &jetsPhi);
	RUNAtree->Branch( "jetsE", "vector<float>", &jetsE);

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
	histos1D_[ "jetMass" ] = fs_->make< TH1D >( "jetMass", "jetMass", 50, 0., 500. );
	histos1D_[ "jetMass" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 150, 0., 1500. );
	histos1D_[ "HT" ]->Sumw2();
	histos1D_[ "NPV" ] = fs_->make< TH1D >( "NPV", "NPV", 80, 0., 80. );
	histos1D_[ "NPV" ]->Sumw2();


	histos1D_[ "jetPt_triggerCuts" ] = fs_->make< TH1D >( "jetPt_triggerCuts", "jetPt_triggerCuts", 100, 0., 1000. );
	histos1D_[ "jetPt_triggerCuts" ]->Sumw2();
	histos1D_[ "jetEta_triggerCuts" ] = fs_->make< TH1D >( "jetEta_triggerCuts", "jetEta_triggerCuts", 100, -5., 5. );
	histos1D_[ "jetEta_triggerCuts" ]->Sumw2();
	histos1D_[ "jetNum_triggerCuts" ] = fs_->make< TH1D >( "jetNum_triggerCuts", "jetNum_triggerCuts", 10, 0., 10. );
	histos1D_[ "jetNum_triggerCuts" ]->Sumw2();
	histos1D_[ "jetMass_triggerCuts" ] = fs_->make< TH1D >( "jetMass_triggerCuts", "jetMass_triggerCuts", 50, 0., 500. );
	histos1D_[ "jetMass_triggerCuts" ]->Sumw2();
	histos1D_[ "HT_triggerCuts" ] = fs_->make< TH1D >( "HT_triggerCuts", "HT_triggerCuts", 150, 0., 1500. );
	histos1D_[ "HT_triggerCuts" ]->Sumw2();
	histos1D_[ "NPV_triggerCuts" ] = fs_->make< TH1D >( "NPV_triggerCuts", "NPV_triggerCuts", 80, 0., 80. );
	histos1D_[ "NPV_triggerCuts" ]->Sumw2();

	histos1D_[ "jet4Pt_best" ] = fs_->make< TH1D >( "jet4Pt_best", "jet4Pt_best", 100, 0., 1000. );
	histos1D_[ "jet4Pt_best" ]->Sumw2();
	histos1D_[ "massAve_best" ] = fs_->make< TH1D >( "massAve_best", "massAve_best", 50, 0., 500. );
	histos1D_[ "massAve_best" ]->Sumw2();
	histos1D_[ "massRes_best" ] = fs_->make< TH1D >( "massRes_best", "massRes_best", 50, 0., 2. );
	histos1D_[ "massRes_best" ]->Sumw2();
	histos1D_[ "deltaEta_best" ] = fs_->make< TH1D >( "deltaEta_best", "deltaEta_best", 400, 0., 10. );
	histos1D_[ "deltaEta_best" ]->Sumw2();
	histos1D_[ "minDeltaR_best" ] = fs_->make< TH1D >( "minDeltaR_best", "minDeltaR_best", 400, 0., 10. );
	histos1D_[ "minDeltaR_best" ]->Sumw2();
	histos1D_[ "HT_best" ] = fs_->make< TH1D >( "HT_best", "HT_best", 150, 0., 1500. );
	histos1D_[ "HT_best" ]->Sumw2();
	histos2D_[ "deltavsMassAve_best" ] = fs_->make< TH2D >( "deltavsMassAve_best", "deltavsMassAve_best", 200, 0., 2000.,  300, -500., 1000. );
	histos2D_[ "deltavsMassAve_best" ]->Sumw2();

	/*histos1D_[ "polAngle13412_best" ] = fs_->make< TH1D >( "polAngle13412_best", "polAngle13412_best", 20, 0., 1. );
	histos1D_[ "polAngle13412_best" ]->Sumw2();
	histos1D_[ "polAngle31234_best" ] = fs_->make< TH1D >( "polAngle31234_best", "polAngle31234_best", 20, 0., 1. );
	histos1D_[ "polAngle31234_best" ]->Sumw2();
	histos2D_[ "polAngle13412vs31234_best" ] = fs_->make< TH2D >( "polAngle13412vs31234_best", "polAngle13412vs31234_best", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "polAngle13412vs31234_best" ]->Sumw2();
	histos1D_[ "mu1_best" ] = fs_->make< TH1D >( "mu1_best", "mu1_best", 150, 0., 1.5 );
	histos1D_[ "mu1_best" ]->Sumw2();
	histos1D_[ "mu2_best" ] = fs_->make< TH1D >( "mu2_best", "mu2_best", 150, 0., 1.5 );
	histos1D_[ "mu2_best" ]->Sumw2();
	histos1D_[ "mu3_best" ] = fs_->make< TH1D >( "mu3_best", "mu3_best", 150, 0., 1.5 );
	histos1D_[ "mu3_best" ]->Sumw2();
	histos2D_[ "mu1234_best" ] = fs_->make< TH2D >( "mu1234_best", "mu1234_best", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "mu1234_best" ]->Sumw2();
	histos2D_[ "dalitz1234_best" ] = fs_->make< TH2D >( "dalitz1234_best", "dalitz1234_best", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "dalitz1234_best" ]->Sumw2();
	histos1D_[ "mu4_best" ] = fs_->make< TH1D >( "mu4_best", "mu4_best", 150, 0., 1.5 );
	histos1D_[ "mu4_best" ]->Sumw2();
	histos1D_[ "mu5_best" ] = fs_->make< TH1D >( "mu5_best", "mu5_best", 150, 0., 1.5 );
	histos1D_[ "mu5_best" ]->Sumw2();
	histos1D_[ "mu6_best" ] = fs_->make< TH1D >( "mu6_best", "mu6_best", 150, 0., 1.5 );
	histos1D_[ "mu6_best" ]->Sumw2();
	histos2D_[ "mu3412_best" ] = fs_->make< TH2D >( "mu3412_best", "mu3412_best", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "mu3412_best" ]->Sumw2();
	histos2D_[ "dalitz3412_best" ] = fs_->make< TH2D >( "dalitz3412_best", "dalitz3412_best", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "dalitz3412_best" ]->Sumw2();*/

	histos1D_[ "HT_allCuts" ] = fs_->make< TH1D >( "HT_allCuts", "HT_allCuts", 150, 0., 1500. );
	histos1D_[ "HT_allCuts" ]->Sumw2();
	histos1D_[ "jet4Pt_allCuts" ] = fs_->make< TH1D >( "jet4Pt_allCuts", "jet4Pt_allCuts", 100, 0., 1000. );
	histos1D_[ "jet4Pt_allCuts" ]->Sumw2();
	histos1D_[ "massAve_allCuts" ] = fs_->make< TH1D >( "massAve_allCuts", "massAve_allCuts", 50, 0., 500. );
	histos1D_[ "massAve_allCuts" ]->Sumw2();
	histos1D_[ "massRes_allCuts" ] = fs_->make< TH1D >( "massRes_allCuts", "massRes_allCuts", 50, 0., 2. );
	histos1D_[ "massRes_allCuts" ]->Sumw2();
	histos1D_[ "deltaEta_allCuts" ] = fs_->make< TH1D >( "deltaEta_allCuts", "deltaEta_allCuts", 400, 0., 10. );
	histos1D_[ "deltaEta_allCuts" ]->Sumw2();
	histos1D_[ "minDeltaR_allCuts" ] = fs_->make< TH1D >( "minDeltaR_allCuts", "minDeltaR_allCuts", 400, 0., 10. );
	histos1D_[ "minDeltaR_allCuts" ]->Sumw2();
	histos2D_[ "deltavsMassAve_allCuts" ] = fs_->make< TH2D >( "deltavsMassAve_allCuts", "deltavsMassAve_allCuts", 200, 0., 2000.,  300, -500., 1000. );
	histos2D_[ "deltavsMassAve_allCuts" ]->Sumw2();

	/*histos1D_[ "polAngle13412_allCuts" ] = fs_->make< TH1D >( "polAngle13412_allCuts", "polAngle13412_allCuts", 20, 0., 1. );
	histos1D_[ "polAngle13412_allCuts" ]->Sumw2();
	histos1D_[ "polAngle31234_allCuts" ] = fs_->make< TH1D >( "polAngle31234_allCuts", "polAngle31234_allCuts", 20, 0., 1. );
	histos1D_[ "polAngle31234_allCuts" ]->Sumw2();
	histos2D_[ "polAngle13412vs31234_allCuts" ] = fs_->make< TH2D >( "polAngle13412vs31234_allCuts", "polAngle13412vs31234_allCuts", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "polAngle13412vs31234_allCuts" ]->Sumw2();
	histos1D_[ "mu1_allCuts" ] = fs_->make< TH1D >( "mu1_allCuts", "mu1_allCuts", 150, 0., 1.5 );
	histos1D_[ "mu1_allCuts" ]->Sumw2();
	histos1D_[ "mu2_allCuts" ] = fs_->make< TH1D >( "mu2_allCuts", "mu2_allCuts", 150, 0., 1.5 );
	histos1D_[ "mu2_allCuts" ]->Sumw2();
	histos1D_[ "mu3_allCuts" ] = fs_->make< TH1D >( "mu3_allCuts", "mu3_allCuts", 150, 0., 1.5 );
	histos1D_[ "mu3_allCuts" ]->Sumw2();
	histos2D_[ "mu1234_allCuts" ] = fs_->make< TH2D >( "mu1234_allCuts", "mu1234_allCuts", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "mu1234_allCuts" ]->Sumw2();
	histos2D_[ "dalitz1234_allCuts" ] = fs_->make< TH2D >( "dalitz1234_allCuts", "dalitz1234_allCuts", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "dalitz1234_allCuts" ]->Sumw2();
	histos1D_[ "mu4_allCuts" ] = fs_->make< TH1D >( "mu4_allCuts", "mu4_allCuts", 150, 0., 1.5 );
	histos1D_[ "mu4_allCuts" ]->Sumw2();
	histos1D_[ "mu5_allCuts" ] = fs_->make< TH1D >( "mu5_allCuts", "mu5_allCuts", 150, 0., 1.5 );
	histos1D_[ "mu5_allCuts" ]->Sumw2();
	histos1D_[ "mu6_allCuts" ] = fs_->make< TH1D >( "mu6_allCuts", "mu6_allCuts", 150, 0., 1.5 );
	histos1D_[ "mu6_allCuts" ]->Sumw2();
	histos2D_[ "mu3412_allCuts" ] = fs_->make< TH2D >( "mu3412_allCuts", "mu3412_allCuts", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "mu3412_allCuts" ]->Sumw2();
	histos2D_[ "dalitz3412_allCuts" ] = fs_->make< TH2D >( "dalitz3412_allCuts", "dalitz3412_allCuts", 150, 0., 1.5, 150, 0., 1.5 );
	histos2D_[ "dalitz3412_allCuts" ]->Sumw2();*/



	cutLabels.push_back("Processed");
	cutLabels.push_back("Trigger");
	cutLabels.push_back("HT");
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

void RUNAnalysis::clearVariables() {

	jetsPt->clear();
	jetsEta->clear();
	jetsPhi->clear();
	jetsE->clear();

}

void RUNAnalysis::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("scale", 1);
	desc.add<double>("cutMassRes", 1);
	desc.add<double>("cutDelta", 1);
	desc.add<double>("cutEtaBand", 1);
	desc.add<double>("cutJetPt", 1);
	desc.add<double>("cutHT", 1);
	desc.add<bool>("bjSample", false);
	desc.add<string>("HLTtriggerOne", "HLT_PFHT800");
	desc.add<string>("HLTtriggerTwo", "HLT_PFHT800");

	desc.add<InputTag>("Lumi", 	InputTag("eventInfo:evtInfoLumiBlock"));
	desc.add<InputTag>("Run", 	InputTag("eventInfo:evtInfoRunNumber"));
	desc.add<InputTag>("Event", 	InputTag("eventInfo:evtInfoEventNumber"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK4:jetAK4Pt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK4:jetAK4Eta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK4:jetAK4Phi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK4:jetAK4E"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK4:jetAK4Mass"));
	desc.add<InputTag>("jetCSV", 	InputTag("jetsAK4:jetAK4CSV"));
	desc.add<InputTag>("jetCSVV1", 	InputTag("jetsAK4:jetAK4CSVV1"));
	desc.add<InputTag>("NPV", 	InputTag("eventUserData:npv"));
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
DEFINE_FWK_MODULE(RUNAnalysis);
