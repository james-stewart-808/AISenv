import sys
import numpy as np
import pandas as pd

def emissions(ais_ves):
    """
    A function that evaluates the Instantaneous GHG Emissions associated with
    vessel activity. To achieve this, the function combines estimates of fuel
    consumption with associated Fuel-based Emission Factors to calculate
    Carbon Dioxide (CO2) emissions, or combines estimates of energy demand with
    Energy-based Emission Factors to calculate Methane (CH4) and Nitrous Oxide
    (N2O) emissions. To understand the total warming potential of GHGs emitted
    as a result of vessel activity, CO2e emissions are evaluated by introducing
    a scaling factor of 25x to methane emissions and 273x for N2O emissions, in
    alignment with the 4th IMO GHG Study and IPCC protocol.

    Input Data Fields

        fc_me_i_g               Instantaneous Fuel Consumption (g) of the Main Engine
        w_me_i_wf_c_kw          Instantaneous Power Demand (kWh) of the Main Engine, corrected by Weather and Fouling
        fc_aux_i_g              Instantaneous Fuel Consumption (g) of the Auxiliary Engine
        w_aux_i_kw              Instantaneous Power Demand (kWh) of the Auxiliary Engine, corrected by Weather and Fouling
        fc_boi_i_g              Instantaneous Fuel Consumption (g) of the Boiler Engine
        w_boi_i_kw              Instantaneous Power Demand (kWh) of the Boiler Engine, corrected by Weather and Fouling
        co2_me_g_per_gfuel      CO2 (g) produced per gram of Fuel Consumed by the Main Engine
        ch4_me_g_per_kWh        CH4 (g) produced per kWh of Energy Demanded by the Main Engine
        n2o_me_g_per_kWh        N2O (g) produced per kWh of Energy Demanded by the Main Engine
        co2_aux_g_per_gfuel     CO2 (g) produced per gram of Fuel Consumed by the Auxiliary Engine
        ch4_aux_g_per_kWh       CH4 (g) produced per kWh of Energy Demanded by the Auxiliary Engine
        n2o_aux_g_per_kWh       N2O (g) produced per kWh of Energy Demanded by the Auxiliary Engine
        co2_boi_g_per_gfuel     CO2 (g) produced per gram of Fuel Consumed by the Boiler Engine
        ch4_boi_g_per_kWh       CH4 (g) produced per kWh of Energy Demanded by the Boiler Engine
        n2o_boi_g_per_kWh       N2O (g) produced per kWh of Energy Demanded by the Boiler Engine

    Output Data Fields

        co2_me_g                Total CO2 (g) produced by the Main Engine
        ch4_me_g                Total CH4 (g) produced by the Main Engine
        n2o_me_g                Total N2O (g) produced by the Main Engine
        co2e_me_g               Total CO2e (g) produced by the Main Engine
        co2_aux_g               Total CO2 (g) produced by the Auxiliary Engine
        ch4_aux_g               Total CH4 (g) produced by the Auxiliary Engine
        n2o_aux_g               Total N2O (g) produced by the Auxiliary Engine
        co2e_aux_g              Total CO2e (g) produced by the Auxiliary Engine
        co2_boi_g               Total CO2 (g) produced by the Boiler Engine
        ch4_boi_g               Total CH4 (g) produced by the Boiler Engine
        n2o_boi_g               Total N2O (g) produced by the Boiler Engine
        co2e_boi_g              Total CO2e (g) produced by the Boiler Engine
        co2_tot_g               Total CO2 (g) produced by all Engines
        ch4_tot_g               Total CH4 (g) produced by all Engines
        n2o_tot_g               Total N2O (g) produced by all Engines
        co2e_tot_g              Total CO2e (g) produced by all Engines

    """

    # Main Engine Emissions Generation
    ais_ves["co2_me_g"] = ais_ves.fc_me_i_g * ais_ves.co2_me_g_per_gfuel
    ais_ves["ch4_me_g"] = ais_ves.w_me_i_wf_c_kw * ais_ves.ch4_me_g_per_kWh
    ais_ves["n2o_me_g"] = ais_ves.w_me_i_wf_c_kw * ais_ves.n2o_me_g_per_kWh
    ais_ves["co2e_me_g"] = ais_ves.co2_me_g + 25.0 * ais_ves.ch4_me_g + 273.0 * ais_ves.n2o_me_g

    # Auxiliary Engine Emissions Generation
    ais_ves["co2_aux_g"] = ais_ves.fc_aux_i_g * ais_ves.co2_aux_g_per_gfuel
    ais_ves["ch4_aux_g"] = ais_ves.w_aux_i_kw * ais_ves.ch4_aux_g_per_kWh
    ais_ves["n2o_aux_g"] = ais_ves.w_aux_i_kw * ais_ves.n2o_aux_g_per_kWh
    ais_ves["co2e_aux_g"] = ais_ves.co2_aux_g + 25.0 * ais_ves.ch4_aux_g + 273.0 * ais_ves.n2o_aux_g

    # Boiler Engine Emissions Generation
    ais_ves["co2_boi_g"] = ais_ves.fc_boi_i_g * ais_ves.co2_boi_g_per_gfuel
    ais_ves["ch4_boi_g"] = ais_ves.w_boi_i_kw * ais_ves.ch4_boi_g_per_kWh
    ais_ves["n2o_boi_g"] = ais_ves.w_boi_i_kw * ais_ves.n2o_boi_g_per_kWh
    ais_ves["co2e_boi_g"] = ais_ves.co2_boi_g + 25.0 * ais_ves.ch4_boi_g + 273.0 * ais_ves.n2o_boi_g

    # Total Emissions across all Engines
    ais_ves["co2_tot_g"] = ais_ves.co2_me_g + ais_ves.co2_aux_g + ais_ves.co2_boi_g
    ais_ves["ch4_tot_g"] = ais_ves.ch4_me_g + ais_ves.ch4_aux_g + ais_ves.ch4_boi_g
    ais_ves["n2o_tot_g"] = ais_ves.n2o_me_g + ais_ves.n2o_aux_g + ais_ves.n2o_boi_g
    ais_ves["co2e_tot_g"] = ais_ves.co2e_me_g + ais_ves.co2e_aux_g + ais_ves.co2e_boi_g

    print("\nEvaluating Instantaneous GHG Generation as the product of Emission Factors and Fuel Consumption or Energy Demand: \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
