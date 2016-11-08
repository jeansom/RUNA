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
// OLD!!!!!!!!! ----- weights for Winter15_25ns are taken from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py
// weights for Fall15MC are taken from https://github.com/cms-sw/cmssw/blob/CMSSW_7_6_X/SimGeneral/MixingModule/python/mix_2015_25ns_FallMC_matchData_PoissonOOTPU_cfi.py
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
/*                              4.8551E-07,
                              1.74806E-06,
                              3.30868E-06,
                              1.62972E-05,
                              4.95667E-05,
                              0.000606966,
                              0.003307249,
                              0.010340741,
                              0.022852296,
                              0.041948781,
                              0.058609363,
                              0.067475755,
                              0.072817826,
                              0.075931405,
                              0.076782504,
                              0.076202319,
                              0.074502547,
                              0.072355135,
                              0.069642102,
                              0.064920999,
                              0.05725576,
                              0.047289348,
                              0.036528446,
                              0.026376131,
                              0.017806872,
                              0.011249422,
                              0.006643385,
                              0.003662904,
                              0.001899681,
                              0.00095614,
                              0.00050028,
                              0.000297353,
                              0.000208717,
                              0.000165856,
                              0.000139974,
                              0.000120481,
                              0.000103826,
                              8.88868E-05,
                              7.53323E-05,
                              6.30863E-05,
                              5.21356E-05,
                              4.24754E-05,
                              3.40876E-05,
                              2.69282E-05,
                              2.09267E-05,
                              1.5989E-05,
                              4.8551E-06,
                              2.42755E-06,
                              4.8551E-07,
                              2.42755E-07,
                              1.21378E-07,
                              4.8551E-08};*/
		0.000108643,
                0.000388957,
                0.000332882,
                0.00038397,
                0.000549167,
                0.00105412,
                0.00459007,
                0.0210314,
                0.0573688,
                0.103986,
                0.142369,
                0.157729,
                0.147685,
                0.121027,
                0.08855,
                0.0582866,
                0.0348526,
                0.019457,
                0.0107907,
                0.00654313,
                0.00463195,
                0.00370927,
                0.0031137,
                0.00261141,
                0.00215499,
                0.00174491,
                0.00138268,
                0.00106731,
                0.000798828,
                0.00057785,
                0.00040336,
                0.00027161,
                0.000176535,
                0.00011092,
                6.75502e-05,
                4.00323e-05,
                2.32123e-05,
                1.32585e-05,
                7.51611e-06,
                4.25902e-06,
                2.42513e-06,
                1.39077e-06,
                8.02452e-07,
                4.64159e-07,
                2.67845e-07,
                1.5344e-07,
                8.68966e-08,
                4.84931e-08,
                2.6606e-08,
                1.433e-08};

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

