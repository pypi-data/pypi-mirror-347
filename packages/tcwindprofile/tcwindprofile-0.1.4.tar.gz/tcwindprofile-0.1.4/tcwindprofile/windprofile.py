
from tcwindprofile.tc_outer_radius_estimate import estimate_outer_radius

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%% Function for E04 outer wind profile with R0mean input
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def E04_outerwind_r0input_nondim_MM0(r0, fcor, C_d, w_cool, Nr):
    """
    Computes nondimensional radial profile of angular momentum (M/M0) versus (r/r0).
    """
    
    import numpy as np
    
    fcor = abs(fcor)
    M0 = 0.5 * fcor * r0**2
    drfracr0 = 0.001
    if r0 > 2500 * 1000 or r0 < 200 * 1000:
        drfracr0 = drfracr0 / 10.0
    if Nr > 1 / drfracr0:
        Nr = 1 / drfracr0
    rfracr0_max = 1
    rfracr0_min = rfracr0_max - (Nr - 1) * drfracr0
    rrfracr0 = np.arange(rfracr0_min, rfracr0_max + drfracr0, drfracr0)
    MMfracM0 = np.full(rrfracr0.shape, np.nan)
    MMfracM0[-1] = 1
    rfracr0_temp = rrfracr0[-2]  # one step inwards from r0
    MfracM0_temp = MMfracM0[-1]
    MMfracM0[-2] = MfracM0_temp

    # Piecewise linear fit parameters from Donelan2004_fit.m
    C_d_lowV = 6.2e-4
    V_thresh1 = 6
    V_thresh2 = 35.4
    C_d_highV = 2.35e-3
    linear_slope = (C_d_highV - C_d_lowV) / (V_thresh2 - V_thresh1)

    for ii in range(int(Nr) - 2):
        gam = C_d * fcor * r0 / w_cool
        dMfracM0_drfracr0_temp = gam * ((MfracM0_temp - rfracr0_temp**2)**2) / (1 - rfracr0_temp**2)
        MfracM0_temp = MfracM0_temp - dMfracM0_drfracr0_temp * drfracr0
        rfracr0_temp = rfracr0_temp - drfracr0
        MMfracM0[-ii - 2 - 1] = MfracM0_temp
    return rrfracr0, MMfracM0

