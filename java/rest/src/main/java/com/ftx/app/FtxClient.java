package com.ftx.app;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import org.json.JSONObject;

public class FtxClient {
  String host = "https://ftx.com";
  String apiKey = "";
  String apiSecretKey = "";
  String subaccount = "test";

  HttpClient client = HttpClient.newHttpClient();
  HttpRequest.Builder builder = HttpRequest.newBuilder().header("FTX-KEY", this.apiKey).header("FTX-SUBACCOUNT",
      this.subaccount);

  private HttpRequest makeRequest(String endpoint, String method, String body) {
    Long now = new Date().getTime();
    URI uri = URI.create(this.host + endpoint);
    String signature = now.toString() + method + endpoint;

    if (body != "") {
      signature += body;
    }

    try {
      Mac hasher = Mac.getInstance("HmacSHA256");
      SecretKeySpec secretKey = new SecretKeySpec(apiSecretKey.getBytes(), "HmacSHA256");
      hasher.init(secretKey);
      byte[] hash = hasher.doFinal(signature.getBytes());
      final StringBuilder sb = new StringBuilder();
      for (byte b : hash) {
        sb.append(String.format("%02x", b));
      }
      signature = sb.toString();
    } catch (Exception e) {
      e.printStackTrace();
    }

    HttpRequest.Builder builder = HttpRequest.newBuilder()
      .uri(uri)
      .header("accept", "application/json")
      .header("Content-Type", "application/json; utf-8")
      .header("FTX-KEY", this.apiKey)
      .header("FTX-SUBACCOUNT", this.subaccount)
      .header("FTX-TS", now.toString())
      .header("FTX-SIGN", signature);

    switch (method) {
      case "POST":
        builder.POST(BodyPublishers.ofString(body));
        break;
      case "PUT":
        builder.PUT(BodyPublishers.ofString(body));
        break;
      case "DELETE":
        builder.DELETE();
        break;
      default:
        builder.GET();
    }

    return builder.build();
  }

  private HttpResponse<String> get(String endpoint) throws IOException, InterruptedException {
    HttpRequest request = this.makeRequest(endpoint, "GET", "");
    return this.client.send(request, BodyHandlers.ofString());
  }

  private HttpResponse<String> get(String endpoint, Map<String, Object> params) throws IOException, InterruptedException {
    Boolean isFirstParam = true;
    String uri = endpoint;

    for (Map.Entry<String, Object> entry: params.entrySet()) {
      String key = entry.getKey();
      Object value = entry.getValue();
      if (isFirstParam) {
        isFirstParam = false;
        uri = uri + "?" + key + "=" + value.toString();
      } else {
        uri = uri + "&" + key + "=" + value.toString();
      }
    }

    return this.get(uri);
  }

  private HttpResponse<String> post(String endpoint, Map<String, Object>params) throws IOException, InterruptedException {
    JSONObject json = new JSONObject(params);
    HttpRequest request = this.makeRequest(endpoint, "POST", json.toString());
    return this.client.send(request, BodyHandlers.ofString());
  }

  private HttpResponse<String> delete(String endpoint) throws IOException, InterruptedException {
    HttpRequest request = this.makeRequest(endpoint, "DELETE", "");
    return this.client.send(request, BodyHandlers.ofString());
  }

  public HttpResponse<String> listFutures() throws IOException, InterruptedException {
    return this.get("/api/futures");
  }

  public HttpResponse<String> listMarkets () throws IOException, InterruptedException {
    return this.get("/api/markets");
  }

  public HttpResponse<String> getOrderBook (String market, Integer depth) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("depth", depth.toString());

