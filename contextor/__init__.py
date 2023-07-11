from multiprocessing.pool import ThreadPool

from pyglet import app

from . import logging, processing
from . import tools, binds


def run():
    tools.event_mngr.install_daemon()

    pool = ThreadPool()
    try:
        binds.start()
        app.run()
    finally:
        pool.close()
        pool.join()
