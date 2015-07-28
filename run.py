import gevent
from gevent.pywsgi import WSGIServer
import zmq.green as zmq
from geventwebsocket.handler import WebSocketHandler

from itertools import cycle
import json

from pricing_app import app
from pricing_app.model.index import EquityIndex

WAIT = 60


def zmq_qry_pub(context):
    """PUB -- queries and PUBLISHES the data
    """
    app.logger.info("zmq_qry_pub started")
    socket = context.socket(zmq.PUB)
    socket.connect('tcp://127.0.0.1:7000')

    timestamps = ['0810', '0811', '0812']
    idx = EquityIndex('CAC')

    # for ts in cycle(timestamps):
    for ts in timestamps:
        price_data = idx.components_last_px(ts)

        for topic, msg_data in price_data.iteritems():
            if msg_data:
                # push the code/ticker into the dict
                msg_data['ticker'] = topic
                # reformat with a colon
                msg_data['ts'] = ts[:2] + ':' + ts[2:]
                # and jsonify....
                msg = json.dumps(msg_data)
                socket.send(msg)

        gevent.sleep(WAIT)

    app.logger.info("zmq_qry_pub closed")


def zmq_sub(context):
    """SUBscribe to PUBlished message then PUBlish to inproc://queue
    """
    app.logger.info("zmq_sub started")
    sock_incoming = context.socket(zmq.SUB)
    sock_outgoing = context.socket(zmq.PUB)

    sock_incoming.bind('tcp://*:7000')
    sock_outgoing.bind('inproc://queue')
    sock_incoming.setsockopt(zmq.SUBSCRIBE, "")

    while True:
        msg = sock_incoming.recv()
        sock_outgoing.send(msg)


class WebSocketApp(object):
    """Funnel messages coming from an inproc zmq socket to the websocket"""

    def __init__(self, context):
        app.logger.info("WebSocketApp initialised")
        self.context = context

    def __call__(self, environ, start_response):
        app.logger.info("WebSocketApp __call__")
        ws = environ['wsgi.websocket']
        sock = self.context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect('inproc://queue')
        while True:
            msg = sock.recv()
            ws.send(msg)


def main():

    app.logger.info("setting context")
    context = zmq.Context()

    gevent.spawn(zmq_qry_pub, context)

    # websocket server: copies inproc zmq messages to websocket
    ws_server = WSGIServer(
        ('', 9999),
        WebSocketApp(context),
        handler_class=WebSocketHandler
    )

    http_server = WSGIServer(('', 8080), app)

    http_server.start()
    ws_server.start()

    zmq_sub(context)


if __name__ == '__main__':
    main()
