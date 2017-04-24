# Transactions
Server app for interacting with a MongoDB transactions database.
Written for Hootsuite Backend Internship Challenge 2017


## About the app

Transactions is a server app written in Python 2, using Flask and MongoEngine.
To run the app, just type:
```sh
$ ./run.sh
```
To run functionality or performance tests:
```sh
$ ./run_tests.sh
```


## About the API usage

The server can answer three types of requests:
* POST to ​ http://127.0.0.1:5000/transactions​/ with a JSON payload adds a new
transaction into the database. All fields must be positive integers. The
"timestamp" field is considered a Unix timestamp.
* GET to ​ http://127.0.0.1:5000/transactions/ - user value must be a user id
(positive integer), threshold must be a positive integer and day must be a date
of the form "DD-MM-YYYY"
* GET to ​ http://127.0.0.1:5000/balance/​ - user value must be a user id
(positive integer), since and until must be dates of the form "DD-MM-YYYY"


## Application structure

The app is divided into three main functionalities:
 * serving requests - main module; uses Flask to handle connections
 * validating input - used by the server; checks if received requests are valid
 (i. a. received strings represent numbers, dates, etc)
 * managing the database - used by the server; uses MongoEngine to interact
 with the database. The manager implements the main functionalities of the API:
 posting new transactions, querying for transactions during given days or
 querying for a user's balance over a given time periods.

Since the database objects have a fixed schema, I chose to use MongoEngine's
Documents for increased code readability and stability.


## Database structure

Each transaction is represented by two entries in the database, of the form
(sender, receiver, amount, timestamp). Each transaction means:
* one entry for (+ amount) of money sent from sender to receiver and
* one entry for (- amount) of money sent from receiver to sender.

Even though memory-wise it's inefficient, this design favors faster querying
and may be easily used to later add sharding (for example, shard by
geographical zones).

Also, this design makes adding indexes very easy.

I considered that given the scenario (a prosecutor searching transaction logs),
GET functions should be the most efficient ones.

The 'receiver' field could have been omitted from the entry, but I chose to
keep it since future extensions to the API might need it.


## Database querying

Particularities:
* for adding multiple entries into the database with only one request, I used
bulk inserting
* for computing a user's balance, I used aggregation (the sum function) - in
order to perform the calculus on the database side and only load useful
information locally
* by using indexes, both GET queries are significantly improved.

I chose to use a (sender, timestamp) index. Considering each day has
60 * 60 * 24 seconds, filtering by user first is the most efficient method
(since the database has more distinct timestamps than users). This index suits
this database structure, since most filterings are by sender and timestamp.

After running performance tests, this design appeared to be the most efficient.
Test results for different database structures and used indexes may be found in
results.txt.


## Testing API

Unit tests for functionality and performance tests are available by running
run_tests.sh. This will run the tests in the same container as the server and
display the results.
