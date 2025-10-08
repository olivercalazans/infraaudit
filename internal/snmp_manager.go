package internal

import (
	"fmt"
	"strings"
)


type SnmpManager struct {
	data      *Data
	community string
	oids      *OIDs
}



func NewSnmpManager(data *Data, community string) *SnmpManager{
	return &SnmpManager{
		data:      data,
		community: community,
		oids:      NewOIDs(),
	} 
}



func (m *SnmpManager) PruneOfflineDevices() {
	fmt.Println("> Checking which devices are online")
	for ip, _ := range m.data.Hosts {
		ok, err := queryDevice(ip, m.community, m.oids.General)
		if ok { continue }
		m.data.AddOfflineHost(ip, err)
	}
}



func (m *SnmpManager) GetModel() {
	fmt.Println("> Fetching model")
	for ip, _ := range m.data.Hosts{
		_, snmpResp := queryDevice(ip, m.community, m.oids.Model)
		model := strings.SplitN(snmpResp, " = ", 2)
		m.data.AddModel(ip, model[1])
	}
}



func (m *SnmpManager) GetFirmware() {
	fmt.Println("> Fetching Firmware version")
	for ip, _ := range m.data.Hosts {
		_, snmpResp := queryDevice(ip, m.community, m.oids.Firmware)

		model := strings.SplitN(snmpResp, " = ", 2)
		m.data.AddFirmwareVersion(ip, model[1])
	}
}