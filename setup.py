import os
import sys
from setuptools import setup, find_packages


version = '0.8.0'


with open('README.md', 'rt') as f:
    long_description = f.read()


with open('requirements.txt', 'rt') as f:
    requirements = tuple(f.read().split())


setup(
    name = 'django-cachekiller',
    version = version,
    url = 'https://github.com/meeb/django-cachekiller',
    author = 'https://github.com/meeb',
    author_email = 'meeb@meeb.org',
    description = ('Static file CDN cache buster for fast site updates.'),
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    license = 'MIT',
    include_package_data = True,
    install_requires = requirements,
    packages = find_packages(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords = ['django', 'cache', 'buster', 'cdn', 'cachebuster'],
)
