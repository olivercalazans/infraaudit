# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import asyncio
from models.data       import Data
from snmp.snmp_fetcher import SNMP_Fetcher
from oid.oid_manager   import OID_Manager
from zabbix.api_zabbix import API_ZABBIX


class Main:
    
    _instance:"Main" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ('_data', '_loop', '_snmp_fetcher')

    def __init__(self):
        self._data:Data                      = Data()
        self._loop:asyncio.AbstractEventLoop = None
        self._snmp_fetcher:SNMP_Fetcher      = None



    def __enter__(self):
        self._retrieve_host_information_from_zabbix_api()
        self._collect_data_using_snmp()
        self._display_result()
        self._display_devices_with_no_response()
        return self



    def __exit__(self, exc_type, exc_value, traceback):
        return False



    def _retrieve_host_information_from_zabbix_api(self) -> None:
        print('>> Retrieving data from Zabbix API')
        with API_ZABBIX(self._data) as API:
            API._get_hosts_information()



    def _collect_data_using_snmp(self) -> None:
        print('>> Collecting data from devices using SNMP')
        self._start_async_loop()
        self._run_snmp_fetcher()
        self._close_jobs()


    
    def _start_async_loop(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)



    def _close_jobs(self) -> None:
        pending = asyncio.all_tasks(self._loop)
        if pending:
            self._loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        
        self._loop.close()

    

    def _run_snmp_fetcher(self) -> None:
        with SNMP_Fetcher(self._data) as self._snmp_fetcher:
            self._get_ruckus_information()



    def _run_tasks(self, oids:str) -> list[tuple]:
        return self._loop.run_until_complete(self._fetch_all_snmp(oids))



    async def _fetch_all_snmp(self, oid:str) -> list[tuple]:
        tasks:list[asyncio.Task] = [self._snmp_fetcher.snmpget(ip, oid) for ip in self._data.hosts]
        return await asyncio.gather(*tasks)



    def _get_ruckus_information(self) -> None:
        print('   # Collecting data from Ruckus APs')
        oids:list = [OID_Manager.SYS_DESCRIPTION, OID_Manager.RUCKUS_AP_MODEL, OID_Manager.RUCKUS_FIRMWARE_VERSION]
        self._run_tasks(oids)
        

    
    def _display_result(self) -> None:
        for i in self._data.hosts:
            print(i, self._data.hosts[i])

    

    def _display_devices_with_no_response(self) -> None:
        for ip, info in self._data.removed_hosts.items():
            print(f'{ip:<15} ({info["name"]}): Error: {info["error"]}')





if __name__ == '__main__':
    with Main() as infraaudit:
        ...