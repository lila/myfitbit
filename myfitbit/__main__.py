#!/usr/bin/env python3
"""
Usage:
  myfitbit [options] steps [--range=<period>]
  myfitbit [options] heartrate [--day=<day>]
  myfitbit -h | --help | --version

Options:
  --range=period    either 1d, 1w, or 1m [default: 1d]
  --day=day         string in the form %Y-%m-%d
  --debug           Show debug info
  --raw             return the raw json packet
  --omh             convert data into openmhealth standard
  -h --help         Show this screen.
  --version         Show version.
"""

import os
import sys
import datetime
import json
import requests
from codetiming import Timer
from docopt import docopt 

from .setup import setup

def main(args=None):

    arguments = docopt(__doc__, version="v1.0.0")
    if arguments["--debug"]:
        print(arguments)
    if arguments["--help"]:
        print(__doc__)
        quit()

    fitbit = setup(debug=arguments["--debug"])
    
    t = Timer()
    t.start()

    if arguments["--omh"]:
        if os.environ['OPENMHEALTH_ENDPOINT']:
            urlhost = os.environ['OPENMHEALTH_ENDPOINT']
        else:
            print("set environment variable OPENMHEALTH_ENDPOINT to convert from fitbit to openmhealth standard")
            quit()

    if arguments["--day"]:
        today = arguments["--day"]
    else:
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
            print(json.dumps(hr, indent=4))
        elif arguments["--omh"]:
            url = urlhost + "/heart-rate/intraday/"
            headers = {
                'Content-Type': 'application/json',
            }
            req = requests.post(url = url, data = json.dumps(hr), headers=headers)
            print(json.dumps(json.loads(req.text), indent=4))
        else:
            print(json.dumps(hr['activities-heart-intraday']['dataset']))
    
    t.stop()


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
