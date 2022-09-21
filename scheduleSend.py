import time
from datetime import datetime

import schedule
from pytz import timezone

from app import sendMessage

# 7:00 == 22:00
schedule.every().days.at("22:00").do(sendMessage)

print(datetime.now())

while True:
    schedule.run_pending()
    time.sleep(1)
