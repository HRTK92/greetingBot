import time
from datetime import datetime

from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app import sendMessage

def a ():
    print('a')

# 7:00 == 22:00
sched = BackgroundScheduler(daemon=True)
sched.add_job(sendMessage,'cron', hour=22)
sched.start()

app = Flask(__name__)

@app.route("/")
def index():
    return {'status':'ok'}

if __name__ == "__main__":
    print(datetime.now())
    app.run(host='0.0.0.0')
