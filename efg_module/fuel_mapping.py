import sys
import numpy as np
import pandas as pd

def fuel_mapping(ais_ves, sfcs_dir):
    """
    This function is used to understand the type of fuel being consumed by Main,
    Auxiliary and Boiler engines, and use this information to introduce a 'Base'
    Specific Fuel Consumption for each engine that can be used in the conversion
    of Energy Demand and Fuel Consumption.

    There are a total of 14 Main Engine Code & Type pairs contained in the
    existing IMO Vessel Specifications dataset sourced from IHS Markit (now S&P
    Global). It's worth noting that Auxiliary and Boiler Engines are included in
    this list, which is as follows:

        1	Slow-Speed Diesel-cycle (SSD)
        2	Medium-Speed Diesel-cycle (MSD)
        3	High-Speed Diesel-cycle (HSD)
        4	Slow-Speed LNG Otto-cycle Dual-Fuel
        5	Medium-Speed LNG Otto-cycle Dual-Fuel
        6	LNG Diesel-cycle Dual-Fuel
        7	Lean Burn Spark-Ignited (LBSI)
        8	Methanol
        9	Gas Turbine
        10	Sail
        11	Steam Turbine and Boilers
        12	Batteries
        13	'Non-propelled'
        14	Diesel Electric
        *	Auxiliary Engines

    In addition, the Matlab code underpinning the 4th IMO GHG Study considers 8
    alternative fuel types that include:

        1	Heavy Fuel Oil (2.7%)
        2	Low Sulphur Heavy Fuel Oil (1.5%)
        3	Low Sulphur Heavy Fuel Oil (1.0%)
        4	Low Sulphur Heavy Fuel Oil (0.5%)
        5	Marine Diesel Oil/Marine Gas Oil (0.1%)
        6	Liquified Natural Gas (LNG)
        7	Methanol
        8	Nuclear (no fuel)

    On inspection of the 4th IMO GHG Study method, it seems likely that the
    LSHFO variants are included owing to the study considering multiple years
    across the time period 2012-18, where the sulphur content of HFO is noted to
    vary (Faber et al, 2020). Whilst relevant to that study, this EFG module
    won't be designed to account for this just yet. In addition, no Nuclear-
    powered vessels were noted to be included in the Vessel Specifications
    dataset, and so these have been left out. The remaining fuel types (which
    are noted to align with the IMO IV Vessel Specifications dataset) are as
    follows, renumbered to align with the IMO IV Vessel Specifications dataset:

        1	Heavy Fuel Oil
        4	Marine Diesel Oil/Marine Gas Oil (0.1%)
        5	Liquified Natural Gas (LNG)
        6	Methanol

    The question then is how each of these 4 fuel types allocate to the
    engine types presented above. In the first instance, it seems that the IMO
    IV Vessel Specifications dataset contains fields designating the types of
    fuel consumed by each engine of every vessel in the database. These data
    fields are therefore taken forward, however the origin of these fields
    should be investigated further. For now it's assumed that these are taken
    directly from the IHS Markit dataset and are reliable.

    A secondary question regards what 'Base' Specific Fuel Consumption value is
    appropriate for each Engine Code & Type pair with Fuel Type in order to be
    taken forward for the conversion of Energy Demand to Fuel Consumption. In
    this instance, these values have been sourced from the IMO IV folder,
    specifically the spreadsheet 'EF_g_per_kWh.xlsx'. This version of the module
    goes by the SFC tables published in 4th IMO GHG Study report, meaning that
    SFCs are assigned per 'Tier' of the engine. However, a future version of
    this function may wish to incorporate the differentiation by Engine
    'Generation', contained in the separate spreadsheets of the IMO IV folder.
    This likely explains the differences between the existing '_sfoc' fields in
    the Vessel Specifications dataset and the 'sfc_base_ _g_per_kWh' fields
    newly derived in this function.

    Future iterations of this function may wish to consider instantaneous
    operational characteristics of vessel activity such as whether the vessel
    is operating within a special geographic area such as an Emission Control
    Area (ECA) where Low-Sulphur variants of fuel are often used. For this
    reason, a 'placeholder' is included in the code, setting up new fields
    ('fuel_code_map_') that take the existing fuel type fields ('_fuel') per
    engine and 'map' them to new values. They just copy the existing fields for
    now.

    Finally, this function will be increasingly important for evaluating the
    fuel consumed by engines equipped with dual-fuel engines, which are likely
    to form an increasingly large share of the fleet in the years to come.

    Input Data Fields

        engine_code             Code of the Engine provided in the Vessel Specifications dataset
        tier                    Code the Engine Tier representing the engine's manufacture date
        me_fuel                 Code of fuel consumed by the Main Engine before mapping against Operational Characteristics
        aux_fuel                Code of fuel consumed by the Auxiliary Engine before mapping against Operational Characteristics
        boiler_fuel             Code of fuel consumed by the Boiler Engine before mapping against Operational Characteristics
        sfcs                    Dataset read in that provides 'Base' Specific Fuel Consumption values by Engine Type, Tier and Fuel Consumed

    Output Data Fields

        fuel_code_map_me        Code of fuel consumed by the Main Engine after mapping against Operational Characteristics
        fuel_code_map_aux       Code of fuel consumed by the Auxiliary Engine after mapping against Operational Characteristics
        fuel_code_map_boi       Code of fuel consumed by the Boiler Engine after mapping against Operational Characteristics
        sfc_base_me_g_per_kwh   'Base' Specific Fuel Consumption (g per g_fuel) of the Main Engine
        sfc_base_aux_g_per_kwh  'Base' Specific Fuel Consumption (g per g_fuel) of the Auxiliary Engine
        sfc_base_boi_g_per_kwh  'Base' Specific Fuel Consumption (g per g_fuel) of the Boiler Engine

    """

    ## PLACEHOLDER for Amending Fuel Type consumed per Engine Type depending on Operational Characteristics.
    ais_ves["fuel_code_map_me"] = ais_ves.me_fuel.values
    ais_ves["fuel_code_map_aux"] = ais_ves.aux_fuel.values
    ais_ves["fuel_code_map_boi"] = ais_ves.boiler_fuel.values


    # Remove 'Sail', 'Batteries', 'Non-propelled' and 'Diesel Electric from ais_ves
    # 11 and 15 added here so that a vessel's Main Engine can be Steam Turbine/Boiler (or Auxiliary) if necessary
    ais_ves = ais_ves[ais_ves.engine_code.isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 15])]
    # tier_c = np.where(ais_ves.tier... )

    ## DERIVING SFCs
    # Read-in the table of SFCs by Engine Type, Tier and Fuel Type
    sfcs = pd.read_csv(sfcs_dir)
    print("\nReading in Specific Fuel Consumption values by Engine Type, Tier and Fuel Type: \n\n", sfcs.iloc[:2], "\n")

    # Main SFCs
    sfcs_main_r = {"fuel_code": "fuel_code_map_me", "fuel_type": "fuel_type_map_me", "base_sfc":"sfc_base_me_g_per_kwh"}
    sfcs_main = sfcs[sfcs.engine_code.isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 15])].rename(columns=sfcs_main_r)

    # Auxiliary SFCs
    sfcs_aux_c = ["fuel_code", "fuel_type", "base_sfc"]
    sfcs_aux_r = {"fuel_code": "fuel_code_map_aux", "fuel_type": "fuel_type_map_aux", "base_sfc":"sfc_base_aux_g_per_kwh"}
    sfcs_aux = sfcs[sfcs_aux_c][sfcs.engine_code.isin([15])].rename(columns=sfcs_aux_r)

    # Boiler SFCs
    sfcs_boiler_c = ["fuel_code", "fuel_type", "base_sfc"]
    sfcs_boiler_r = {"fuel_code": "fuel_code_map_boi", "fuel_type": "fuel_type_map_boi", "base_sfc":"sfc_base_boi_g_per_kwh"}
    sfcs_boiler = sfcs[sfcs_boiler_c][sfcs.engine_code.isin([11])].rename(columns=sfcs_boiler_r)


    ## MAIN ENGINE
    ais_ves = pd.merge(ais_ves, sfcs_main, left_on=["engine_code", "tier", "fuel_code_map_me"], right_on=["engine_code", "tier", "fuel_code_map_me"], how="left")

    ## AUXILIARY ENGINE
    ais_ves = pd.merge(ais_ves, sfcs_aux, left_on=["fuel_code_map_aux"], right_on=["fuel_code_map_aux"], how="left")

    ## BOILER ENGINE
    ais_ves = pd.merge(ais_ves, sfcs_boiler, left_on=["fuel_code_map_boi"], right_on=["fuel_code_map_boi"], how="left")
    print("\nSpecific Fuel Consumption values integrated into ais_ves dataframe: \n\n", ais_ves.iloc[:2], "\n")

    return ais_ves
