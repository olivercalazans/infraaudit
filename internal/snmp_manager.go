package internal

import "fmt"


const (
	general        = ".1.3.6.1.2.1.1.1.0"
	ruckusModel    = ".1.3.6.1.4.1.25053.1.1.2.1.1.1.1.0"
	ruckusFirmware = ".1.3.6.1.4.1.25053.1.1.3.1.1.1.1.1.3.1"
)



func GetDataFromDevices(data *Data, community string) {
	for _, host := range data.Hosts {
		_, x := queryDevice(host.Ip, community, general)
		fmt.Println(host.Ip, x)
	}
}