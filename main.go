package main

import (
	"github.com/olivercalazans/infraaudit/internal"
)



func main() {
	secrets := internal.Secrets{}
	device  := internal.Data{}
	hosts   := internal.GetDataFromZabbix(secrets.APIURL)
}
