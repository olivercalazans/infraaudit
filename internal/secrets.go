package internal

import (
	"encoding/json"
	"fmt"
	"os"
)


type Secrets struct {
	APIURL    string   			`json:"api_url"`
	Prefixes  map[string]string `json:"prefixes"`
	Community string   			`json:"community"`
}



func NewSecrets() *Secrets {
	file, err := os.Open("secrets.json")
	if err != nil {
		panic(fmt.Sprintf("failed to open config file: %v", err))
	}
	defer file.Close()

	var secrets Secrets
	if err := json.NewDecoder(file).Decode(&secrets); err != nil {
		panic(fmt.Sprintf("failed to load config: %v", err))
	}

	return &secrets
}