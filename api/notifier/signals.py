from api.celery import app
from celery import states
from celery.signals import after_task_publish
from django_celery_results.backends import DatabaseBackend
from django_celery_results.models import TaskResult


# Signal to persist PENDING tasks to db.
# http://docs.celeryproject.org/en/latest/userguide/signals.html#basics
@after_task_publish.connect
def update_pending_state(sender=None, headers=None, body=None, **kwargs):
    info = headers if "task" in headers else body
    backend: DatabaseBackend = app.backend
    task_id = info["id"]
    backend._store_result(
        task_id=task_id, result=None, status=states.PENDING, request=info
    )
    # unable to set task_name using the _store_result method so setting it explicitly
    task_result = TaskResult.objects.get(task_id=task_id)
    task_result.task_name = sender
    task_result.save()
