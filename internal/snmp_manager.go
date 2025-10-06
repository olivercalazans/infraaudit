package internal

import (
	"fmt"
	"strings"
)


type SnmpManager struct {
	data      *Data
	community string
	oids      OIDs 
}


type OIDs struct {
	general        string
	ruckusModel    string
	ruckusFirmware string
}



func NewSnmpManager(data *Data, community string) *SnmpManager{
	return &SnmpManager{
		data:      data,
		community: community,
		oids:      OIDs{    
			general: 		".1.3.6.1.2.1.1.1.0",
			ruckusModel:    ".1.3.6.1.4.1.25053.1.1.2.1.1.1.1.0",
			ruckusFirmware: ".1.3.6.1.4.1.25053.1.1.3.1.1.1.1.1.3.1",
		},
	} 
}



func (snmp *SnmpManager) SendSnmpProbes() {
	snmp.pruneOfflineDevices()

	fmt.Println("> Collecting Ruckus data")
	snmp.getRuckusModel()
	snmp.getRuckusFirmware()
}



func (snmp *SnmpManager) pruneOfflineDevices() {
	fmt.Println("> Checking which devices are online")
	for ip, _ := range snmp.data.Hosts {
		ok, err := queryDevice(ip, snmp.community, snmp.oids.general)
		
		if ok {continue }
		
		snmp.data.AddOfflineHost(ip, err)
	}
}



func (snmp *SnmpManager) getRuckusModel() {
	for ip, _ := range snmp.data.Hosts {
		_, snmpResp := queryDevice(ip, snmp.community, snmp.oids.ruckusModel)

		model := strings.SplitN(snmpResp, " = ", 2)
		snmp.data.AddModel(ip, model[1])
	}
}



func (snmp *SnmpManager) getRuckusFirmware() {
	for ip, _ := range snmp.data.Hosts {
		_, snmpResp := queryDevice(ip, snmp.community, snmp.oids.ruckusFirmware)

		model := strings.SplitN(snmpResp, " = ", 2)
		snmp.data.AddFirmwareVersion(ip, model[1])
	}
}