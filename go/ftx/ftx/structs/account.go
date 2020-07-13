package structs

type Positions struct {
	Success bool `json:"success"`
	Result  []struct {
		Cost                         float64 `json:"cost"`
		EntryPrice                   float64 `json:"entryPrice"`
		EstimatedLiquidationPrice    float64 `json:"estimatedLiquidationPrice"`
		Future                       string  `json:"future"`
		InitialMarginRequirement     float64 `json:"initialMarginRequirement"`
		LongOrderSize                float64 `json:"longOrderSize"`
		MaintenanceMarginRequirement float64 `json:"maintenanceMarginRequirement"`
		NetSize                      float64 `json:"netSize"`
		OpenSize                     float64 `json:"openSize"`
		RealizedPnl                  float64 `json:"realizedPnl"`
		ShortOrderSize               float64 `json:"shortOrderSize"`
		Side                         string  `json:"side"`
		Size                         float64 `json:"size"`
		UnrealizedPnl                float64 `json:"unrealizedPnl"`
	} `json:"result"`
}
