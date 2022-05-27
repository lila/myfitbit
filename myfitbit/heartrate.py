# heartrate.py

# convenience functions for returning time series data from fitbit api
# and converting them to xarray tensors.

import time

import pandas as pd
from fitbit.api import Fitbit


def getHeartrateAsDataframe(f, dates):
    first = True
    for day in dates:
        fit_statsHR = f.intraday_time_series(
            "activities/heart", base_date=day, detail_level="1sec"
        )
        if not fit_statsHR["activities-heart-intraday"]["dataset"]:
            print(f"no data for {day}")
            continue
        tmp = pd.DataFrame(
            fit_statsHR["activities-heart-intraday"]["dataset"]
        ).rename({"value": day}, axis=1)
        tmp["time"] = pd.TimedeltaIndex(tmp["time"]).round("1min")
        tmp = tmp.set_index(["time"])
        tmp = tmp.resample("1min").mean()
        if first:
            first = False
            df = tmp
        else:
            df = df.join(tmp)
        time.sleep(5)
    return df
