package structs

import (
	"time"
)

type NewOrder struct {
	Market                  string  `json:"market"`
	Side                    string  `json:"side"`
	Price                   float64 `json:"price"`
	Type                    string  `json:"type"`
	Size                    float64 `json:"size"`
	ReduceOnly              bool    `json:"reduceOnly"`
	Ioc                     bool    `json:"ioc"`
	PostOnly                bool    `json:"postOnly"`
	ExternalReferralProgram string  `json:"externalReferralProgram"`
	// ClientID                string  `json:"clientId"`
}

type NewOrderResponse struct {
	Success bool  `json:"success"`
	Result  Order `json:"result"`
}

type Order struct {
	CreatedAt     time.Time `json:"createdAt"`
	FilledSize    float64   `json:"filledSize"`
	Future        string    `json:"future"`
	ID            int64     `json:"id"`
	Market        string    `json:"market"`
	Price         float64   `json:"price"`
	AvgFillPrice  float64   `json:"avgFillPrice"`
	RemainingSize float64   `json:"remainingSize"`
	Side          string    `json:"side"`
	Size          float64   `json:"size"`
	Status        string    `json:"status"`
	Type          string    `json:"type"`
	ReduceOnly    bool      `json:"reduceOnly"`
	Ioc           bool      `json:"ioc"`
	PostOnly      bool      `json:"postOnly"`
	ClientID      string    `json:"clientId"`
}

type OpenOrders struct {
	Success bool    `json:"success"`
	Result  []Order `json:"result"`
}

type OrderHistory struct {
	Success     bool    `json:"success"`
	Result      []Order `json:"result"`
	HasMoreData bool    `json:"hasMoreData"`
}

type NewTriggerOrder struct {
	Market           string  `json:"market"`
	Side             string  `json:"side"`
	Size             float64 `json:"size"`
	Type             string  `json:"type"`
	ReduceOnly       bool    `json:"reduceOnly"`
	RetryUntilFilled bool    `json:"retryUntilFilled"`
	TriggerPrice     float64 `json:"triggerPrice,omitempty"`
	OrderPrice       float64 `json:"orderPrice,omitempty"`
	TrailValue       float64 `json:"trailValue,omitempty"`
}

type NewTriggerOrderResponse struct {
	Success bool         `json:"success"`
	Result  TriggerOrder `json:"result"`
}

type TriggerOrder struct {
	CreatedAt        time.Time `json:"createdAt"`
	Error            string    `json:"error"`
	Future           string    `json:"future"`
	ID               int64     `json:"id"`
	Market           string    `json:"market"`
	OrderID          int64     `json:"orderId"`
	OrderPrice       float64   `json:"orderPrice"`
	ReduceOnly       bool      `json:"reduceOnly"`
	Side             string    `json:"side"`
	Size             float64   `json:"size"`
	Status           string    `json:"status"`
	TrailStart       float64   `json:"trailStart"`
	TrailValue       float64   `json:"trailValue"`
	TriggerPrice     float64   `json:"triggerPrice"`
	TriggeredAt      string    `json:"triggeredAt"`
	Type             string    `json:"type"`
	OrderType        string    `json:"orderType"`
	FilledSize       float64   `json:"filledSize"`
	AvgFillPrice     float64   `json:"avgFillPrice"`
	OrderStatus      string    `json:"orderStatus"`
	RetryUntilFilled bool      `json:"retryUntilFilled"`
}

type OpenTriggerOrders struct {
	Success bool           `json:"success"`
	Result  []TriggerOrder `json:"result"`
}

type TriggerOrderHistory struct {
	Success     bool           `json:"success"`
	Result      []TriggerOrder `json:"result"`
	HasMoreData bool           `json:"hasMoreData"`
}

type Triggers struct {
	Success bool `json:"success"`
	Result  []struct {
		Error      string    `json:"error"`
		FilledSize float64   `json:"filledSize"`
		OrderSize  float64   `json:"orderSize"`
		OrderID    int64     `json:"orderId"`
		Time       time.Time `json:"time"`
	} `json:"result"`
}
