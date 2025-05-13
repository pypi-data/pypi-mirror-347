import os
import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        # First run the normal install
        install.run(self)
        
        # Then install the wheel file
        wheel_path = os.path.join('vendor', 'inprw', 'inpRW-2023.10.6-py3-none-any', 'inpRW-2023.10.6-py3-none-any.whl')
        if os.path.exists(wheel_path):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', wheel_path])

setup(
    cmdclass={
        'install': CustomInstall,
    }
) 