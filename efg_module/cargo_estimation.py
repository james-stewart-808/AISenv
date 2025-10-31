import sys
import numpy as np
import pandas as pd

def cargo_estimation(ais_ves): # bin_spd_draught.m
    """
    A function to first estimate cargo mass associated with vessel activity.
    First, vessel lightweight is estimated using a bespoke function.
    Then, the Block Coefficient is derived and used to estimate payload mass
    based on (corrected) draught. Finally, estimated cargo mass is evaluated.

    IMO IV code to include:
        bin_speed_draught.m:
            Deriving Lightweight-Tonnage (LWT), cargo weight, Block Coefficient
            and payload using Instantanous Draught.

    In  imo         integer         Vessel IMO number.
        ts          timestamp       Timestamp of instantaneous vessel activity.
    Out voyage      dataframe       Voyage information associated with activity.
        ...
    """

    return ais_ves
