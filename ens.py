import os, sys

# Make the ecCodes DLL findable (must run BEFORE importing xarray/cfgrib)
os.environ["PATH"] = os.path.join(sys.prefix, "Library", "bin") + os.pathsep + os.environ["PATH"]

import xarray as xr
import cfgrib
import snotelpy as sp
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np




def load_forecast(grib_file, index_dir='indexes', FORECAST_VAR='sf'):
    """Open a GRIB file and return the dataset containing FORECAST_VAR.

    The .idx index cfgrib writes remembers the exact path string of the GRIB.
    If the path differs on the next open (relative vs absolute, file moved),
    cfgrib says "incompatible", ignores the index and rescans the whole file.
    So: always use the absolute path, and name the index by the GRIB's basename.
    """
    grib_file = os.path.abspath(grib_file)
    if index_dir is None:
        kwargs = {}  # default: cfgrib writes the .idx next to the GRIB
    else:
        os.makedirs(index_dir, exist_ok=True)
        base = os.path.basename(grib_file)
        kwargs = {"indexpath": os.path.join(os.path.abspath(index_dir), base + ".{short_hash}.idx")}
    dss = cfgrib.open_datasets(grib_file, backend_kwargs=kwargs)
    # pick the dataset containing the variable instead of trusting list order
    for ds in dss:
        if FORECAST_VAR in ds.data_vars:
            return ds
    raise ValueError(f"{FORECAST_VAR} not found in {grib_file}")




def forecast_basin(ds, target_start, target_end,lat_bounds, lon_bounds):



    sf_bounded = ds['sf'].sel(latitude = slice(lat_bounds[1], lat_bounds[0]),
                              longitude = slice(lon_bounds[0],lon_bounds[1]))


    sf_start = sf_bounded.sel(valid_time = target_start)
    sf_end = sf_bounded.sel(valid_time = target_end)


    sf_diff = (sf_end - sf_start) / 25.4

    basin_fc = sf_diff.mean(dim = ["latitude", "longitude"])

    return basin_fc



def observed_gain(snotel, target_start, target_end,element = 'WTEQ'):


    obs_start = snotel[element].sel(time = target_start)
    obs_end = snotel[element].sel(time = target_end)


    obs_gain = (obs_end - obs_start).mean(dim='station')    

    return obs_gain



def score_members(members, obs):
    print(f"Ensemble mean Error: {float((members.mean() - obs.values))}")
    print(f"Rank of Obs: { float((members < obs).mean())}")
    print(f"STD: {float(members.std())}")


