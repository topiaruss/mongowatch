##############################################################################
#
# Copyright (c) 2011 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Mongo Watcher Tests"""
import doctest
import pprint
from pymongo import dbref, objectid

from mongowatch import testing
from mongowatch.mongo import watcher

def doctest_MongoWatch_simple():
    r"""MongoWatch: simple

    MongoWatch provides an easy way to overview mongo database traffic::

    First access the database and ensure a collection is created

     >>> db = conn[DBNAME]

     >>> traffic = db.cars
     >>> traffic.insert({'car': 'red'})
     ObjectId('...')

     >>> crowd = db.people

    Now create a watcher to watch for fresh traffic to the selected database

     >>> wa = watcher.Watcher(conn,[DBNAME])

    Add an item to traffic:

     >>> traffic.insert({'truck':'blue'})
     ObjectId('...')

    Add two people to the crowd:

     >>> crowd.insert({'name':'billy'})
     ObjectId('...')
     >>> crowd.insert({'name':'jane'})
     ObjectId('...')

    Which resulted in the following actions being recorded in the watcher

     >>> wa.dump()
     ops...
       inserts: 3
     summary...
       database... mongowatch_test
          cars
            inserts: 1
          people
            inserts: 2
     details...
       {u'millis': 0, u'ts': datetime.datetime(2011, 11, 15, 11, 48, 36, 626000), u'ns': u'mongowatch_test.cars', u'op': u'insert'}
       {u'millis': 0, u'ts': datetime.datetime(2011, 11, 15, 11, 48, 36, 627000), u'ns': u'mongowatch_test.people', u'op': u'insert'}
       {u'millis': 0, u'ts': datetime.datetime(2011, 11, 15, 11, 48, 36, 627000), u'ns': u'mongowatch_test.people', u'op': u'insert'}
    """


def test_suite():
    return doctest.DocTestSuite(
        setUp=testing.setUp, tearDown=testing.tearDown,
        checker=testing.checker,
        optionflags=testing.OPTIONFLAGS)
