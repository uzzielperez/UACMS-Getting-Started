#!/usr/bin/python

import ROOT
from ROOT import *

# Suppress canvas from popping up. Speeds up plots produciton
gROOT.SetBatch()

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
hgenpho1pt = createHist(f, kBlack, "genPho1Pt")
hpatpho1pt = createHist(f, kRed, "patPho1Pt")


hgenpho1pt.Draw()
hpatpho1pt.Draw("same")

c.Draw()
c.SaveAs("plots/GenVsPatPho1pt.pdf")
# Compare
# hpatpho1ptLoose = createHist(f, kBlue, "patPho1PtLoose")
