dependencies = ("pandas","requests")
missing_dependencies = []
for dependency in dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append("{}: {}".format(dependency, e))
        del e
if missing_dependencies:
    raise ImportError(
        "Unable to import required packages: \n" + "\n".join(missing_dependencies)
    )


__version__ = "0.1.2"

del dependencies, dependency, missing_dependencies

from optshare.option import *
from optshare.index import *
from optshare.market_yield import *
