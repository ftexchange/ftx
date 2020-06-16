package main

import (
	"net/http"
)

type FtxClient struct {
	Client *http.Client
	Api    string
	Secret []byte
}

type Quote struct {
	BaseCurrency     string  `json:"baseCurrency"`
	QuoteCurrency    string  `json:"quoteCurrency"`
	Side             string  `json:"side"`
	BaseCurrencySize float64 `json:"baseCurrencySize"`
	WaitForPrice     bool    `json:"waitForPrice"`
}
