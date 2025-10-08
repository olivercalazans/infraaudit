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
	for ip := range m.data.Hosts {
		ok, err := queryDevice(ip, m.community, m.oids.General)
		if ok { continue }
		m.data.AddOfflineHost(ip, err)
	}
}



func (m *SnmpManager) fetchAllHosts(addMethod func(string, string), oid string) {
	for ip := range m.data.Hosts{
		_, snmpResp := queryDevice(ip, m.community, oid)
		
		parts := strings.SplitN(snmpResp, " = ", 2)
		addMethod(ip, parts[1])
	}
}



func (m *SnmpManager) GetModel() {
	fmt.Println("> Fetching model")
	m.fetchAllHosts(m.data.AddModel, m.oids.Model)
}



func (m *SnmpManager) GetFirmware() {
	fmt.Println("> Fetching Firmware version")
	m.fetchAllHosts(m.data.AddFirmwareVersion, m.oids.Firmware)
}



func (m *SnmpManager) GetCpuUsage() {
	fmt.Println("> Fetching CPU usage")
	m.fetchAllHosts(m.data.AddCPU, m.oids.CPU)
}



func (m *SnmpManager) GetMemoryUsage() {
	fmt.Println("> Fetching Memory usage")
	m.fetchAllHosts(m.data.AddMemory, m.oids.Memory)
}