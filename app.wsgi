python_home = 'opt/streamflow/.venv/'
import sys
import site
sys.path.insert(0, /opt/streamflows/')
#from RiverFlows import app as application
python_vertsion = '.'.join(map(str, sys.version.info[:2'))
site_packages = python_home + '/lib/python%s/site-packages' % python_version

site.addsitedir(site_packages)

#from RiverFlows import app as application
#python_home = /opt/streamflows/.venv/bin

#activate_this = python_home + 'activate'
#execfile(activate_this, dict(__file__=activate_this
