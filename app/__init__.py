import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from config import Config

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from pymodm import connect

app = Flask(__name__)
app.config.from_object(Config)
app.redis = Redis.from_url(app.config['REDIS_URL'])
queue = Queue('bank-service', connection=app.redis)
scheduler = Scheduler(queue=queue, connection=Redis(host='localhost', port=6379, db=0))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()


from app import routes, models
