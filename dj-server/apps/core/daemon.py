import sys
import os
import time
import atexit
from signal import SIGTERM

from .log import logger


class Daemon(object):
    """
    This class was took from http://www.demoriz.ru/post-7/
    """

    def __init__(
            self,
            pidfile,
            root_dir=None,
            stdin='/dev/null',
            stdout='/dev/null',
            stderr='/dev/null',
    ):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.root_dir = root_dir

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            msg = "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror)
            logger.exception(msg)
            sys.exit(1)

        if self.root_dir:
            os.chdir(self.root_dir)
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            msg = "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror)
            logger.exception(msg)
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            msg = "pidfile %s already exist. Daemon already running?\n"
            msg = msg % self.pidfile
            sys.stderr.write(msg)
            sys.exit(1)

        self.daemonize()
        self.run()

    def status(self):
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon running\n"
            sys.stdout.write(message % self.pidfile)
            sys.exit(1)
        else:
            message = "pidfile %s does not exist. Daemon not running\n"
            sys.stdout.write(message % self.pidfile)
            sys.exit(1)

    def stop(self):
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        pass
