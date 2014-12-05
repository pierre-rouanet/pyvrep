#!/usr/bin/env python

from setuptools import setup


setup(name='pyvrep',
      version='0.1',
      packages=['pyvrep', ],

      author='Pierre Rouanet',
      author_email='pierre.rouanet@gmail.com',
      description='Makes it simple to spawn v-rep simulated experiment',
      url='https://github.com/pierre-rouanet/pyvrep',
      license='GNU GENERAL PUBLIC LICENSE Version 3',
      )


print '*** Make sure you setup the VREP_PATH variable in your environment! ***'
