package internal

import (
	"fmt"
	"strings"
)

type Data struct {
    Secrets      Secrets
    Hosts        map[string]Host
    OfflineHosts []OfflineHost
}


type Host struct {
	Vendor   string
	Name     string
	Model    string
	Firmware string
}


type OfflineHost struct {
	Ip   string
	Name string
	Err  string
}



func NewData() *Data {
    return &Data{
        Secrets:      Secrets{},
        Hosts:        make(map[string]Host),
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
	d.Hosts[ip] = Host{
		Vendor: vendor,
		Name:   name,
	}
}



func (d *Data) AddOfflineHost(ip, err string) {
	d.OfflineHosts = append(d.OfflineHosts,
		OfflineHost{
			Ip:   ip,
			Name: d.Hosts[ip].Name,
			Err:  err,
		},
	)
	delete(d.Hosts, ip)
}


func (d *Data) DisplayOfflineHosts() {
	for _, offHost := range d.OfflineHosts {
		fmt.Printf("%-12s - %-15s - %s\n", offHost.Name, offHost.Ip, offHost.Err)
	}
}