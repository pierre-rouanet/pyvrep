#!/usr/bin/env python

from setuptools import setup


def setup_vrep_folder():
    with open('pyvrep/_env.py', 'w') as f:
        vrep_folder = raw_input('V-Rep Folder? --> ')
        f.write('VREP_PATH = "{}"\n'.format(vrep_folder))

setup_vrep_folder()

setup(name='pypot',
      version='0.1',
      packages=['pyvrep', ],

      author='Pierre Rouanet',
      author_email='pierre.rouanet@gmail.com',
      description='Makes it simple to spawn v-rep simulated experiment',
      url='https://github.com/pierre-rouanet/pyvrep',
      license='GNU GENERAL PUBLIC LICENSE Version 3',
      )
