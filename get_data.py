import cdsapi
import os
os.makedirs("DATA", exist_ok=True)


dataset = "s2s-forecasts"
client = cdsapi.Client()


# NOTE YOU Must HAVE Creditials from https://ecds.ecmwf.int/datasets/s2s-forecasts?tab=download, put in a config file

# (year, month, day): Mondays, so leads to Mar 21 are 7, 14, 21, 28 days
inits = [
    ("2016", "03", "14"),   # lead 7 d
    ("2016", "03", "07"),   # lead 14 d
    ("2016", "02", "29"),   # lead 21 d
    ("2016", "02", "22"),   # lead 28 d
]

# 0 to 840 h covers Mar 28 even for the Feb 22 init (35 days)
steps = [str(h) for h in range(0, 841, 24)]

for year, month, day in inits:
    request = {
        "origin": "ecmwf",
        "year": year,
        "month": month,
        "day": day,
        "time": "00:00",
        "level_type": "single_level",
        "variable": [
            "10_m_u_component_of_wind",
            "10_m_v_component_of_wind",
            "snow_fall_water_equivalent",
            "total_precipitation",
        ],
        "forecast_type": "perturbed_forecast",
        "leadtime_hour": steps,
        "data_format": "grib",
        "area": [43, -110, 36, -101],
    }
    target = rf"C:\Users\tatev\OneDrive\Desktop\Chaos_final\ATOC_4500_CHAOS\DATA\s2s_{year}{month}{day}.grib"
    print("requesting", target)
    client.retrieve(dataset, request).download(target)