![go_ftx](go_ftx.png)

Go Sample code of FTX

```go
package main

import (
	"./ftx"
	"fmt"
)

func main() {
	// Connect to main account, use empty string for main account and subaccount name for a subaccount
	// API key, API secret, subaccount name
	client := ftx.New("", "", "")

	// Get your Positions
	// showAvgPrice = true
	positions, _ := client.GetPositions(true)
	fmt.Println(positions)

	// Place Order
	// market, side, price, type, size, reduceOnly, ioc, postOnly
	order, _ := client.PlaceOrder("BTC-PERP", "buy", 1, "limit", 0.001, false, false, true)
	fmt.Println(order)

	// Get Open Orders
	// market
	openOrders, _ := client.GetOpenOrders("BTC-PERP")
	fmt.Println(openOrders)

	// Cancel Order
	cancel, _ := client.CancelOrder(order.Result.ID)
	fmt.Println(cancel)

	// Get Order History
	// market, start_time, end_time, limit
	orderHistory, _ := client.GetOrderHistory("BTC-PERP", 1593561600, 1594460795, 10)
	fmt.Println(orderHistory)

	// Place Trigger Order
	// market, side, size, type, reduceOnly, retryUntilFilled, triggerPrice, orderPrice, trailValue
	triggerOrder, _ := client.PlaceTriggerOrder("BTC-PERP", "sell", 0.1, "stop", true, true, 5000, 0, 0)
	fmt.Println(triggerOrder)

	// Get Open Trigger Orders
	// market, type
	openTriggerOrders, _ := client.GetOpenTriggerOrders("BTC-PERP", "stop")
	fmt.Println(openTriggerOrders)

	// Cancel Trigger Order
	// OrderId
	cancelTriggerOrder, _ := client.CancelTriggerOrder(triggerOrder.Result.ID)
	fmt.Println(cancelTriggerOrder)

	// Get Trigger Order History
	// market, start_time, end_time, limit
	triggerOrderHistory, _ := client.GetTriggerOrdersHistory("BTC-PERP", 1593561600, 1594460795, 10)
	fmt.Println(triggerOrderHistory)

	// Get Historical Prices
	// market, resolution, limit, start_time, end_time
	candles, _ := client.GetHistoricalPrices("BTC-PERP", 86400, 7, 1593561600, 1594460795)
	fmt.Println(candles)

	// Get Trades
	// market, limit, start_time, end_time
	trades, _ := client.GetTrades("BTC-PERP", 100, 1593561600, 1594460795)
	fmt.Println(trades)

	// Get Subaccounts
	subaccounts, _ := client.GetSubaccounts()
	fmt.Println(subaccounts)

}

```
