# test_windprofile.py

import os
import sys

# Add parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tcwindprofile import generate_wind_profile

# Define input parameters
Vmaxmean_ms = 45.8           # [m/s]
Rmax_km = 38.1              # [km]
R34ktmean_km = 228.3        # [km]
lat = 20                      # [degrees]

# Call the main function
# Make the plot
rr_km, vv_ms, R0_estimate_km = generate_wind_profile(Vmaxmean_ms, Rmax_km, R34ktmean_km, lat, plot=True)
print(f"Estimated R0 = {R0_estimate_km:.1f} km")
# No plot
# rr_km, vv_ms, R0_km = generate_wind_profile(Vmaxmean_ms, Rmax_km, R34ktmean_km, lat)
print(f"Estimated R0 = {R0_estimate_km:.1f} km")



# ONLY retrieve the estimated outer radius R0
from tcwindprofile.tc_outer_radius_estimate import estimate_outer_radius
import numpy as np
import math
ms_kt = 0.5144444             # 1 kt = 0.514444 m/s
V34kt_ms = 34 * ms_kt            # [m/s]; outermost radius to calculate profile
R34ktmean_m = R34ktmean_km * 1000
omeg = 7.292e-5  # Earth's rotation rate
fcor = 2 * omeg * math.sin(math.radians(abs(lat)))  # [s^-1]
R0 = estimate_outer_radius(R34ktmean_m=R34ktmean_m, V34kt_ms=V34kt_ms, fcor=fcor)
print(f"Estimated R0 = {R0/1000:.1f} km")