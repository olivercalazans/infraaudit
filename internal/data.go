package internal

import (
	"strings"
)

type Data struct {
    Secrets      Secrets
    Hosts        []Host
    OfflineHosts []OfflineHost
}


type Host struct {
	Ip       string
	Vendor   string
	Name     string
	Model    string
	Firmware string
}


type OfflineHost struct {
	Ip  string
	Err string
}



func NewData() *Data {
    return &Data{
        Secrets:      Secrets{},
        Hosts:        []Host{},
        OfflineHosts: []OfflineHost{},
    }
}



func (d *Data) FilterDevices(prefixes map[string]string, devices []HostInfo) {
	for _, host := range devices {
		ip := host.Interfaces[0].IP

		for vendor, prefix := range prefixes {
			if strings.HasPrefix(ip, prefix) {
				d.addHost(ip, vendor, host.Name)
				break
			}
		}
	}
}



func (d *Data) addHost(ip, vendor, name string) {
	d.Hosts = append(d.Hosts, Host{
		Ip:     ip,
		Vendor: vendor,
		Name:   name,
	})
}
