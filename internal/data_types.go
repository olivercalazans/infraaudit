package internal

type Data struct {
	Result       []string
	Hosts        map[string]Host
	OfflineHosts map[string]string
}

type Host struct {
	Model    string
	Firmware string
}
