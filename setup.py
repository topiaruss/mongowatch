"""Setup
"""
import os
from setuptools import setup, find_packages

setup (
    name='mongowatch',
    version='0.1.1dev',
    author = "Russ Ferriday",
    author_email = "russf@topia.com",
    description = "MongoDB traffic pattern watcher",
    license = "ZPL 2.1",
    keywords = "mongo testing",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Framework :: ZODB',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent'],
    packages = find_packages('src'),
    package_dir = {'':'src'},
    extras_require = dict(
        test = (
            'zope.app.testing',
            'zope.testing',
            ),
        mongo = (
            ),
        ),
    install_requires = [
        'pymongo',
        'setuptools',
    ],
    include_package_data = True,
    zip_safe = False,
    )
