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
		parts := strings.SplitN(snmpResp, " = ", 2)
		m.data.AddModel(ip, parts[1])
	}
}



func (m *SnmpManager) GetFirmware() {
	fmt.Println("> Fetching Firmware version")
	for ip, _ := range m.data.Hosts {
		_, snmpResp := queryDevice(ip, m.community, m.oids.Firmware)

		parts := strings.SplitN(snmpResp, " = ", 2)
		m.data.AddFirmwareVersion(ip, parts[1])
	}
}



func (m *SnmpManager) GetCPU() {
	fmt.Println("> Fetching CPU usage")
	for ip, _ := range m.data.Hosts {
		_, snmpResp := queryDevice(ip, m.community, m.oids.CPU)

		parts := strings.SplitN(snmpResp, " = ", 2)
		m.data.AddCPU(ip, fmt.Sprintf("%s%%", parts[1]))
	}
}