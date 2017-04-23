# Transactions
Server app for interactiong with a MongoDB transactions database.

Written for Hootsuite Backend Internship Challenge 2017

### About the app

Transactions is a server app written in Python 2, using Flask and MongoEngine.
To run the app, just type:
```sh
$ chmod +x run.sh
$ ./run.sh
```

To run functionality or performance tests:
```sh
$ chmod +x run_tests.sh
$ ./run_tests.sh
```

### About the API usage
The server can answer three types of requests:
* "POST to ​ http://127.0.0.1:5000/transactions​/ with a JSON payload of the
form: {“sender”:sender_id(integer), “receiver”: receiver_id(integer),
“timestamp”: ts(integer), “sum”:x(integer)}. This adds a new transaction into
the database." All integers must be positive.
* GET to ​ http://127.0.0.1:5000/transactions/?user=XXXX&day=YYYY&threshold=ZZZZ
- user value must be a user id (positive integer), threshold must be a positive
integer and day must be a date of the form "DD-MM-YYYY"
* GET to ​ http://127.0.0.1:5000/balance/?user=XXXX&since=YYYY&until=ZZZZ​ -
user value must be a user id (positive integer), since and until must be dates
of the form "DD-MM-YYYY"


### Application structure

The app is divided into three main functionalities:
 * the server - main module; uses Flask to handle connections
 * the validator - called by the server; checks if received requests are valid
 (i. a. received strings represent numbers, dates, etc)
 * the database manager - called by the server; uses MongoEngine to interact
 with the database. It implements the main functionalities of the API: posting
 new transactions, querying for transactions during given days or querying for
 a user's balance over a given time periods.

Since the database objects have a fixed schema, I chose to use MongoEngine's
Documents for increased code readability and stability.

