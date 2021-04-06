#from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from WMCore.Configuration import Configuration
config = config()

#config.General.requestName = '%s_%s_%s'%(CFG,PU,EVTCONT)
config.General.requestName = 'TESTFirstAN'
config.General.workArea = 'outcrab'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'TestFirstAN_cfg.py'
config.JobType.maxMemoryMB = 2800

config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 100
config.Data.totalUnits = 500
config.Data.publication = False
# config.Data.outputDatasetTag = '%s_%s_%s'

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T2_CH_CERN'
config.Site.blacklist = ['T1_RU_JINR', 'T2_US_Vanderbilt']

#crab submit -c crabConfig_MC.py
