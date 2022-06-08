import cProfile
import logging
from contextlib import ContextDecorator
from pstats import SortKey, Stats

logger = logging.getLogger(__name__)


class profile(ContextDecorator):  # noqa
    def __init__(self, name: str | None = None, write_to_file=False):
        self.name = name
        self.write_to_file = write_to_file
        self.profile = cProfile.Profile()

    def __call__(self, func):
        # use decorated function's name if no name is provided
        if not self.name:
            self.name = func.__name__

        return super().__call__(func)

    def __enter__(self):
        if self.name:
            logger.info(f"Profiling {self.name}")
        self.profile.enable()
        return self

    def __exit__(self, *exc):
        self.profile.disable()

        stats = Stats(self.profile)
        stats.sort_stats(SortKey.CUMULATIVE).print_stats(60)

        if self.write_to_file:
            filename = f"{self.name}.prof"
            self.profile.dump_stats(filename)
            logger.info(f"Profile stats written to {filename}")

        return False
