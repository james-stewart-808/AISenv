import sys
import time
import numpy as np
import pandas as pd

"""
Energy Demand, Fuel Consumption and GHG Generation (EFG) Module

The EFG Module builds on the development of the Fuel Use Statistics and
Emissions (FUSE) model developed by UMAS throughout the 2010's, ultimately
culminating in the model underpinning the 4th IMO GHG Study. This model has been
developed primarily to serve the research purposes of the UCL Shipping and
Oceans Research Group, however it is freely available for other academics,
research organisations and national government agencies interested in its
application to suit their own needs.

The aim has been to develop an open source version of the fuel consumption model
developed in the 4th IMO GHG Study using basic Python and Pandas operations,
incorporating Git versioning. The model is designed to pass Pandas dataframes
between a series of functions relating to the various functionalities of the
model such that calculations are vectorised, a design that takes
advantage of the the Pandas library’s ability to run calcuations in C for
enhanced computational speed.

This wrapper function is intended to be used to execute the EFG Module for the
evaluation of Energy Demands, Fuel Consumption and GHG Emissions associated with
Vessel Activity, as represented in AIS data. The module requires three datasets
as input which are loaded using the 'load_datasets' function:

    - AIS

    The AIS dataset should represent hourly movements for each vessel in
    a format that will enable the rest of the EFG module to run.

    - Vessel Specifications

    The Vessel Specifications dataset should cover data fields that will enable
    the evaluation of energy demand of the Main Engine via the Admiralty
    Formula, as well as fuel consumption of Main, Auxiliary and Boiler engines.

    - Voyages

    A stops identification process should have been run to identify
    stops and infer individual voyages conducted by the vessel. Voyages data is
    useful as it can provide inference on the exposure of vessel activity to
    regional maritime GHG regulations such FuelEU Maritime or the EU ETS,
    other regulations such as requirements to submit EU MRV data, plus voyage
    data is utilised heavily in calculations to derive corrected instantaneous
    vessel draught, which is subsequently an important input into Main Engine
    energy demand calculations.

Further information and context surrounding the EFG Module is available via a
series of iPython notebooks written in the Jupyter language, where users can
explore the theory underpinning the model and the core assumptions that enable
it to operate. A validation of the model against EU MRV data is also provided.

The wrapper is intended to be run locally from a Command-line Interface, for
example on Mac Terminal using the following command:

    % python3 efg_wrapper.py

Output from the module will be saved in CSV format to the directory assigned to
the variable 'efg_module_dir', so this should be amended to the correct location
before running.
"""

print("\n### INITIATING EFG MODULE ###")
start = time.perf_counter()
efg_module_dir = "/Users/apple/repos/AISenv/efg_module/"

print("\nEXECUTING LOAD_DATASETS.PY\n")
from load_datasets import load_datasets
ais_ves = load_datasets() # could include IMO number as an input field.
print("\nEnding load_datasets.py.\n")
print("\n______________________________________________________________________\n")

print("\nnEXECUTING FUEL_MAPPING.PY\n") # Already accounted for in Vessel Specs? Check if necessary! What's different in this case?
from fuel_mapping import fuel_mapping # Update description once Fuel-Engine-Emissions mapping is in-place.
ais_ves = fuel_mapping(ais_ves)
print("\nEnding fuel_mapping.py.\n")
print("\n______________________________________________________________________\n")

#print("\nEXECUTING VOYAGE_LOOKUP.py\n")
#from voyage_lookup import voyage_lookup
#ais_ves = voyage_lookup(ais_ves)
#print("\nEnding voyage_lookup.py.\n")
#print("\n______________________________________________________________________\n")

#print("\nEXECUTING CORRECTED_DRAUGHT.PY\n")
#from corrected_draught import corrected_draught
#ais_ves = corrected_draught(ais_ves)
#print("\nEnding corrected_draught.py.\n")
#print("\n______________________________________________________________________\n")

#print("\nEXECUTING CARGO_ESTIMATION.PY\n")
#from cargo_estimation import cargo_estimation
#ais_ves = cargo_estimation(ais_ves)
#print("\nEnding cargo_estimation.py.\n")
#print("\n______________________________________________________________________\n")

print("\nEXECUTING POWER_MAIN_ENGINE.PY\n")
from power_main_engine import power_main_engine
ais_ves = power_main_engine(ais_ves)
print("\nEnding power_main_engine.py.\n")
print("\n______________________________________________________________________\n")

print("\nEXECUTING OPERATIONAL_MODE.PY\n") # Replace with np.where() ?
from operational_mode import operational_mode
ais_ves = operational_mode(ais_ves)
print("\nEnding operational_mode.py.\n")
print("\n______________________________________________________________________\n")

print("\nEXECUTING POWER_AUX_BOILER_ENGINE.PY\n")
from power_aux_boiler_engines import power_aux_boiler_engines
ais_ves = power_aux_boiler_engines(ais_ves)
print("\nEnding power_aux_boiler_engines.py.\n")
print("\n______________________________________________________________________\n")

print("\nEXECUTING FUEL_CONSUMPTION.PY\n")
from fuel_consumption import fuel_consumption
ais_ves = fuel_consumption(ais_ves)
print("\nEnding fuel_consumption.py.\n")
print("\n______________________________________________________________________\n")

print("\nEXECUTING EMISSION_FACTORS.PY\n")
from emission_factors import emission_factors
ais_ves = emission_factors(ais_ves)
print("\nEnding emission_factors.py.\n")
print("\n______________________________________________________________________\n")

print("\nEXECUTING EMISSIONS.PY\n")
from emissions import emissions
ais_ves = emissions(ais_ves)
print("\nEnding emissions.py.\n")
print("\n______________________________________________________________________\n")

ais_ves.head().to_csv(efg_module_dir + "runs/output.csv", index=False)
finish = time.perf_counter()
print("\nFinished running the EFG Module ({0} minutes).\n".format(int((finish-start) / 60)))
print("**********************************************************************")
print("**********************************************************************")
print("**********************************************************************\n\n\n\n\n\n")
