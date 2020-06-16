package main

import (
	"net/http"
)

type FtxClient struct {
	Client *http.Client
	Api    string
	Secret []byte
}

type Order struct {
	Market     string  `json:"market"`
	Side       string  `json:"side"`
	Price      float64 `json:"price"`
	Type       string  `json:"type"`
	Size       float64 `json:"size"`
	ReduceOnly bool    `json:"reduceOnly",omitempty`
	Ioc        bool    `json:"ioc",omitempty`
	PostOnly   bool    `json:"postOnly",omitempty`
}

type Market struct {
	Name           string  `json:"name"`
	Type           string  `json:"type"`
	BaseCurrency   string  `json:"baseCurrency",omitempty`
	quoteCurrency  string  `json:"quoteCurrency",omitempty`
	Underlying     string  `json:"underlying"`
	Enable         bool    `json:"enable"`
	Ask            float64 `json:"ask"`
	Bid            float64 `json:"bid"`
	Last           float64 `json:"last"`
	PriceIncrement float64 `json:"priceIncrement"`
	sizeIncrement  float64 `json:"sizeIncrement"`
	Restricted     bool    `json:"restricted"`
}
