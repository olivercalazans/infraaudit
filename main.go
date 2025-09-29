package main

import (
	"fmt"

	"github.com/olivercalazans/infraaudit/internal"
)



func main() {
	secrets := internal.NewSecrets()
	//device  := internal.Data{}
	hosts   := internal.GetDataFromZabbix(secrets.APIURL)

	for _, item := range hosts {
		fmt.Println(item)
	}
}
