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

typedef struct Jet_struc {
	TLorentzVector p4;
	TLorentzVector subjet0;
	TLorentzVector subjet1;
	double mass;
	double tau1;
	double tau2;
	double tau3;
	double btagCSV;
} JETtype;


static float massAverage( float m1, float m2 ){ return ( (m1 + m2)/2 ); }

static float massAsymmetry( float m1, float m2 ){ return abs( ( m1 - m2 )/( m1 + m2 ) ); }

static float deltaValue( float p1, float p2 ){ return abs( p1 - p2 ); }

static float calculateCosThetaStar( TLorentzVector jet1, TLorentzVector jet2 ){

	TLorentzVector tmpCM = jet1 + jet2;
	jet1.Boost( -tmpCM.BoostVector() );
	jet2.Boost( -tmpCM.BoostVector() );
	float valueCosThetaStar = TMath::Abs( ( jet1.Px() * tmpCM.Px() +  jet1.Py() * tmpCM.Py() + jet1.Pz() * tmpCM.Pz() ) / (jet1.E() * tmpCM.E() ) ) ;

	return valueCosThetaStar;
}

static bool loosejetID( double jetE, double jecFactor, double neutralHadronEnergy, double neutralEmEnergy, double chargedHadronEnergy, double chargedEmEnergy, int chargedHadronMultiplicity, int neutralHadronMultiplicity, double chargedMultiplicity ){ 

	double jec = 1. / ( jecFactor * jetE );
	double nhf = neutralHadronEnergy * jec;
	double nEMf = neutralEmEnergy * jec;
	double chf = chargedHadronEnergy * jec;
	//double muf = muonEnergy * jec;
	double cEMf = chargedEmEnergy * jec;
	int numConst = chargedHadronMultiplicity + neutralHadronMultiplicity ;  //// REMEMBER TO INCLUDE # of constituents
	double chm = chargedMultiplicity * jec;

	//bool idL = ( (nhf<0.99) && (nEMf<0.99) && (muf<0.8) && (cEMf<0.9) );  /// 8TeV recommendation
	bool idL = ( (nhf<0.99) && (nEMf<0.99) && (numConst>1) && (chf>0) && (chm>0) && (cEMf<0.99) );

	return idL;
}

static bool checkTriggerBits( Handle<vector<string>> triggerNames, Handle<vector<float>> triggerBits, TString HLTtrigger  ){

	float triggerFired = 0;
	for (size_t t = 0; t < triggerNames->size(); t++) {
		if ( TString( (*triggerNames)[t] ).Contains( HLTtrigger ) ) {
			triggerFired = (*triggerBits)[t];
			//LogWarning("triggerbit") << (*triggerNames)[t] << " " <<  (*triggerBits)[t];
		}
	}
	if ( HLTtrigger.Contains( "NOTRIGGER" ) ) triggerFired = 1;

	return triggerFired;
}	

static bool checkORListOfTriggerBits( Handle<vector<string>> triggerNames, Handle<vector<float>> triggerBits, vector<string>  triggerPass  ){

	vector<bool> triggersFired;
	for (size_t t = 0; t < triggerPass.size(); t++) {
		bool triggerFired = checkTriggerBits( triggerNames, triggerBits, triggerPass[t] );
		triggersFired.push_back( triggerFired );
		//if ( triggerFired ) LogWarning("test") << triggerPass[t] << " " << triggerFired;
	}
	
	bool ORTriggers = !none_of(triggersFired.begin(), triggersFired.end(), [](bool v) { return v; }); 
	//if( ORTriggers ) LogWarning("OR") << std::none_of(triggersFired.begin(), triggersFired.end(), [](bool v) { return v; }); 
	
	return ORTriggers;
}
