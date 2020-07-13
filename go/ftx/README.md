![go_ftx](go_ftx.png)

```go
package main

import (
	"./ftx"
	"fmt"
)

func main() {
	// Connect to main account, use empty string for main account and subaccount name for a subaccount
	// https://docs.ftx.com/#authentication
	client := ftx.New("", "", "")

	// Get your Positions
	// https://docs.ftx.com/#get-positions
	positions, _ := client.GetPositions(true)
	fmt.Println(positions)

	// Place Order
	// https://docs.ftx.com/#place-order
	order, _ := client.PlaceOrder("BTC-PERP", "buy", 1, "limit", 0.001, false, false, true)
	fmt.Println(order)

	// Get Open Orders
	// https://docs.ftx.com/#get-open-orders
	openOrders, _ := client.GetOpenOrders("BTC-PERP")
	fmt.Println(openOrders)

	// Cancel Open Order
	// https://docs.ftx.com/#cancel-order
	cancel, _ := client.CancelOrder(order.Result.ID)
	fmt.Println(cancel)

	// Get Order History
	// https://docs.ftx.com/#get-order-history
	orderHistory, _ := client.GetOrderHistory("BTC-PERP", 1593561600, 1594460795, 10)
	fmt.Println(orderHistory)

	// Place Trigger Order
	// https://docs.ftx.com/#place-trigger-order
	triggerOrder, _ := client.PlaceTriggerOrder("BTC-PERP", "sell", 0.1, "stop", true, true, 5000, 0, 0)
	fmt.Println(triggerOrder)

	// Get Open Trigger Orders
	// https://docs.ftx.com/#get-open-trigger-orders
	openTriggerOrders, _ := client.GetOpenTriggerOrders("BTC-PERP", "stop")
	fmt.Println(openTriggerOrders)

	// Cancel Open Trigger Order
	// https://docs.ftx.com/#cancel-open-trigger-order
	cancelTriggerOrder, _ := client.CancelTriggerOrder(triggerOrder.Result.ID)
	fmt.Println(cancelTriggerOrder)

	// Get Trigger Order History
	// https://docs.ftx.com/#get-trigger-order-history
	triggerOrderHistory, _ := client.GetTriggerOrdersHistory("BTC-PERP", 1593561600, 1594460795, 10)
	fmt.Println(triggerOrderHistory)

	// Get Historical Prices
	// https://docs.ftx.com/#get-historical-prices
	candles, _ := client.GetHistoricalPrices("BTC-PERP", 86400, 7, 1593561600, 1594460795)
	fmt.Println(candles)

	// Get Trades
	// https://docs.ftx.com/#get-trades
	trades, _ := client.GetTrades("BTC-PERP", 100, 1593561600, 1594460795)
	fmt.Println(trades)

	// Get Subaccounts
	// https://docs.ftx.com/#get-all-subaccounts
	subaccounts, _ := client.GetSubaccounts()
	fmt.Println(subaccounts)

}

```
