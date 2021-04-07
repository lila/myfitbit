# MyFitbit 

`myfitbit` is a simple little program to connect to fitbit backend and 
retrieve the user's data.  This includes both a commandline app, called 
`myfitbit` that when run has a few options for data retrieval.  for example

`% myfitbit steps` 

returns the number of steps for the user as of the time the user runs it.

In addition, you can use a jupyter notebook and get the raw data and process it
with pandas.  See the example notebook `myfitbit.ipynb`.

## configuration

First step is to register with fitbit.dev and get a `client_id` and `secret_key`.  
create a file in `~/.config/myfitbit/client_id.json` and put these values in there.

then, install the commandline tools:

`% sudo python3 setup.py install`

finally, run the command:

`% myfitbit steps`

This will kick off an oauth2 process to authenticate your fitbit user account and 
grant permission to the application to access your data.

## Commandline Usage

```
% myfitbit
Usage:
  myfitbit [options] steps [--range=<period>]
  myfitbit -h | --help | --version

Options:
  --range=period    either 1d, 1w, or 1m [default: 1d]
  --debug           Show debug info
  -h --help         Show this screen.
  --version         Show version.
```

### Examples

Return the number of steps so far today:
```
% myfitbit steps
5114
```

Return the number of steps over the past week:
```
% myfitbit steps --range=1w
67606
```

## Notebook usage

You have to configure the `client_id.json` file with the client id and secret
as above.  Then you can call the setup routine.

```
sys.path.append('src/myfitbit')

from src.myfitbit.setup import setup
f = setup()
f
```

Then use `f` to access the fitbit API directly.

