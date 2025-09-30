package internal

import (
	"fmt"
	"log"
	"time"

	goSnmp "github.com/gosnmp/gosnmp"
)


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



func (snmpData SnmpManager) GetDataFromDevices(community, ip string) {
	snmp := &goSnmp.GoSNMP {
		Target:    ip,
		Port:      161,
		Community: community,
		Version:   goSnmp.Version2c,
		Timeout:   2 * time.Second,
		Retries:   2,
	}

	// Connect
	err := snmp.Connect()
	if err != nil {
		log.Fatalf("Error connecting: %v", err)
	}
	defer snmp.Conn.Close()

	oid := ruckusModel
	result, err := snmp.Get([]string{oid})
	if err != nil {
		log.Fatalf("SNMP Get error: %v", err)
	}

	for _, variable := range result.Variables {
		switch variable.Type {
    		case goSnmp.OctetString:
    		    // Type assertion from interface{} to []byte
    		    if b, ok := variable.Value.([]byte); ok {
    		        fmt.Printf("%s = %s\n", variable.Name, string(b))
    		    } else {
    		        fmt.Printf("%s = (unable to convert to string)\n", variable.Name)
    		    }
    		default:
    		    fmt.Printf("%s = %v\n", variable.Name, variable.Value)
    	}
	}
}