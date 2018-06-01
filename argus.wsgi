from argus import app as application
#import site
#site.addsitedir('/var/local/virtualenvs/python2.X/site-packages')

import os
# activate virtualenv
activate_this = os.path.expanduser("/opt/ve/ve_name/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))
