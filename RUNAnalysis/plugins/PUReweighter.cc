#include "RUNA/RUNAnalysis/interface/PUReweighter.h"


//==============================================================================================
// Get weight factor dependent on number of added PU interactions
float PUReweighter::getPUWeight(const int trueNInt, std::vector<int> bunchCrossing ){

	//std::vector<float> puWeigths_;
	//generateWeights( nameOfDataDistribution );

	float trueNPV = -1;
	for (unsigned int i = 0; i < bunchCrossing.size(); i++) {
		if( bunchCrossing[i] == 0 ) trueNPV = trueNInt; 
	}
	float w = LumiWeights_.weight( trueNPV );
	return w;
}

//==============================================================================================
// Generate weights for given data PU distribution
// Code adapted from: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupReweighting
// weights for Spring16MC are taken from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py
void PUReweighter::generateWeights(const std::string& nameOfDataDistribution) {

	// Get data distribution from file
	TFile file(nameOfDataDistribution.c_str(), "READ");
	TH1* data_npu_estimated = NULL;
	file.GetObject("pileup",data_npu_estimated);
	if( data_npu_estimated == NULL ) {
		std::cerr << "\n\nERROR in PUReweighter: Histogram 'pileup' does not exist in file '" << nameOfDataDistribution << "'\n.";
		throw std::exception();
	}
	data_npu_estimated->SetDirectory(0);
	file.Close();

	// Store probabilites for each pu bin
	unsigned int trueNIntMax = 0;

	trueNIntMax = 50;
	float npuWinter15_25ns[ trueNIntMax ] = {
		0.000829312873542,
 		0.00124276120498,
 		0.00339329181587,
 		0.00408224735376,
 		0.00383036590008,
		0.00659159288946,
 		0.00816022734493,
 		0.00943640833116,
 		0.0137777376066,
 		0.017059392038,
 		0.0213193035468,
 		0.0247343174676,
 		0.0280848773878,
 		0.0323308476564,
 		0.0370394341409,
 		0.0456917721191,
 		0.0558762890594,
 		0.0576956187107,
 		0.0625325287017,
 		0.0591603758776,
 		0.0656650815128,
 		0.0678329011676,
 		0.0625142146389,
 		0.0548068448797,
 		0.0503893295063,
 		0.040209818868,
 		0.0374446988111,
 		0.0299661572042,
 		0.0272024759921,
 		0.0219328403791,
 		0.0179586571619,
 		0.0142926728247,
 		0.00839941654725,
 		0.00522366397213,
 		0.00224457976761,
 		0.000779274977993,
 		0.000197066585944,
 		7.16031761328e-05,
 		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
 		0.0,
 		0.0,
		0.0 
	};

	// Check that binning of data-profile matches MC scenario
	if( trueNIntMax != static_cast<unsigned int>(data_npu_estimated->GetNbinsX()) ) {
		std::cerr << "\n\nERROR number of bins (" << data_npu_estimated->GetNbinsX() << ") in data PU-profile does not match number of bins (" << trueNIntMax << ")" << std::endl;
		throw std::exception();
	}

	std::vector<float> result(trueNIntMax,0.);
	std::vector<float> puMC;
	std::vector<float> puData;
	for(unsigned int npu = 0; npu < trueNIntMax; ++npu) {
		puMC.push_back( npuWinter15_25ns[npu] );
		puData.push_back( data_npu_estimated->GetBinContent(data_npu_estimated->GetXaxis()->FindBin(npu)) );
	}

	LumiWeights_ = edm::LumiReWeighting(puMC, puData);
}

