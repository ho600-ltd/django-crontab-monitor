#!/usr/bin/env python
import re
from setuptools import setup, find_packages

from crontab_monitor.__version__ import VERSION

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    REQUIREMENTS = []

install_requires = [r for r in REQUIREMENTS.split('\n') if r and not re.match('^ *#.*', r)]

setup(
    name='django-crontab-monitor',
    description='''Store crontab-based functions in Django Model so that users can add/disable/delete crontab-based functions on API service rather than login the server to deal with system crontab configuration.''',
    version=VERSION,
    author='ho600 Ltd.',
    author_email='django-crontab-monitor@ho600.com',
    license='MIT',
    url='https://github.com/ho600-ltd/django-crontab-monitor',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests*', 'trunk*']),
    package_data={'crontab_monitor': ['locale/ja_JP/LC_MESSAGES/django*.*',
                                      'locale/zh_Hant/LC_MESSAGES/django*.*',
                                      'locale/zh_Hans/LC_MESSAGES/django*.*',
                                      'templates/crontab_monitor/*.html',
                                     ]},
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Installation/Setup'
    ]
)
