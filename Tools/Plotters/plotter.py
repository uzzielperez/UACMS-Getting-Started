#!/usr/bin/python

import ROOT
from ROOT import *

# Suppress canvas from popping up. Speeds up plots produciton
gROOT.SetBatch()
gStyle.SetOptStat(0)

infile = "../EventLooper/Kinematics.root"

f = ROOT.TFile(infile, "READ");

def createHist(f, color, obj):
    hist = f.Get(obj)
    hist.SetLineColor(color)
    return hist

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("RATIO")
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    return h3

## main

# Compare genPho1pt with patPho1Pt
c = TCanvas("c", "canvas", 500, 500)
hgenpho1pt = createHist(f, kOrange+8, "genPho1Pt")
hpatpho1pt = createHist(f, kBlack, "patPho1Pt")

hgenpho1pt.SetFillColor(kOrange-2)
hpatpho1pt.SetMarkerStyle(3)

hgenpho1pt.Draw("hist")
hpatpho1pt.Draw("same")

leg = TLegend(0.60, 0.75, 1.0, 0.85)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(hgenpho1pt, "genPho1", "f")
leg.AddEntry(hpatpho1pt, "patPho1", "ep")
leg.Draw()


c.Draw()
c.SaveAs("plots/GenVsPatPho1pt.pdf")

# Compare patPho1 with those that passed Loose
cLoose = TCanvas("cLoose", "canvasLoose", 500, 500)

hpatpho1ptLoose = createHist(f, kBlack, "patPho1PtLoose")
hRatio = createRatio(hpatpho1pt, hpatpho1ptLoose)

hpatpho1pt.SetLineColor(kOrange+8)
hpatpho1pt.SetMarkerStyle(1)
hpatpho1pt.SetFillColor(kOrange-2)
hpatpho1pt.SetFillStyle(3144)
hpatpho1ptLoose.SetFillColor(kCyan-9)
hpatpho1ptLoose.SetFillStyle(3144)

hpatpho1pt.Draw("hist")
hpatpho1ptLoose.Draw("same, hist")

l = TLegend(0.60, 0.75, 1.0, 0.85)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.035)
l.AddEntry(hpatpho1pt, "No ID", "f")
l.AddEntry(hpatpho1ptLoose, "Loose ID", "f")
l.Draw()

cLoose.Draw()
cLoose.SaveAs("plots/LoosePhoEff.pdf")

# pad1.Draw()

# Ratio

# pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
# pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
# pad1.cd()
# pad1.SetBottomMargin(0)
# pad2.cd()
# pad2.SetTopMargin(0)
# pad2.SetBottomMargin(0.2)
# pad2.SetGridy()

hRatio.Draw("same")

# pad2.Draw()

# Task: Make Ratio plot with python script
