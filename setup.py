#!/usr/bin/env python

from setuptools import setup

setup(name='Bufftweet',
      version='1.0',
      description='Twitter Buffer App',
      author='Subhendu Ghosh',
      author_email='subho.prp@gmail.com',
      packages=['bufftweet'],
      license = "GPL2",
      scripts = ['runapp.py','createdb.py'],
      install_requires = ['psutil==3.1.1','python-daemon==2.0.5','SQLAlchemy==1.0.8','tweepy==3.3.0'],
     )