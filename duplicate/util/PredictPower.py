# charging power prediction for backend

import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np

def predict_power(self, charger_id, current_time):
    charging_power = np.array([self.maximum_dc_charging_power] * 4 + [self.maximum_ac_charging_power] * 6)
    return charging_power