    return this.get("/api/markets/" + market + "/orderbook", params);
  }

  public HttpResponse<String> getTrades (String market) throws IOException, InterruptedException {
    return this.get("/api/markets/" + market + "/trades");
  }

  public HttpResponse<String> getAccountInfo () throws IOException, InterruptedException {
    return this.get("/api/account");
  }

  public HttpResponse<String> getOpenOrders (String market) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("market", market);
    return this.get("/api/orders", params);
  }

  public HttpResponse<String> getOrderHistory (String market, String side, String orderType, long startTime, long endTime) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("market", market);
    params.put("side", side);
    params.put("orderType", orderType);
    params.put("start_time", Long.toString(startTime));
    params.put("end_time", Long.toString(endTime));
    return this.get("/api/orders/history", params);
  }

  public HttpResponse<String> getConditionalOrderHistory (
    String market,
    String side,
    String type,
    String orderType,
    long startTime,
    long endTime
  ) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("market", market);
    params.put("side", side);
    params.put("type", type);
    params.put("orderType", orderType);
    params.put("start_time", Long.toString(startTime));
    params.put("end_time", Long.toString(endTime));
    return this.get("/api/conditional_orders/history", params);
  }

  // by existing orderId
  public HttpResponse<String> modifyOrder (Double size, Double price, String clientId, String orderId) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("size", size);
    params.put("price", price);
    params.put("clientId", clientId);
    return this.post("/api/orders/" + orderId + "/modify", params);
  }

  // by clientId
  public HttpResponse<String> modifyOrder (Double size, Double price, String clientId) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("size", size);
    params.put("price", price);
    params.put("clientId", clientId);
    return this.post("/api/orders/by_client_id/" + clientId + "/modify", params);
  }

  public HttpResponse<String> getConditionalOrders(String market) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("market", market);
    return this.get("/api/conditional_orders", params);
  }

  public HttpResponse<String> placeOrder (
    String market,
    String side,
    Double price,
    Double size,
    String type,
    Boolean reduceOnly,
    Boolean ioc,
    Boolean postOnly,
    String clientId
  ) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("market", market);
    params.put("side", side);
    params.put("price", price);
    params.put("size", size);
    params.put("type", type);
    params.put("reduceOnly", reduceOnly);
    params.put("ioc", ioc);
    params.put("postOnly", postOnly);
    params.put("clientId", clientId);
    return this.post("/api/orders", params);
  }

  public HttpResponse<String> placeConditionalOrder (
    String market,
    String side,
    Double size,
    String type,
    Double orderPrice,
    Double triggerPrice,
    Double trailValue,
    Boolean reduceOnly,
    Boolean cancelLimitOnTrigger
  ) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("market", market);
    params.put("side", side);
    params.put("size", size);
    params.put("type", type);
    params.put("reduceOnly", reduceOnly);
    params.put("orderPrice", orderPrice);
    params.put("triggerPrice", triggerPrice);
    params.put("trilValue", trailValue);
    params.put("cancelLimitOnTrigger", cancelLimitOnTrigger);
    return this.post("/conditional_orders", params);
  }

  public HttpResponse<String> getFills() throws IOException, InterruptedException {
    return this.get("/api/fills");
  }

  public HttpResponse<String> getBalances() throws IOException, InterruptedException {
    return this.get("/api/wallet/balances");
  }

  public HttpResponse<String> getDepositAddress(String ticker) throws IOException, InterruptedException {
    return this.get("/api/wallet/deposit_address/" + ticker);
  }

  public HttpResponse<String> getPositions (Boolean showAvgPrice) throws IOException, InterruptedException {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("showAvgPrice", showAvgPrice);
    return this.get("/api/positions", params);
  }

  public HttpResponse<String> cancelOrder (String orderId) throws IOException, InterruptedException {
    return this.delete("/api/orders/" + orderId);
  }

  public static void main(String args[]) throws IOException, InterruptedException {
    // FtxClient client = new FtxClient();
    // String market = "BTC-0327";
    // Long now = new Date().getTime() / 1000;
    // Double price = 0.01;
    // Double size = 0.1;
    // String side = "buy";
    // String orderType = "limit";
    // String type = "stop";
    // HttpResponse<String> response = client.listFutures();
    // HttpResponse<String> response = client.getOrderBook(market, 20);
    // HttpResponse<String> response = client.getTrades(market);
    // HttpResponse<String> response = client.getAccountInfo();
    // HttpResponse<String> response = client.getOpenOrders(market);
    // HttpResponse<String> response = client.getOrderHistory(market, side, orderType, now - 1000, now);
    // HttpResponse<String> response = client.getConditionalOrderHistory(market, side, type, orderType, now - 1000, now);
    // HttpResponse<String> response = client.getConditionalOrders(market);
    // HttpResponse<String> response = client.placeOrder(market, side, price, size, type, false, false, false, "null");
    // HttpResponse<String> response = client.getFills();
    // HttpResponse<String> response = client.getBalances();

    // System.out.println("aaassddd: " + response.statusCode());
    // System.out.println(response.body());
  }
}
