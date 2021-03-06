import json
import os
import sys

from fitbit.api import Fitbit

# internal imports
from .oauthserver import OAuth2Server

# Environment constants
FITBIT_DIR = "./"
if "XDG_CONFIG_HOME" in os.environ:
    FITBIT_DIR = os.path.join(os.environ["XDG_CONFIG_HOME"], "myfitbit")
KEYS_FILE = os.path.join(FITBIT_DIR, "client_id.json")
TOKEN_FILE = os.path.join(FITBIT_DIR, "user_token.json")


def savetoken(settings):
    print("refreshing token")
    with open(TOKEN_FILE, "w") as outfile:
        credentials_as_dict = {
            "access_token": settings["access_token"],
            "refresh_token": settings["refresh_token"],
            "expires_at": settings["expires_at"],
        }
        json.dump(credentials_as_dict, outfile, indent=4)


def setup(debug=False):
    if debug:
        print("myfitbit setup:")

    if not os.path.exists(FITBIT_DIR):
        if debug:
            print(f"creating: ${FITBIT_DIR}")
        os.makedirs(FITBIT_DIR)

    if not os.path.exists(KEYS_FILE):
        print(f"No config file found at : {KEYS_FILE}")
        print(
            "Creating empty file.  Fill in with your clientID and client_secret"
        )
        with open(KEYS_FILE, "w") as outfile:
            json.dump({"client_id": "", "client_secret": ""}, outfile, indent=4)
        sys.exit(1)

    with open(KEYS_FILE) as f:
        client = json.load(f)

    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE) as f:
                client.update(json.load(f))
        except:
            pass

    if debug:
        print(f"client = ${client}")

    if "access_token" not in client:
        server = OAuth2Server(**client)
        server.browser_authorize()
        profile = server.fitbit.user_profile_get()
        print(
            "You are authorized to access data for the user: {}".format(
                profile["user"]["fullName"]
            )
        )
        savetoken(server.fitbit.client.session.token)

    return Fitbit(**client, refresh_cb=savetoken)
