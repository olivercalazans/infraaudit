package main

import (
	"fmt"

	"github.com/olivercalazans/infraaudit/internal"
)



func main() {
	secrets := internal.NewSecrets()
	data    := internal.NewData()
	hosts   := internal.GetDataFromZabbix(secrets.APIURL)

	data.FilterDevices(secrets.Prefixes, hosts)

	for ip, i := range data.Hosts {
		fmt.Println(ip, i.Name)
	}
}
