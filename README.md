[![Build Status](https://travis-ci.org/RobertSudwarts/bts_tech_task.svg?branch=master)](https://travis-ci.org/RobertSudwarts/bts_tech_task)

# technical assignment

## precis

This web application has been built using [Flask](http://flask.pocoo.org/) wrapped with wsgi WebSocket middleware using the ØMQ library.

Rather than using 'long-polling' to refresh the client, the table/grid displaying the prices uses a WebSocket (using the ws: URI scheme) to connect to a **PUB**lish/**SUB**scribe process running in the background.

A single PUB/SUB instance has been created (for the CAC index) but the benefit of the model I have used is its scalability. Further instances (eg one per index) can be easily added, each one subscribing to a different dataset and pushing its data on a discrete port.

## model / backend

The backend consists of four classes: `EquityIndex` (which inherits from `Index`) and `Equity` (which inherits from `Asset`). The rationale for this is that the task specifies use of .csv files, with a database used in the 'real world'.  The Equity/Asset classes are unused but demonstrate the association of an index to its components...

The structure is effectively a one-to-one mapping to 'would-be' SQLAlchemy classes -- indeed the implicit relationships that could be made using SQLAlchemy would make the model simpler.

When parsing price data from the (text) trades files, use is made of `Decimal().quantize()` to remove downstream floating-point issues (and a four-decimal place) display in the final price grid.

## PUB/SUB

As mentioned above, the WebSocket data transfer has been implemented as WSGI middleware. There are three 'moving parts' to the process which can be seen in run.py:

* zmq_qry_pub()
    - creates an instance of EquityIndex
    - starts a loop
    - queries index data per timestamp
    - publishes the data (port 7000)
    - sleeps for 60 seconds
* zmq_sub()
    - starts a continuous loop
    - subscribes via tcp (port 7000)
    - publishes via inproc://queue
* WebSocketApp(object)
    - starts a continuous loop
    - subscribes for messages from an inproc://queue
    - sends via wsgi.websocket

**Note:** `zmq_qry_pub()` uses a `for...` loop over the given timestamps ['0810', '0811', '0812']. In production this would be changed to `while True:`

The javascript function (see templates/index.html) sets up a WebSocket connection, waits for data (the `ws.onmessage` event) and updates the table accordingly; highlights changed rows and updates the 'last updated' text. Other WebSocket events are used in this function to track the status of the connection and change the text in the connection_status element (ie the orange label on the page)

The ØMQ library is highly configurable and is a proven solution for scaling extremely well to serve multiple clients/browsers.  To use this library to best effect in production would require some benchmarking/tests but the implementation could be adjusted very easily to provide a robust solution depending on the pattern of client usage and hardware/network availabilty.  In production, clearly, the ports/communications layer would be set up using discrete processes (ie daemons)

## javascript libraries

The following javascript libraries are used by the application:

* jquery
* bootstrap (v3)
* DataTables
* datatables-plugins (for bootstrap3 compatible styles)
* jquery-color-animation (used for animating the table rows)
* metisMenu (a jquery menu plugin)

I have used the [bower](http://bower.io/) package manager which takes care of dependency tracking between javascript libraries.  A bower.json file is included in the repository and although the 'full-stack' can be reinstalled/recreated using this file, its use requires system-wide installation of `Node` and `npm`.

I have included the stripped down packages directly in this repository so **no further download or installation is required for the js libraries.**

## user interface

The front end has been implemented with bootstrap using [Jinja2 templates](http://jinja.pocoo.org/docs/dev/). According to their documentation (and with suitable caveats), Jinja2 is "between 10 and 20 times faster than Django’s template engine".

By using the combination of [metisMenu](http://mm.onokumus.com/), [Flask-Menu](http://flask-menu.readthedocs.org/en/latest/) and Jinja2 I have created a skeleton menu system with five dummy links in the navigation bar at the top of the screen.  The Flask plugin (and suitable templates) makes it trivial to integrate additional areas of the web application: essentially, any new controller method can be decorated with `@menu.register()` (a user/permissions structure could also be integrated) and a link will be automatically added to the page. (see mod_stubs/controllers.py and templates/top_nav.html)

**Note:** these links are for illustration purposes only and clicking on them will cause a 404 error. But you're welcome to copy/paste one of these controller methods (in mod_stubs/controllers.py) restart the server, and the links will (should!) appear in the navigation bar.

The final page-layout demonstrates how the price table/widget can be placed in a grid layout with surrounding dummy content for some context.  The clear advantage of using bootstrap is that the grid system makes it trivial to arrange a dynamic layout suitable for large screens as well as tablets and phones -- although some further tweaking would be required for optimal layout, a cursory check shows that this works more or less as intended.

I have used a bootstrap theme (courtesy of [bootswatch](https://bootswatch.com/)) with some minimal modifications -- although the interface I've presented is (admittedly) rather anodyne, the library (via LESS) makes it possible to fine-tune colours/gradients and content to give a unified feel to an entire site.

*Incidentally, I was going to incorporate your logo in my application but, for reasons of copyright infringement etc, I restrained myself(!)*

## installation

```bash
$ git clone https://github.com/RobertSudwarts/bts_tech_task
$ cd bts_tech_task
$ pip install -r requirements.txt
```

**Note:** The only complication I am aware of might be the pyzmq package. In preference to virtualenv, I use the [Anaconda](https://store.continuum.io/cshop/anaconda/) package management environment which comes with a prebuilt zeromq package but when attempting to install pyzmq (in a fresh standard virtual environment) via pip I found that I had to install the ØMQ library system-wide eg

```bash
$ [sudo] apt-get install libzmq1 libzmq-dev
$ (venv) pip install pyzmq
```

**If you have any problems whatsoever with installation, please let me know!!**

## running

Once the packages are installed the application can be run from the commandline by executing:

```bash
$ python run.py
```

And then navigating to localhost:8080

## tests

The entire flask codebase (models and controllers) has 100% test coverage using test classes provided by the Flask-Testing plugin

The zmq pub/sub (ie the wsgi wrapper) requires tests...

In addition, this github repository is covered by Travis CI

## further work & improvements

1. a single class incorporating the WebSocketApp and the zmq pub/sub functions would allow for communication between them -- particularly as (with the given setup, there are only three datafiles) the socket should be closed when there's no more data.
2. it'd be nice to add a look back at the previous price -- this could be done either in python or by the client in javascript to provide a signal for price change; an up/down arrow, highlighted in green/red etc.
3. the template is hardcoded to point at a single WebSocket only.  Ideally, there would be additional tabs/buttons to refresh the datatable for additional indexes which would then switch to collect data from a different WebSocket/port