def generate_wind_profile(Vmaxmean_ms, Rmax_km, R34ktmean_km, lat, plot=False):
    

    import numpy as np
    import math
    import matplotlib.pyplot as plt
    from scipy.interpolate import interp1d
    
    # Set default plot properties: font size 12 (half of 24) and default font
    plt.rcParams.update({
        'font.size': 12,
        'lines.linewidth': 2
    })
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ### INPUTS: AZIMUTHAL-MEAN VALUES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # If you have VmaxNHC (i.e. Best Track values): Vmaxmean_ms = VmaxNHC_ms - 0.55 * Vtrans_ms (Eq 2 of CKK25 -- simple method to estimate azimuthal-mean Vmax from NHC point-max; factor originally from Lin and Chavas (2012))
    # If you have R34ktNHCquadmax (i.e. Best Track values): R34ktmean_m = 0.85 * fac_R34ktNHCquadmax2mean (Eq 1 of CKK25 -- simple estimate of mean R34kt radius from NHC R34kt (which is maximum radius of 34kt); factor originally from DeMaria et al. (2009))
    
    #Vmaxmean_ms = 45.8            # [m/s]; default 45.8; AZIMUTHAL-MEAN maximum wind speed
    #Rmax_m = 38.1 * 1000          # [m]; default 38.1*1000; from bias-adjusted CK22
    #R34ktmean_m = 228.3 * 1000    # [m]; default R34kt = 228.3*1000; MEAN radius of 34kt wind speed
    #lat = 20                      # [degN]; default 20N; storm-center latitude;
    
    Rmax_m = Rmax_km * 1000
    R34ktmean_m = R34ktmean_km * 1000
    ## Default values: Vmaxmean_ms = 45.8 m/s, Rmax_m = 38.1 km, R34ktmean_m = 228.3 km, lat = 20 --> R0=1174.6 km (sanity check)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ### CALCULATE WIND PROFILE
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    print("This code uses a modified‐Rankine vortex between Rmax and R34ktmean_m (default R34kt) and the E04 model beyond R34ktmean_m (and a quadratic profile inside the eye).")
    print("It is designed to guarantee that the profile fits both Rmax and R34kt and will be very close to the true outer radius (R0) as estimated by the full E04 outer solution.")
    print("It is also guaranteed to be very well‐behaved for basically any input parameter combination.")
    
    #%% Calculate some params
    ms_kt = 0.5144444             # 1 kt = 0.514444 m/s
    V34kt_ms = 34 * ms_kt            # [m/s]; outermost radius to calculate profile
    km_nautmi = 1.852
    omeg = 7.292e-5  # Earth's rotation rate
    fcor = 2 * omeg * math.sin(math.radians(abs(lat)))  # [s^-1]
    
    #%% Initial radius vector
    dr = 100  # [m]
    R0mean_initialtoolarge = 3000 * 1000
    rr_full = np.arange(0, R0mean_initialtoolarge + dr, dr)  # [m]
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%% STEP 1) Outer region wind profile (r>R34kt)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%% STEP 1a) Very good estimate of outer edge of storm, R0mean (where v=0)
    #%% Analytic approximation of R0mean, from physical model of non-convecting wind profile (Emanuel 2004; Chavas et al. 2015 JAS)
    # Environmental params
    # Cd = 1.5e-3  # [-]
    # w_cool = 2 / 1000  # [m/s]
    # chi = 2 * Cd / w_cool
    # Mfit = R34ktmean_m * V34kt_ms + 0.5 * fcor * R34ktmean_m**2
    
    # beta = 1.35
    # c1 = 0.5 * fcor
    # c2 = 0.5 * beta * fcor * R34ktmean_m
    # c3 = -Mfit
    # c4 = -R34ktmean_m * Mfit - chi * (beta * R34ktmean_m * V34kt_ms)**2
    # coeffs = [c1, c2, c3, c4]
    # x = np.roots(coeffs).real
    # R0mean_candidates = x[x > 0]
    # R0mean_dMdrcnstmod = R0mean_candidates[0]
    
    Cd = 1.5e-3  # [-]
    w_cool = 2 / 1000  # [m/s]
    beta = 1.35
    R0mean_dMdrcnstmod = estimate_outer_radius(
    R34ktmean_m=R34ktmean_m,
    V34kt_ms=V34kt_ms,
    fcor=fcor,
    Cd=Cd,
    w_cool=w_cool,
    beta=beta
    )

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%% STEP 1b) Wind profile from R0mean --> R34kt
    #%% Exact solution to model of non-convecting wind profile (Emanuel 2004; Chavas et al. 2015 JAS)
    #%% Notes:
    #%% - It is a single integration inwards from R0. *Cannot* integrate out
    #%%   from R34kt, it may blow up (math is weird)
    #%% - Could do a simpler approximate profile instead, but this solution is
    #%%   just as fast doing some sort of curve fit, so might as well use exact
    
    Nr = 100000
    rrfracr0_E04, MMfracM0_E04 = E04_outerwind_r0input_nondim_MM0(R0mean_dMdrcnstmod, fcor, Cd, w_cool, Nr)
    M0_E04approx = 0.5 * fcor * R0mean_dMdrcnstmod**2
    rr_E04approx = rrfracr0_E04 * R0mean_dMdrcnstmod
    vv_E04approx = (M0_E04approx / R0mean_dMdrcnstmod) * ((MMfracM0_E04 / rrfracr0_E04) - rrfracr0_E04)
    vv_E04approx[vv_E04approx > 2 * V34kt_ms] = np.nan
    
    # Zoom into relevant radii
    r0_plot = 1.2 * R0mean_dMdrcnstmod
    rr = rr_full[rr_full < r0_plot]
    # Interpolate approx-E04 solution to original radius vector
    vv_E04approx = np.interp(rr, rr_E04approx, vv_E04approx)
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%% STEP 2) Inner region wind profile (r<=R34kt)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    #%% Simple modified Rankine profile between R34kt and Rmax
    #%% With quadratic profile inside of Rmax
    alp_outer = np.log(Vmaxmean_ms / V34kt_ms) / np.log(Rmax_m / R34ktmean_m)
    vv_outsideRmax = np.full(rr.shape, np.nan)
    rr_outer_mask = rr > Rmax_m
    vv_outsideRmax[rr_outer_mask] = Vmaxmean_ms * (rr[rr_outer_mask] / Rmax_m)**alp_outer
    alp_eye = 2  # quadratic profile in eye
    vv_eye = Vmaxmean_ms * (rr / Rmax_m)**alp_eye
    vv_MR = np.concatenate((vv_eye[rr <= Rmax_m], vv_outsideRmax[(rr > Rmax_m) & (rr < r0_plot)]))
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%% STEP 3) Merge inner and outer wind profiles
    #%% Simple exponential smoother of (inner-outer) moving outwards from R34kt
    
    # No smoothing: direct merge at R34ktmean_m -- will *not* match dV/dr without smoothing
    # vv_MR_E04_R34ktmean_nosmooth = np.concatenate((vv_MR[rr <= R34ktmean_m], vv_E04approx[rr > R34ktmean_m]))
    
    # Match dV/dr at R34kt: exponential smoother of (inner-outer) moving outwards from R34kt
    ii_temp = rr > R34ktmean_m
    rr_beyondR34ktmean = rr[ii_temp]
    vv_MR_beyondR34ktmean = vv_MR[ii_temp]
    vv_E04approx_beyondR34ktmean = vv_E04approx[ii_temp]
    v_adj = -(vv_E04approx_beyondR34ktmean - vv_MR_beyondR34ktmean) * np.exp(-(rr_beyondR34ktmean - R34ktmean_m) / R34ktmean_m)
    vv_E04approx_adj = vv_E04approx_beyondR34ktmean + v_adj
    vv_MR_E04_R34ktmean = np.concatenate((vv_MR[rr <= R34ktmean_m], vv_E04approx_adj))
    
    if plot:
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%% Make plot
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Figure dimensions: original 30 cm x 30 cm, now half: 15 cm x 15 cm (converted to inches)
        fig, ax = plt.subplots(figsize=(15/2.54, 15/2.54))
        ax.plot(rr / 1000, vv_MR_E04_R34ktmean, 'm-', linewidth=3)
        # ax.plot(rr / 1000, vv_MR_E04_R34ktmean_nosmooth, 'g:', linewidth=3)
        ax.plot(Rmax_m / 1000, Vmaxmean_ms, 'k.', markersize=20)
        ax.plot(R34ktmean_m / 1000, V34kt_ms, 'k.', markersize=20)
        ax.plot(R0mean_dMdrcnstmod / 1000, 0, 'm*', markersize=20)
        ax.set_xlabel('radius [km]')
        ax.set_ylabel('azimuthal wind speed [m/s]')
        ax.axis([0, 1.1 * R0mean_dMdrcnstmod / 1000, 0, 1.1 * Vmaxmean_ms])
        # ax.axis([0, 600, 0, 1.1 * Vmaxmean_ms])
        ax.set_title('Complete wind profile (ModRank inner + E04approx outer)', fontsize=12)
        
        # Annotate the top right corner with "Inputs:" and the values of Vmaxmean_ms, Rmax_m, (R34ktmean_m, V34kt_ms), and lat
        annotation = (f"Inputs:\n"
                      f"Vmax_mean = {Vmaxmean_ms:.1f} m/s\n"
                      f"Rmax = {Rmax_m/1000:.1f} km\n"
                      f"(R34kt_mean, V34kt_ms) = ({R34ktmean_m/1000:.1f} km, {V34kt_ms:.1f} m/s)\n"
                      f"lat = {lat:.1f}°N\n"
                      f"\n"
                      f"Output:\n"
                      f"R0_mean = {R0mean_dMdrcnstmod / 1000:.1f} km")
        ax.text(0.95, 0.95, annotation, transform=ax.transAxes, ha='right', va='top',
                fontsize=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        plt.savefig('Operational_demo_vmaxR34ktRmax_to_windprofile.jpg', format='jpeg')
        plt.show()
        
    # Return radius [km], wind speed [m/s], and R0mean [km]
    # Interpolate to 1 km resolution
    rr_km = rr / 1000
    rr_km_interp = np.arange(0, rr_km.max(), 0.1)  # 0.1 km resolution
    vv_mps_interp = np.interp(rr_km_interp, rr_km, vv_MR_E04_R34ktmean)
    return rr_km_interp, vv_mps_interp, R0mean_dMdrcnstmod / 1000


    
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--vmax_ms", type=float, default=45.8, help="Vmax in m/s")
    parser.add_argument("--rmax_km", type=float, default=38.1, help="Rmax in km")
    parser.add_argument("--r34_km", type=float, default=228.3, help="R34ktmean in km")
    parser.add_argument("--lat", type=float, default=20, help="Latitude in degrees")
    args = parser.parse_args()

    # Convert km to m
    rr_km, vv_ms, R0_km = generate_wind_profile(args.vmax_ms, args.rmax_km, args.r34_km, args.lat)

