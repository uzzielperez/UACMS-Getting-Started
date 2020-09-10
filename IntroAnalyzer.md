Live Workshop Session on September 11.

## Introduction

The tutorials here are in general useful to get started with CMS Data Analysis. However, the format of the Analyzer follows the general format we've always used under Henderson group. There are other ways of storing information and retrieving them and the differences are not difficult to learn. We like to store the physics quantities we need on the tree, even if they're derived ones like the invariant mass. I owe a lot of my technical analyzer knowledge to Andrew Buccilli, the first person who graduated with particle physics PhD in our group! I hope I can help with the same level of generosity and coolness that he had. :)

If you haven't already gone through these, Dr. Henderson has a series of Getting Started tutorials on ROOT and C++ [here](http://chenderson.people.ua.edu/getting-started-with-cms.html). There is also an old but nice tutorial on Physics Analysis Tools in this [link](http://people.physics.tamu.edu/kamon/research/CMS/CMS_meetings/2008/080515_PATintro.pdf).

If you have any questions you can contact me on mattermost (which is like Slack only free and better :P).

You can find several tutorials in the CMSSW Workbook in twiki for additional information too:

- [Analyzer](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookWriteFrameworkModule)
- [PhotonAnalysis](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPhotonAnalysis)

#### Homework: Read on Data Tiers and Data Formats like miniAOD/nanoAOD

