package ftx

import (
	"net/http"
	"net/url"
)

type FtxClient struct {
	Client     *http.Client
	Api        string
	Secret     []byte
	Subaccount string
}

func New(api string, secret string, subaccount string) *FtxClient {
	return &FtxClient{Client: &http.Client{}, Api: api, Secret: []byte(secret), Subaccount: url.PathEscape(subaccount)}
}
