package internal

import (
	"fmt"
	"strings"
	"sync"
)


type SnmpManager struct {
	data      *Data
	community string
	oids      *OIDs
}



func NewSnmpManager(data *Data, community string) *SnmpManager{
	return &SnmpManager{
		data:      data,
		community: community,
		oids:      NewOIDs(),
	} 
}



func (m *SnmpManager) PruneOfflineDevices() {
    fmt.Println("> Checking which devices are online")

    sem := make(chan struct{}, 50)
    var wg sync.WaitGroup

    for ip := range m.data.Hosts {
        wg.Add(1)
        sem <- struct{}{}

        go func(ip string) {
            defer wg.Done()
            defer func() { <-sem }()

            ok, err := queryDevice(ip, m.community, m.oids.General)
            if !ok {
                m.data.AddOfflineHost(ip, err)
            }
        }(ip)
    }

    wg.Wait()
}




func (m *SnmpManager) fetchAllHosts(addMethod func(string, string), oid string) {
    sem := make(chan struct{}, 50)
    var wg sync.WaitGroup

    for ip := range m.data.Hosts {
        wg.Add(1)
        sem <- struct{}{}

        go func(ip string) {
            defer wg.Done()
            defer func() { <-sem }()

            _, snmpResp := queryDevice(ip, m.community, oid)
            parts := strings.SplitN(snmpResp, " = ", 2)
            if len(parts) == 2 {
                addMethod(ip, parts[1])
            } else {
                addMethod(ip, "<invalid response>")
            }
        }(ip)
    }

    wg.Wait()
}




func (m *SnmpManager) GetModel() {
	fmt.Println("> Fetching model")
	m.fetchAllHosts(m.data.AddModel, m.oids.Model)
}



func (m *SnmpManager) GetFirmware() {
	fmt.Println("> Fetching Firmware version")
	m.fetchAllHosts(m.data.AddFirmwareVersion, m.oids.Firmware)
}



func (m *SnmpManager) GetCpuUsage() {
	fmt.Println("> Fetching CPU usage")
	m.fetchAllHosts(m.data.AddCPU, m.oids.CPU)
}



func (m *SnmpManager) GetMemoryUsage() {
	fmt.Println("> Fetching Memory usage")
	m.fetchAllHosts(m.data.AddMemory, m.oids.Memory)
}