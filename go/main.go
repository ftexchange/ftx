package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"time"
)

var URL = "https://ftx.com/api/"

func (client *FtxClient) prepareRequest(method string, path string, body []byte) *http.Request {
	ts := strconv.FormatInt(time.Now().UTC().Unix()*1000, 10)
	signaturePayload := ts + method + "/api/" + path + string(body)
	signature := client.signRequest(signaturePayload)
	req, _ := http.NewRequest(method, URL+path, bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("FTX-KEY", client.Api)
	req.Header.Set("FTX-SIGN", signature)
	req.Header.Set("FTX-TS", ts)
	return req
}

func (client *FtxClient) _get(path string, body []byte) (*http.Response, error) {
	preparedRequest := client.prepareRequest("GET", path, body)
	resp, err := client.Client.Do(preparedRequest)
	return resp, err
}

func (client *FtxClient) _post(path string, body []byte) (*http.Response, error) {
	preparedRequest := client.prepareRequest("POST", path, body)
	resp, err := client.Client.Do(preparedRequest)
	return resp, err
}

func (client *FtxClient) _delete(path string, body []byte) (*http.Response, error) {
	preparedRequest := client.prepareRequest("DELETE", path, body)
	resp, err := client.Client.Do(preparedRequest)
	return resp, err
}

func (client *FtxClient) getMarkets() (*http.Response, error) {
	return client._get("markets", []byte(""))
}

func (client *FtxClient) deleteOrder(orderId int64) (*http.Response, error) {
	path := "orders/" + strconv.FormatInt(orderId, 10)
	return client._delete(path, []byte(""))
}

func (client *FtxClient) deleteAllOrders() (*http.Response, error) {
	return client._delete("orders", []byte(""))
}

func (client *FtxClient) placeOrder(market string, side string, price float64, _type string, size float64) (*http.Response, error) {
	newOrder := Order{Market: market, Side: side, Price: price, Type: _type, Size: size}
	body, _ := json.Marshal(newOrder)
	resp, err := client._post("orders", body)
	return resp, err
}

func main() {
	client := FtxClient{Client: &http.Client{}, Api: "API", Secret: "SECRET"}
	resp, _ := client.getMarkets()
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
}
