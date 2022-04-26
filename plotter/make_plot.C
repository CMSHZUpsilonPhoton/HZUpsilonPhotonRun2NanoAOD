#include "tdrstyle.C"
#include "CMS_lumi.C"
#include "TH1.h"
#include "TH1F.h"

TCanvas *make_canvas()
{

	int W = 800;
	int H = 600;
	int H_ref = 600;
	int W_ref = 800;
	float T = 0.08 * H_ref;
	float B = 0.12 * H_ref;
	float L = 0.12 * W_ref;
	float R = 0.04 * W_ref;

	TString canvName = "FigExample_";
	TCanvas *canv = new TCanvas(canvName, canvName, 50, 50, W, H);
	canv->SetFillColor(0);
	canv->SetBorderMode(0);
	canv->SetFrameFillStyle(0);
	canv->SetFrameBorderMode(0);
	canv->SetLeftMargin(L / W);
	canv->SetRightMargin(R / W);
	canv->SetTopMargin(T / H);
	canv->SetBottomMargin(B / H);
	canv->SetTickx(0);
	canv->SetTicky(0);

	return canv;
}

void make_plot()
{
	setTDRStyle();
	writeExtraText = true;
	lumi_sqrtS = "13 TeV";
	lumi_13TeV = "59.7 fb^{-1}";
	extraText = "Preliminary";

	gStyle->SetPalette(kBird);

	size_t n_histos = 23;
	const char *branch[23] = {"delta_phi_upsilon_photon", "boson_mass", "boson_pt", "boson_eta", "boson_phi", "upsilon_mass", "upsilon_pt", "upsilon_eta", "upsilon_phi", "photon_mass", "photon_pt", "photon_eta", "photon_phi", "mu_1_mass", "mu_1_pt", "mu_1_eta", "mu_1_phi", "mu_2_mass", "mu_2_pt", "mu_2_eta", "mu_2_phi", "delta_eta_upsilon_photon", "delta_r_upsilon_photon"};
	const char *x_legend[23] = {"|#Delta#phi(#Upsilon,#gamma)|", "Z/H Mass (GeV)", "Z/H p_{T} (GeV)", "Z/H #eta", "Z/H #phi", "#Upsilon Mass (GeV)", "#Upsilon p_{T} (GeV)", "#Upsilon #eta", "#Upsilon #phi", "#gamma Mass (GeV)", "#gamma p_{T} (GeV)", "#gamma #eta", "#gamma #phi", "#mu_{1} Mass (GeV)", "#mu_{1} p_{T} (GeV)", "#mu_{1} #eta", "#mu_{1} #phi", "#mu_{2} Mass (GeV)", "#mu_{2} p_{T} (GeV)", "#mu_{2} #eta", "#mu_{2} #phi", "|#Delta#eta(#Upsilon,#gamma)|", "|#DeltaR(#Upsilon,#gamma)|"};
	int n_bins[23] = {50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50};
	double l_bin[23] = {0., 50., 0., -3., -3.14, 8., 0., -3., -3.14, 0., 0., -3., -3.14, 0., 0., -3., -3.14, 0., 0., -3., -3.14, 0., 0.};
	double up_bin[23] = {5., 150., 200., 3., 3.14, 11., 200., 3., 3.14, 10., 200., 3., 3.14, 10., 200., 3., 3.14, 10., 200., 3., 3.14, 5., 3.};

	//	const char *selection[2] = {"preselected","selected"};
	TString selection[2] = {"preselected", "selected"};

	for (int jj = 0; jj < 2; jj++)
	{
		for (int j = 0; j < n_histos; j++)
		{

			TFile *_file1 = TFile::Open("../" + selection[jj] + "_ggH_HToUps1SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
			TFile *_file2 = TFile::Open("../" + selection[jj] + "_ggH_HToUps2SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
			TFile *_file3 = TFile::Open("../" + selection[jj] + "_ggH_HToUps3SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
			TFile *_file4 = TFile::Open("../" + selection[jj] + "_ZToUpsilon1SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
			TFile *_file5 = TFile::Open("../" + selection[jj] + "_ZToUpsilon2SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
			TFile *_file6 = TFile::Open("../" + selection[jj] + "_ZToUpsilon3SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
			TFile *_file7 = TFile::Open("../" + selection[jj] + "_ZGTo2MuG_MMuMu-2To15_TuneCP5_13TeV-madgraph-pythia8_2018.root");
			TFile *_file8 = TFile::Open("../" + selection[jj] + "_GluGluHToMuMuG_M125_MLL-0To60_Dalitz_012j_13TeV_amcatnloFXFX_pythia8_PSWeight_2018.root");
			TFile *_file0 = TFile::Open("../" + selection[jj] + "_Run2018.root");

			TTree *tree8 = (TTree *)_file8->Get("Events");
			TTree *tree7 = (TTree *)_file7->Get("Events");
			TTree *tree6 = (TTree *)_file6->Get("Events");
			TTree *tree5 = (TTree *)_file5->Get("Events");
			TTree *tree4 = (TTree *)_file4->Get("Events");
			TTree *tree3 = (TTree *)_file3->Get("Events");
			TTree *tree2 = (TTree *)_file2->Get("Events");
			TTree *tree1 = (TTree *)_file1->Get("Events");
			TTree *tree = (TTree *)_file0->Get("Events");

			TH1F *h1_data = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_data->SetMarkerStyle(20);

			if (jj == 0)
			{
				h1_data->GetYaxis()->SetTitle("a.u.");
			}

			h1_data->GetYaxis()->SetTitle("Events");
			h1_data->GetYaxis()->SetTitleOffset(1);
			h1_data->GetXaxis()->SetTitle(x_legend[j]);
			Float_t var; // Double_t var;
			tree->SetBranchAddress(branch[j], &var);
			Double_t var_w;
			tree->SetBranchAddress("weight", &var_w);
			Double_t var_d;
			tree->SetBranchAddress(branch[j], &var_d);
			for (int i = 0; i < tree->GetEntries(); i++)
			{
				tree->GetEntry(i);
				if (j != 1 && j != 5)
					h1_data->Fill(var, var_w);
				if (j == 1 && !((var_d < 96 && var_d > 86) || (var_d < 135 && var_d > 115)))
					h1_data->Fill(var_d, var_w); // blind signal ragion in boson mass plot
				if (j == 5)
					h1_data->Fill(var_d, var_w);
			}

			TH1F *h1_MC1 = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC1->SetLineWidth(4);
			h1_MC1->SetLineColor(kGreen + 3);
			Float_t var1; // Double_t var1;
			tree1->SetBranchAddress(branch[j], &var1);
			Double_t var1_w;
			tree1->SetBranchAddress("weight", &var1_w);
			Double_t var1_d;
			tree1->SetBranchAddress(branch[j], &var1_d);
			for (int i = 0; i < tree1->GetEntries(); i++)
			{
				tree1->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC1->Fill(var1, var1_w);
				if (j == 1 || j == 5)
					h1_MC1->Fill(var1_d, var1_w);
			}

			TH1F *h1_MC2 = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC2->SetLineWidth(4);
			h1_MC2->SetLineColor(kGreen - 3);
			Float_t var2; // Double_t var2;
			tree2->SetBranchAddress(branch[j], &var2);
			Double_t var2_w;
			Double_t var2_d;
			tree2->SetBranchAddress(branch[j], &var2_d);
			tree2->SetBranchAddress("weight", &var2_w);
			for (int i = 0; i < tree2->GetEntries(); i++)
			{
				tree2->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC2->Fill(var2, var2_w);
				if (j == 1 || j == 5)
					h1_MC2->Fill(var2_d, var2_w);
			}

			TH1F *h1_MC3 = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC3->SetLineWidth(4);
			h1_MC3->SetLineColor(kGreen - 8);
			Float_t var3; // Double_t var3;
			tree3->SetBranchAddress(branch[j], &var3);
			Double_t var3_w;
			tree3->SetBranchAddress("weight", &var3_w);
			Double_t var3_d;
			tree3->SetBranchAddress(branch[j], &var3_d);
			for (int i = 0; i < tree3->GetEntries(); i++)
			{
				tree3->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC3->Fill(var3, var3_w);
				if (j == 1 || j == 5)
					h1_MC3->Fill(var3_d, var3_w);
			}

			TH1F *h1_MC4 = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC4->SetLineWidth(4);
			h1_MC4->SetLineColor(kBlue + 2);
			Float_t var4; // Double_t var4;
			tree4->SetBranchAddress(branch[j], &var4);
			Double_t var4_w;
			tree4->SetBranchAddress("weight", &var4_w);
			Double_t var4_d;
			tree4->SetBranchAddress(branch[j], &var4_d);
			for (int i = 0; i < tree4->GetEntries(); i++)
			{
				tree4->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC4->Fill(var4, var4_w);
				if (j == 1 || j == 5)
					h1_MC4->Fill(var4_d, var4_w);
			}

			TH1F *h1_MC5 = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC5->SetLineWidth(4);
			h1_MC5->SetLineColor(kBlue - 7);
			Float_t var5; // Double_t var5;
			tree5->SetBranchAddress(branch[j], &var5);
			Double_t var5_d;
			tree5->SetBranchAddress(branch[j], &var5_d);
			Double_t var5_w;
			tree5->SetBranchAddress("weight", &var5_w);
			for (int i = 0; i < tree5->GetEntries(); i++)
			{
				tree5->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC5->Fill(var5, var5_w);
				if (j == 1 || j == 5)
					h1_MC5->Fill(var5_d, var5_w);
			}

			TH1F *h1_MC6 = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC6->SetLineWidth(4);
			h1_MC6->SetLineColor(kBlue - 9);
			Float_t var6; // Double_t var6;
			tree6->SetBranchAddress(branch[j], &var6);
			Double_t var6_d;
			tree6->SetBranchAddress(branch[j], &var6_d);
			Double_t var6_w;
			tree6->SetBranchAddress("weight", &var6_w);
			for (int i = 0; i < tree6->GetEntries(); i++)
			{
				tree6->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC6->Fill(var6, var6_w);
				if (j == 1 || j == 5)
					h1_MC6->Fill(var6_d, var6_w);
			}

			TH1F *h1_MC7 = new TH1F("h1", "h1", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC7->SetLineWidth(4);
			h1_MC7->SetLineColor(kYellow - 7);
			Float_t var7; // Double_t var7;
			tree7->SetBranchAddress(branch[j], &var7);
			Double_t var7_d;
			tree7->SetBranchAddress(branch[j], &var7_d);
			Double_t var7_w;
			tree7->SetBranchAddress("weight", &var7_w);
			for (int i = 0; i < tree7->GetEntries(); i++)
			{
				tree7->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC7->Fill(var7, var7_w);
				if (j == 1 || j == 5)
					h1_MC7->Fill(var7_d, var7_w);
			}

			TH1F *h1_MC8 = new TH1F("h", "h", n_bins[j], l_bin[j], up_bin[j]);
			h1_MC8->SetLineWidth(4);
			h1_MC8->SetLineColor(kRed - 3);
			Float_t var8; // Double_t var8;
			tree8->SetBranchAddress(branch[j], &var8);
			Double_t var8_d;
			tree8->SetBranchAddress(branch[j], &var8_d);
			Double_t var8_w;
			tree8->SetBranchAddress("weight", &var8_w);
			for (int i = 0; i < tree8->GetEntries(); i++)
			{
				tree8->GetEntry(i);
				if (j != 1 && j != 5)
					h1_MC8->Fill(var8, var8_w);
				if (j == 1 || j == 5)
					h1_MC8->Fill(var8_d, var8_w);
			}

			h1_MC1->Add(h1_MC2);
			h1_MC1->Add(h1_MC3);

			h1_MC4->Add(h1_MC5);
			h1_MC4->Add(h1_MC6);

			if (jj == 0)
			{
				h1_data->Scale(1 / h1_data->Integral());
				h1_MC1->Scale(1 / h1_MC1->Integral());
				h1_MC4->Scale(1 / h1_MC4->Integral());
				h1_MC8->Scale(1 / h1_MC8->Integral());
				h1_MC7->Scale(1 / h1_MC7->Integral());
			}

			if (jj == 1)
			{
				h1_MC1->Scale(1.e+6);
				h1_MC4->Scale(150.);
				h1_MC8->Scale(100.);
			}

			double factor_max = 1.4;
			double max = 0.;
			if (h1_data->GetMaximum() > max)
				max = h1_data->GetMaximum();
			if (h1_MC1->GetMaximum() > max)
				max = h1_MC1->GetMaximum();
			if (h1_MC4->GetMaximum() > max)
				max = h1_MC4->GetMaximum();
			if (h1_MC7->GetMaximum() > max)
				max = h1_MC7->GetMaximum();
			if (h1_MC8->GetMaximum() > max)
				max = h1_MC8->GetMaximum();

			h1_data->SetMaximum(max * factor_max);

			TCanvas *canv = make_canvas();
			canv->cd();
			gPad->SetTickx();
			gPad->SetTicky();

			h1_data->Draw("E0P");
			h1_MC1->Draw("HIST SAME PLC");
			h1_MC4->Draw("HIST SAME PLC");
			h1_MC7->Draw("HIST SAME PLC");
			h1_MC8->Draw("HIST SAME PLC");
			h1_data->Draw("E0P SAME");

			auto legend = new TLegend(0.7, 0.65, 1., 0.90);
			legend->AddEntry(h1_data, "Data", "lep");

			if (jj == 0)
			{
				legend->AddEntry(h1_MC1, "H #rightarrow #Upsilon(nS)#gamma", "f");
				legend->AddEntry(h1_MC4, "Z #rightarrow #Upsilon(nS)#gamma", "f");
				legend->AddEntry(h1_MC8, "H Dalitz", "f");
				legend->AddEntry(h1_MC7, "Z #rightarrow #mu#mu#gamma_{FSR}", "f");
			}

			legend->AddEntry(h1_MC1, "H #rightarrow #Upsilon(nS)#gamma x10^{6}", "f");
			legend->AddEntry(h1_MC4, "Z #rightarrow #Upsilon(nS)#gamma x150", "f");
			legend->AddEntry(h1_MC8, "H Dalitz x100", "f");
			legend->AddEntry(h1_MC7, "Z #rightarrow #mu#mu#gamma_{FSR}", "f");

			legend->SetBorderSize(0);
			legend->SetFillColor(0);
			legend->SetTextSize(0.032);
			legend->Draw();

			TLatex t(.5, .85, selection[jj]);
			t.SetNDC(kTRUE);
			t.Draw();

			CMS_lumi(canv, 4, 11);
			canv->Update();
			canv->RedrawAxis();
			canv->GetFrame()->Draw();

			TString canvName = branch[j];
			canv->Print(selection[jj] + "_" + canvName + "_.pdf", ".pdf");
			canv->Print(selection[jj] + "_" + canvName + "_.png", ".png");
		}
	}
}
