package internal

type Data struct {
	Result []string
	Hosts  map[string]Host
}

type Host struct {
	Model    string
	Firmware string
}
