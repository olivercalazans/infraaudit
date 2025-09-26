package internal

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
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

	hosts, err := getHosts(apiUrl, token)
	if err != nil {
		return nil, err
	}

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
		panic(fmt.Sprintf("Failed to get token from server: %v", err))
	}

	var token string
	if err := json.Unmarshal(resp.Result, &token); err != nil {
		panic(fmt.Sprintf("No token received from server: %v", err))
	}

	return token
}



func getHosts(apiURL, auth string) []HostInfo {
	req := map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  "host.get",
		"params": map[string]interface{}{
			"output":           []string{"hostid", "name"},
			"selectInterfaces": []string{"ip"},
		},
		"auth": auth,
		"id":   2,
	}

	resp, err := sendRequest(apiURL, req)
	if err != nil {
		return nil
	}

	var hosts []HostInfo
	if err := json.Unmarshal(resp.Result, &hosts); err != nil {
		return nil
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
