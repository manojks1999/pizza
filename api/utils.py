from celery import Celery

def make_celery(app):
    celery = Celery('tasks',
        backend='redis://default:52ca23275f6a488b8d655368b358f612@hot-walrus-34045.upstash.io:34045',
        broker='redis://default:52ca23275f6a488b8d655368b358f612@hot-walrus-34045.upstash.io:34045'
    )
    print(app.config)
    # celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery