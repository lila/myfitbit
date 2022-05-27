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

import datetime
import json
import os
import sys

import requests
from codetiming import Timer
from docopt import docopt

from .setup import setup


def main():
    """run the main"""

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
        if os.environ["OPENMHEALTH_ENDPOINT"]:
            urlhost = os.environ["OPENMHEALTH_ENDPOINT"]
        else:
            print(
                "set environment variable OPENMHEALTH_ENDPOINT to convert from fitbit to openmhealth standard"
            )
            quit()

    if arguments["--day"]:
        today = arguments["--day"]
    else:
        today = str(datetime.datetime.now().strftime("%Y-%m-%d"))

    if arguments["steps"]:
        steps = fitbit.time_series(
            "activities/steps", base_date=today, period=arguments["--range"]
        )
        if steps != {} and isinstance(
            steps["activities-steps"][0]["value"], str
        ):
            steps["activities-steps"][0]["value"] = int(
                steps["activities-steps"][0]["value"]
            )

        if arguments["--raw"]:
            print(json.dumps(steps, indent=4))
            # print(steps)
        elif arguments["--omh"]:
            url = urlhost + "/step-count/summary"
            headers = {"Content-Type": "application/json"}
            req = requests.post(
                url=url, data=json.dumps(steps), headers=headers
            )
            print(json.dumps(json.loads(req.text), indent=4))
        else:
            print(sum(int(d["value"]) for d in steps["activities-steps"]))

    elif arguments["heartrate"]:
        heartrate = fitbit.intraday_time_series(
            "activities/heart", base_date=today, detail_level="1sec"
        )

        if arguments["--raw"]:
            print(json.dumps(heartrate, indent=4))
        elif arguments["--omh"]:
            url = urlhost + "/heart-rate/intraday/"
            headers = {"Content-Type": "application/json"}
            req = requests.post(
                url=url, data=json.dumps(heartrate), headers=headers
            )
            print(json.dumps(json.loads(req.text), indent=4))
        else:
            print(json.dumps(heartrate["activities-heart-intraday"]["dataset"]))

    t.stop()


def do_main():
    """run the program, catch any interrupts and exit"""
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            # hard exit
            os._exit(0)  # pylint: disable=protected-access


if __name__ == "__main__":
    main()
