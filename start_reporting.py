from apscheduler.schedulers.blocking import BlockingScheduler
from reporting.main import SendReportFTX


def start_scheduler():
    sender = SendReportFTX()
    scheduler = BlockingScheduler()
    scheduler.add_job(sender.send_negative_futures_rate_check, 'interval', minutes=10)
    scheduler.add_job(sender.send_daily_statement, 'interval', days=1)
    scheduler.start()


start_scheduler()
