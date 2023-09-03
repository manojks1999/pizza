# environment
import os
# from dotenv import load_dotenv

# import application factory
from api import create_app

# load environment variables
# load_dotenv()
# get environment
environment = os.environ.get("ENVIRONMENT")
# check environment
if environment is None:
    # use development (default)
    environment = "development"
# create app with environment
app, celery = create_app(environment=environment)
app.app_context().push()
print(app)
# security headers
@app.after_request
def after_request_in(response):
    response.headers["strict-transport-security"] = "max-age=15552000"
    response.headers["Content-Security-Policy"] = 'frame-src "none"'
    response.headers["x-frame-options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Server"] = "pivony"
    return response


# run application
if __name__ == "__main__":
    app.run(host='0.0.0.0')



# from typing import List, Dict
# from flask import Flask
# import mysql.connector
# import json

# app = Flask(__name__)


# def favorite_colors() -> List[Dict]:
#     config = {
#         'user': 'root',
#         'password': 'root',
#         'host': 'db',
#         'port': '3306',
#         'database': 'local_db'
#     }
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM items')
#     # results = [{name: color} for (name, color) in cursor]
#     print("reeeee". connection)
#     cursor.close()
#     connection.close()

#     return "results"


# @app.route('/')
# def index() -> str:
#     return json.dumps({'favorite_colors': favorite_colors()})


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')