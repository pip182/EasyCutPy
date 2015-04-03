from distutils.core import setup
import py2exe
#sys.argv.append('py2exe')
file = "easycut.pyw"


setup(
    options = {'py2exe': {'bundle_files': 1,
                          "includes":["sip"],
                          "optimize": 2}},
    windows = [{'script': file}],
    zipfile = None,
    )