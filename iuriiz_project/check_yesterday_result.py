import time
import constants

from rest.client import FtxClient
from data import view_api_key, view_api_secret, futures_markets, markets

MILLISECONDS_IN_DAY = constants.MILLISECONDS_IN_DAY
ts = round(time.time() * 1000)
full_days = ts // MILLISECONDS_IN_DAY
#  to check more days increase delta (1 delta = 1 day)
delta = 1
timestamp_today = float(full_days * MILLISECONDS_IN_DAY / 1000)
timestamp_yesterday = float(timestamp_today - MILLISECONDS_IN_DAY / 1000 * delta) + 1


class CheckYesterdayResult:

    def __init__(self, api_key, api_secret, mar, f_mar):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = FtxClient(self.api_key, self.api_secret)
        self.markets = mar
        self.futures_market = f_mar
        self.balances = self.client.get_balances()
        self.future_position = []

    def spot_balance(self):
        usd_free_balance, total_balance = 0, 0
        spot_coins = []

        for balance in self.balances:
            if balance['coin'] == 'USD':
                usd_free_balance = balance['free']
                total_balance += int(balance['free'])
            if balance['coin'] in self.markets:
                spot_coins.append([balance['coin'], int(balance['total']), int(balance['usdValue'])])
                total_balance += int(balance['usdValue'])
        return usd_free_balance, spot_coins, total_balance

    def futures_position(self):
        futures = self.client.get_position(self.futures_market)
        self.future_position = int(futures['size'])
        self.delta = self.spot_coins - self.future_position

    def check_funding_payments(self):
        total_payments = 0
        paid_futures_payments = self.client.get_funding_payments(start_time=timestamp_yesterday,
                                                                 end_time=timestamp_today, future=self.futures_market)
        raw_data = []

        for funding_payment in paid_futures_payments:
            tm = str(int(funding_payment['time'].split(':')[0].split('T')[1])) + ':00'
            if tm == '0:00':
                tm = '24:00'
            if len(tm) < 5:
                tm = '0' + tm
            fr = round(float(funding_payment['rate']) * 100, 3)
            p = -round(funding_payment['payment'], 2)
            total_payments += p
            raw_data.append([tm, fr, p])

        return total_payments, raw_data

    def print_funding_result(self, total, raw):
        if self.delta > 10:
            print('ATTENTION. SOMETHING IS WRONG WITH POSITION!!!')
        else:
            print('Position is well hedged')
        print('-' * 10)
        print('Yesterday result: ', total)
        print('-' * 10)
        for d in raw:
            print(d)

    def check_results(self):
        result, data = self.check_funding_payments()
        self.spot_balance()
        self.futures_position()
        self.print_funding_result(result, data)

    @staticmethod
    def print_spot_coins(datas):
        text = ''
        for data in datas:
            text += data[0] + str(data[1]) + 'USD Value' + str(data[2]) + '/n'
        return text

    def prepare_message(self):
        usd, spot_coins, total = self.spot_balance()
        coins = self.print_spot_coins(spot_coins)
        subject = 'ADD'
        text = f"""----------
        Position well hedged
        ----------
        Spot:
        USD: {usd}
        {coins}
        Total: {total}
        ----------
        Futures:
        Size:
        Liquidation price:
        ----------
        
        """
        message = 'Subject: {}\n\n{}'.format(subject, text)

        return text


# a = CheckYesterdayResult(view_api_key, view_api_secret, markets, futures_markets)
# # a.check_results()
#
# a.prepare_message()

client = FtxClient(view_api_key, view_api_secret)
balances = client.get_balances()

