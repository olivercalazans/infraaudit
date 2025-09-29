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



func NewData() *Data {
    return &Data{
        Secrets:      Secrets{},
        Result:       []string{},
        Hosts:        make(map[string]Host),
        OfflineHosts: make(map[string]string),
    }
}
