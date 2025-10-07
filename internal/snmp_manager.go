package internal

import (
	"fmt"
	"strings"
)


type SnmpManager struct {
	data      *Data
	community string
}


const(
	general        = ".1.3.6.1.2.1.1.1.0"
	ruckusModel    = ".1.3.6.1.4.1.25053.1.1.2.1.1.1.1.0"
	ruckusFirmware = ".1.3.6.1.4.1.25053.1.1.3.1.1.1.1.1.3.1"
)



func NewSnmpManager(data *Data, community string) *SnmpManager{
	return &SnmpManager{
		data:      data,
		community: community,
	} 
}



func (m *SnmpManager) PruneOfflineDevices() {
	fmt.Println("> Checking which devices are online")
	for ip, _ := range m.data.Hosts {
		ok, err := queryDevice(ip, m.community, general)
		if ok { continue }
		m.data.AddOfflineHost(ip, err)
	}
}



func (m *SnmpManager) GetModel() {
	fmt.Println("> Fetching model")
	for ip, _ := range m.data.Hosts{
		_, snmpResp := queryDevice(ip, m.community, ruckusModel)
		model := strings.SplitN(snmpResp, " = ", 2)
		m.data.AddModel(ip, model[1])
	}
}



func (m *SnmpManager) GetFirmware() {
	fmt.Println("> Fetching Firmware version")
	for ip, _ := range m.data.Hosts {
		_, snmpResp := queryDevice(ip, m.community, ruckusFirmware)

		model := strings.SplitN(snmpResp, " = ", 2)
		m.data.AddFirmwareVersion(ip, model[1])
	}
}