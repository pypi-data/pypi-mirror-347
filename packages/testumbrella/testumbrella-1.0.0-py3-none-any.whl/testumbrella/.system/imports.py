from clight.system.importer import cli  # DON'T REMOVE THIS LINE

# <umbrella-package>
# import testufirst==1:0:0
# import testusecond==1:0:0
# import testuthird==1:0:0
# </umbrella-package>

import os
import sys
import testufirst
import importlib.metadata

from modules.jobs import jobs
