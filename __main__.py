''' app entry point '''

import sys
import os

sys.path.append(os.path.dirname(__file__))
from redshifttray import RedshiftTray

app = RedshiftTray([])
sys.exit(app.exec_())
