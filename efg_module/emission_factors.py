import sys
import numpy as np
import pandas as pd

def emission_factors(ais_ves, fuel_emissions_dir):
    """
    A function that assigns Emission Factors for all emission species considered
    in the model. The Emission Factors applied can either be Fuel-based or
    Energy-based. Fuel-based Emission Factors apply a constant value per gram of
    fuel consumed and are used in this version of the EFG module to estimate
    quantities of CO2 emitted as a result of vessel activity. Energy-based
    Emission Factors apply a constant value per kWh of energy demanded, and are
    used in this version of the EFG module to estimate quantities of Methane and
    N2O emitted as a result of vessel activity.

    Within the IMO IV model, Emission Factors associated with Main Engine fuel
    consumption are evaluated as a function of multiple technical features:

        i.   4x  Generations of Engine (0: <1984; 1: 1984-2001; 2: 2001+; 3:
                    2016+)
        ii.  14x Types of Engine (1-SSD; 2-MSD; 3-HSD; 4-LNG-Otto SSD; 5-LNG-
                    Otto MSD; 6-LNG-Diesel; 7-LBSI; 8-Methanol; 9-Gas Turbine;
                    10-Sail; 11-Steam Turbine; 12-Batteries; 13-Non-propelled;
                    14-Diesel Electric)
        iii. 8x  Fuel Types (1: FO2.7S; 2: LSFO1.5S; 3: LSFO1.0S; 4: LSFO0.5S;
                    5: MDOMGO0.1S, 6: LNG, 7: Methanol, 8: Nuclear_No_fuel).
        iv.  4x  Tiers of Engine Construction Date (0: <01.01.00; 1: <01.01.11;
                    2: <01.01.16; 3: >01.01.16)
        v.   4x  'Bins' of Engine Load (0-7%; 7-10%; 10-20%; 20-100%)
        vi.  2x  'Bins' of Engine RPM affecting NOx (0-2000 RPM; 2000+ RPM)

    However, this function instead assigns simplified Emission Factors per major
    fuel type as presented in 'fuel_emissions_v0.1.csv'. This is observed to be
    a reasonable assumption except in particular instances such as Methane
    emissions from LNG-based Main Engines, where Emission Factors can vary from
    0.2 - 5.5 g/kWh.

    Input Data Fields

        fuel_code_map_me        Code of fuel consumed by the Main Engine after mapping against Operational Characteristics
        fuel_code_map_aux       Code of fuel consumed by the Auxiliary Engine after mapping against Operational Characteristics
        fuel_code_map_boi       Code of fuel consumed by the Boiler Engine after mapping against Operational Characteristics

    Output Data Fields

        co2_me_g_per_gfuel      CO2 (g) produced per gram of Fuel Consumed by the Main Engine
        ch4_me_g_per_kWh        CH4 (g) produced per kWh of Energy Demanded by the Main Engine
        n2o_me_g_per_kWh        N2O (g) produced per kWh of Energy Demanded by the Main Engine
        co2_aux_g_per_gfuel     CO2 (g) produced per gram of Fuel Consumed by the Auxiliary Engine
        ch4_aux_g_per_kWh       CH4 (g) produced per kWh of Energy Demanded by the Auxiliary Engine
        n2o_aux_g_per_kWh       N2O (g) produced per kWh of Energy Demanded by the Auxiliary Engine
        co2_boi_g_per_gfuel     CO2 (g) produced per gram of Fuel Consumed by the Boiler Engine
        ch4_boi_g_per_kWh       CH4 (g) produced per kWh of Energy Demanded by the Boiler Engine
        n2o_boi_g_per_kWh       N2O (g) produced per kWh of Energy Demanded by the Boiler Engine

    """

    fuel_emissions = pd.read_csv(fuel_emissions_dir)

    # Main Engine
    me_fuel_emissions_r = {"fuel_code":"fuel_code_map_me", "g_CO2_per_g_fuel":"co2_me_g_per_gfuel", "g_CH4_per_kWh":"ch4_me_g_per_kWh", "g_N2O_per_kWh":"n2o_me_g_per_kWh"}
    me_fuel_emissions = fuel_emissions.drop(columns="fuel").copy().rename(columns=me_fuel_emissions_r)

    # Auxiliary Engine
    aux_fuel_emissions_r = {"fuel_code":"fuel_code_map_aux", "g_CO2_per_g_fuel":"co2_aux_g_per_gfuel", "g_CH4_per_kWh":"ch4_aux_g_per_kWh", "g_N2O_per_kWh":"n2o_aux_g_per_kWh"}
    aux_fuel_emissions = fuel_emissions.drop(columns="fuel").copy().rename(columns=aux_fuel_emissions_r)

    # Boiler Engine
    boiler_fuel_emissions_r = {"fuel_code":"fuel_code_map_boi", "g_CO2_per_g_fuel":"co2_boi_g_per_gfuel", "g_CH4_per_kWh":"ch4_boi_g_per_kWh", "g_N2O_per_kWh":"n2o_boi_g_per_kWh"}
    boiler_fuel_emissions = fuel_emissions.drop(columns="fuel").copy().rename(columns=boiler_fuel_emissions_r)

    # Merge
    ais_ves_temp_1 = pd.merge(ais_ves, me_fuel_emissions, left_on="fuel_code_map_me", right_on="fuel_code_map_me", how="left")
    ais_ves_temp_2 = pd.merge(ais_ves_temp_1, aux_fuel_emissions, left_on="fuel_code_map_aux", right_on="fuel_code_map_aux", how="left")
    ais_ves = pd.merge(ais_ves_temp_2, boiler_fuel_emissions, left_on="fuel_code_map_boi", right_on="fuel_code_map_boi", how="left")

    print("\nIntroducing Fuel-based and Energy-based Emission Factors for Carbon Dioxide (CO2), Methane (CH4) and Nitrous Oxide (N2O): \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
