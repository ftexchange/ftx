package ftx

import (
	"./structs"
	"encoding/json"
	"log"
)

type SubaccountsList structs.SubaccountsList
type Subaccount structs.Subaccount
type Response structs.Response
type SubaccountBalances structs.SubaccountBalances
type TransferSubaccounts structs.TransferSubaccounts

func (client *FtxClient) GetSubaccounts() (SubaccountsList, error) {
	var subaccounts SubaccountsList
	resp, err := client._get("subaccounts", []byte(""))
	if err != nil {
		log.Printf("Error GetSubaccounts", err)
		return subaccounts, err
	}
	err = _processResponse(resp, &subaccounts)
	return subaccounts, err
}

func (client *FtxClient) CreateSubaccount(nickname string) (Subaccount, error) {
	var subaccount Subaccount
	requestBody, err := json.Marshal(map[string]string{"nickname": nickname})
	if err != nil {
		log.Printf("Error CreateSubaccount", err)
		return subaccount, err
	}
	resp, err := client._post("subaccounts", requestBody)
	if err != nil {
		log.Printf("Error CreateSubaccount", err)
		return subaccount, err
	}
	err = _processResponse(resp, &subaccount)
	return subaccount, err
}

func (client *FtxClient) ChangeSubaccountName(nickname string, newNickname string) (Response, error) {
	var changeSubaccount Response
	requestBody, err := json.Marshal(map[string]string{"nickname": nickname, "newNickname": newNickname})
	if err != nil {
		log.Printf("Error ChangeSubaccountName", err)
		return changeSubaccount, err
	}
	resp, err := client._post("subaccounts/update_name", requestBody)
	if err != nil {
		log.Printf("Error ChangeSubaccountName", err)
		return changeSubaccount, err
	}
	err = _processResponse(resp, &changeSubaccount)
	return changeSubaccount, err
}

func (client *FtxClient) DeleteSubaccount(nickname string) (Response, error) {
	var deleteSubaccount Response
	requestBody, err := json.Marshal(map[string]string{"nickname": nickname})
	if err != nil {
		log.Printf("Error DeleteSubaccount", err)
		return deleteSubaccount, err
	}
	resp, err := client._delete("subaccounts", requestBody)
	if err != nil {
		log.Printf("Error DeleteSubaccount", err)
		return deleteSubaccount, err
	}
	err = _processResponse(resp, &deleteSubaccount)
	return deleteSubaccount, err
}

func (client *FtxClient) GetSubaccountBalances(nickname string) (SubaccountBalances, error) {
	var subaccountBalances SubaccountBalances
	resp, err := client._get("subaccounts/"+nickname+"/balances", []byte(""))
	if err != nil {
		log.Printf("Error SubaccountBalances", err)
		return subaccountBalances, err
	}
	err = _processResponse(resp, &subaccountBalances)
	return subaccountBalances, err
}

func (client *FtxClient) TransferSubaccounts(coin string, size float64, source string, destination string) (TransferSubaccounts, error) {
	var transferSubaccounts TransferSubaccounts
	requestBody, err := json.Marshal(map[string]interface{}{
		"coin":        coin,
		"size":        size,
		"source":      source,
		"destination": destination,
	})
	if err != nil {
		log.Printf("Error TransferSubaccounts", err)
		return transferSubaccounts, err
	}
	resp, err := client._post("subaccounts/transfer", requestBody)
	if err != nil {
		log.Printf("Error TransferSubaccounts", err)
		return transferSubaccounts, err
	}
	err = _processResponse(resp, &transferSubaccounts)
	return transferSubaccounts, err
}
