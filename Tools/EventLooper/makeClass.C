void makeClass(){
  TChain chain("demo/fTree");
  chain.Add("../../DemoDiPhotonInfo.root");
  chain.MakeClass("PhotonAnalysis");
  return 0;
}
