from distutils.core import setup
import py2exe

setup(options = {"py2exe":{   "excludes": ["_pytest","qtpy"] } },
      console = ['game.py'])

#run in cmd: python setup.py py2exe