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

type Config struct {
	APIURL string `json:"api_url"`
}

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

func GetDataFromZabbix() ([]HostInfo, error) {
	cfg, err := loadConfig("config.json")
	if err != nil {
		return nil, err
	}

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("User: ")
	userRaw, _ := reader.ReadString('\n')
	user := strings.TrimSpace(userRaw)

	fmt.Print("Password: ")
	bytePass, _ := term.ReadPassword(int(syscall.Stdin))
	fmt.Println()
	pass := strings.TrimSpace(string(bytePass))

	token, err := login(cfg.APIURL, user, pass)
	if err != nil {
		return nil, err
	}

	hosts, err := getHosts(cfg.APIURL, token)
	if err != nil {
		return nil, err
	}

	return hosts, nil
}

func loadConfig(path string) (*Config, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var cfg Config
	if err := json.NewDecoder(file).Decode(&cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}

func login(apiURL, user, pass string) (string, error) {
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
		return "", err
	}

	var token string
	if err := json.Unmarshal(resp.Result, &token); err != nil {
		return "", err
	}
	return token, nil
}

func getHosts(apiURL, auth string) ([]HostInfo, error) {
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
		return nil, err
	}

	var hosts []HostInfo
	if err := json.Unmarshal(resp.Result, &hosts); err != nil {
		return nil, err
	}
	return hosts, nil
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
