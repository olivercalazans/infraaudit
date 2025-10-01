package main

import (
	"fmt"

	"github.com/olivercalazans/infraaudit/internal"
)



func main() {
	secrets := internal.NewSecrets()
	data    := internal.NewData()

	hosts := internal.GetDataFromZabbix(secrets.APIURL)
	data.FilterDevices(secrets.Prefixes, hosts)
	fmt.Println(data.Hosts)
	//GetDataFromDevices(data, secrets.Community)
}
