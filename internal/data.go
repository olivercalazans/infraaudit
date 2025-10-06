package internal

import (
	"fmt"
	"strings"
)

type Data struct {
    Secrets      Secrets
    Hosts        map[string]*Host
    OfflineHosts []*OfflineHost
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
        Hosts:        make(map[string]*Host),
        OfflineHosts: []*OfflineHost{},
    }
}



func (d *Data) FilterDevices(prefixes map[string]string, devices []HostInfo) {
	fmt.Println("> Filtering devices")
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
	d.Hosts[ip] = &Host{
		Vendor: vendor,
		Name:   name,
	}
}



func (d *Data) AddModel(ip, model string) {
	d.Hosts[ip].Model = model
}



func (d *Data) AddFirmwareVersion(ip, firmware string) {
	d.Hosts[ip].Firmware = firmware
}



func (d *Data) AddOfflineHost(ip, err string) {
	d.OfflineHosts = append(d.OfflineHosts,
		&OfflineHost{
			Ip:   ip,
			Name: d.Hosts[ip].Name,
			Err:  err,
		},
	)
	delete(d.Hosts, ip)
}


func displayHeader(title, header string) {
	fmt.Printf("\n### %s\n", title)
	headerLen := len(header)
	displayLine(headerLen)
	fmt.Printf("%s", header)
	displayLine(headerLen)
}



func displayLine(len int) {
	fmt.Printf("+%s+\n", strings.Repeat("-", len - 3))
}



func (d *Data) DisplayRuckus() {
	header := fmt.Sprintf("| %-15s | %-15s | %-7s | %s |\n", "Name", "IP", "Model", "Firmware Version")
	displayHeader("Ruckus devices", header)

	for ip, host := range d.Hosts {
		if host.Vendor != "ruckus" { continue }
		fmt.Printf("  %-15s | %-15s | %-7s | %s\n", host.Name, ip, host.Model, host.Firmware)
	}
}



func (d *Data) DisplayOfflineHosts() {
	header := fmt.Sprintf("| %-15s | %-15s | %-7s |\n", "Name", "IP", "Error")
	displayHeader("Offline devices", header)

	for _, offHost := range d.OfflineHosts {
		fmt.Printf("  %-15s | %-15s | %s\n", offHost.Name, offHost.Ip, offHost.Err)
	}
}
