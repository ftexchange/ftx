import time
import datetime

from rest.client import FtxClient
from reporting.constants import ONE_HOUR, MILLISECONDS_IN_DAY
from reporting.send_mail import send_email, send_funding_email
from reporting.data import view_api_key, view_api_secret, futures_markets, markets


class SendReportFTX:

    def __init__(self):
        self.api_key = view_api_key
        self.api_secret = view_api_secret
        self.client = FtxClient(view_api_key, view_api_secret)

    def get_spot_balance(self):
        balances = self.client.get_balances()
        usd_free_balance, total_balance = 0, 0
        spot_coins = []

        for balance in balances:
            if balance['coin'] == 'USD':
                usd_free_balance = int(balance['free'])
                total_balance += int(balance['free'])
            if balance['coin'] in markets:
                spot_coins.append([balance['coin'], int(balance['total']), int(balance['usdValue'])])
                total_balance += int(balance['usdValue'])
        return usd_free_balance, spot_coins, total_balance

    def get_futures_position(self):
        futures_position = []
        for market in futures_markets:
            try:
                future = self.client.get_position(market)
                coin = future['future']
                size = int(future['size'])
                side = future['side']
                liquidation_price = round(float(future['estimatedLiquidationPrice']), 2)
                futures_position.append([coin, size, side, liquidation_price])
            except:
                pass
        return futures_position

    @staticmethod
    def get_timestamp(days):
        return days * MILLISECONDS_IN_DAY / 1000

    def get_funding_payments(self, end_time, start_time):
        total_payments = 0
        detailed_data = []
        for market in futures_markets:
            paid_futures_payments = self.client.get_funding_payments(start_time=start_time + 1,
                                                                     end_time=end_time, future=market)
            market_payments = []
            total_market_paid = 0

            for funding_payment in paid_futures_payments:
                tm = str(int(funding_payment['time'].split(':')[0].split('T')[1])) + ':00'
                if tm == '0:00':
                    tm = '24:00'
                if len(tm) < 5:
                    tm = '0' + tm
                fr = round(float(funding_payment['rate']) * 100, 3)
                p = -round(funding_payment['payment'], 2)
                total_payments += p
                total_market_paid += p
                market_payments.append([tm, fr, p])

            detailed_data.append([market, total_market_paid, market_payments])

        return total_payments, detailed_data

    @staticmethod
    def text_spot_coins(datas):
        text = ''
        for data in datas:
            text += data[0] + ': ' + str(data[1]) + ' | ' + 'USD Value: ' + str(data[2]) + '\n'
        return text

    @staticmethod
    def text_futures_position(datas):
        text = ''
        for data in datas:
            text += data[0] + ': ' + str(data[1]) + ' ' + data[2] + ' | ' + 'Liquidation price: ' + str(data[3]) + '\n'
        return text

    @staticmethod
    def text_funding_payments(datas):
        text = ''
        for data in datas:
            text += data[0] + ' result ' + str(data[1]) + '\n' + '----------' + '\n'
            for hour in data[2]:
                text += str(hour) + '\n'
        return text

    def prepare_daily_report_data(self):
        full_days_now = round(time.time() * 1000) // MILLISECONDS_IN_DAY
        #  to check more days increase delta (1 delta = 1 day)
        delta = 1
        end_time = self.get_timestamp(full_days_now)
        start_time = self.get_timestamp(full_days_now - delta)

        spot_usd, spot_coins, spot_total = self.get_spot_balance()
        futures = self.get_futures_position()
        total_payments, funding = self.get_funding_payments(end_time, start_time)
        date = datetime.date.fromtimestamp(end_time) - datetime.timedelta(days=1)

        return spot_usd, spot_coins, spot_total, futures, total_payments, funding, date

    def prepare_daily_report_message(self):
        spot_usd, spot_coins, spot_total, futures, total_payments, funding, date = self.prepare_daily_report_data()
        spot_text = self.text_spot_coins(spot_coins)
        futures_text = self.text_futures_position(futures)
        funding_test = self.text_funding_payments(funding)

        subject = f'Daily report {date}'
        text = f"""----------
Yesterday result: {total_payments}
----------
Spot:
USD: {spot_usd}
{spot_text}Total: {spot_total}
----------
Futures:
{futures_text}----------
Funding payments:
{funding_test}----------
            """
        message = 'Subject: {}\n\n{}'.format(subject, text)

        return message

    def analyze_funding_data(self):
        # get current funding rates
        current_time = datetime.datetime.now().timestamp()
        raw_funding_rates = self.client.get_funding_rates(current_time - ONE_HOUR, current_time)
        funding_rates = []
        for data in raw_funding_rates:
            if data['future'] in futures_markets:
               # if data['rate'] <= 0:
                    market = data['future']
                    fr = float(data['rate']) * 100
                    funding_rates.append([market, fr])

        return funding_rates

    def send_negative_futures_rate_check(self):
        data = self.analyze_funding_data()
        if len(data) > 0:
            send_funding_email(data)

    def send_daily_statement(self):
        message = self.prepare_daily_report_message()
        send_email(message)
