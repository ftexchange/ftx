import datetime
import constants
import send_mail

from rest.client import FtxClient
from data import view_api_key, view_api_secret, futures_markets
from apscheduler.schedulers.blocking import BlockingScheduler

ONE_HOUR = constants.ONE_HOUR
client = FtxClient(view_api_key, view_api_secret)
current_time = datetime.datetime.now().timestamp()


def analyze_funding_data():
    # get current funding rates
    raw_funding_rates = client.get_funding_rates(current_time - ONE_HOUR, current_time)
    funding_rates = []
    for data in raw_funding_rates:
        if data['future'] in futures_markets:
            if data['rate'] <= 0:
                market = data['future']
                fr = float(data['rate']) * 100
                funding_rates.append([market, fr])

    return funding_rates


def check_hourly_futures_rate():
    send_mail.send_funding_email(analyze_funding_data())


def send_daily_statement():
    pass


def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(check_hourly_futures_rate, 'interval', hours=1)
    scheduler.add_job(send_daily_statement, 'interval', days=1)
    scheduler.start()
