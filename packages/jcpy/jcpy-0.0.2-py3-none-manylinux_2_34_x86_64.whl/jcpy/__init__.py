import sys
import logging
import traceback


LOG_LEVEL_TO_LOGENTRY_MAP = {
    logging.FATAL: "CRITICAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARN",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "UNSPECIFIED",
    -float("inf"): "DEBUG",
}


def _map_log_level(level: int) -> str:
    try:
        return LOG_LEVEL_TO_LOGENTRY_MAP[level]
    except KeyError:
        return max(
            beam_level
            for python_level, beam_level in LOG_LEVEL_TO_LOGENTRY_MAP.items()
            if python_level <= level
        )


class PythonLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self._logger_writer = None

    def emit(self, record: logging.LogRecord):
        if self._logger_writer is None:
            PythonLogWriter = _jcpy.findClass("jcpy.engine.PythonLogWriter")
            self._logger_writer = PythonLogWriter()
        message = self.format(record)
        name = "%s:%s" % (
            record.pathname or record.module,
            record.lineno or record.funcName,
        )
        trace = None
        if record.exc_info:
            trace = "".join(traceback.format_exception(*record.exc_info))
        severity = _map_log_level(record.levelno)
        self._logger_writer.log(name, severity, message, trace)


class StdPrint:
    """
    Redirects Python's sys.stdout to Java's System.out
    """

    def write(self, msg, *args, **kwargs):
        _jcpy.jpcy_print(msg)

    def flush(self):
        pass


sys.stdout = StdPrint()
sys.stderr = StdPrint()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
python_log_handler = PythonLogHandler()
logger.addHandler(python_log_handler)
