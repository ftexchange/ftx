import time
import urllib.parse
from typing import Optional, Dict, Any, List

from requests import Request, Session, Response
import hmac


class FtxClient:
    _ENDPOINT = 'https://ftx.com/api/'

    def __init__(self, api_key=None, api_secret=None, subaccount_name=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request: Request) -> None:
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        if self._subaccount_name:
            request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(self._subaccount_name)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']

    def list_futures(self) -> List[dict]:
        return self._get('futures')

    def list_markets(self) -> List[dict]:
        return self._get('markets')

    def get_orderbook(self, market: str, depth: int = None) -> dict:
        return self._get(f'markets/{market}/orderbook', {'depth': depth})

    def get_trades(self, market: str) -> dict:
        return self._get(f'markets/{market}/trades')

    def get_account_info(self) -> dict:
        return self._get(f'account')

    def get_open_orders(self, market: str = None) -> List[dict]:
        return self._get(f'orders', {'market': market})
    
    def get_order_history(self, market: str = None, side: str = None, order_type: str = None, start_time: float = None, end_time: float = None) -> List[dict]:
        return self._get(f'orders/history', {'market': market, 'side': side, 'orderType': order_type, 'start_time': start_time, 'end_time': end_time})
        
    def get_conditional_order_history(self, market: str = None, side: str = None, type: str = None, order_type: str = None, start_time: float = None, end_time: float = None) -> List[dict]:
        return self._get(f'conditional_orders/history', {'market': market, 'side': side, 'type': type, 'orderType': order_type, 'start_time': start_time, 'end_time': end_time})

    def modify_order(
        self, existing_order_id: Optional[str] = None,
        existing_client_order_id: Optional[str] = None, price: Optional[float] = None,
        size: Optional[float] = None, client_order_id: Optional[str] = None,
    ) -> dict:
        assert (existing_order_id is None) ^ (existing_client_order_id is None), \
            'Must supply exactly one ID for the order to modify'
        assert (price is not None) or (size is not None), 'Must modify price or size of order'
        path = f'orders/{existing_order_id}/modify' if existing_order_id is not None else \
            f'orders/by_client_id/{existing_client_order_id}/modify'
        return self._post(path, {
            **({'size': size} if size is not None else {}),
            **({'price': price} if price is not None else {}),
            ** ({'clientId': client_order_id} if client_order_id is not None else {}),
        })

    def get_conditional_orders(self, market: str = None) -> List[dict]:
        return self._get(f'conditional_orders', {'market': market})

    def place_order(self, market: str, side: str, price: float, size: float, type: str = 'limit',
                    reduce_only: bool = False, ioc: bool = False, post_only: bool = False,
                    client_id: str = None) -> dict:
        return self._post('orders', {'market': market,
                                     'side': side,
                                     'price': price,
                                     'size': size,
                                     'type': type,
                                     'reduceOnly': reduce_only,
                                     'ioc': ioc,
                                     'postOnly': post_only,
                                     'clientId': client_id,
                                     })

    def place_conditional_order(
        self, market: str, side: str, size: float, type: str = 'stop',
        limit_price: float = None, reduce_only: bool = False, cancel: bool = True,
        trigger_price: float = None, trail_value: float = None
    ) -> dict:
        """
        To send a Stop Market order, set type='stop' and supply a trigger_price
        To send a Stop Limit order, also supply a limit_price
        To send a Take Profit Market order, set type='trailing_stop' and supply a trigger_price
        To send a Trailing Stop order, set type='trailing_stop' and supply a trail_value
        """
        assert type in ('stop', 'take_profit', 'trailing_stop')
        assert type not in ('stop', 'take_profit') or trigger_price is not None, \
            'Need trigger prices for stop losses and take profits'
        assert type not in ('trailing_stop') or (trigger_price is None and trail_value is not None), \
            'Trailing stops need a trail value and cannot take a trigger price'

        return self._post('conditional_orders',
                          {'market': market, 'side': side, 'triggerPrice': trigger_price,
                           'size': size, 'reduceOnly': reduce_only, 'type': 'stop',
                           'cancelLimitOnTrigger': cancel, 'orderPrice': limit_price})

    def cancel_order(self, order_id: str) -> dict:
        return self._delete(f'orders/{order_id}')

    def cancel_orders(self, market_name: str = None, conditional_orders: bool = False,
                      limit_orders: bool = False) -> dict:
        return self._delete(f'orders', {'market': market_name,
                                        'conditionalOrdersOnly': conditional_orders,
                                        'limitOrdersOnly': limit_orders,
                                        })

    def get_fills(self) -> List[dict]:
        return self._get(f'fills')

    def get_balances(self) -> List[dict]:
        return self._get('wallet/balances')

    def get_deposit_address(self, ticker: str) -> dict:
        return self._get(f'wallet/deposit_address/{ticker}')

    def get_positions(self, show_avg_price: bool = False) -> List[dict]:
        return self._get('positions', {'showAvgPrice': show_avg_price})

    def get_position(self, name: str, show_avg_price: bool = False) -> dict:
        return next(filter(lambda x: x['future'] == name, self.get_positions(show_avg_price)), None)
   
    def get_subaccounts(self)->dict:
        return self._get(f'subaccounts/')

    def create_subaccount(self, nickname:str)-> dict:
        return self._post(f'subaccounts/', {'nickname':nickname})

    def change_subaccount(self, nickname:str, newNickname:str)->dict:
        return self._post(f'subaccounts/update_name', {'nickname':nickname, 'newNickname':newNickname})

    def delete_subaccount(self, nickname:str)->dict:
        return self._delete(f'subaccounts/', {'nickname':nickname})

    def get_subaccount_balances(self, nickname:str)->dict:
        return self._get(f'subaccounts/{nickname}/balances')

    def transfer_subaccounts(self, coin:str, size:float, source:str, destination:str)->dict:
        """
        use None or 'main' for the main account
        """
        self._post(f'subaccounts/transfer', {'coin':coin, 'size':size, 'source':source, 'destination':destination})

    def get_historical_prices(self, market_name: str, resolution:float, limit:float = None, start_time:float=None, end_time:float=None)-> List[dict]:
        return self._get(f'markets/{market_name}/candles?resolution={resolution}&limit={limit}&start_time={start_time}&end_time={end_time}')

    def get_future(self, future_name:str)->dict:
        return self._get(f'futures/{future_name}')

    def get_future_stats(self, future_name:str)->dict:
        return self._get(f'futures/{future_name}/stats')

    def get_funding_rate(self, future:str=None, end_time:float=None, start_time:float=None)->dict:
        return self._get(f'funding_rates', {'future':future, 'end_time':end_time, 'start_time':start_time})

    def get_market(self, market_name: str) -> dict:
        return next(filter(lambda x: x['name'] == market_name, self.list_markets()), None)

    def change_leverage(self, leverage: float)->dict:
        return self._post(f'account/leverage', {'leverage':leverage})

    def get_coins(self)-> dict:
        return self._get(f'wallet/coins')

    def get_balances_all_accounts(self)->dict:
        return self._get(f'wallet/all_balances')

    def get_deposit_history(self)-> dict:
        return self._get(f'wallet/deposits')

    def get_withdrawal_history(self)->dict:
        return self._get(f'wallet/withdrawals')

    def request_withdrawal(self,coin:str, size:float, address:str, tag:str=None, password:str=None, code:str=None)->dict:
        return self._post(f'wallet/withdrawals', {'coin':coin, 'size':size, 'address':address, 'tag':tag, 'password':password, 'code':code})

    def get_trigger_order_triggers(self, order_id:str)->dict:
        return self._get(f'conditional_orders/{order_id}/triggers')

    def modify_conditional_order(self, order_id:float, size:float, triggerPrice:float=None, trailValue:float=None)->dict:
        return self._post(f'conditional_orders/{order_id}/modify', {'size':size, 'triggerPrice':triggerPrice, 'traiValue':trailValue})

    def get_order_status(self, order_id:str)->dict:
        return self._get(f'orders/{order_id}')

    def get_order_status_by_client_id(self, client_order_id:str)-> dict:
        return self._get(f'orders/by_client_id/{client_order_id}')

    def cancel_order_by_client_id(self, client_order_ide:str)->dict:
        return self._delete(f'orders/by_client_id/{client_order_id}')

    def cancel_open_trigger_order(self, id:str)->dict:
        return self._delete(f'conditional_orders/{id}')

    def get_funding_payments(self, future:str=None, start_time:float=None, end_time:float=None)->dict:
        return self._get(f'funding_payments', {'future':future, 'end_time':end_time, 'start_time':start_time})

    def list_leveraged_tokens(self)->List[dict]:
        return self._get(f'lt/tokens')

    def get_token_info(self, token_name:str)->dict:
        return self._get(f'lt/{token_name}')

    def get_leveraged_token_balance(self)->List[dict]:
        return self._get(f'lt/balances')

    def list_leveraged_token_creation_requests(self)-> List[dict]:
        return self._get(f'lt/creations')

    def request_leveraged_tokens_creation(self, token_name:str, size:float)->dict:
        return self._post(f'lt/{token_name}/create', {'size':size})

    def list_leveraged_token_redemption_requests(self)->List[dict]:
        return self._get(f'lt/redemptions')

    def request_leveraged_token_redemption(self, token_name:str, size:float)->dict:
        return self._post(f'lt/{token_name}/redeem', {'size':size})

    def list_quote_requests(self)->List[dict]:
        return self._get(f'options/requests')

    def get_my_quote_requests(self)->List[dict]:
        return self._get(f'options/my_requests')

    def create_quote_request(self, type:str, strike:float, expiry:float, side:str, size:float, limitPrice:Optional[float]=None, hideLimitPrice:bool=False, requestExpiry:Optional[float]=None)->dict:
        return self._post(f'options/requests', {'underlying':'BTC', 'type':type, 'strike':strike, 'expiry':expiry, 'side':side, 'size':size, **({'limitPrice': limitPrice} if limitPrice is not None else {}), 'hideLimitPrice':hideLimitPrice, **({'requestExpiry': requestExpiry} if requestExpiry is not None else {})})

    def cancel_quote_request(self, request_id:str)->dict:
        return self._delete(f'options/requests/{request_id}')

    def get_quote_for_my_quote_request(self, request_id:str)->dict:
        return self._get(f'options/requests/{request_id}/quotes')

    def create_quote(self, request_id:str, price:float)-> dict:
        return self._post(f'options/requests/{request_id}/quotes', {'price':price})

    def get_my_quotes(self):
        return self._get(f'options/my_quotes')

    def cancel_quote(self, quote_id:str)->dict:
        return self._delete(f'options/quotes/{quote_id}')

    def accept_quote(self, quote_id:str)->dict:
        return self._post(f'options/quotes/{quote_id}/accept')

    def get_account_option_info(self)->dict:
        return self._get(f'options/account_info')

    def get_positions_options(self)->List[dict]:
        return self._get(f'options/positions')

    def get_public_options_trade(self, limit:float=None, start_time:float=None, end_time:float=None)->List[dict]:
        return self._get(f'options/trades', {'limit':limit, 'start_time':start_time, 'end_time':end_time})

    def get_options_fills(self, limit:float=None, start_time:float=None, end_time:float=None)->List[dict]:
        return self._get(f'options/fills', {'limit':limit, 'start_time':start_time, 'end_time':end_time})

    def get_expired_futures(self)->dict:
        return self._get(f'expired_futures')
