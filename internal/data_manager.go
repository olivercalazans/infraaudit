package internal

func (d *Data) AddHost(ip, model, firmware string) {
	d.Hosts[ip] = Host{
		Model:    model,
		Firmware: firmware,
	}
}

func (d *Data) AddOfflineHost(ip, error string) {
	d.OfflineHosts[ip] = error
}
