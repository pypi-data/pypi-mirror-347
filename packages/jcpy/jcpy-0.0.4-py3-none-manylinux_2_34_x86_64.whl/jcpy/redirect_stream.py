import sys
import logging
import redirection


class StdOutCatcher(object):
    """
    Redirects Python's sys.stdout to Java's System.out
    """

    def write(self, stuff, *args, **kwargs):
        redirection.stdout_redirect(stuff)

    def flush(self):
        pass


class StdErrCatcher(object):
    """
    Redirects Python's sys.stderr to Java's System.err
    """

    def write(self, stuff, *args, **kwargs):
        redirection.stderr_redirect(stuff)

    def flush(self):
        pass


sys.stdout = StdOutCatcher()
sys.stderr = StdErrCatcher()
logging.getLogger().info = sys.stdout.write
logging.getLogger().error = sys.stderr.write
