from celery import shared_task
from celery.contrib.abortable import AbortableTask
from api import db_session
from .schema import Orders
from datetime import datetime

@shared_task(bind=True, base=AbortableTask)
def asyncUpdate(self, data):
    print("Data", data)
    id = data["id"]
    status = data["status"]
    # a_user = session.query(User).filter(User.id == 3).one()
    current_data = db_session.query(Orders).filter(Orders.id == id).one()
    current_data.status = status
    current_data.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    db_session.commit()
    return 'DONE!'