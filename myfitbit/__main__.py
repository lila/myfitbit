#!/usr/bin/env python3
"""
Usage:
  myfitbit [options] steps [--range=<period>]
  myfitbit [options] heartrate [--range=<period>]
  myfitbit -h | --help | --version

Options:
  --range=period    either 1d, 1w, or 1m [default: 1d]
  --debug           Show debug info
  --raw             return the raw json packet
  -h --help         Show this screen.
  --version         Show version.
"""

import os
import sys
import datetime
from docopt import docopt

import myfitbit.setup as setup


def main(args=None):

    arguments = docopt(__doc__, version="v1.0.0")
    if arguments["--debug"]:
        print(arguments)
    if arguments["--help"]:
        print(__doc__)
        quit()

    fitbit = setup.setup()

    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))

    if arguments["steps"]:
        steps = fitbit.time_series(
            "activities/steps", base_date=today, period=arguments["--range"]
        )
        if arguments["--raw"]:
            print(steps["activities-steps"])
        else:
            print(sum(int(d["value"]) for d in steps["activities-steps"]))
    
    elif arguments["heartrate"]:
        hr = fitbit.intraday_time_series('activities/heart', base_date=today, detail_level='1sec')

        if arguments["--raw"]:
            print(hr['activities-heart-intraday']['dataset'])
        else:
            print(hr['activities-heart-intraday']['dataset'])


def do_main():
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main(sys.argv)
