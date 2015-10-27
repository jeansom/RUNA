#include "TH1.h"
#include "TFile.h"

void addErrors()
{
  for( int pt = 1; pt < 1001; pt += 20 )
    {
      int bin = h_bjet_pt_wt->FindBin(pt);
      float err = sqrt(h_bjet_wt_errorsquared->GetBinContent(bin));
      h_bjet_pt_wt->SetBinError(bin,err);
    }
 
  return;
}
