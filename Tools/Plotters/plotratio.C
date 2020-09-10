void ratioPlot(TH1D *h2, TH1D *h3){
  TH1D *hRatio = (TH1D*) h2->Clone("h2");
  hRatio->SetLineColor(kBlack);
  hRatio->SetMarkerColor(kBlack);
  hRatio->SetMinimum(0.01);
  hRatio->SetMaximum(2);
  hRatio->SetStats(0);
  hRatio->Divide(h3);
  hRatio->Draw("ep");
  hRatio->SetTitle("");

  hRatio->GetYaxis()->SetTitle("");
  hRatio->GetYaxis()->SetNdivisions(505);
  hRatio->GetYaxis()->SetTitleSize(14);
  hRatio->GetYaxis()->CenterTitle();
  hRatio->GetYaxis()->SetTitleFont(43);
  hRatio->GetYaxis()->SetTitleOffset(1.3);
  hRatio->GetYaxis()->SetLabelFont(43);
  hRatio->GetYaxis()->SetLabelSize(5);
  hRatio->GetXaxis()->SetTitle("M_{#gamma#gamma} (GeV)");
  hRatio->GetXaxis()->SetTitleSize(0.1);
  hRatio->GetXaxis()->SetTitleOffset(1);

}

void plotratio(){
  gROOT->SetBatch(0);
  gStyle->SetOptStat(0);

  TFile *f = TFile::Open("../EventLooper/Kinematics.root");

  TH1D *hgenpho1pt = (TH1D*) f->Get("genPho1Pt");
  TH1D *hpatpho1pt = (TH1D*) f->Get("patPho1Pt");
  TH1D *hpatpho1ptLoose = (TH1D*) f->Get("patPho1PtLoose");

  TCanvas *canvas = new TCanvas("canvas","canvas",1500,600);
  canvas->Divide(2,1);

  canvas->cd(1);
  hgenpho1pt->Draw("E1");
  hpatpho1pt->SetLineColor(kOrange);; 
  hpatpho1pt->Draw("same");
  hgenpho1pt->GetXaxis()->SetTitle("pT (GeV)");
  hgenpho1pt->GetYaxis()->SetTitle("Events / (20 GeV)");
  hgenpho1pt->GetYaxis()->SetTitleOffset(1.4);

  canvas->cd(2);
  hpatpho1pt->Draw("E1");
  hpatpho1ptLoose->Draw("same");
  hpatpho1pt->GetXaxis()->SetTitle("pT (GeV)");
  hpatpho1pt->GetYaxis()->SetTitle("Events / (20 GeV)");
  hpatpho1pt->GetYaxis()->SetTitleOffset(1.4);

  canvas->SaveAs("plots/CanvasSplit.pdf");

  //Task: Add Legend

  // Ratio Plot
  TCanvas *c = new TCanvas("c", "c", 500, 500);
  c->cd();
  TPad *pad = new TPad("pad", "", 0, 0.3, 1, 1.0);
  pad->SetBottomMargin(0.01);
  pad->Draw();
  pad->cd();
  hpatpho1pt->Draw("E1");
  hpatpho1ptLoose->SetLineColor(kGreen); 
  hpatpho1ptLoose->Draw("same");
  hpatpho1pt->GetXaxis()->SetTitle("pT (GeV)");
  hpatpho1pt->GetYaxis()->SetTitle("Events / (20 GeV)");
  hpatpho1pt->GetYaxis()->SetTitleOffset(1.4);

  c->cd();
  TPad *padRatio = new TPad("padRatio", "", 0, 0, 1, 0.3);
  padRatio->SetTopMargin(0);
  padRatio->SetBottomMargin(0.3);
  padRatio->Draw();
  padRatio->cd();
  padRatio->SetGrid(0, 1);
  ratioPlot(hpatpho1ptLoose, hpatpho1pt);

  c->SaveAs("plots/LooseRatio.pdf");

  return 0;
}

