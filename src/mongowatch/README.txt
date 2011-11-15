===========
Mongo Watch
===========

MongoWatch provides an easy way to overview mongo database accesses::

First let's access the database and ensure a collection is created

 >>> import pymongo
 >>> conn = pymongo.Connection('localhost', 27017, tz_aware=False)
 >>> db = conn['mongowatch_test']

We'll start with collections related to street life, traffic and crowds

 >>> traffic = db.cars
 >>> crowd = db.people

We'll create a vehicle to represent something pre-existing in the 
collection

 >>> obj = traffic.insert({'car': 'red'})

Now create a watcher to watch for fresh profile entries created
by any future actions on the selected database

 >>> from mongowatch.mongo import watcher
 >>> wa = watcher.Watcher(conn,[DBNAME])

Now, let's add one item to traffic:

 >>> obj = traffic.insert({'truck':'blue'})

And we'll add two people to the crowd:

 >>> obj = crowd.insert({'name':'billy'})
 >>> obj = crowd.insert({'name':'jane'})

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
   {u'millis': 0, u'ts': datetime.datetime(2011, 11, 15, 11, 48, 36, 626000), u'ns': u'mongowatch_test.cars', u'op': u'insert'}
   {u'millis': 0, u'ts': datetime.datetime(2011, 11, 15, 11, 48, 36, 627000), u'ns': u'mongowatch_test.people', u'op': u'insert'}
   {u'millis': 0, u'ts': datetime.datetime(2011, 11, 15, 11, 48, 36, 627000), u'ns': u'mongowatch_test.people', u'op': u'insert'}

 >>> conn.disconnect()

