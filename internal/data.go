package internal


type Data struct {
	Secrets      Secrets
	Result       []string
	Hosts        map[string]Host
	OfflineHosts map[string]string
}


type Host struct {
	Name     string
	Model    string
	Firmware string
}

