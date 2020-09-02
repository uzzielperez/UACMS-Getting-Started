import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:/uscms/home/cuperez/nobackup/tribosons/CMSSW_10_2_8/src/GGGJets_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_spring.root'

    )
)


process.TFileService = cms.Service("TFileService",
                fileName = cms.string("DemoDiPhotonInfo.root")
                            )

process.demo = cms.EDAnalyzer('PhotonAnalyzer',
    particles = cms.InputTag("prunedGenParticles")
)


process.p = cms.Path(process.demo)
