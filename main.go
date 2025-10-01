package main

import (
	"github.com/olivercalazans/infraaudit/internal"
)



func main() {
	secrets := internal.NewSecrets()
	data    := internal.NewData()

	hosts := internal.GetDataFromZabbix(secrets.APIURL)
	data.FilterDevices(secrets.Prefixes, hosts)
	
	snmp := internal.NewSnmpManager(data, secrets.Community)
	snmp.SendSnmpProbes()

	data.DisplayOfflineHosts()

}
