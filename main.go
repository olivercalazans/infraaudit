package main

import (
	"github.com/olivercalazans/infraaudit/internal"
)



func main() {
	secrets := internal.NewSecrets()
	data    := internal.NewData()

	hosts := internal.GetDataFromZabbix(secrets.APIURL)
	data.FilterDevices(secrets.Prefixes, hosts)

	snmp := internal.NewSnmpManager()

	for ip, _ := range data.Hosts {
		snmp.GetDataFromDevices(secrets.Community, ip)
	}
}
