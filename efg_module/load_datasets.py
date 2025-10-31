import sys
import numpy as np
import pandas as pd

def load_datasets():
    """
    A function that loads input datasets for the EFG module. This version of the
    function loads the AIS and Vessel Specification datasets locally, however
    an alternative version may seek to load these datasets in from cloud-based
    databases via a package such as PySpark.

    The AIS dataset should represent hourly movements for each vessel and
    use a format that will enable the rest of the EFG module to run. The AIS
    dataset should include the following: hourly timestamp, longitude, latitude,
    instantaneous speed and draught. This version of the EFG Module is also
    built around the Windward AIS dataset that features 'distance to shore', a
    data field that is necessary for the evaluation of Operational Mode.

    The Vessel Specifications dataset should cover necessary vessels and
    include data fields that will enable the evaluation of energy demand of the
    Main Engine via the Admiralty Formula and fuel consumption of Main,
    Auxiliary and Boiler engines. The Vessel Specifications dataset should
    include the following as a minimum, unless a suitable approximation method
    is put in-place: Length, Beam, Type, Size, Build Year, Gross Tonnage,
    Deadweight Tonngage, Main Engine Code, Main Engine Type, Main Engine Tier,
    Main Engine Power, Main Engine RPM, Reference Draught, and Reference Speed.

    No Input Data
    Output Data

        ais_ves      AIS and Vessel Specifications data combined into a single Pandas Dataframe

    """

    ais_cols = {"imo":int, "lon":"float", "lat":"float", "distance_to_shore":"float", "reported_draught":"float", "sog":"float", "cog":"float"}
    ais = pd.read_csv("/Users/apple/repos/AISenv/datasets/ais_test/ais_test_v0.3.csv", dtype=ais_cols)
    ais["ts"] = ais["ts"].astype({"ts":"datetime64[ns]"})
    print("\nAIS dataframe: \n\n", ais.iloc[:2], "\n")

    ves_cols = {
        "imo":"int", "mmsi":"float", "type_bin":"int", "size_bin":"int", "year_of_built":"int", "gross_tonnage":"float", "deadweight":"float",
        "draught":"float", "service_speed":"float", "main_engine_rpm":"float", "eng_total_kw":"float", "engine_code":"int", "tier":"int",
        "me_sfoc":"float", "aux_sfoc":"float", "boiler_sfoc":"float", "aux_at_berth":"float", "aux_anchor":"float", "aux_manoeuvring":"float", "aux_slow":"float", "aux_sea":"float"
    }
    ves = pd.read_csv("/Users/apple/repos/AISenv/datasets/vessels_test/vessels_test_v0.3.csv", dtype=ves_cols)
    print("\nVessel specifications: \n\n", ves.iloc[:2], "\n")

    ais_ves = pd.merge(ais, ves, left_on="imo", right_on="imo", how="left")
    print("Combined AIS and Vessel Specifications dataset: \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
