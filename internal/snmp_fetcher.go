package internal

import (
	"fmt"
	"time"

	goSnmp "github.com/gosnmp/gosnmp"
)



func queryDevice(ip, community, oid string) (bool, string) {
	snmp := &goSnmp.GoSNMP{
		Target:    ip,
		Port:      161,
		Community: community,
		Version:   goSnmp.Version2c,
		Timeout:   2 * time.Second,
		Retries:   1,
	}

	if err := snmp.Connect(); err != nil {
		return false, fmt.Sprintf("ERROR connecting to %s: %v", ip, err)
	}
	defer snmp.Conn.Close()

	result, err := snmp.Get([]string{oid})
	if err != nil {
		return false, fmt.Sprintf("ERROR querying %s: %v", ip, err)
	}

	if len(result.Variables) == 0 {
		return false, fmt.Sprintf("ERROR %s: no response", ip)
	}

	return true, fmt.Sprintf("%s = %s", result.Variables[0].Name, snmpPDUToString(result.Variables[0]))
}



func snmpPDUToString(pdu goSnmp.SnmpPDU) string {
	switch pdu.Type {
	case goSnmp.OctetString:
		if b, ok := pdu.Value.([]byte); ok {
			return string(b)
		}
		return "(unable to convert to string)"
	default:
		return fmt.Sprintf("%v", pdu.Value)
	}
}
