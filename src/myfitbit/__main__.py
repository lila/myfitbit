#!/usr/bin/env python
"""
Usage:
  myfitbit [options] steps [--range=<period>]
  myfitbit -h | --help | --version

Options:
  --range=period    either 1d, 1w, or 1m [default: 1d]
  --debug           Show debug info
  -h --help         Show this screen.
  --version         Show version.
"""

import os
import sys
import json
import cherrypy
import threading
import traceback
import webbrowser
import datetime

from urllib.parse import urlparse
from base64 import b64encode
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError
from docopt import docopt


# Environment constants
FITBIT_DIR = "./"
if 'XDG_CONFIG_HOME' in os.environ:
    FITBIT_DIR = os.path.join(os.environ['XDG_CONFIG_HOME'], 'myfitbit')
KEYS_FILE = os.path.join(FITBIT_DIR, 'client_id.json')
TOKEN_FILE = os.path.join(FITBIT_DIR, 'user_token.json')

class OAuth2Server:
    def __init__(self, 
                 client_id, 
                 client_secret, 
                 access_token=None, 
                 refresh_token=None, 
                 expires_at=None, 
                 redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""

        self.fitbit = Fitbit(
            client_id,
            client_secret, 
            access_token,
            refresh_token,
            expires_at,
            redirect_uri=redirect_uri,
            timeout=10,
        )

        self.redirect_uri = redirect_uri

    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()

        # Same with redirect_uri hostname and port.
        urlparams = urlparse(self.redirect_uri)
        cherrypy.config.update({'server.socket_host': urlparams.hostname,
                                'server.socket_port': urlparams.port})

        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()

def savetoken(dict):
    print("refreshing token")
    with open(TOKEN_FILE, 'w') as outfile:
        credentials_as_dict = {
            'access_token': dict['access_token'],
            'refresh_token': dict['refresh_token'],
            'expires_at': dict['expires_at']
        }
        json.dump(credentials_as_dict, outfile, indent=4)
    

def main(args=None):

    arguments = docopt(__doc__, version='v1.0.0') 
    if arguments['--debug']:
        print(arguments)
    if arguments['--help']:
        print(__doc__)
        quit()
    
    if not os.path.exists(FITBIT_DIR):
      os.makedirs(FITBIT_DIR)

    if not os.path.exists(KEYS_FILE):
        print(f'No config file found at : {KEYS_FILE}')
        print( 'Creating empty file.  Fill in with your clientID and client_secret')
        with open(KEYS_FILE, 'w') as outfile:
            json.dump({'client_id': '', 'client_secret':''}, outfile, indent=4)
        sys.exit(1)
    
    with open(KEYS_FILE) as f:
        client = json.load(f)

    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE) as f:
                client.update(json.load(f))
        except:
            pass

    if 'access_token' not in client:
        server = OAuth2Server(**client)
        server.browser_authorize()
        profile = server.fitbit.user_profile_get()
        print('You are authorized to access data for the user: {}'.format(
               profile['user']['fullName']))
        savetoken(server.fitbit.client.session.token)
    
    fitbit = Fitbit(**client, refresh_cb=savetoken)

    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))

    steps = fitbit.time_series('activities/steps', base_date=today, period=arguments['--range'])
    print(sum(int(d['value']) for d in steps['activities-steps']))



def do_main():
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    main(sys.argv)