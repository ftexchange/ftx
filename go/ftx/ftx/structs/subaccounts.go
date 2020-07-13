package structs

import (
	"time"
)

type SubaccountsList struct {
	Success bool `json:"success"`
	Result  []struct {
		Nickname  string `json:"nickname"`
		Deletable bool   `json:"deletable"`
		Editable  bool   `json:"editable"`
	} `json:"result"`
}

type Subaccount struct {
	Success bool `json:"success"`
	Result  struct {
		Nickname  string `json:"nickname"`
		Deletable bool   `json:"deletable"`
		Editable  bool   `json:"editable"`
	} `json:"result"`
}

type SubaccountBalances struct {
	Success bool `json:"success"`
	Result  []struct {
		Coin  string  `json:"coin"`
		Free  float64 `json:"free"`
		Total float64 `json:"total"`
	} `json:"result"`
}

type TransferSubaccounts struct {
	Success bool `json:"success"`
	Result  struct {
		ID     int       `json:"id"`
		Coin   string    `json:"coin"`
		Size   float64   `json:"size"`
		Time   time.Time `json:"time"`
		Notes  string    `json:"notes"`
		Status string    `json:"status"`
	} `json:"result"`
}
