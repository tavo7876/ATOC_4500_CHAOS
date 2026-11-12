# This Repository is for ATOC 4500 Chaos Class Final Project. 


### RMSE.ipynb holds the code for plotting lead time vs skill(RMSE) 
- Use the knobs at the top to select your data for snotel.
- Forecast files are from ECMWF, download from https://ecds.ecmwf.int/datasets/s2s-forecasts?tab=download. 
- Currently this will only work with SWE 






#### Things to remember
- This plots the change of snow, the forecast is all incoming and dosent hold current conditions, the inital snow is removed from snotel observations to solve for this.

- The Forecast data is converted from SWE in kg/m^2 to Inchs to match snotels units.
