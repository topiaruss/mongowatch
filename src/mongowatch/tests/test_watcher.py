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
from mongowatch import testing
from mongowatch.mongo import watcher

def doctest_MongoWatch_simple():
    r"""MongoWatch: simple

    MongoWatch provides an easy way to overview mongo database accesses::

    First access the database and ensure a collection is created

     >>> db = conn[DBNAME]

     >>> traffic = db.cars
     >>> traffic.insert({'car': 'red'})
     ObjectId('...')

     >>> crowd = db.people

    Now create a watcher to watch for fresh profile entries to the
    selected database

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
     total ops:
       inserts: 3
     summary:
       database: mongowatch_test
          cars
            inserts: 1
          people
            inserts: 2
     details:
       ns mongowatch_test.cars
       op insert
       ts 2011-12-13 08:30:54.850000
       millis ...
     <BLANKLINE>
       ns mongowatch_test.people
       op insert
       ts 2011-12-13 08:30:54.851000
       millis ...
     <BLANKLINE>
       ns mongowatch_test.people
       op insert
       ts 2011-12-13 08:30:54.851000
       millis ...
     <BLANKLINE>

    """

def doctest_MongoWatch_multiple_databases():
    r"""MongoWatch: multiple databases

     >>> db = conn['streetlife']
     >>> traffic = db.cars
     >>> ob = traffic.insert({'car': 'red'})
     >>> crowd = db.people

     >>> db = conn['culture']
     >>> artists = db.artists

     >>> wa = watcher.Watcher(conn,['streetlife', 'culture'])

     >>> ob = traffic.insert({'truck':'blue'})
     >>> ob = artists.insert({'impressionist':'Monet'})

    Which resulted in the following actions being recorded in the watcher

     >>> wa.dump()
     total ops:
       inserts: 2
     summary:
       database: streetlife
          cars
            inserts: 1
       database: culture
          artists
            inserts: 1
     details:
       ns streetlife.cars
       op insert
       ts 2011-12-13 08:32:23.360000
       millis ...
     <BLANKLINE>
       ns culture.artists
       op insert
       ts 2011-12-13 08:32:23.361000
       millis ...
     <BLANKLINE>

    """

def doctest_MongoWatch_reset():
    r"""MongoWatch: reset

     >>> db = conn['streetlife']
     >>> traffic = db.cars
     >>> ob = traffic.insert({'car': 'red'})
     
     >>> wa = watcher.Watcher(conn,['streetlife', 'culture'])

     >>> ob = traffic.insert({'truck':'blue'})

    Which resulted in the following actions being recorded in the watcher

     >>> wa.dump()
     total ops:
       inserts: 1
     summary:
       database: streetlife
          cars
            inserts: 1
       database: culture
     details:
       ns streetlife.cars
       op insert
       ts 2011-12-13 07:47:51.921000
       millis ...
     <BLANKLINE>

     >>> wa.reset()
     >>> ob = traffic.insert({'truck':'green'})
     >>> ob = traffic.insert({'truck':'white'})
     >>> wa.dump()
     total ops:
       inserts: 2
     summary:
       database: streetlife
          cars
            inserts: 2
       database: culture
     details:
       ns streetlife.cars
       op insert
       ts 2011-12-13 07:47:51.921000
       millis ...
     <BLANKLINE>
       ns streetlife.cars
       op insert
       ts 2011-12-13 07:47:51.921000
       millis ...
     <BLANKLINE>

    """


def test_suite():
    return doctest.DocTestSuite(
        setUp=testing.setUp, tearDown=testing.tearDown,
        checker=testing.checker,
        optionflags=testing.OPTIONFLAGS)
