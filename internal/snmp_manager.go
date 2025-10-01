package internal

import "fmt"


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

	for _, i := range snmp.data.Hosts {
		fmt.Println(i)
	}
}



func (snmp *SnmpManager) pruneOfflineDevices() {
	for ip, _ := range snmp.data.Hosts {
		online, err := queryDevice(ip, snmp.community, snmp.oids.general)
		if online { continue }
		snmp.data.AddOfflineHost(ip, err)
	}
}