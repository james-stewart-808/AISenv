import sys
import numpy as np
import pandas as pd

def fuel_consumption(ais_ves):
    """
    A function that determines the Fuel Consumption of Main, Auxiliary and
    Boiler engines. To achieve this, the function takes 'Base' Specific Fuel
    Consumption, SFC_base, (grams of fuel per kWh of energy) associated with
    engine and fuel type (? !!) (as derived in 'fuel_mapping.py'), then derives
    estimates of Instantaneous Specific Fuel Consumption, SFC_i, for each
    engine. These are then multiplied by Power Consumption estimates derived in
    'power_main_engine.py' and 'power_aux_boiler_engines.py' to derive final
    estimates of fuel consumption for each engine.

    In the case of the Main Engine, the 'Base' SFC is modified by the Main
    Engine Load Correction Factor, CF_L, to derive the Instantaneous SFC. This
    parabolic relationship represents the dependence of its fuel consumption per
    unit of power output on its load condition, where it's most efficient point
    is at around 75-80% of 'Maximum Continuous Rating' (MCR). The 4th IMO GHG
    Study notes that application of the CF_L is only valid for propulsion
    systems that use Internal Combustion Engines (ICE), where oil- and LNG-based
    engines are given as examples. For other engine types (such as gas and steam
    turbine engines), the SFC is noted not to be dependent on engine load, and
    the 'Base' SFC is simply taken forward as Instantaneous SFC instead.
    Regardless of engine type, the Instantaneous SFC is then multiplied by
    Energy Demand estimates produced in 'power_main_engine.py' and
    'power_aux_boiler_engines.py' to derive final estimates of fuel
    consumption.

    'Base' SFC values for the Main Engine are taken from Table 19 of the 4th IMO
    # GHG Study. [Replace with equivalent from Appendix !!].

    As compared with the 4th IMO GHG Study model, the EFG Module breaks up the
    evaluation of fuel consumption and emissions as documented in 'fuel_map.m',
    'ef_match.m', 'emissions_at_op.m' and 'efactors_p_all.m' across multiple
    functions:

         -  fuel_mapping.py (included much earlier on in the workflow)
         -  fuel_consumption.py
         -  emission_factors.py
         -  emissions.py

    Input Data Fields

        engine_code             Code of the Engine provided in the Vessel Specifications dataset
        w_me_load_c             Average Main Engine Power corrected by limiting to 0.98x it's 'Reference Power'
        sfc_base_me_g_per_kwh   'Base' Specific Fuel Consumption (SFC) (g per kwh) of the Main Engine
        sfc_base_aux_g_per_kwh  'Base' Specific Fuel Consumption (SFC) (g per kwh) of the Auxiliary Engine
        sfc_base_boi_g_per_kwh  'Base' Specific Fuel Consumption (SFC) (g per kwh) of the Boiler Engine

    Output Data Fields

        cf_l                    Main Engine Load Correction Factor
        sfc_me_i_g_per_kWh      Instantaneous Specific Fuel Consumption (SFC) (g per kwh) of the Main Engine
        fc_me_i_g               Instantaneous Fuel Consumption (g) of the Main Engine
        sfc_i_aux_g_per_kWh     Instantaneous Specific Fuel Consumption (SFC) (g per kwh) of the Boiler Engine
        fc_aux_i_g              Instantaneous Fuel Consumption (g) of the Auxiliary Engine
        sfc_i_boi_g_per_kWh     Instantaneous Specific Fuel Consumption (SFC) (g per kwh) of the Boiler Engine
        fc_boi_i_g              Instantaneous Fuel Consumption (g) of the Boiler Engine

    """

    ## MAIN ENGINE
    # Evaluate the Main Engine Load Correction Factor, CF_L, if an ICE-based engine, otherwise assign unity.
    # Assumes 9: Gas Turbine, 10: Sail, 11: Steam Turbine & Boilers, 12: Batteries, 13: Non-propelled and 14: Diesel Electric aren't ICE-based)
    ais_ves["cf_l"] = np.where(ais_ves.engine_code.isin([1, 2, 3, 4, 5, 6, 7, 8, 15]), 0.455 * ais_ves.w_me_load_c ** 2.0 - 0.710 * ais_ves.w_me_load_c + 1.280, 1.0)

    # Evaluate the Instantaneous Specific (g/kWh) and Total Fuel Consumption (g) of the Main Engine
    ais_ves["sfc_me_i_g_per_kwh"] = ais_ves.sfc_base_me_g_per_kwh * ais_ves.cf_l
    ais_ves["fc_me_i_g"] = ais_ves.sfc_me_i_g_per_kwh * ais_ves.w_me_i_wf_c_kw


    ## AUXILIARY ENGINE
    # Evaluate the Instantaneous Specific (g/kWh) and Total Fuel Consumption (g) of the Auxiliary Engine
    ais_ves["sfc_i_aux_g_per_kwh"] = ais_ves.sfc_base_aux_g_per_kwh.values
    ais_ves["fc_aux_i_g"] = ais_ves.sfc_i_aux_g_per_kwh * ais_ves.w_aux_i_kw


    ## BOILER ENGINE
    # Evaluate the Instantaneous Specific (g/kWh) and Total Fuel Consumption (g) of the Boiler Engine, g/h
    ais_ves["sfc_i_boi_g_per_kwh"] = ais_ves.sfc_base_boi_g_per_kwh.values
    ais_ves["fc_boi_i_g"] = ais_ves.sfc_i_boi_g_per_kwh * ais_ves.w_boi_i_kw

    print("\nCombining Energy Demand with Specific Fuel Consumption to derive Instantaneous Fuel Consumption associated with Main, Auxiliary and Boiler engines: \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
