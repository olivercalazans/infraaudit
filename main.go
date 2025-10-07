package main

import (
	"github.com/olivercalazans/infraaudit/internal"
)



func main() {
	secrets := internal.NewSecrets()
	data    := internal.NewData()

	hosts := internal.GetDataFromZabbix(secrets.APIURL)
	data.FilterDevices(secrets.Prefix, hosts)
	
	snmp := internal.NewSnmpManager(data, secrets.Community)
	snmp.PruneOfflineDevices()
	snmp.GetModel()
	snmp.GetFirmware()

	data.DisplayRuckus()
	data.DisplayOfflineHosts()
}
