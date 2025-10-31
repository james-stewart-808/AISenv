import sys
import numpy as np
import pandas as pd

def operational_mode(ais_ves):
    """
    This function categorises a vessel's instantaneous activity into one of five
    Operational Phases for the purposes of evaluating Energy Demand associated
    with Auxiliary and Boiler Engines. These five Operational Phases include:
    'At Berth', 'At Anchor', 'Manouevering', 'Slow Transit' and 'At Sea'. In
    order to evaluate the Instantaneous Operational Mode, the function considers
    four features: Vessel Speed, Main Engine Load, Distance from Port and
    Distance from Coastline. The conditions for each mode are carried forward
    from the 4th IMO GHG Study.

    As compared with the 4th IMO GHG Study, the EFG Module breaks up the
    evaluation of power output associated with Main, Auxiliary and Boiler
    engines, plus Operational Mode, as documented in 'power_at_op.m' across
    multiple functions:

         -  power_main_engine.py
         -  operational_mode.py
         -  power_aux_boiler_engines.py
         -  fuel_consumption.py (Main Engine Load Correction Factor, CF_L, only)

    Input Data Fields

        sog                     Fuel ...
        distance_to_port        Distance (nm) to nearest port, generated in the Setup phase
        distance_to_shore       Distance (nm) to nearest shoreline, provided as field in the AIS dataset
        w_me_load_c             Average Main Engine Power corrected by limiting to 0.98x it's 'Reference Power'

    Output Data Fields

        op_mode                 Assumed Instantaneous 'Operational Mode' of the vessel's activity based on operational features

    """

    ## Evaluation of Operational Mode
    ais_ves["op_mode"] = "Cruising"

    # When vessel speed is less than 1 nm ('Anchored', unless close to port in which case 'At berth')
    ais_ves.loc[(ais_ves.sog <= 1.0), "op_mode"] = "Anchored"
    ais_ves.loc[(ais_ves.sog <= 1.0) & (ais_ves.distance_to_port <= 1.0), "op_mode"] = "At berth"

    # When vessel speed is between 1 to 3 nm ('Anchored')
    ais_ves.loc[(ais_ves.sog > 1.0) & (ais_ves.sog <= 3.0), "op_mode"] = "Anchored"

    # When vessel speed is between 3 to 5 nm ('Manoeuvering')
    ais_ves.loc[(ais_ves.sog > 3.0) & (ais_ves.sog <= 5.0), "op_mode"] = "Manoeuvering"
    ais_ves.loc[(ais_ves.sog > 3.0) & (ais_ves.sog <= 5.0) & (ais_ves.distance_to_shore >= 5.0) & (ais_ves.w_me_load_c <= 0.65), "op_mode"] = "Slow transit"
    ais_ves.loc[(ais_ves.sog > 3.0) & (ais_ves.sog <= 5.0) & (ais_ves.distance_to_shore >= 5.0) & (ais_ves.w_me_load_c > 0.65), "op_mode"] = "Cruising"

    # When vessel speed is greater 5 nm ('Cruising' is engine load is greater than 0.65, 'Slow transit' if less than 0.65, 'Maneouvering' is distance to port is less than 1.0 nm)
    ais_ves.loc[(ais_ves.sog > 5.0), "op_mode"] = "Cruising"
    ais_ves.loc[(ais_ves.sog > 5.0) & (ais_ves.w_me_load_c <= 0.65), "op_mode"] = "Slow transit"
    ais_ves.loc[(ais_ves.sog > 5.0) & (ais_ves.distance_to_port <= 1.0), "op_mode"] = "Manoeuvering"
    print("\nEvaluation of Operational Mode based on Speed, Distance to Port, Distance to Shore and Main Engine Load: \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
