# MIT License
# Copyright (c) 2025 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from models.data       import Data
from snmp.snmp_manager import SNMP_Manager
from zabbix.api_zabbix import API_ZABBIX


class Main:
    
    _instance:"Main" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ('_data')

    def __init__(self):
        self._data:Data = Data()



    def __enter__(self):
        self._retrieve_host_information_from_zabbix_api()
        self._data.filter_devices()
        self._run_snmp_probes()
        self._display_result()
        self._display_devices_with_no_response()
        return self



    def __exit__(self, exc_type, exc_value, traceback):
        return False



    def _retrieve_host_information_from_zabbix_api(self) -> None:
        print('>> Retrieving data from Zabbix API')
        with API_ZABBIX(self._data) as api:
            api._get_hosts_information()


    
    def _run_snmp_probes(self) -> None:
        print('>> Running SNMP probes')
        with SNMP_Manager(self._data) as manager:
            manager._verify_which_devices_are_active()
            self._data.prune_offline_devices()
            manager._get_ruckus_information()
            self._data.update_information()
        

    
    def _display_result(self) -> None:
        for i in self._data.hosts:
            print(i, self._data.hosts[i])

    

    def _display_devices_with_no_response(self) -> None:
        for ip, info in self._data.removed_hosts.items():
            print(f'{ip:<15} ({info["name"]}): Error: {info["error"]}')





if __name__ == '__main__':
    with Main() as infraaudit:
        ...