import logging
import signal
import sys
import time

import flask
import pyjokes

app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route("/")
def home():
    return flask.render_template("home.html", joke=pyjokes.get_joke(category="chuck"))


def teardown(*args):
    """
    This is called before the application is closed.
    """
    if len(args) > 0:
        app.logger.info("received termination signal %s", args[0])

    app.logger.info("terminating the application")

    # in a production application, perform shutdown operations, such as
    # waiting to finish any request/transactions in the queue
    time.sleep(2)

    app.logger.info("bye!")

    # quit with exit code 0, which means success
    sys.exit(0)


# handle termination when running inside uwsgi
try:
    import uwsgi
    uwsgi.atexit = teardown
except Exception as exc:
    app.logger.info("uwsgi atexit handler not registered %s", exc)
    pass

if __name__ == "__main__":

    # handle OS termination signals when running in standalone mode
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, teardown)

    app.run(host="0.0.0.0", port=8000, threaded=True)
