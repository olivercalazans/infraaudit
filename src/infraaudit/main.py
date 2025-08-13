# MIT License
# Copyright (c) 2025 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from models.data       import Data
from snmp.snmp_manager import SNMP_Manager
from zabbix.api_zabbix import API_ZABBIX
from _secrets.secrets import Secret_Data


class Main:
    
    _data:Data = Data()


    @classmethod
    def execute(cls):
        cls._retrieve_host_information_from_zabbix_api()
        cls._run_snmp_probes()
        cls._display_result()
        cls._display_devices_with_no_response()



    @classmethod
    def _retrieve_host_information_from_zabbix_api(cls) -> None:
        print('>> Retrieving data from Zabbix API')
        with API_ZABBIX(cls._data):
            ...



    @classmethod
    def _run_snmp_probes(cls) -> None:
        print('>> Running SNMP probes')
        with SNMP_Manager(cls._data):
            ...



    @classmethod
    def _display_result(cls) -> None:
        cls._display_ap_ruckus_result()
    


    @classmethod
    def _display_ap_ruckus_result(cls) -> None:
        ip_prefix:str = Secret_Data.IP_PREFIX['AP Ruckus']
        if not ip_prefix in cls._data.information: return
        
        print('\n# AP RUCKUS RESULTS')
        for device, firmware in cls._data.information[ip_prefix]:
            print(f'Device model: {device:>7} - Firmware Version: {firmware}')



    @classmethod
    def _display_devices_with_no_response(cls) -> None:
        print('\n# DEVICES WITH NO RESPONSES', '=' * 60)
        for ip, info in cls._data.removed_hosts.items():
            print(f'{info["name"]:<12} {ip:<15} -> Error: {info["error"]}')





if __name__ == '__main__':
    infraaudit = Main()
    infraaudit.execute()