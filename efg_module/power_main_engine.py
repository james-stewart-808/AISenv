import sys
import numpy as np
import pandas as pd

def power_main_engine(ais_ves):
    """
    A script to evaluate the instantaneous power output of the main engine. The
    script applies a version of the Admiralty formula to estimate the energy
    requirements associated with a vessel in motion through water. The
    evaluation of Main Engine Power is 'agnostic' to the specifications of the
    engine itself, instead based on hydrodynamic calculations that consider the
    resistive force of a vessel's hull as it moves through water in terms of the
    vessel's instantaneous draught and speed as compared with it's reference
    conditions. Correction factors are also applied to account for the impacts
    of weather and hull fouling.

    Finally, Corrected Main Engine Power values are provided by limiting
    estimated Instantaneous Power of the Main Engine (as derived via the
    Admiralty Formula) to 0.98x the Reference Power of the Main Engine. More
    information on these calculations is available in the 'EFG notebook' on
    application of the formula.

    As compared with the 4th IMO GHG Study, the EFG Module breaks up the
    evaluation of power output associated with Main, Auxiliary and Boiler
    engines, plus Operational Mode, as documented in 'power_at_op.m' across
    multiple functions:

         -  power_main_engine.py
         -  operational_mode.py
         -  power_aux_boiler_engines.py
         -  fuel_consumption.py (Main Engine Load Correction Factor, CF_L, only)

    The Speed-power Correction Factors applied in the 4th IMO GHG Study to
    Cruise vessels and Containerships of Size 8 & 9 are not applied here, and
    that model also catalogues instances where the vessel's Reference Speed
    is exceeded by more than 1.5x, both of which may be useful to integrate
    in this function in future.

    Input Data Fields

        draught                 Design Draught recorded for the Vessel in the Vessel Specifications dataset
        reported_draught        Vessel Draught reported in the AIS dataset
        service_speed           Design Speed recorded for the Vessel in the Vessel Specifications dataset
        sog                     Vessel Speed reported in the AIS dataset
        eng_total_kw            Design Power of the Main Engine recorded in the Vessel Specifications dataset

    Output Data Fields

        t_ref                   'Reference Draught' (m) recorded for the Vessel to be applied in the Admiralty Formula, taken as 'draught' from the Specifications dataset
        t_i                     'Instantaneous Draught' (m) reported for the Vessel, taken as 'reported_draught' from the AIS dataset
        t_i_c                   'Instantaneous Draught' (m) corrected by limiting to Reference Draught, to be applied in the Admiralty Formula
        v_ref                   'Reference Speed' (kn) recorded for the Vessel to be applied in the Admiralty Formula, taken as 'service_speed' of the Specifications dataset
        v_i                     'Instantaneous Speed' (kn) recorded for the Vessel to be applied in the Admiralty Formula, taken as 'sog' from the AIS dataset
        w_me_ref_kw             'Reference Power' (kw) for the Vessel to be applied in the Admiralty Formula, taken as 'eng_total_kw' from the Specifications dataset
        c_w                     Weather Correction Factor to be applied to Main Engine Energy Demand estimated via the Admiralty Formula
        c_f                     Fouling Correction Factor to be applied to Main Engine Energy Demand estimated via the Admiralty Formula
        w_me_i_kw               Main Engine 'Instantaneous Power' (kw) evaluated using the Admiralty Formula
        w_me_i_wf_kw            Main Engine 'Instantaneous Power' (kw), with Weather and Fouling correction factors applied
        w_me_i_wf_c_kw          Main Engine 'Instantaneous Power' (kw), with Weather and Fouling correction factors applied and corrected by limiting to 'Reference Power'
        w_me_load               Average Main Engine Power as proportion of its rated 'Reference Power'
        w_me_load_c             Average Main Engine Power corrected by limiting to 0.98x it's 'Reference Power'

    """

    # Setting up the data fields required for the Admiralty Formula
    ais_ves["t_ref"] = ais_ves.draught
    ais_ves["t_i"] = ais_ves.reported_draught
    ais_ves["t_i_c"] = np.where(ais_ves.t_i > ais_ves.t_ref, ais_ves.t_ref, ais_ves.t_i) # Correct Instantaneous Draft to be less than equal to the Reference Draft
    ais_ves["v_ref"] = ais_ves.service_speed
    ais_ves["v_i"] = ais_ves.sog
    ais_ves["w_me_ref_kw"] = ais_ves.eng_total_kw
    print("\nSetting up the data fields required for the Admiralty Formula: \n\n", ais_ves.iloc[:2], "\n")

    # Introducing correction factors for Main Engine Power Demand owing to Weather and Fouling
    weather_fouling_cf_cols = ["type_bin", "size_bin", "c_w", "c_f"]
    weather_fouling_cf_d = {"c_w":"float", "c_f":"float"}
    weather_fouling_cf = pd.read_csv("/Users/apple/repos/AISenv/EFG Module/weather_fouling/weather_fouling_v0.1.csv", usecols=weather_fouling_cf_cols, dtype=weather_fouling_cf_d)
    ais_ves = pd.merge(ais_ves, weather_fouling_cf, left_on=["type_bin", "size_bin"], right_on=["type_bin", "size_bin"], how="left")
    print("\nIntroducing correction factors for Main Engine Power Demand owing to Weather and Fouling: \n\n", ais_ves.iloc[:2], "\n")

    # Evaluate Instantaneous Power (kW) using the Admiralty Formula
    ais_ves["w_me_i_kw"] = ais_ves.w_me_ref_kw * ((ais_ves.t_i_c / ais_ves.t_ref) ** (2.0 / 3.0)) * ((ais_ves.v_i / ais_ves.v_ref) ** 3.0)
    ais_ves["w_me_i_wf_kw"] = ais_ves.w_me_i_kw / (ais_ves.c_w * ais_ves.c_f)
    ais_ves["w_me_i_wf_c_kw"] = np.where(ais_ves.w_me_i_wf_kw > 0.98 * ais_ves.w_me_ref_kw, 0.98 * ais_ves.w_me_ref_kw, ais_ves.w_me_i_wf_kw)

    # Evaluate Instantaneous Average Load of the Main Engine Compared to its Reference Value
    ais_ves["w_me_load"] = ais_ves.w_me_i_wf_kw / ais_ves.w_me_ref_kw
    ais_ves["w_me_load_c"] = ais_ves.w_me_i_wf_c_kw / ais_ves.w_me_ref_kw
    print("\nEvaluating Main Engine Power Demand using the Admiralty Formula and correcting for Weather and Fouling: \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
