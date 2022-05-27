"""simple commondline moodule to connect and display fitbit stats

package provides a main function as well as modules for setup
configuration and modules for use with jupyter notebooks.

Typical use:

    This package provides two modules, `setup` and `heartrate` and
    a commandline main.

    1. mostly, you will use the main.  see README file that provides
        installation instructions.

    2. setup module reads the client_ids and tokens saved from previous
        runs and returns an object that can be used to query data::

        f = fitbit.setup.setup()
        steps = fitbit.time_series(
            "activities/steps", base_date=today, period=arguments["--range"]
        )

        `f` in this case is from `fitbit.api` from
        https://pypi.org/project/fitbit/

    3. you can do the same from a jupyter notebook, an example is provided.

Notice:

This is meant as illustrative, example for connecting to the web
apis.  Only basic functionality is provided (steps and heartrate),
but can be easily extended.


"""


__all__ = ["setup", "heartrate"]
from myfitbit import heartrate, setup
