from setuptools import setup
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        # Your post-install logic here
        print(f"Running post-install script")
        subprocess.call(['python', 'post_install_script.py'])

setup(
    name='py_setup_tool',
    version='0.0.2',
    packages=['py_setup_tool'],
    install_requires=[],
    cmdclass={
        'install': PostInstallCommand,
    },
)
