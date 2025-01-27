from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .token import *
 
def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(sehedule_api, 'cron', day='1', hour='0', minute='6')
    scheduler.add_job(updateJobs, 'interval',seconds=3600)
    scheduler.add_job(updateItemsalepriceJobs, 'interval',seconds=80000)
    # scheduler.add_job(sehedule_api, 'interval',seconds=5)
    scheduler.start()
 
    # # Manually trigger the job
    # sehedule_api()
 
# Call the start function to begin scheduling the job
start()
 