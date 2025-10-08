package internal


type OIDs struct {
	General  string
	Model    string
	Firmware string
	CPU      string
	Memory   string
}



func NewOIDs() *OIDs {
	return &OIDs{
		General:  ".1.3.6.1.2.1.1.1.0",
		Model: 	  ".1.3.6.1.4.1.25053.1.1.2.1.1.1.1.0",
		Firmware: ".1.3.6.1.4.1.25053.1.1.3.1.1.1.1.1.3.1",
		CPU:      ".1.3.6.1.4.1.25053.1.1.11.1.1.1.1.0",
		Memory:   ".1.3.6.1.4.1.25053.1.1.11.1.1.1.2",
	}
}