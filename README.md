# UACMS Getting Started
Tutorials on getting started with CMS Analysis within the UA group 

# CRAB Notes

* https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3FAQ
* https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial


# Private Production

* https://exo-mc-and-i.gitbook.io/exo-mc-and-interpretation/how-to-sample-production-private

# EOS at LPC 

* https://uscms.org/uscms_at_work/computing/LPC/usingEOSAtLPC.shtml
* https://uscms.org/uscms_at_work/computing/LPC/usingEOSAtLPC.shtml#eosQuotaIncrease

# CMS EOS and FNAL EOS 

* https://uscms.org/uscms_at_work/computing/LPC/additionalEOSatLPC.shtml
* Example of command to ls 
```
eos root://cmseos.fnal.gov ls /store/user/cuperez
```
* Example of copying a directory from FNAL EOS to CMS EOS (lxplus)
```
  xrdcp root://cmseos.fnal.gov//store/user/lpcml/cuperez/diphotonClosureTest root://eosuser.cern.ch//eos/cms/store/group/phys_exotica/diphoton/fullRun2/uzzie
  xrdcp -r root://cmseos.fnal.gov//store/user/cuperez/GluGluSpin0ToGammaGamma_W_0p014_M_750_TuneCP2_UL/RunIISummer20UL17_GEN root://eosuser.cern.ch//eos/cms/store/group/phys_exotica/diphoton/fullRun2/uzzie

```

## CERN GPUs

* CMSLPC - https://uscms.org/uscms_at_work/computing/setup/gpu.shtml
* LXPLUS - https://clouddocs.web.cern.ch/gpu/index.html

# CMS Analysis Journey
* https://cms.cern/content/publishing-analysis


