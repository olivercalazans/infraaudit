package internal

import (
	"fmt"
	"strings"
	"sync"
)

type Data struct {
    Hosts        map[string]*Host
    OfflineHosts []*OfflineHost
	mu 			 sync.Mutex
}


type Host struct {
	Name     string
	Model    string
	Firmware string
	CPU      string
	Memory   string
}


type OfflineHost struct {
	Name   string
	Vendor string
	Ip     string
	Err    string
}



func NewData() *Data {
    return &Data{
        Hosts:        make(map[string]*Host),
        OfflineHosts: []*OfflineHost{},
    }
}



func (d *Data) FilterDevices(prefix string, devices []HostInfo) {
	fmt.Println("> Filtering devices")
	for _, host := range devices {
		ip := host.Interfaces[0].IP
		if strings.HasPrefix(ip, prefix) {
			d.addHost(ip, host.Name)
		}
	}
}



func (d *Data) AddOfflineHost(ip, err string) {
	d.mu.Lock()
    defer d.mu.Unlock()

	d.OfflineHosts = append(d.OfflineHosts,
		&OfflineHost{
			Name:   d.Hosts[ip].Name,
			Ip:     ip,
			Err:    err,
		},
	)

	delete(d.Hosts, ip)
}



func (d *Data) addHost(ip, name string) {
	d.Hosts[ip] = &Host{ Name: name }
}



func (d *Data) AddModel(ip, model string) {
	d.mu.Lock()
    defer d.mu.Unlock()
	d.Hosts[ip].Model = model
}



func (d *Data) AddFirmwareVersion(ip, firmware string) {
	d.mu.Lock()
    defer d.mu.Unlock()
	d.Hosts[ip].Firmware = firmware
}



func (d *Data) AddCPU(ip, cpu string) {
	d.mu.Lock()
    defer d.mu.Unlock()
	d.Hosts[ip].CPU = fmt.Sprintf("%s%%", cpu)
}



func (d *Data) AddMemory(ip, memory string) {
	d.mu.Lock()
    defer d.mu.Unlock()
	d.Hosts[ip].Memory = fmt.Sprintf("%s%%", memory)
}



func displayHeader(headers []string, lens []int) {
	var header strings.Builder
	var line strings.Builder

	for i := range headers {
		header.WriteString(fmt.Sprintf("%-*s   ", lens[i], headers[i]))
		line.WriteString(fmt.Sprintf("%s   ", strings.Repeat("-", lens[i])))
	}

	fmt.Printf("\n\n%s\n", header.String())
	fmt.Println(line.String())
}



func (d *Data) DisplayRuckus() {
	headers := []string{"Name", "IP", "Model", "%CPU", "%Memory", "Firmware Version"}
	lens    := []int{15, 15, 8, 4, 7, 18}  
	displayHeader(headers, lens)

	for ip, h := range d.Hosts {
		fmt.Printf("%-15s   %-15s   %-8s   %-4s   %-7s   %s\n", h.Name, ip, h.Model, h.CPU, h.Memory, h.Firmware)
	}
}



func (d *Data) DisplayOfflineHosts() {
	headers := []string{"Name", "IP", "Error"}
	lens    := []int{15, 15, 7}
	displayHeader(headers, lens)

	for _, offHost := range d.OfflineHosts {
		fmt.Printf("%-15s   %-15s   %s\n", offHost.Name, offHost.Ip, offHost.Err)
	}
}
