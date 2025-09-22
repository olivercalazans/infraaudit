package main

import (
	"fmt"

	"github.com/olivercalazans/infraaudit/internal"
)

func main() {
	device := internal.Data{}
	jsonData, err := internal.GetDataFromZabbix()
	if err != nil {
		fmt.Println("Error fetching data:", err)
		return
	}

	fmt.Println(string(jsonData))
	fmt.Print(device)
}
