#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    packages = find_packages()
except ImportError:
    from distutils import setup
    packages = ['task_conversion']

from task_conversion import __version__ as version

reqs = [line.strip() for line in open('requirements.txt')]

setup(name='task-conversion',
      version=version,
      description='Converts a CSV of tasks into the taskwarrior JSON format',
      license='MIT',
      author_email='luke.s.campbell@gmail.com',
      packages=packages,
      setup_requires=reqs,
      entry_points={
          'console_scripts': [
              'task-conversion = task_conversion:main',
          ],
      })
