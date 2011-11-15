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
"""Mongo Watch"""

import pymongo

class Watcher(object):

    def __init__(self, conn, dbs):
        self.conn = conn
        self.dbs = dbs
        self.reset()

    def reset(self):
        for db in self.dbs:
            self.conn[db].set_profiling_level(pymongo.ALL)
        self.start = self.conn[db].system.profile.find()
        self.running = True

    def stop(self):
        self.running = False

        for db in self.dbs:
            self.conn[db].set_profiling_level(pymongo.OFF)

        raw = {}
        for db in self.dbs:
            actions = self.conn[db].system.profile.find()
            raw[db] = list(actions)
        self.raw = raw
    
        stats = {}
        for db in self.dbs:
            actions = self.raw[db]
            stats[db] = {}
            for a in actions:
                stats[db][a['op']] = stats[db].setdefault(a['op'], 0) + 1
        self.summary = stats

    def print_ops(self):              
        print 'ops...'
        for db in self.dbs:
            for s in self.summary[db].items():
                print s
    
    def print_summary(self):
        print 'summary...'
        for db in self.dbs:
            print 'database...', db
            collections = {}
            for actions in self.raw[db]:
                for a in actions:
                    if u'command' in a and a[u'command'] == {u'profile': 0}:
                        continue    
                    collection = a[u'ns'].split('.')[1]
                    collection = collections.setdefault(collection, {})
                    op = a[u'op']
                    collection[op] = collection.setdefault(op, 0) + 1
            for c, ops in collections.items():
                print c
                print ops


    def print_details(self):
        print 'details...'
        for db in self.dbs:
            for s in self.raw[db]:
                if u'command' in s and s[u'command'] == {u'profile': 0}:
                    continue    
                print s
        
    def dump(self):
        if self.running:
            self.stop()
        self.ops()
        self.print_summary()
        self.print_details()


"""        [{u'millis': 0, 
            u'ts': datetime.datetime(2011, 11, 15, 9, 44, 6, 939000), 
            u'client': u'127.0.0.1', 
            u'user': u'', 
            u'ns': u'mongowatch_test.mycollection', 
            u'op': u'insert'}]

"""