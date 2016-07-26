#include "TH1.h"
#include "TFile.h"
#include "TCanvas.h"

void MakePlots()
{
  
  TCanvas *c1 = new TCanvas(); 

  h_delta_r->Sumw2();
  h_delta_r->GetXaxis()->SetTitle("Delta R");
  h_delta_r->GetYaxis()->SetTitle("N Events");
  h_delta_r->SetTitle("h_delta_r");
  h_delta_r->Draw();
  c1->SaveAs("h_delta_r.pdf");

  h_delta_r_min->Sumw2();
  h_delta_r_min->GetXaxis()->SetTitle("Delta R");
  h_delta_r_min->GetYaxis()->SetTitle("N Events");
  h_delta_r_min->SetTitle("h_delta_r_min");
  h_delta_r_min->Draw();
  c1->SaveAs("h_delta_r_min.pdf");

  h_delta_r_2nd_min->Sumw2();
  h_delta_r_2nd_min->GetXaxis()->SetTitle("Delta R");
  h_delta_r_2nd_min->GetYaxis()->SetTitle("N Events");
  h_delta_r_2nd_min->SetTitle("h_delta_r_2nd_min");
  h_delta_r_2nd_min->Draw();
  c1->SaveAs("h_delta_r_2nd_min.pdf");

  h_delta_r_1st2nd_min->Sumw2();
  h_delta_r_1st2nd_min->GetXaxis()->SetTitle("Delta R");
  h_delta_r_1st2nd_min->GetYaxis()->SetTitle("N Events");
  h_delta_r_1st2nd_min->SetTitle("h_delta_r_1st2nd_min");
  h_delta_r_1st2nd_min->Draw();
  c1->SaveAs("h_delta_r_1st2nd_min.pdf");

  h_num_matches_foreach_AK8->Sumw2();
  h_num_matches_foreach_AK8->GetXaxis()->SetTitle("N Matches");
  h_num_matches_foreach_AK8->GetYaxis()->SetTitle("N Events");
  h_num_matches_foreach_AK8->SetTitle("h_num_matches_foreach_AK8");
  h_num_matches_foreach_AK8->Draw();
  c1->SaveAs("h_num_matched_foreach_AK8.pdf");

  h_delta_r_1st_v_2nd_min->Sumw2();
  h_delta_r_1st_v_2nd_min->GetXaxis()->SetTitle("Delta R Min");
  h_delta_r_1st_v_2nd_min->GetYaxis()->SetTitle("Delta R 2nd Min");
  h_delta_r_1st_v_2nd_min->SetTitle("h_delta_r_1st_v_2nd_min");
  h_delta_r_1st_v_2nd_min->Draw();
  c1->SaveAs("h_delta_r_1st_v_2nd_min.pdf");

  h_eta_all_true_bjet_AK8->Sumw2();
  h_eta_all_true_bjet_AK8->GetXaxis()->SetTitle("Eta");
  h_eta_all_true_bjet_AK8->GetYaxis()->SetTitle("N Events");
  h_eta_all_true_bjet_AK8->SetTitle("h_eta_all_true_bjet_AK8");
  h_eta_all_true_bjet_AK8->Draw();
  c1->SaveAs("h_eta_all_true_bjet_AK8.pdf");

  h_eta_all_true_bjet_AK4->Sumw2();
  h_eta_all_true_bjet_AK4->GetXaxis()->SetTitle("Eta");
  h_eta_all_true_bjet_AK4->GetYaxis()->SetTitle("N Events");
  h_eta_all_true_bjet_AK4->SetTitle("h_eta_all_true_bjet_AK4");
  h_eta_all_true_bjet_AK4->Draw();
  c1->SaveAs("h_eta_all_true_bjet_AK4.pdf");

  h_eta_true_bjet_with_match_AK8->Sumw2();
  h_eta_true_bjet_with_match_AK8->GetXaxis()->SetTitle("Eta");
  h_eta_true_bjet_with_match_AK8->GetYaxis()->SetTitle("N Events");
  h_eta_true_bjet_with_match_AK8->SetTitle("h_eta_true_bjet_with_match_AK8");
  h_eta_true_bjet_with_match_AK8->Draw();
  c1->SaveAs("h_eta_true_bjet_with_match_AK8.pdf");

  h_eta_true_bjet_with_match_AK4->Sumw2();
  h_eta_true_bjet_with_match_AK4->GetXaxis()->SetTitle("Eta");
  h_eta_true_bjet_with_match_AK4->GetYaxis()->SetTitle("N Events");
  h_eta_true_bjet_with_match_AK4->SetTitle("h_eta_true_bjet_with_match_AK4");
  h_eta_true_bjet_with_match_AK4->Draw();
  c1->SaveAs("h_eta_true_bjet_with_match_AK4.pdf");

  h_pt_bjet_with_match_AK8->Sumw2();
  h_pt_bjet_with_match_AK8->GetXaxis()->SetTitle("Pt");
  h_pt_bjet_with_match_AK8->GetYaxis()->SetTitle("N Events");
  h_pt_bjet_with_match_AK8->SetTitle("h_pt_true_bjet_with_match_AK8");
  h_pt_bjet_with_match_AK8->Draw();
  c1->SaveAs("h_pt_bjet_with_match_AK8.pdf");
  c1->SetLogy();
  c1->SaveAs("h_pt_bjet_with_match_AK8_Logy.pdf");
  c1->SetLogy(0);

  h_pt_all_true_bjet_AK8->Sumw2();
  h_pt_all_true_bjet_AK8->GetXaxis()->SetTitle("Pt");
  h_pt_all_true_bjet_AK8->GetYaxis()->SetTitle("N Events");
  h_pt_all_true_bjet_AK8->SetTitle("h_pt_all_true_bjet_AK8");
  h_pt_all_true_bjet_AK8->Draw();
  c1->SaveAs("h_pt_all_true_bjet_AK8.pdf");
  c1->SetLogy();
  c1->SaveAs("h_pt_all_true_bjet_AK8_Logy.pdf");
  c1->SetLogy(0);

  h_pt_bjet_with_match_AK4->Sumw2();
  h_pt_bjet_with_match_AK4->GetXaxis()->SetTitle("Pt");
  h_pt_bjet_with_match_AK4->GetYaxis()->SetTitle("N Events");
  h_pt_bjet_with_match_AK4->SetTitle("h_pt_bjet_with_match_AK4");
  h_pt_bjet_with_match_AK4->Draw();
  c1->SaveAs("h_pt_bjet_with_match_AK4.pdf");
  c1->SetLogy();
  c1->SaveAs("h_pt_bjet_with_match_AK4_Logy.pdf");
  c1->SetLogy(0);

  h_pt_all_true_bjet_AK4->Sumw2();
  h_pt_all_true_bjet_AK4->GetXaxis()->SetTitle("Pt");
  h_pt_all_true_bjet_AK4->GetYaxis()->SetTitle("N Events");
  h_pt_all_true_bjet_AK4->SetTitle("h_pt_all_true_bjet_AK4");
  h_pt_all_true_bjet_AK4->Draw();
  c1->SaveAs("h_pt_all_true_bjet_AK4.pdf");
  c1->SetLogy();
  c1->SaveAs("h_pt_all_true_bjet_AK4_Logy.pdf");
  c1->SetLogy(0);

  h_csv_all_true_bjet_AK8->Sumw2();
  h_csv_all_true_bjet_AK8->GetXaxis()->SetTitle("CSV");
  h_csv_all_true_bjet_AK8->GetYaxis()->SetTitle("N Events");
  h_csv_all_true_bjet_AK8->SetTitle("h_csv_all_true_bjet_AK8");
  h_csv_all_true_bjet_AK8->Draw();
  c1->SaveAs("h_csv_all_true_bjet_AK8.pdf");
  
  h_csv_all_true_bjet_AK4->Sumw2();
  h_csv_all_true_bjet_AK4->GetXaxis()->SetTitle("CSV");
  h_csv_all_true_bjet_AK4->GetYaxis()->SetTitle("N Events");
  h_csv_all_true_bjet_AK4->SetTitle("h_csv_all_true_bjet_AK4");
  h_csv_all_true_bjet_AK4->Draw();
  c1->SaveAs("h_csv_all_true_bjet_AK4.pdf");

  h_csv_AK8->Sumw2();
  h_csv_AK8->GetXaxis()->SetTitle("CSV");
  h_csv_AK8->GetYaxis()->SetTitle("N Events");
  h_csv_AK8->SetTitle("h_csv_AK8_match");
  h_csv_AK8->Draw();
  c1->SaveAs("h_csv_AK8.pdf");

  h_csv_AK4->Sumw2();
  h_csv_AK4->GetXaxis()->SetTitle("CSV");
  h_csv_AK4->GetYaxis()->SetTitle("N Events");
  h_csv_AK4->SetTitle("h_csv_AK4_match");
  h_csv_AK4->Draw();
  c1->SaveAs("h_csv_AK4.pdf");

  h_npv_matched_jet_events->Sumw2();
  h_npv_matched_jet_events->GetXaxis()->SetTitle("NPV");
  h_npv_matched_jet_events->GetYaxis()->SetTitle("N Events");
  h_npv_matched_jet_events->SetTitle("h_npv_matched_jet_events");
  h_npv_matched_jet_events->Draw();
  c1->SaveAs("h_npv_matched_jet_events.pdf");

  h_npv_all_events->Sumw2();
  h_npv_all_events->GetXaxis()->SetTitle("NPV");
  h_npv_all_events->GetYaxis()->SetTitle("N Events");
  h_npv_all_events->SetTitle("h_npv_all_events");
  h_npv_all_events->Draw();
  c1->SaveAs("h_npv_all_events.pdf");

  h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut->Sumw2();
  h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut->SetTitle("Matched AK8 jets passed csv8 AND cut");
  h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut->GetXaxis()->SetTitle("AK8 pt");
  h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut->GetYaxis()->SetTitle("N Events");
  h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut->Draw();
  c1->SaveAs("h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut.pdf");

  h_matchedjetAK8_pt_pass_csv8_cut->Sumw2();
  h_matchedjetAK8_pt_pass_csv8_cut->SetTitle("Matched AK8 jets ONLY passed csv8 cut");
  h_matchedjetAK8_pt_pass_csv8_cut->GetXaxis()->SetTitle("AK8 pt");
  h_matchedjetAK8_pt_pass_csv8_cut->GetYaxis()->SetTitle("N Events");
  h_matchedjetAK8_pt_pass_csv8_cut->Draw();
  c1->SaveAs("h_matchedjetAK8_pt_pass_ONLYcsv8_cut.pdf");

  h_matchedjetAK8_pt_pass_csv4_cut->Sumw2();
  h_matchedjetAK8_pt_pass_csv4_cut->SetTitle("Matched AK8 jets ONLY passed csv4 cut");
  h_matchedjetAK8_pt_pass_csv4_cut->GetXaxis()->SetTitle("AK8 pt");
  h_matchedjetAK8_pt_pass_csv4_cut->GetYaxis()->SetTitle("N Events");
  h_matchedjetAK8_pt_pass_csv4_cut->Draw();
  c1->SaveAs("h_matchedjetAK8_pt_pass_ONLYcsv4_cut.pdf");

  h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut->Sumw2();
  h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut->SetTitle("Matched AK4 jets passed csv8 AND cut");
  h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut->GetXaxis()->SetTitle("AK4 pt");
  h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut->GetYaxis()->SetTitle("N Events");
  h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut->Draw();
  c1->SaveAs("h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut.pdf");

  h_matchedjetAK4_pt_pass_csv8_cut->Sumw2();
  h_matchedjetAK4_pt_pass_csv8_cut->SetTitle("Matched AK4 jets ONLY passed csv8 cut");
  h_matchedjetAK4_pt_pass_csv8_cut->GetXaxis()->SetTitle("AK4 pt");
  h_matchedjetAK4_pt_pass_csv8_cut->GetYaxis()->SetTitle("N Events");
  h_matchedjetAK4_pt_pass_csv8_cut->Draw();
  c1->SaveAs("h_matchedjetAK4_pt_pass_ONLYcsv8_cut.pdf");

  h_matchedjetAK4_pt_pass_csv4_cut->Sumw2();
  h_matchedjetAK4_pt_pass_csv4_cut->SetTitle("Matched AK4 jets ONLY passed csv4 cut");
  h_matchedjetAK4_pt_pass_csv4_cut->GetXaxis()->SetTitle("AK4 pt");
  h_matchedjetAK4_pt_pass_csv4_cut->GetYaxis()->SetTitle("N Events");
  h_matchedjetAK4_pt_pass_csv4_cut->Draw();
  c1->SaveAs("h_matchedjetAK4_pt_pass_ONLYcsv4_cut.pdf");

  h_num_AK4->Sumw2();
  h_denom_AK4->Sumw2();
  h_num_AK4_bin_with_AK8pt->Sumw2();
  h_denom_AK4_bin_with_AK8pt->Sumw2();

  h_num_AK8->Sumw2();
  h_denom_AK8->Sumw2();
  h_num_AK8_bin_with_AK4pt->Sumw2();
  h_denom_AK8_bin_with_AK4pt->Sumw2();

  h_num_AK4->GetXaxis()->SetTitle("AK4 pt");
  h_num_AK4->GetYaxis()->SetTitle("N Events");
  h_num_AK4->SetTitle("h_num_AK4");

  h_num_AK4_bin_with_AK8pt->GetXaxis()->SetTitle("AK8 pt");
  h_num_AK4_bin_with_AK8pt->GetYaxis()->SetTitle("N Events");
  h_num_AK4_bin_with_AK8pt->SetTitle("h_num_AK4_bin_with_AK8pt");

  h_denom_AK4->GetXaxis()->SetTitle("AK4 pt");
  h_denom_AK4->GetYaxis()->SetTitle("N Events");
  h_denom_AK4->SetTitle("h_denom_AK4");

  h_denom_AK4_bin_with_AK8pt->GetXaxis()->SetTitle("AK8 pt");
  h_denom_AK4_bin_with_AK8pt->GetYaxis()->SetTitle("N Events");
  h_denom_AK4_bin_with_AK8pt->SetTitle("h_denom_AK4_bin_with_AK8pt");
 
  h_num_AK8->GetXaxis()->SetTitle("AK8 pt");
  h_num_AK8->GetYaxis()->SetTitle("N Events");
  h_num_AK8->SetTitle("h_num_AK8");
 
  h_num_AK8_bin_with_AK4pt->GetXaxis()->SetTitle("AK4 pt");
  h_num_AK8_bin_with_AK4pt->GetYaxis()->SetTitle("N Events");
  h_num_AK8_bin_with_AK4pt->SetTitle("h_num_AK8_bin_with_AK4pt");

  h_denom_AK8->GetXaxis()->SetTitle("AK8 pt");
  h_denom_AK8->GetYaxis()->SetTitle("N Events");
  h_denom_AK8->SetTitle("h_denom_AK8");

  h_denom_AK8_bin_with_AK4pt->GetXaxis()->SetTitle("AK4 pt");
  h_denom_AK8_bin_with_AK4pt->GetYaxis()->SetTitle("N Events");
  h_denom_AK8_bin_with_AK4pt->SetTitle("h_denom_AK8_bin_with_AK4pt");
  
  h_num_AK4->Draw();
  c1->SaveAs("h_num_AK4.pdf");
  c1->SetLogy();
  c1->SaveAs("h_num_AK4_Logy.pdf");
  c1->SetLogy(0);
  
  h_denom_AK4->Draw();
  c1->SaveAs("h_denom_AK4.pdf");
  c1->SetLogy();
  c1->SaveAs("h_denom_AK4_Logy.pdf");
  c1->SetLogy(0);
  
  h_num_AK4_bin_with_AK8pt->Draw();
  c1->SaveAs("h_num_AK4_bin_with_AK8pt.pdf");
  c1->SetLogy();
  c1->SaveAs("h_num_AK4_bin_with_AK8pt_Logy.pdf");
  c1->SetLogy(0);

  h_denom_AK4_bin_with_AK8pt->Draw();
  c1->SaveAs("h_denom_AK4_bin_with_AK8pt.pdf");
  c1->SetLogy();
  c1->SaveAs("h_denom_AK4_bin_with_AK8pt_Logy.pdf");
  c1->SetLogy(0);

  h_num_AK8->Draw();
  c1->SaveAs("h_num_AK8.pdf");
  c1->SetLogy();
  c1->SaveAs("h_num_AK8_Logy.pdf");
  c1->SetLogy(0);

  h_denom_AK8->Draw();
  c1->SaveAs("h_denom_AK8.pdf");
  c1->SetLogy();
  c1->SaveAs("h_denom_AK8_Logy.pdf");
  c1->SetLogy(0);

  h_num_AK8_bin_with_AK4pt->Draw();
  c1->SaveAs("h_num_AK8_bin_with_AK4pt.pdf");
  c1->SetLogy();
  c1->SaveAs("h_num_AK8_bin_with_AK4pt_Logy.pdf");
  c1->SetLogy(0);

  h_denom_AK8_bin_with_AK4pt->Draw();
  c1->SaveAs("h_denom_AK8_bin_with_AK4pt.pdf");
  c1->SetLogy();
  c1->SaveAs("h_denom_AK8_bin_with_AK4pt_Logy.pdf");
  c1->SetLogy(0);
 
  TH1D *h_eff_AK4 = (TH1D*)h_num_AK4->Clone();

  h_eff_AK4->Divide(h_denom_AK4);
  
  h_eff_AK4->SetTitle("h_eff_AK4");
  h_eff_AK4->GetXaxis()->SetTitle("AK4 pt");
  h_eff_AK4->GetYaxis()->SetTitle("AK4 eff");

  TH1D *h_eff_AK4_bin_with_AK8pt = (TH1D*)h_num_AK4_bin_with_AK8pt->Clone();

  h_eff_AK4_bin_with_AK8pt->Divide(h_denom_AK4_bin_with_AK8pt);

  h_eff_AK4_bin_with_AK8pt->SetTitle("h_eff_AK4");

  h_eff_AK4_bin_with_AK8pt->GetXaxis()->SetTitle("AK8 pt");

  h_eff_AK4_bin_with_AK8pt->GetYaxis()->SetTitle("AK4 eff");
  
  TH1D *h_eff_AK8 = (TH1D*)h_num_AK8->Clone();
  h_eff_AK8->Divide(h_denom_AK8);
  h_eff_AK8->SetTitle("h_eff_AK8");
  h_eff_AK8->GetXaxis()->SetTitle("AK8 pt");
  h_eff_AK8->GetYaxis()->SetTitle("AK8 eff");

  TH1D *h_eff_AK8_bin_with_AK4pt = (TH1D*)h_num_AK8_bin_with_AK4pt->Clone();
  h_eff_AK8_bin_with_AK4pt->Divide(h_denom_AK8_bin_with_AK4pt);
  h_eff_AK8_bin_with_AK4pt->SetTitle("h_eff_AK8");
  h_eff_AK8_bin_with_AK4pt->GetXaxis()->SetTitle("AK4 pt");
  h_eff_AK8_bin_with_AK4pt->GetYaxis()->SetTitle("AK8 eff");

  //Efficiency Errors
  int lastBin = h_num_AK4->FindBin(1000);
  for( int bin = 0; bin < lastBin; ++bin )
    {
      float denom = h_denom_AK4->GetBinContent(bin);
      float num = h_num_AK4->GetBinContent(bin);
      float failed = denom - num;

      float error = 0;
      
      if( !(failed == 0 || num == 0)) {
	error = sqrt( (1/failed) + (1/num) ) * failed * num / (pow(num + failed, 2));
	h_eff_AK4->SetBinError( bin, error );
      }

      denom = h_denom_AK4_bin_with_AK8pt->GetBinContent(bin);
      num = h_num_AK4_bin_with_AK8pt->GetBinContent(bin);
      failed = denom - num;

      if( !(failed == 0 || num == 0)) {
	error = sqrt( (1/failed) + (1/num) ) * failed * num / (pow(num + failed, 2));
	h_eff_AK4_bin_with_AK8pt->SetBinError( bin, error );
      }

      denom = h_denom_AK8->GetBinContent(bin);
      num = h_num_AK8->GetBinContent(bin);
      failed = denom - num;

      if( !(failed == 0 || num == 0)) {
	error = sqrt( (1/failed) + (1/num) ) * failed * num / (pow(num + failed, 2));
	h_eff_AK8->SetBinError( bin, error );
      }

      denom = h_denom_AK8_bin_with_AK4pt->GetBinContent(bin);
      num = h_num_AK8_bin_with_AK4pt->GetBinContent(bin);
      failed = denom - num;

      if( !(failed == 0 || num == 0)) {
	error = sqrt( (1/failed) + (1/num) ) * failed * num / (pow(num + failed, 2));
	h_eff_AK8_bin_with_AK4pt->SetBinError( bin, error );
      }
    }

  h_eff_AK4->Draw("E");
  c1->SaveAs("h_eff_AK4.pdf");

  h_eff_AK4_bin_with_AK8pt->Draw("E");
  c1->SaveAs("h_eff_AK4_bin_with_AK8pt.pdf");

  h_eff_AK8->Draw("E");
  c1->SaveAs("h_eff_AK8.pdf");

  h_eff_AK8_bin_with_AK4pt->Draw("E");
  c1->SaveAs("h_eff_AK8_bin_with_AK4pt.pdf");

  TH1D *h_ratio_AK4eff_AK8eff_AK4pt = (TH1D*)h_eff_AK4->Clone();
  h_ratio_AK4eff_AK8eff_AK4pt->Divide(h_eff_AK8_bin_with_AK4pt);
  
  TH1D *h_ratio_AK4eff_AK8eff_AK8pt = (TH1D*)h_eff_AK4_bin_with_AK8pt->Clone();
  h_ratio_AK4eff_AK8eff_AK8pt->Divide(h_eff_AK8);

  h_ratio_AK4eff_AK8eff_AK4pt->SetTitle("h_ratio_AK4eff_AK8eff");
  h_ratio_AK4eff_AK8eff_AK4pt->GetXaxis()->SetTitle("AK4 pt");
  h_ratio_AK4eff_AK8eff_AK4pt->GetYaxis()->SetTitle("AK4 eff/AK8 eff");
  h_ratio_AK4eff_AK8eff_AK4pt->GetYaxis()->SetRangeUser(.8,1.2);
  
  
  h_ratio_AK4eff_AK8eff_AK8pt->SetTitle("h_ratio_AK4eff_AK8eff");
  h_ratio_AK4eff_AK8eff_AK8pt->GetXaxis()->SetTitle("AK8 pt");
  h_ratio_AK4eff_AK8eff_AK8pt->GetYaxis()->SetTitle("AK4 eff/AK8 eff");
  h_ratio_AK4eff_AK8eff_AK8pt->GetYaxis()->SetRangeUser(.8,1.2);

  for( int bin = 1; bin < lastBin; ++bin )
    {
      float nPassOnlyAK8CSVcut = h_matchedjetAK4_pt_pass_csv8_cut->GetBinContent(bin);
      float nPassOnlyAK4CSVcut = h_matchedjetAK4_pt_pass_csv4_cut->GetBinContent(bin);
      float nPassBothAK4AK8CSVcut = h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut->GetBinContent(bin);

      cout << "nPassOnlyAK8CSVcut " << nPassOnlyAK8CSVcut << " nPassOnlyAK4CSVcut " << nPassOnlyAK4CSVcut << " nPassBoth " << nPassBothAK4AK8CSVcut << " bin " << bin << endl;

      float Error = 0;
      if( !(nPassBothAK4AK8CSVcut + nPassOnlyAK8CSVcut == 0) ) {
	Error = sqrt( nPassOnlyAK4CSVcut * pow(( nPassBothAK4AK8CSVcut + nPassOnlyAK8CSVcut ), 2) + nPassBothAK4AK8CSVcut * pow((nPassOnlyAK4CSVcut - nPassOnlyAK8CSVcut), 2) + nPassOnlyAK8CSVcut * pow((nPassOnlyAK4CSVcut + nPassBothAK4AK8CSVcut),2) ) / pow( nPassOnlyAK8CSVcut + nPassBothAK4AK8CSVcut, 2);
      
      cout << "Error " << Error << endl;

      h_ratio_AK4eff_AK8eff_AK4pt->SetBinError( bin, Error );
      }

      nPassOnlyAK8CSVcut = h_matchedjetAK8_pt_pass_csv8_cut->GetBinContent(bin);
      nPassOnlyAK4CSVcut = h_matchedjetAK8_pt_pass_csv4_cut->GetBinContent(bin);
      nPassBothAK4AK8CSVcut = h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut->GetBinContent(bin);

      if( !(nPassBothAK4AK8CSVcut + nPassOnlyAK8CSVcut == 0) ) {
	Error = sqrt( nPassOnlyAK4CSVcut + nPassOnlyAK8CSVcut )/( nPassBothAK4AK8CSVcut + nPassOnlyAK8CSVcut );

	h_ratio_AK4eff_AK8eff_AK8pt->SetBinError( bin, Error );
      }
      
    }

  h_ratio_AK4eff_AK8eff_AK4pt->Draw();
  c1->SaveAs("h_ratio_AK4eff_AK8eff.pdf");

  h_ratio_AK4eff_AK8eff_AK8pt->Draw();
  c1->SaveAs("h_ratio_AK4eff_AK8eff_bin_with_AK8pt.pdf");

  fit1 = new TF1("fit1","pol0",300,1000);
  fit2 = new TF1("fit2","pol0",300,1000);
  h_ratio_AK4eff_AK8eff_AK4pt->Fit(fit1,"R");
  gStyle->SetOptFit(1111);

  h_ratio_AK4eff_AK8eff_AK8pt->Fit(fit2,"R");
  gStyle->SetOptFit(1111);

  h_ratio_AK4eff_AK8eff_AK4pt->Draw();
  c1->SaveAs("h_ratio_AK4eff_AK8eff_fit.pdf");

  h_ratio_AK4eff_AK8eff_AK8pt->Draw();
  c1->SaveAs("h_ratio_AK4eff_AK8eff_bin_with_AK8pt_fit.pdf");

  return;
}
 
