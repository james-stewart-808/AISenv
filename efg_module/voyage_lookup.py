import sys
import numpy as np
import pandas as pd

def voyage_lookup(ais_ves):
    """
    A function to look up details of the voyage associated with instantaneous
    vessel activity. This is useful for the calculation of Corrected
    Instantaneous Draught in 'corrected_draught.py'.

    In the IMO IV model this functionality is included in 'corrected_draught.m',
    however it has been separated here as it has the potential to be useful as
    a standalone function for fetching data fields derived during the Stops/
    Voyages Identification process, e.g. capturing whether an Origin or
    Destination is in the EU for recording an MRV flag or whether the voyage is
    exposed to EU regulation such as FuelEU Maritime or the EU ETS.

    In  imo         integer         Vessel IMO number.
        ts          timestamp       Timestamp of instantaneous vessel activity.
    Out voyage      dataframe       Voyage information associated with activity.
        ...
    """

    return ais_ves
