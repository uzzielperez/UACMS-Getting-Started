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

from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runVID=True,
                       era='2018-Prompt',
                       phoIDModules=['RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V2_cff',
                       'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff']
                       )


process.TFileService = cms.Service("TFileService",
                fileName = cms.string("DemoDiPhotonInfo.root")
                            )

process.demo = cms.EDAnalyzer('PhotonAnalyzer',
    genparticles = cms.InputTag("prunedGenParticles"),
    photonsMiniAOD = cms.InputTag("slimmedPhotons"),
)


process.p = cms.Path(process.demo * process.egammaPostRecoSeq )
