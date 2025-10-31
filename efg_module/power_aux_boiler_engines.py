import sys
import numpy as np
import pandas as pd

def power_aux_boiler_engines(ais_ves):
    """
    A function that determines the power output of Auxiliary and Boiler engines
    based on the Operational Mode of vessel. In the 4th IMO GHG Study model,
    Auxiliary and Boiler engine power outputs are included in the Vessel
    Specifications dataset from the start, however in the EFG model they are
    read-in and 'joined' into the dataset. This should save a few columns on the
    Dataframe as it makes its way through the module.

    This script reads in a table of values taken from Table 17 of the 4th IMO
    GHG Study. Appendix G of the same study provides contrasting values for
    auxiliary engine power demand, however Table 17 values are utilised here as
    Appendix G doesn't provide values for Boiler Engines.

    As compared with the 4th IMO GHG Study, the EFG Module breaks up the
    evaluation of power output associated with Main, Auxiliary and Boiler
    engines, plus Operational Mode, as documented in 'power_at_op.m' across
    multiple functions:

         -  power_main_engine.py
         -  operational_mode.py
         -  power_aux_boiler_engines.py
         -  fuel_consumption.py (Main Engine Load Correction Factor, CF_L, only)

    Input Data Fields

        type_bin                Type 'bin' of the vessel
        size_bin                Size 'bin' of the vessel
        op_mode                 Assumed Instantaneous 'Operational Mode' of the vessel's activity based on operational features

    Output Data Fields

        w_aux_i_kw              Assumed Instantaneous Power Demand (kw) of the Auxiliary Engine based on Operational Mode
        w_boi_i_kw              Assumed Instantaneous Power Demand (kw) of the Boiler Engine based on Operational Mode

    """

    # Read-in and merge Energy Demands Associated with Auxiliary and Boiler Engines from pre-Prepared CSV
    aux_boiler_power_output_cols = ["type_bin", "size_bin", "op_mode", "aux_power_kw", "boiler_power_kw"]
    aux_boiler_power_output_d = {"aux_power_kw":"float", "boiler_power_kw":"float"}
    aux_boiler_power_output_r = {"aux_power_kw":"w_aux_i_kw", "boiler_power_kw":"w_boi_i_kw"}
    aux_boiler_power_output = pd.read_csv("/Users/apple/repos/AISenv/EFG Module/aux_boiler_power_output/aux_boiler_power_output_v0.2.csv", usecols=aux_boiler_power_output_cols, dtype=aux_boiler_power_output_d).rename(columns=aux_boiler_power_output_r)
    ais_ves = pd.merge(ais_ves, aux_boiler_power_output, left_on=["type_bin", "size_bin", "op_mode"], right_on=["type_bin", "size_bin", "op_mode"], how="left")

    print("\nIntroducing the Instantaneous Power Demands associated with Auxiliary and Boiler engines: \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
