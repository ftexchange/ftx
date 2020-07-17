const axios = require('axios')
const hmacSHA256 = require('crypto-js/hmac-sha256')
const sha256 = require('crypto-js/sha256')
const Hex = require('crypto-js/enc-hex')

class FtxClient {
  constructor(apiKey, apiSecretKey, subaccount) {
    this.instance = axios.create({
      baseURL: 'https://ftx.com/api/',
      timeout: 5000,
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json; utf-8',
        'FTX-KEY': apiKey,
        'FTX-SUBACCOUNT': subaccount
      }
    });

    // make signature
    this.instance.interceptors.request.use(config => {
      const now = Date.now()
      const method = config.method.toUpperCase()
      const { data, params } = config
      let sign = now + method

      config.headers['FTX-TS'] = now

      switch (method) {
        case 'GET':
        case 'DELETE':
          sign += `/api/${config.url}?${new URLSearchParams(params).toString()}`
          break;
        case 'POST':
        case 'PUT':
        case 'PATCH':
          sign += `/api/${config.url}${JSON.stringify(data)}`
      }
      config.headers['FTX-SIGN'] = hmacSHA256(sign, apiSecretKey).toString(Hex)

      return config
    }, err => Promise.reject(err))
  }

  _get(endpoint, params = {}) {
    return this.instance
      .get(endpoint, { params })
      .then(res => console.log(res.data))
      .catch(e => console.log(e.toJSON()))
  }

  _delete(endpoint, params = {}) {
    return this.instance
      .delete(endpoint, { params })
      .then(res => console.log(res.data))
      .catch(e => console.log(e.toJSON()))
  }

  _post(endpoint, data = {}) {
    return this.instance
      .post(endpoint, data)
      .then(res => console.log(res.data))
      .catch(e => console.log(e.toJSON()))
  }

  listFutures() {
    return this._get('futures')
  }

  listMarkets() {
    return this._get('markets')
  }

  getOrderbook(market, depth = null) {
    return this._get(`markets/${market}/orderbook`, { depth })
  }

  getTrades(market) {
    return this._get(`markets/${market}/trades`)
  }

  getAccountInfo() {
    return this._get('account')
  }

  getOrderOrders(market) {
    return this._get('orders', { market })
  }

  getOrderHistory(market, side, orderType, start_time, end_time) {
    return this._get('orders/history', { market, side, orderType, start_time, end_time })
  }

  getConditionalOrderHistory(market, side, type, orderType, start_time, end_time) {
    return this._get('conditional_orders/history', { market, side, type, orderType, start_time, end_time })
  }

  modifyOrder(orderId, price, size, clientId) {
    return this._post(`orders/${orderId}/modify`, { size, price, clientId })
  }

  modifyOrderByClientId(clientOrderId, price, size, clientId) {
    return this._post(`orders/by_client_id/${clientOrderId}/modify`, { size, price, clientId })
  }

  getConditionalOrders(market) {
    return this._get('conditional_orders', { market })
  }

  placeOrder(market, side, price, size, type = 'limit', reduceOnly = false, ioc = false, postOnly = false, clientId = null) {
    return this._post('orders', { market, side, price, size, type, reduceOnly, ioc, postOnly, clientId })
  }

  placeConditionalOrder(
    market,
    side,
    size,
    type = 'stop',
    orderPrice = null,
    reduceOnly = false,
    cancelLimitOnTrigger = true,
    triggerPrice = null,
    trailValue = null
  ) {
    return this._post('conditional_orders', {
      market,
      side,
      size,
      type,
      orderPrice,
      reduceOnly,
      cancelLimitOnTrigger,
      triggerPrice,
      trailValue
    })
  }

  cancelOrder(orderId) {
    return this._delete(`orders/${orderId}`)
  }

  cancelOrders(market, conditionalOrdersOnly = false, limitOrders = false) {
    return this._delete('orders', { market, conditionalOrdersOnly, limitOrdersOnly })
  }

  getFills() {
    return this._get('fills')
  }

  getBalances() {
    return this._get('wallet/balances')
  }

  getDepositAddress(ticker) {
    return this._get(`wallet/deposit_address/${ticker}`)
  }

  getPositions(showAvgPrice = false) {
    return this._get('positions', { showAvgPrice })
  }
}

const ftxClient = new FtxClient(
  'apiKey',
  'apiSecretKey',
  'subaccount'
)

// test code
// const market = 'BTC-0327'
// const now = new Date().getTime() / 1000;
// const price = 100;
// const size = 0.1;
// const side = 'buy';
// const orderType = 'limit'
// const type = 'stop'
//
// ftxClient.listFutures()
// ftxClient.getOrderbook(market)
// ftxClient.placeOrder(market, side, price, size)
// ftxClient.getPositions()

