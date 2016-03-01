from functools import wraps
import os
import time

from django.conf import settings
from line_profiler import LineProfiler

from diya_dnipro.settings import rel_path


__all__ = [
    'profile', 'line_profile',
]

PROFILE_LOG_BASE = getattr(settings, 'PROFILE_LOG_BASE', rel_path('..', 'logs'))


def profile(log_file):
    """
    Profile some callable.

    This decorator uses the hotshot profiler to profile some callable (like a view function or method) and dumps the
    profile data somewhere sensible for later processing and examination.

    It takes one argument, the profile log name. If it's a relative path, it places it under the PROFILE_LOG_BASE. It
    also inserts a time stamp into the file name, such that 'my_view.prof' become 'my_view-20100211T170321.prof',
    where the time stamp is in UTC. This makes it easy to run and compare multiple trials.
    """

    if not os.path.isabs(log_file):
        log_file = os.path.join(PROFILE_LOG_BASE, log_file)

    def _outer(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            # Add a timestamp to the profile output when the callable is actually called.
            (base, ext) = os.path.splitext(log_file)
            base = base + '-' + time.strftime('%Y%m%dT%H%M%S', time.gmtime())
            final_log_file = base + ext
            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(f, *args, **kwargs)
            finally:
                prof.close()
            return ret

        return _inner

    return _outer


def line_profile(log_file=None, show=False):
    """
    Decorator to wrap function with line-by-line profiler http://pythonhosted.org/line_profiler/

    Profiler shows the execution time of each line of code. Can be useful in some cases when hotshot profiler shows
    most time spent in django internals.

    To view stored profile data use:
        bin/python -m line_profiler path_to_file

    :param str log_file: store data to file (timestamp will be added)
    :param bool show: print stats to stdout
    """
    if log_file is not None and not os.path.isabs(log_file):
        log_file = os.path.join(PROFILE_LOG_BASE, log_file)

    def decor(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            prof = LineProfiler()
            try:
                ret = prof(f)(*args, **kwargs)
            finally:
                if log_file is not None:
                    # Add a timestamp to the profile output when the callable is actually called.
                    (base, ext) = os.path.splitext(log_file)
                    base = base + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())
                    final_log_file = base + ext
                    prof.dump_stats(final_log_file)
                if show:
                    prof.print_stats()
            return ret

        return wrapped

    return decor


if __name__ == '__main__':
    import sys
    import hotshot.stats


    stats = hotshot.stats.load(sys.argv[1])
    stats.sort_stats('time', 'calls')
    stats.print_stats(20)
