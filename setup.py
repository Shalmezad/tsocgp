import sys
from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 6)

if CURRENT_PYTHON < MIN_PYTHON:
    sys.stderr.write("""
        ============================
        Unsupported Python Version
        ============================
        
        Python {} is unsupported. Please use a version newer than Python {}.
    """.format(CURRENT_PYTHON, MIN_PYTHON, ))
    sys.exit(1)

with open('VERSION') as f:
    VERSION = f.read().strip()

setup(name='tsocgp',
      version=VERSION,
      description='An attempt to use GP to solve "Train Schedule Optimisation Challenge"',
      author='Richard W',
      author_email='shalmezad+tsocgp@gmail.com',
      license='MIT',
      #packages=find_packages(), # I don't have any requirements for packages right now
      entry_points={},
      zip_safe=False)