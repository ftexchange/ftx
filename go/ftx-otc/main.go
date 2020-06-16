package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	client := FtxClient{Client: &http.Client{}, Api: "", Secret: []byte("")}
	resp, _ := client.getQuote("BTC", "USDT", "buy", 0.001, true)
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
}
