package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	client := FtxClient{Client: &http.Client{}, Api: "API KEY", Secret: []byte("SECRET")}
	resp, _ := client.getMarkets()
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
}
