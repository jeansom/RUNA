// system include files
#include <memory>
#include <TH1D.h>
#include <TH2D.h>
#include <TFile.h>
#include <TLorentzVector.h>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondFormats/BTauObjects/interface/BTagCalibrationReader.h"

using namespace edm;
using namespace std;

//
// class declaration
//

class QCDAnalyzer : public EDAnalyzer {
   public:
      explicit QCDAnalyzer(const ParameterSet&);
      ~QCDAnalyzer();

   private:
      virtual void analyze(const Event&, const EventSetup&) override;
      // ----------member data ---------------------------

      Service<TFileService> fs_;
	//map< string, TH1D* > histos1D_;
	//map< string, TH2D* > histos2D_;
     
       TFile * f_EffMap_AK4 = new TFile("EfficiencyMaps.root");  //Name of the Efficiency Map file

      // Book a set of histograms      
      TH1D * h_bjet_pt_AK4 = fs_->make<TH1D>("h_bjet_pt_AK4","",50,0.,1000.);
      TH1D * h_bjet_pt_wt_AK4 = fs_->make<TH1D>("h_bjet_pt_wt_AK4","",50,0.,1000.);
      TH1D * h_weights_AK4 = fs_->make<TH1D>("h_weights_AK4","",50,-2,2);
      TH1D * h_bjet_wt_errorsquared_AK4 = fs_->make<TH1D>("h_bjet_wt_errorsquared_AK4","",50,0.,1000.);

      EDGetTokenT<reco::VertexCollection> vtxToken_;
      EDGetTokenT<pat::MuonCollection> muonToken_;
      EDGetTokenT<pat::ElectronCollection> electronToken_;
      EDGetTokenT<pat::TauCollection> tauToken_;
      EDGetTokenT<pat::PhotonCollection> photonToken_;
      EDGetTokenT<pat::JetCollection> jetToken_;
      EDGetTokenT<pat::JetCollection> ak8jetToken_;
      EDGetTokenT<pat::JetCollection> puppijetToken_;
      EDGetTokenT<pat::METCollection> metToken_;

      TH2D * h2_EffMapB_AK4 = (TH2D*)f_EffMap_AK4->Get("efficiency_b"); //Name of the b efficiency map
      TH2D * h2_EffMapC_AK4 = (TH2D*)f_EffMap_AK4->Get("efficiency_c"); //Name of the c efficiency map
      TH2D * h2_EffMapUDSG_AK4 = (TH2D*)f_EffMap_AK4->Get("efficiency_udsg"); //Name of the udsg efficiency map
};

QCDAnalyzer::QCDAnalyzer(const ParameterSet& iConfig):
    vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<InputTag>("vertices"))),
    muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<InputTag>("muons"))),
    electronToken_(consumes<pat::ElectronCollection>(iConfig.getParameter<InputTag>("electrons"))),
    tauToken_(consumes<pat::TauCollection>(iConfig.getParameter<InputTag>("taus"))),
    photonToken_(consumes<pat::PhotonCollection>(iConfig.getParameter<InputTag>("photons"))),
    jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("jets"))),
    ak8jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("ak8jets"))),
    puppijetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("puppijets"))),
    metToken_(consumes<pat::METCollection>(iConfig.getParameter<InputTag>("mets")))
{
}

QCDAnalyzer::~QCDAnalyzer()
{
}

