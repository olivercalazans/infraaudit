package internal

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"syscall"

	"golang.org/x/term"
)



type HostInfo struct {
	HostID     string `json:"hostid"`
	Name       string `json:"name"`
	Interfaces []struct {
		IP string `json:"ip"`
	} `json:"interfaces"`
}



type ZabbixResponse struct {
	Jsonrpc string          `json:"jsonrpc"`
	Result  json.RawMessage `json:"result"`
	Error   *struct {
		Code    int    `json:"code"`
		Message string `json:"message"`
		Data    string `json:"data"`
	} `json:"error,omitempty"`
	ID int `json:"id"`
}



func GetDataFromZabbix(apiUrl string) []HostInfo {
	user  := getUser()
	pass  := getPassword()
	token := getZabbixToken(apiUrl, user, pass)
	hosts := getHosts(apiUrl, token)
	return hosts
}



func getUser() string {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("User: ")
	userRaw, _ := reader.ReadString('\n')
	user := strings.TrimSpace(userRaw)
	return user
}



func getPassword() string {
	fmt.Print("Password: ")
	bytePass, _ := term.ReadPassword(int(syscall.Stdin))
	fmt.Println()
	pass := strings.TrimSpace(string(bytePass))
	return pass
}



func getZabbixToken(apiURL, user, pass string) string {
	req := map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  "user.login",
		"params": map[string]string{
			"user":     user,
			"password": pass,
		},
		"id": 1,
	}

	resp, err := sendRequest(apiURL, req)
	if err != nil {
		log.Fatal("Failed to get token from server:", err)
	}

	var token string
	if err := json.Unmarshal(resp.Result, &token); err != nil {
		log.Fatal("No token received from server:", err)
	}

	return token
}



func getHosts(apiURL, token string) []HostInfo {
	fmt.Println("\n> Retrieving data from Zabbix")
	req := map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  "host.get",
		"params": map[string]interface{}{
			"output":           []string{"hostid", "name"},
			"selectInterfaces": []string{"ip"},
		},
		"auth": token,
		"id":   2,
	}

	resp, err := sendRequest(apiURL, req)
	if err != nil {
		log.Fatal("Impossible to communicate with Zabbix server:", err)
	}

	var hosts []HostInfo
	if err := json.Unmarshal(resp.Result, &hosts); err != nil {
		log.Fatal("Failed to parse hosts response from Zabbix:", err)
	}

	return hosts
}



func sendRequest(apiURL string, req map[string]interface{}) (*ZabbixResponse, error) {
	data, _ := json.Marshal(req)
	httpResp, err := http.Post(apiURL, "application/json", bytes.NewBuffer(data))
	if err != nil {
		return nil, err
	}
	defer httpResp.Body.Close()

	var zResp ZabbixResponse
	if err := json.NewDecoder(httpResp.Body).Decode(&zResp); err != nil {
		return nil, err
	}

	if zResp.Error != nil {
		return nil, fmt.Errorf("API error %d: %s - %s",
			zResp.Error.Code, zResp.Error.Message, zResp.Error.Data)
	}
	
	return &zResp, nil
}