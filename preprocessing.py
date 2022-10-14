import uproot3
import os
import sys
import pandas as pd
import numpy as np


bl = int(sys.argv[1])
br = int(sys.argv[2])
test = sys.argv[3]

for j in range(bl, br):
    root_file = f"sample_elecsim-{j}.root"
    if test == "True":
        en = sys.argv[4]
        eos_path = f"/eos/juno/users/a/arsg/TAO_test/{en}MeV"
    else:
        eos_path = "/eos/juno/users/a/arsg/TAO/"

    os.system("export EOS_MGM_URL=root://eos.jinr.ru")
    os.system(f"xrdcp root://eos.jinr.ru/{eos_path}/{root_file} TAO_data/{root_file}")

    file = uproot3.open(f"TAO_data/{root_file}")
    df = file["Event/Sim/SimEvent"].pandas.df(flatten=False)

    edeps = []
    edepXs = []
    edepYs = []
    edepZs = []

    HitTs = []
    HitIds = []

    for evt in range(len(df)):
        edeps.append(df.iloc[evt].fGdLSEdep)
        edepXs.append(df.iloc[evt].fGdLSEdepX / 1000.)
        edepYs.append(df.iloc[evt].fGdLSEdepY / 1000.)
        edepZs.append(df.iloc[evt].fGdLSEdepZ / 1000.)  

        HitT = np.array(df.iloc[evt].fSiPMHitT)
        HitId = np.array(df.iloc[evt].fSiPMHitID)

        HitTs.append(HitT)
        HitIds.append(HitId)

    HitTs = np.array(HitTs, dtype=object)
    HitIds = np.array(HitIds, dtype=object)
    raw_data = np.vstack((HitIds, HitTs))

    data = np.vstack(
        (edeps, edepXs, edepYs, edepZs)
    ).T

    description = "Data description: \n \
    By 'hits' key: SiPMHitID,  SiPMHitT \n \
    By 'primaries' key: edep, edepX, edepY, edepZ"
    if test == "True":
        np.savez_compressed(
            f"/mnt/cephfs/ml_data/TAO_detsim_J22/test/{en}MeV/detsim_" + root_file.split("-")[1][:-5] + ".npz",
            hits=raw_data,
            primaries=data,
            description=description
        )
    else:
        np.savez_compressed(
            "/mnt/cephfs/ml_data/TAO_detsim_J22/train/detsim_" + root_file.split("-")[1][:-5] + ".npz",
            hits=raw_data,
            primaries=data,
            description=description
        )

    os.system(f"rm TAO_data/{root_file}")
