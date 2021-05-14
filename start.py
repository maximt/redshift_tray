''' app entry point '''

import sys
from redshifttray import RedshiftTray

if __name__ == "__main__":
    app = RedshiftTray([])
    sys.exit(app.exec_())
