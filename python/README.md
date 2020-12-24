# FTX-Trader

## Warning

This is an UNOFFICIAL wrapper for FTX exchange [HTTP API](https://docs.ftx.com/) written in Python 3.7

The library can be used to fetch market data, make trades, place orders or create third-party clients

USE THIS WRAPPER AT YOUR OWN RISK, I WILL NOT CORRESPOND TO ANY LOSES

## Features

- Except OTC and Option, implementation of all [public](#) and [private](#) endpoints
- Simple handling of [authentication](https://docs.ftx.com/#authentication) with API key and secret
- For asset safety, WITHDRAWAL function will never be supported !

## Donate

If useful, buy me a coffee?

- ETH: 0xA9D89A5CAf6480496ACC8F4096fE254F24329ef0

## Installation

    $ git clone https://github.com/LeeChunHao2000/ftx-api-wrapper-python3

 - This wrapper requires [requests](https://github.com/psf/requests)

## Requirement

1. [Register an account](https://ftx.com/#a=2500518) with FTX exchange _(referral link)_
2. [Generate API key and secret](https://ftx.com/profile), assign relevant permissions to it
3. Clone this repository, and put in the key and secret
4. Write your own trading policies 

## Quickstart

This is an introduction on how to get started with FTX client. First, make sure the FTX library is installed.

The next thing you need to do is import the library and get an instance of the client:

    from FTX.client import Client
    client = Client('PUY_MY_API_KEY_HERE', 'PUY_MY_API_SECRET_HERE')

### Get ordedrbook

    >>> from FTX.client import Client
    >>> client = Client('PUY_MY_API_KEY_HERE', 'PUY_MY_API_SECRET_HERE')
    >>> result = client.get_public_orderbook('BTC/USD', 1)
    >>> result
    {'asks': [[10854.5, 11.856]], 'bids': [[10854.0, 0.4315]]}
    >>> result['asks']
    [[10854.5, 11.856]]
    >>> result['bids']
    [[10854.0, 0.4315]]

### Positions (DataFrame)

    >>> import pandas as pd
    >>> result = pd.DataFrame(client.get_private_account_positions())
    >>> result = result.sort_values(by=['realizedPnl'], ascending=False)
    >>> result
            collateralUsed      cost  entryPrice  ...  side     size  unrealizedPnl
    0          0.00000     0.000         NaN  ...   buy     0.00            0.0
    49         0.00000     0.000         NaN  ...   buy     0.00            0.0
    4        535.09500  2972.750    594.5500  ...   buy     5.00            0.0
    35       206.93750  2069.375     82.7750  ...   buy    25.00            0.0
    3          0.00000     0.000         NaN  ...   buy     0.00            0.0
    5        152.28000  1522.800      2.5380  ...   buy   600.00            0.0
### Version Logs
#### 2020-12-24

**Bugfixes**
 - Fixed a bug with function of cancel orders

**Features**
 - Add Spot Margin Support
#### 2020-09-14

 - Birth!
