ls void makeClass(){
  TChain chain("demo/fTree");
  chain.Add("../../PhotonAnalyzer/DemoDiPhotonInfo.root");
  chain.MakeClass("PhotonAnalysis");
  return 0;
}
