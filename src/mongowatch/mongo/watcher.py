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
            latest = self.conn[db].system.profile.find_one(\
                                 sort=[(u'ts', pymongo.DESCENDING)])
        self.start = latest and latest[u'ts'] or None
        self.running = True

    def stop(self):
        self.running = False

        for db in self.dbs:
            self.conn[db].set_profiling_level(pymongo.OFF)

        raw = {}
        for db in self.dbs:
            actions = [ a for a in self.conn[db].system.profile.find() if \
                          self.start is None or a[u'ts'] > self.start]

            def isProfile(a):
                return u'command' in a and a[u'command'] == {u'profile': 0}
            def isSystem(a):
                return a[u'ns'].endswith(u'system.profile')

            raw[db] = [a for a in actions if not \
                       isProfile(a) and not isSystem(a)]

        self.raw = raw
    
        stats = {}
        for db in self.dbs:
            actions = self.raw[db]
            stats[db] = {}
            for a in actions:
                stats[db][a['op']] = stats[db].setdefault(a['op'], 0) + 1
        self.summary = stats

    def print_ops(self):              
        print 'total ops:'
        ops = {}
        for db in self.dbs:
            for k,v in self.summary[db].items():
                ops[k] = ops.setdefault(k, 0) + v
        for k,v in ops.items():
            print '  %ss: %d' % (k,v)
    
    def print_summary(self):
        print 'summary:'
        for db in self.dbs:
            print '  database:', db
            collections = {}
            for a in self.raw[db]:
                collection = a[u'ns'].split('.')[1]
                collection = collections.setdefault(collection, {})
                op = a[u'op']
                collection[op] = collection.setdefault(op, 0) + 1
            for c, ops in collections.items():
                print '    ', c
                for k,v in ops.items():
                    print '       %ss: %d' % (k,v)

    def print_details(self):
        print 'details:'
        for db in self.dbs:
            for s in self.raw[db]:
                for k in (u'client', u'user'):
                    s.pop(k)
                print ' ', s
        
    def dump(self):
        if self.running:
            self.stop()
        self.print_ops()
        self.print_summary()
        self.print_details()
