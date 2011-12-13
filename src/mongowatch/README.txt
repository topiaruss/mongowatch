===========
Mongo Watch
===========

MongoWatch provides an easy way to measure mongo database access
counts, and timeing, between certain points in a program.

First let's access the database and get a db object

 >>> import pymongo
 >>> conn = pymongo.Connection('localhost', 27017, tz_aware=False)
 >>> db = conn[DBNAME]

Our example collections relate to street life, traffic, and crowds

 >>> traffic = db.cars
 >>> crowd = db.people

Let's create a vehicle to represent something already in a 
collection

 >>> obj = traffic.insert({'car': 'red'})

Now create a watcher track mongo profile entries created
by actions on the selected database

 >>> from mongowatch.mongo import watcher
 >>> wa = watcher.Watcher(conn,[DBNAME])

Now, let's add one item to traffic:

 >>> obj = traffic.insert({'truck':'blue'})

And we'll add two people to the crowd:

 >>> obj = crowd.insert({'name':'billy'})
 >>> obj = crowd.insert({'name':'jane'})

Which resulted in the following actions being recorded in the watcher.

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
   ts 2011-12-13 08:27:05.496000
   millis ...
 <BLANKLINE>
   ns mongowatch_test.people
   op insert
   ts 2011-12-13 08:27:05.498000
   millis ...
 <BLANKLINE>
   ns mongowatch_test.people
   op insert
   ts 2011-12-13 08:27:05.498000
   millis ...
 <BLANKLINE>

Let's reset the counters

 >>> wa.reset()

So now do some more work

 >>> crowd.remove({})
 >>> traffic.remove({})
 >>> obj = crowd.insert({'name':'bonzo'})

This time we stop the watcher explicity
 >>> wa.stop()
 >>> wa.dump()
 total ops:
   inserts: 1
   removes: 2
 summary:
   database: mongowatch_test
      cars
        removes: 1
      people
        inserts: 1
        removes: 1
 details:
   ns mongowatch_test.people
   op remove
   query {}
   ts 2011-12-13 07:47:51.921000
   millis 0
 <BLANKLINE>
   ns mongowatch_test.cars
   op remove
   query {}
   ts 2011-12-13 07:47:51.921000
   millis 0
 <BLANKLINE>
   ns mongowatch_test.people
   op insert
   ts 2011-12-13 07:47:51.921000
   millis 0
 <BLANKLINE>


 >>> conn.disconnect()

