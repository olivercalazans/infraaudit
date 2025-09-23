package main

import (
	"fmt"

	"github.com/olivercalazans/infraaudit/internal"
)

func main() {
	device := internal.Data{}
	hosts, err := internal.GetDataFromZabbix()

	if err != nil {
		panic(err)
	}

	for _, h := range hosts {
		if len(h.Interfaces) > 0 {
			fmt.Printf("ID: %s | Name: %s | IP: %s\n", h.HostID, h.Name, h.Interfaces[0].IP)
		}
	}

	fmt.Print(device)
}
