import sys
import numpy as np
import pandas as pd

def corrected_draught(ais_ves): # voyage_draight_assignment.m
    """
    A function for providing 'clean' draught values associated with vessel
    movements. First assign as the median draught values across the entire
    voyage, or the average draught value across the entire year where this isn't
    available.

    IMO IV code to include:
        voyage_draught_assignment.m:
            Algorithmic process for assigning corrected instantaneous draught
            values. Assigns average instantaneous draught across the whole
            year where no voyages are recorded, but median instantaneous draught
            observed across each whole voyage where they do exist. Where
            Instantaneous Draught is NaN or exceeds the Reference Draught, the
            Reference Draught replaces Instantaneous Draught. Periods outside of
            captured voyages (at the Start and End of the Year) are also
            accounted for.  


    In  imo         integer         Vessel IMO number.
        ts          timestamp       Timestamp of instantaneous vessel activity.
    Out voyage      dataframe       Voyage information associated with activity.
        ...
    """

    return ais_ves
