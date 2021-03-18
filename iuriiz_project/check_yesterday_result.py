import time
import datetime
import iuriiz_project.constants as constants

from rest.client import FtxClient
from iuriiz_project.data import view_api_key, view_api_secret, futures_markets, markets

MILLISECONDS_IN_DAY = constants.MILLISECONDS_IN_DAY
ts = round(time.time() * 1000)
full_days = ts // MILLISECONDS_IN_DAY
#  to check more days increase delta (1 delta = 1 day)
delta = 1
timestamp_today = float(full_days * MILLISECONDS_IN_DAY / 1000)
timestamp_yesterday = float(timestamp_today - MILLISECONDS_IN_DAY / 1000 * delta) + 1


class CheckYesterdayResult:

    def __init__(self, client, api_key, api_secret, mar, f_mar):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = client
        self.markets = mar
        self.futures_markets = f_mar
        self.balances = self.client.get_balances()

    def spot_balance(self):
        usd_free_balance, total_balance = 0, 0
        spot_coins = []

        for balance in self.balances:
            if balance['coin'] == 'USD':
                usd_free_balance = int(balance['free'])
                total_balance += int(balance['free'])
            if balance['coin'] in self.markets:
                spot_coins.append([balance['coin'], int(balance['total']), int(balance['usdValue'])])
                total_balance += int(balance['usdValue'])
        return usd_free_balance, spot_coins, total_balance

    def futures_position(self):
        futures_position = []
        for market in self.futures_markets:
            try:
                futures = self.client.get_position(market)
                coin = futures['future']
                size = int(futures['size'])
                side = futures['side']
                liquidation_price = round(float(futures['estimatedLiquidationPrice']), 2)
                futures_position.append([coin, size, side, liquidation_price])
            except:
                pass
        return futures_position

    def check_funding_payments(self):
        total_payments = 0
        raw_data = []
        for market in self.futures_markets:
            paid_futures_payments = self.client.get_funding_payments(start_time=timestamp_yesterday,
                                                                     end_time=timestamp_today, future=market)
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

            raw_data.append([market, total_market_paid, market_payments])

        return total_payments, raw_data

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

    def prepare_message(self):
        usd, spot_coins, total = self.spot_balance()
        spot_text = self.text_spot_coins(spot_coins)
        futures = self.futures_position()
        futures_text = self.text_futures_position(futures)
        total_payments, funding = self.check_funding_payments()
        funding_test = self.text_funding_payments(funding)
        date = datetime.date.fromtimestamp(timestamp_today) - datetime.timedelta(days=1)

        subject = f'Daily report {date}'
        text = f"""----------
Yesterday result: {total_payments}
----------
Spot:
USD: {usd}
{spot_text}Total: {total}
----------
Futures:
{futures_text}----------
Funding payments:
{funding_test}----------
            """
        message = 'Subject: {}\n\n{}'.format(subject, text)

        return message
