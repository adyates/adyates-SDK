import os


TOR_APIKEY  = os.environ.get("TOR_ONEAPIKEY", None)
TOR_URI = os.environ.get("TOR_BASEURI", "https://the-one-api.dev/v2")

if not TOR_APIKEY:
    raise RuntimeError('pandelyon-theonesdk: Enviroment variable TOR_ONEAPIKEY is not set.  Please set before importing again')


# Convenience API imports
from tor import movies

Movies = movies.Movies