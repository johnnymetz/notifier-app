import logging
import os
from contextlib import ContextDecorator
from dataclasses import dataclass, field

from django.db import connection

logger = logging.getLogger(__name__)


@dataclass(frozen=True, order=True)
class QueryBlock:
    name: str = field(compare=False)
    count: int
    queries: list[str] = field(compare=False, repr=False)


_query_blocks = []
MAX_LOGGED_QUERIES = 30


class query_count(ContextDecorator):  # noqa
    def __init__(
        self, name: str | None = None, *, should_log=True, should_log_queries=False
    ):
        self.name = name
        self.should_log = should_log
        self.should_log_queries = should_log_queries

    def __call__(self, func):
        # use decorated function's name if no name is provided
        if not self.name:
            self.name = func.__name__

        return super().__call__(func)

    def __enter__(self):
        self.before = len(connection.queries)
        return self

    def __exit__(self, *exc):
        after = len(connection.queries)
        net = after - self.before
        if net:
            queries = connection.queries[self.before : self.before + MAX_LOGGED_QUERIES]

            if self.should_log:
                logger.info(f"{self.name} made {net} queries")
                if os.environ.get("TRACK_QUERY_COUNTS"):
                    _query_blocks.append(
                        QueryBlock(name=self.name, count=net, queries=queries)
                    )

            if self.should_log_queries:
                for query in queries:
                    logger.info(f"\t{query}")

        return False


class query_count_tracker(ContextDecorator):  # noqa
    def __init__(self, name: str | None = None, log_limit: int = 30):
        self.name = name
        self.log_limit = log_limit

    def __call__(self, func):
        # use decorated function's name if no name is provided
        if not self.name:
            self.name = func.__name__

        return super().__call__(func)

    def __enter__(self):
        os.environ["TRACK_QUERY_COUNTS"] = "true"
        return self

    def __exit__(self, *exc):
        del os.environ["TRACK_QUERY_COUNTS"]

        logger.info("\nHighest query count blocks:")
        for x in sorted(_query_blocks, reverse=True)[: self.log_limit]:
            logger.info(x)

        total_query_count = sum(x.count for x in _query_blocks)
        logger.info(f"\nTotal counted queries: {total_query_count}")

        return False
