package ftx

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
)

func (client *FtxClient) sign(signaturePayload string) string {
	mac := hmac.New(sha256.New, client.Secret)
	mac.Write([]byte(signaturePayload))
	return hex.EncodeToString(mac.Sum(nil))
}
