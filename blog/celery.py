from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery("tasks")
app.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/0",
    timezone="UTC",
)

app.conf.imports = ["posts.tasks"]

app.conf.beat_schedule = {
    "update": {
        "task": "dirty_check",
        "schedule": 15.0, 
    }
}