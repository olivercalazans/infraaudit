package internal

import "fmt"


const (
	general        = ".1.3.6.1.2.1.1.1.0"
	ruckusModel    = ".1.3.6.1.4.1.25053.1.1.2.1.1.1.1.0"
	ruckusFirmware = ".1.3.6.1.4.1.25053.1.1.3.1.1.1.1.1.3.1"
)



type SnmpManager struct {
	responses []string
}



func NewSnmpManager() *SnmpManager {
    return &SnmpManager{
        responses: []string{},
    }
}



func (snmp SnmpManager) GetDataFromDevices(data *Data, community string) {
	for ip, _ := range data.Hosts {
		x := queryDevice(ip, community, general)
		fmt.Println(ip, x)
	}
}