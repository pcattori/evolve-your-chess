from sys import platform as _platform
from urllib.request import urlopen
import io
import os
import sys
import zipfile

from require import require
config = require('../config.py')

# Detecting 64-bit OS: http://stackoverflow.com/a/6107982/1490091
is_64bits = sys.maxsize > 2**32

zip_filename_template = 'chromedriver_{}.zip'
download_url = 'http://chromedriver.storage.googleapis.com/2.25/'

version = None
if _platform == 'linux' or _platform == 'linux2':
    # linux
    if is_64bits:
        version = 'linux64'
    else:
        version = 'linux32'
elif _platform == 'darwin' and is_64bits:
    # macos
    version = 'mac64'
elif _platform == 'win32':
    # windows
    version = 'win32'

zip_filename = zip_filename_template.format(version)

with urlopen(download_url + zip_filename) as response:
    data = zipfile.ZipFile(io.BytesIO(response.read())).read('chromedriver')

with open(os.path.join(config.BIN, 'chromedriver'), 'wb') as f:
    f.write(data)
    os.chmod(f.name, os.stat(f.name).st_mode | 0o111)
