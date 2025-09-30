package internal

import "strings"


type Data struct {
    Secrets      Secrets
    Hosts        map[string]Host
    OfflineHosts map[string]string
}


type Host struct {
	Name     string
	Model    string
	Firmware string
}



func NewData() *Data {
    return &Data{
        Secrets:      Secrets{},
        Hosts:        make(map[string]Host),
        OfflineHosts: make(map[string]string),
    }
}



func (d *Data) FilterDevices(prefixes []string, devices []HostInfo) {
	for _, host := range devices {
		ip := host.Interfaces[0].IP

		for _, prefix := range prefixes {
			if strings.Contains(ip, prefix) {
				d.addHost(ip, host.Name)
				break
			}
		}
	}
}



func (d *Data) addHost(ip, name string) {
	d.Hosts[ip] = Host{Name: name}
}