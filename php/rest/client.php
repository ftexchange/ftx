<?php
require_once "HTTP/Request2.php";

class FtxClient {
  function __construct($apiKey, $apiSecretKey, $subaccount) {
    $this->apiKey = $apiKey;
    $this->apiSecretKey = $apiSecretKey;
    $this->subaccount = $subaccount;
    $this->host = 'https://ftx.com';
  }

  private function signature($req, $method, $body = '') {
    $now = time() * 1000;
    $url = $req->getUrl();
    $parseUrl = parse_url($url);
    if ( $parseUrl['query']) {
      $sign = $now . $method . $parseUrl['path'] . '?' . $parseUrl['query'];
    } else {
      $sign = $now . $method . $parseUrl['path'];
    }

    if ($method === HTTP_Request2::METHOD_POST) {
      $sign .= $body;
    }

    return $req->setHeader(array(
      'FTX-SIGN' => hash_hmac('sha256', $sign, $this->apiSecretKey),
      'FTX-TS' => $now
    ))
      ->setBody($body);
  }

  private function makeRequest($endpoint, $method) {
    $req = new HTTP_Request2($this->host . '/api' . $endpoint, $method);

    return $req->setHeader(array(
      'accept' => 'application/json',
      'Content-Type' => 'application/json; utf-8',
      'FTX-KEY' => $this->apiKey,
      'FTX-SUBACCOUNT' => $this->subaccount
    ));
  }

  private function get($endpoint, $params = NULL) {
    $req = $this->makeRequest($endpoint, HTTP_Request2::METHOD_GET);
    if ($params != NULL) {
      $url = $req->getUrl();
      $url->setQueryVariables($params);
    }

    $req = $this->signature($req, HTTP_Request2::METHOD_GET);
    return $req->send()->getBody();
  }

  private function post($endpoint, $params = NULL) {
    $req = $this->makeRequest($endpoint, HTTP_Request2::METHOD_POST);
    if ($params == NULL) {
      $req = $this->signature($req, HTTP_Request2::METHOD_POST);
    } else {
      $body = json_encode($params);
      $req = $this->signature($req, HTTP_Request2::METHOD_POST, $body);
    }

    return $req->send()->getBody();
  }

  private function delete($endpoint, $params = NULL) {
    $req = $this->makeRequest($endpoint, HTTP_Request2::METHOD_DELETE);
    if ($params != NULL) {
      $url = $req->getUrl();
      $url->setQueryVariables($params);
    }

    $req = $this->signature($req, HTTP_Request2::METHOD_DELETE);
    return $req->send()->getBody();
  }

  public function listFutures() {
    return $this->get('/futures');
  }

  public function listMarkets() {
    return $this->get('/markets');
  }

  public function getOrderbook($market, $depth) {
    return $this->get('/markets/' . $market . '/orderbook', array('depth' => $depth));
  }

  public function getTrades($market) {
    return $this->get('/markets/' . $market . '/trades');
  }

  public function getAccountInfo() {
    return $this->get('/account');
  }

  public function getOpenOrders($market) {
    return $this->get('/orders', array('market' => $market));
  }

  public function getOrderHistory($market, $side, $orderType, $startTime, $endTime) {
    return $this->get('/orders/history', array(
      'market' => $market,
      'side' => $side,
      'orderType' => $orderType,
      'start_time' => $startTime,
      'end_time' => $endTime
    ));
  }

  public function getConditionalOrderHistory($market, $side, $orderType, $startTime, $endTime) {
    return $this->get('/conditional_orders/history', array(
      'market' => $market,
      'side' => $side,
      'orderType' => $orderType,
      'start_time' => $startTime,
      'end_time' => $endTime
    ));
  }

  public function modifyOrder($orderId, $price, $size) {
    return $this->post('/orders/' . $orderId . '/modify', array(
      'price' => $price,
      'size' => $size
    ));
  }

  public function modifyOrderByClientId($clientId, $price, $size) {
    return $this->post('/orders/by_client_id/' . $clientId .'/modify', array(
      'price' => $price,
      'size' => $size
    ));
  }

  public function getConditionalOrders($market) {
    return $this->get('/conditional_orders', array('market' => $market));
  }

  public function placeOrder (
    $market,
    $side,
    $price,
    $size,
    $type = 'limit',
    $reduceOnly = FALSE,
    $ioc = FALSE,
    $postOnly = FALSE,
    $clientId = NULL
  ) {
    return $this->post('/orders', array(
      'market' => $market,
      'side' => $side,
      'price' => $price,
      'size' => $size,
      'type' => $type,
      'reduceOnly' => $reduceOnly,
      'ioc' => $ioc,
      'postOnly' => $postOnly,
      'clientId' => $clientId
    ));
  }

  public function placeConditionalOrder(
    $market,
    $side,
    $size,
    $type = 'stop',
    $orderPrice = NULL,
    $reduceOnly = FALSE,
    $cancelLimitOnTrigger = FALSE,
    $triggerPrice = NULL,
    $trailValue = NULL
  ) {
    return $this->post('/condition_orders', array(
      'market' => $market,
      'side' => $side,
      'size' => $size,
      'type' => $type,
      'orderPrice' => $orderPrice,
      'reduceOnly' => $reduceOnly,
      'cancelLimitOnTrigger' => $cancelLimitOnTrigger,
      'triggerPrice' => $triggerPrice,
      'trailValue' => $trailValue
    ));
  }

  public function cancelOrder($orderId) {
    return $this->delete('/orders/' . $orderId);
  }

  public function cancelOrders($market, $conditionalOrdersOnly = FALSE, $limitOrdersOnly = FALSE) {
    return $this->delete('/orders', array(
      'market' => $market,
      'conditionalOrdersOnly' => $conditionalOrdersOnly,
      'limitOrdersOnly' => $limitOrdersOnly
    ));
  }

  public function getFills() {
    return $this->get('/fills');
  }

  public function getBalances() {
    return $this->get('/wallet/balances');
  }

  public function getDepositAddress($ticker) {
    return $this->get('/wallet/deposit_address/' . $ticker);
  }

  public function getPositions($showAvgPrice = FALSE) {
    return $this->get('/positions', array('showAvgPrice' => $showAvgPrice));
  }
}


$ftxClient = new FtxClient(
  'api_key',
  'api_secret_key',
  'account'
);

// * test vars
// $market = "BTC-0327";
// $now = time();
// $price = 100;
// $size = 0.1;
// $side = "buy";
// $orderType = "limit";
// $type = "stop";
//
// echo $ftxClient->listFutures();
// echo $ftxClient->listMarkets();
// echo $ftxClient->listMarkets($market, 1);
// echo $ftxClient->getTrades($market);
// echo $ftxClient->getAccountInfo($market);
// echo $ftxClient->getOpenOrders($market);
// echo $ftxClient->placeOrder($market, $side, $price, $size);
// echo $ftxClient->getPositions();
