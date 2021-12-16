#!/usr/bin/env python

import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response
from os.path import exists

from zap2it import createXML


app = Flask(__name__)


def refresh_xml():
    app.logger.info('refreshing xmltv')
    createXML("milwaukee.ini", '/guides/milwaukee.xmltv', 'en')
    time.sleep(30) # be nice
    createXML("madison.ini", '/guides/madison.xmltv', 'en')


if not exists('/guides/milwaukee.xmltv') and not exists('/guides/madison.xmltv'):
    x = threading.Thread(target=refresh_xml)
    x.start()


sched = BackgroundScheduler(daemon=True)
sched.add_job(refresh_xml, 'interval', minutes=60*24)
sched.start()


@app.route("/<path>")
def get_xml(path):
    app.logger.info('Requested %s', path)
    if not path.endswith('.xmltv'):
        app.logger.error('Unsupported Media Type %s', path)
        return 'Unsupported Media Type', 415
    try:
        with open('/guides/' + path, 'r') as f:
            return Response(f.read(), mimetype='text/xml')
    except Exception as e:
        app.logger.error('Path %s Error: %s', path, e)
        return "Internal Error", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