void
QCDAnalyzer::analyze(const Event& iEvent, const EventSetup& iSetup)
{
    Handle<reco::VertexCollection> vertices;
    iEvent.getByToken(vtxToken_, vertices);
    if (vertices->empty()) return; // skip the event if no PV found
   
    Handle<pat::MuonCollection> muons;
    iEvent.getByToken(muonToken_, muons);
    Handle<pat::ElectronCollection> electrons;
    iEvent.getByToken(electronToken_, electrons);
    Handle<pat::PhotonCollection> photons;
    iEvent.getByToken(photonToken_, photons);
    Handle<pat::TauCollection> taus;
    iEvent.getByToken(tauToken_, taus);
    Handle<pat::JetCollection> jets;
    iEvent.getByToken(jetToken_, jets);
    Handle<pat::JetCollection> ak8jets;
    iEvent.getByToken(ak8jetToken_, ak8jets);
    Handle<pat::JetCollection> puppijets;
    iEvent.getByToken(puppijetToken_, puppijets);
    Handle<pat::METCollection> mets;
    iEvent.getByToken(metToken_, mets);

    //Begin scale factor implementation

    float wtbtag = 1.;
    float wtbtagError = 1.;
    
    float mcTag = 1.;
    float mcNoTag = 1.;
    float dataTag = 1.;
    float dataNoTag = 1.;

    float err1 = 0; 
    float err2 = 0; 
    float err3 = 0; 
    float err4 = 0; 

    BTagCalibration calib_csv("csv","CSV.csv");
    BTagCalibrationReader reader(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "comb",                 //measurement type
				 "central");             //systematics type
    BTagCalibrationReader readerUp(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "comb",                 //measurement type
				 "up");             //systematics type

    for (const pat::Jet &jet : *jets) {

      //cout << "ak4 CSV\t" << jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") << endl;
      //cout << "ak4 CSVV1\t" << jet.bDiscriminator("pfCombinedSecondaryVertexV1BJetTags") << endl;

	    float csv = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
	    int partonFlavor = abs(jet.partonFlavour());
	    float eta = fabs(jet.eta());
	    float pt = fabs(jet.pt());
	    if( eta>2.4) continue;
	    if( partonFlavor==0) continue; //for jets with flavor 0, we ignore.
	    if( csv >= 1 || csv < 0 ) continue;

	    float eff = 1;
	    if( partonFlavor==5 ) {
	      ///the pt/eta dependent efficiency for b-tag for "b jet"
	      eff = h2_EffMapB_AK4->GetBinContent( h2_EffMapB_AK4->GetXaxis()->FindBin(pt), h2_EffMapB_AK4->GetYaxis()->FindBin(fabs(eta)) );
	    }else if( partonFlavor==4){
	      ///the pt/eta dependent efficiency for b-tag for "c jet"
	      eff = h2_EffMapC_AK4->GetBinContent( h2_EffMapC_AK4->GetXaxis()->FindBin(pt), h2_EffMapC_AK4->GetYaxis()->FindBin(fabs(eta)) );
	    }else{
	      ///the pt/eta dependent efficiency for b-tag for "light jet"
	      eff = h2_EffMapUDSG_AK4->GetBinContent( h2_EffMapUDSG_AK4->GetXaxis()->FindBin(pt), h2_EffMapUDSG_AK4->GetYaxis()->FindBin(fabs(eta)) );
	    }
	    bool istag = csv > .8/* csv value*/ && eta<2.4 ;
	    float SF = 0;
	    float SFup = 0;
	    float SFerr = 0;
	    
	    bool greaterThan800 = (pt>800);
	    if (greaterThan800) pt = 800;
	    
	    bool lessThan20 = (pt<20);
	    if (lessThan20) pt=20;
	   
	    if ( partonFlavor == 5 ) {

	      SF = reader.eval(BTagEntry::FLAV_B, 
			       eta,
			       pt);
	      SFup = readerUp.eval(BTagEntry::FLAV_B,
				  eta,
				  pt);
	      SFerr = (SFup - SF);
	      if (greaterThan800 || lessThan20) SFerr*=2;
	      
	    }
	    else if ( partonFlavor == 4 ) {
	      SF = reader.eval(BTagEntry::FLAV_C,
			       eta,
			       pt);
	      SFup = readerUp.eval(BTagEntry::FLAV_C,
				   eta,
				   pt);
	      SFerr = 2*(SFup - SF);
	      if (greaterThan800 || lessThan20) SFerr*=2;
	       }
	    else {
	      SF = reader.eval(BTagEntry::FLAV_UDSG,
			       eta,
			       pt);
	      SFup = readerUp.eval(BTagEntry::FLAV_UDSG,
				   eta,
				   pt);
	      SFerr = SFup - SF;
	      if (greaterThan800 || lessThan20) SFerr*=2;
	    }
	    
	    if( SF == 0 || SFerr == 0 ) continue;
	    if(istag){
	      mcTag *= eff;
	      dataTag *= eff*SF;

	      if(partonFlavor==5 || partonFlavor == 4) err1 += SFerr/SF; //correlated for b/c
	      else err3 += SFerr/SF; //correlated for light
	      
	    }else{
	      mcNoTag *= (1-eff);
	      dataNoTag *= (1-eff*SF);

	      if(partonFlavor==5 || partonFlavor==4) err2 += (-eff*SFerr)/(1-eff*SF); // correlated for b/c
	      else err4 += (-eff*SFerr)/(1-eff*SF); //correlated for light
	      
	    }

	    /*cout << "AK4 SF " << SF << endl;
	      cout << "AK4 SFup " << SFup << endl;
	      cout << "AK4 SFerr " << SFerr << endl;
	      cout << "AK4 pt " << pt << endl;
	      cout << "AK4 eta " << eta << endl;
	      cout << "AK4 partonFlavor " << partonFlavor << endl;*/
    }
    wtbtag = (dataNoTag * dataTag) / (mcNoTag * mcTag);
    wtbtagError = sqrt( pow(err1+err2,2) + pow( err3 + err4, 2)) * wtbtag; //un-correlated for b/c and light
    float errsquared = pow(wtbtag,2) + pow(wtbtagError,2); 
    h_weights_AK4->Fill(wtbtag);
    //cout << "AK4 wtbtag: " << wtbtag << endl;

    //cout << "AK4 wtbtagError: " << wtbtagError << endl;
    
    for( const pat::Jet &jet : *jets) {
      if( jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") > .8 && !(fabs(jet.eta()) > 2.4) && jet.bDiscriminator("pfCombinedIncludsiveSecondaryVertexV2BJetTags") <= 1 ) {
	h_bjet_wt_errorsquared_AK4->Fill(jet.pt(),errsquared);
      }
    }


    for (const pat::Jet &jet : *jets) {
      if( jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>.8 && !(fabs(jet.eta()) > 2.4) && jet.bDiscriminator("pfCombinedIncludsiveSecondaryVertexV2BJetTags") <= 1 ) {
	h_bjet_pt_AK4->Fill(jet.pt());
	h_bjet_pt_wt_AK4->Fill(jet.pt(),wtbtag);
      }
    }
}



//define this as a plug-in
DEFINE_FWK_MODULE(QCDAnalyzer);
