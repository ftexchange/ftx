package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"strconv"
	"time"
)

var URL = "https://otc.ftx.com/api/"

func (client *FtxClient) signRequest(method string, path string, body []byte) *http.Request {
	ts := strconv.FormatInt(time.Now().UTC().Unix()*1000, 10)
	signaturePayload := ts + method + "/" + path + string(body)
	signature := client.sign(signaturePayload)
	req, _ := http.NewRequest(method, URL+path, bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("FTX-APIKEY", client.Api)
	req.Header.Set("FTX-SIGNATURE", signature)
	req.Header.Set("FTX-TIMESTAMP", ts)
	return req
}

func (client *FtxClient) _get(path string, body []byte) (*http.Response, error) {
	preparedRequest := client.signRequest("GET", path, body)
	resp, err := client.Client.Do(preparedRequest)
	return resp, err
}

func (client *FtxClient) _post(path string, body []byte) (*http.Response, error) {
	preparedRequest := client.signRequest("POST", path, body)
	resp, err := client.Client.Do(preparedRequest)
	return resp, err
}

func (client *FtxClient) _delete(path string, body []byte) (*http.Response, error) {
	preparedRequest := client.signRequest("DELETE", path, body)
	resp, err := client.Client.Do(preparedRequest)
	return resp, err
}

func (client *FtxClient) getQuote(baseCurrency string, quoteCurrency string, side string, baseCurrencySize float64, waitForPrice bool) (*http.Response, error) {
	newQuote := Quote{BaseCurrency: baseCurrency, QuoteCurrency: quoteCurrency, Side: side, BaseCurrencySize: baseCurrencySize, WaitForPrice: waitForPrice}
	body, _ := json.Marshal(newQuote)
	resp, err := client._post("otc/quotes", body)
	return resp, err
}

func (client *FtxClient) getPairs() (*http.Response, error) {
	resp, err := client._get("otc/quotes", []byte(""))
	return resp, err
}
