from celery import shared_task
from django.core.cache import cache


# class BaseTask:
#     def __init__(self, uid):
#         self.uid = uid

#     def on_success(self, retval, task_id, args, kwargs):
#         print(f"Task {task_id} with args {args} succeeded with result: {retval}")
        
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print(f"Task {task_id} with args {args} failed with exception: {exc}")
        
#     def on_retry(self, exc, task_id, args, kwargs, einfo):
#         print(f"Task {task_id} with args {args} is being retried due to exception: {exc}")


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 2, 'countdown': 10})
def send_email(self, uid, content):
    cache.set(f"{self.request.id} {uid} emailed: {content}")
    return f"Email sent to {uid}"


