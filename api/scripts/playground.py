from contextlib import ExitStack

from django.contrib.auth.models import Group
from django.db import connection, reset_queries

from api.metrics import query_count, query_count_tracker, timer

Group.objects.all().delete()

with ExitStack() as stack:
    # stack.enter_context(query_count_tracker())
    stack.enter_context(query_count(should_log_queries=True))
    stack.enter_context(timer())

    Group.objects.update_or_create(name="My Group")


def run():
    print("Done.")
