#ifndef PUReweighter_H
#define PUReweighter_H

#include <string>
#include <vector>
#include <iostream>

#include "TFile.h"
#include "TH1.h"
#include "TString.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"


class PUReweighter {
	private:
		int trueNIntMax_;
		edm::LumiReWeighting LumiWeights_ ;
	
	public:
		void generateWeights(const std::string& nameOfDataDistribution);
		float getPUWeight(const int trueNInt, const std::vector<int> bunchCrossing );

};


#endif //PUReweighter_H