Here's the paper on the [MiniAOD](https://iopscience.iop.org/article/10.1088/1742-6596/664/7/072052/pdf). The word mini means it's a smaller version of a larger dataset. This contains some "derived" physics quantities which majority of physics users are interested in. Most analyzers use this lighterweight version and in fact, people are starting to move on to nanoAOD. The disadvantage is that with these smaller datasets we are potentially throwing away some useful information for "finer" studies. In that case, you would have to request for the AOD version to be kept on disk. (You'd usually know if the dataset had been kept on TAPE).


## Making an Analyzer (on MiniAOD data)

First set up the CMSSW environment. You can read more [here](https://uscms.org/uscms_at_work/computing/setup/setup_software.shtml).
```python
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
```
You will get a warning:

```python
WARNING: Release CMSSW_10_2_18 is not available for architecture slc7_amd64_gcc820.
         Developer's area is created for available architecture slc7_amd64_gcc700.
WARNING: Developer's area is created for non-production architecture slc7_amd64_gcc700. Production architecture for this release is slc6_amd64_gcc700.
```
It doesn't matter because we're not in the business of producing central MC samples. So you can safely ignore this.

If you have github set up:
```python
# If you have github set up might you can see the full analyzer here
git clone git@github.com:uzzielperez/UACMS-Getting-Started.git
# This directory acts as the subsystem area
cd UACMS-Getting-Started/
mkedanlzr YourName_Analyzer # Replace YourName with your name
```

You can actually try to do tab completion and see a suite of commands that includes `mke`. The `mkedanlzr` will create you a skeleton of an EDAnalyzer. You can just add some stuff to it depending on the information you need.

If you are using a virtual machine or a docker image for the CMS Open data you'll probably be working with `CMSSW_5_3_32/src`. So just do the same as above except for `export SCRAM_ARCH=slc7_amd64_gcc820` and you can follow along the tutorial. At this point things won't depend much on the CMSSW version until we get to the Photon ID.


Now, compile the code:

```python
scram b
```

Maybe later we'll teach you to make your own samples or get samples from DAS but for now we'll work with a sample which you may get from my google drive, or lxplus public directory:

```python

### This has not been properly edited to point to the correct sample
/uscms/home/cuperez/nobackup/tribosons/CMSSW_10_2_8/src/GGGJets_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_spring.root

```

```python
cd NameOfYourAnalyzer
# Open the configuration file
vi python/ConfFile_cfg.py
# Replace the file:somerootfile.root to point to the file you want
# Run
cmsRun python/ConfFile_cfg.py
```

Notice that it show an error with an exception `MissingParameter: The required parameter 'tracks' was not specified.`. We're not going to deal with tracks first so open the `plugins/PhotonAnalyzer.cc` and comment out L60, L75-76, L103-110. They've sort of built them in with the framework with the latest versions of mkedanlzr. We also just want to run with just 10 events so replace -1 with 10 in `process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))`. Now, compile and try running again.

```python
scram b -j 16
cmsRun python/ConfFile_cfg.py
```
We're just going to follow most of the stuff here in this CMSSW workbook [PhotonAnalyzer](https://github.com/uzzielperez/CMSSW-workbook-practice/tree/master/EDAnalyzer/DiPhotonAnalyzer).

You can copy the contents of the `plugins/BuildFile.xml` and the extra header files from `plugins/DiphotonAnalyzer.cc` to our `PhotonAnalyzer.cc`. And then let's store some physics quantities.

Let's stay we want to store the following information - The Event Information, and some basic quantities like pt, eta, phi, E for every event with two photons that we see. We can add the following, some structs as private members of the PhotonAnalyzer Class.

```python

edm::Service<TFileService> fs;
      edm::EDGetTokenT<vector<reco::GenParticle> > genParticlesToken_;
      # central miniAOD samples call this prunedGenParticles
      edm::InputTag genParticles_;
      edm::InputTag particles_;

      TTree *fgenTree;
      //Structs
      struct eventInfo_t {
      Long64_t run;
      Long64_t LS;
      Long64_t evnum;
      };
      eventInfo_t fEventInfo;

      struct genPhotonInfo_t{
        double pt;
        double eta;
        double phi;
        double E;
       };

```

Try to familiarize yourself with what's needed in the .cc file. Like adding branches in the constructor from [L119-125](https://github.com/uzzielperez/CMSSW-workbook-practice/blob/1fc260fe9c0206caa65c081115d5cf4a3590f59f/EDAnalyzer/DiPhotonAnalyzer/plugins/DiPhotonAnalyzer.cc#L119). Initializing, the struct members from [L15-L171](https://github.com/uzzielperez/CMSSW-workbook-practice/blob/1fc260fe9c0206caa65c081115d5cf4a3590f59f/EDAnalyzer/DiPhotonAnalyzer/plugins/DiPhotonAnalyzer.cc#L150). And then finally updating the struct information by looping through the gen particle collection from [L178-L207](https://github.com/uzzielperez/CMSSW-workbook-practice/blob/1fc260fe9c0206caa65c081115d5cf4a3590f59f/EDAnalyzer/DiPhotonAnalyzer/plugins/DiPhotonAnalyzer.cc#L178). Finally, fill the tree branches.

When you've added the necessary stuff and understood the logic and flow of the code, you can try to compile and run. But it won't probably run because it's going to look for some things in the configuration file. :P

So open `python/ConfFile_cfg.py` and add a few things after `process.source`:

```python
process.TFileService = cms.Service("TFileService",
                fileName = cms.string("DemoDiPhotonInfo.root")
                            )

process.demo = cms.EDAnalyzer('PhotonAnalyzer'
    genparticles = cms.InputTag("genParticles")
)
```

Each time you change the `.cc` file you will need to have to compile but you do not have to do this for the python file.

#### Homework/Question:

What is this for?

```python
`ip->status()==1 && ip->pdgId()==22`
```

### Handling some PAT photons

First things first, we need to add this to the headers section: `#include "DataFormats/PatCandidates/interface/Photon.h"`. Also, add this line `<use name="DataFormats/PatCandidates"/>` to the `BuildFile.xml` in the `plugins` directory.

Now we add the `photonsMiniAODToken_` to the source file and then add the InputTag for `photonsMiniAOD` in the configuration file.

```python
process.demo = cms.EDAnalyzer('PhotonAnalyzer'
    genparticles = cms.InputTag("genParticles"),
    photonsMiniAOD = cms.InputTag("slimmedPhotons"),
)
```

You can look at how the `genParticlesToken_` is called in the source file and basically do the same thing for the `photonsMiniAOD`. We're going to call it "photons" in the lines where you have:

```python
const edm::Handle<edm::View<pat::Photon> >& photons...
iEvent.getByToken(photonsMiniAODToken_,  photons);

```

Then let's add a struct to handle the PAT photon information we want to store. And let's add the corresponding branches to the tree.

```python
fTree->Branch("genPhoton1", &fGenPhoton1, "pt/D:eta:phi:E");
fTree->Branch("genPhoton2", &fGenPhoton2, "pt/D:eta:phi:E");
fTree->Branch("Photon1", &fPhoton1, "pt/D:eta:phi:E");
fTree->Branch("Photon2", &fPhoton2, "pt/D:eta:phi:E");
```

And don't forget to initialize the values:
```python
fPhoton1.pt = -99999.99;
fPhoton1.eta = -99999.99;
.
.
```

Ok, I've added some implementation which deals with vectors and pointers and dereferencing for fun.

For declaring and filling vectors:
```python
std::vector<edm::Ptr<pat::Photon>> patPhotons;
for (size_t i = 0; i < photons->size(); i++){
  const auto pho = photons->ptrAt(i);
  patPhotons.push_back(pho);
}
```

For looping over vectors and retrieving information:
```python
for (std::vector<int>::size_type i = 0; i != patPhotons.size(); i++)
{
  patPho = &(*patPhotons.at(j));
  double pt = patPho->pt();
  double eta = patPho->eta();
  double phi = patPho->phi();
  double E = patPho->energy();
}

```
#### Exercise:
Calculate the deltaR and find if there's a pat photon has a minDR match with a gen Photon. Store the information in the patPhoton struct. You can read more about it [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaIDRecipesRun2).


#### Exercise: Can you make a "pt-sorter" function?

Let's not be so strict and choose `minDR<0.5`.

#### Homework/Question:

### Adding some selections
There are two ways we can go about this. Once we've stored the quantities we need we can apply some offline selection on the Ntuples with a simple python script. The other way is to apply the selection in the analyzer itself so we simply pick out the "histograms" from the Ntuples and just plot them. Whichever you prefer is ok. However, the way we've always done it in our group is the 2nd way.

#### Exercise: Add some selections in the Analyzer
#### Exercise: Make your own selections in the MakeClass script
Will give a template for this later. The MakeClass allows you to loop over all the events in the ntuples, make some selections which you can store in a new ROOT file.

#### VID using RecoEGammaTools
I've added some new members in the PhotonInfo_t struct that will allow us to store if the photons passed the Loose, Medium, Tight standard cut-based E-gamma ID. It's pretty straightforward to add the information to the struct.

```python
struct PhotonInfo_t{
  double pt;
  double eta;
  double phi;
  double E;
  bool isPassLoose;
  bool isPassMedium;
  bool isPassTight;
};
```

The branch definitions should also be updated. Make sure the booleans are stored last. It's some weird ROOT thing.


```python
fTree->Branch("Photon1", &fPhoton1, "pt/D:eta:phi:E:isPassLoose/B:isPassMedium:isPassTight");
fTree->Branch("Photon2", &fPhoton2, "pt/D:eta:phi:E:isPassLoose/B:isPassMedium:isPassTight");
```




Now, we also need to setup the egamma post reco tool in the python config.

```python
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runVID=True,
                       era='2018-Prompt',
                       phoIDModules=['RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V2_cff',
                       'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff']
                       )

```

I've decided to leave the mvaPhotonID just in case your curious about the difference.

We also have to replace this line `process.p = cms.Path(process.demo )` with `process.p = cms.Path(process.demo * process.egammaPostRecoSeq )`.

Let's compile and run.
```python

scram b -j 16
cmsRun python/ConfFile_cfg.py

```
If it does not run then we haven't set up CMSSW correctly. Let's start with a fresh CMSSW env. The recipe can be found [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaMiniAODV2). This is going to take a while so maybe it's a good idea to run this now.



```python
export SCRAM_ARCH=slc7_amd64_gcc820
cmsrel CMSSW_10_2_10 # or CMSSW_10_2_18
cd CMSSW_10_2_10/src # or CMSSW_10_2_18/src
cmsenv
git cms-init
git cms-merge-topic cms-egamma:EgammaPostRecoTools
git cms-merge-topic cms-egamma:PhotonIDValueMapSpeedup1029
git cms-merge-topic cms-egamma:slava77-btvDictFix_10210
#now to add the scale and smearing for 2018 (eventually this will not be necessary in later releases but is harmless to do regardless)
git cms-addpkg EgammaAnalysis/ElectronTools
rm EgammaAnalysis/ElectronTools/data -rf
git clone git@github.com:cms-data/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data
#now build everything
scram b -j 16

```

We also need to add the global tag to the configuration file:

```python

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v18')

```

## Making Basic Plots from Ntuples

In making plots, ROOT documentation and the ROOT forum are your best friends. For now, I'll provide a basic plotter to for you to learn how to access the information in the Ntuples. You can make some cuts, add legends and so on.


### MakeClass Setup

There's a nice and set up way to loop over the events and make the cuts you want. To set it up, do the following:

```python
mkdir Analysis # Change to appropriate name
cd Analysis
root -l
TChain chain("demo/fTree"); # or replace with treename
chain.Add("../DemoDiPhotonInfo.root") # or replace with path-to-filename
# You can add several files with the same tree
chain.MakeClass("FirstAnalysis")
```

You can also create a simple script to quickly run on this multiple times.

```python
vi analyze.C
```

And add the following:
```python
#include "FirstAnalysis.C"
#include <iostream>
using namespace std;

int analyze(){
  FirstAnalysis t;
  t.Loop();
  return 0;
}
```

You can run this by doing `root -l analyze.C`. Since there's nothing set up yet you'll just get zero. Now let's make some cuts, special histograms and plots.

#### Filling histograms and Adding Selections in Script

Simple Tasks:

* Compare the genPhotons (Monte Carlo simulated photons) and the patPhotons.
* Get the Loose Photon Selection Efficiency for the patPhotons
  - First Store all the patPhotons
  - Create a separate histograms for the patPhotons that passed the Loose Photon Selection
  - Create a ratio plot

In the Make Class script `FirstAnalysis.C`, define the histograms you want to fill, make the selections necessary, fill them and write them onto a ROOT file. You can make pretty plots from them directly but I usually have another step where I use a python or another script to prettify them.

Let's do genPho1 pt vs patPho1 first. After the line `Long64_t nentries = fChain->GetEntriesFast();`.

```python
# Create Hist with min pT 0 and max 100, with 20 bins.
TH1D* genPho1Pt = new TH1D("genPho1Pt", "", 20, 0, 100);
TH1D* patPho1Pt = new TH1D("patPho1Pt", "", 20, 0, 100);
TH1D* patPho1PtLoose = new TH1D("patPho1PtLoose", "", 20, 0, 100);
```

We fill these histograms in the event loop:

```python
Long64_t nbytes = 0, nb = 0;
for (Long64_t jentry=0; jentry<nentries;jentry++) {
   Long64_t ientry = LoadTree(jentry);
   if (ientry < 0) break;
   nb = fChain->GetEntry(jentry);   nbytes += nb;
   // if (Cut(ientry) < 0) continue;

   genPho1Pt->Fill(genPhoton1_pt);
   patPho1Pt->Fill(Photon1_pt);

   // Selections
   if (Photon1_isPassLoose) patPho1PtLoose->Fill(Photon1_pt);

}

```

Then let's write out the histograms outside of this event loop.

```python
TFile file_out("Kinematics.root", "RECREATE");
genPho1Pt->Write();
patPho1Pt->Write();
patPho1PtLoose->Write();
 ```
Then, we can run with `root -l analyze.C`

## Envisioned Next session or just homework

As for the next session, we can follow up in two or three week's time on what we think would be the best use of our time in terms of a hands-on session. Otherwise, we can just leave these topics for self-study and you can ask me, the postdocs and the professors for some help.

We'll use the [repository](https://github.com/uzzielperez/UACMS-Getting-Started) to pull changes, make branches, and submit a Pull Request.

- Scaling up and submitting crab jobs
- Learning Git (setting up git as homework)
- Accessing eos
- Generating your own Pythia Events
- Playing with CMS Open Data

## Generating Your Own Pythia Events

Get the sample Pythia fragment. In this case we're trying to generate SM Diphoton events with photons having a minimum pT of 70 GeV and a minimum invariant mass of 500 GeV.

```python
wget https://raw.githubusercontent.com/uzzielperez/CMSSW-workbook-practice/master/Generators/SMGG_TuneCUEP8M1_13TeV_pythia8_cfi.py
```

#### Homework: Look for twiki documentation or google how to generate events with Pythia! Run your analyzer on your output.

