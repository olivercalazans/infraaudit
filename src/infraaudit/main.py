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
        return self



    def __exit__(self, exc_type, exc_value, traceback):
        return False



    def _retrieve_host_information_from_zabbix_api(self) -> None:
        print('>> Retrieving data from Zabbix API')
        with API_ZABBIX(self._data) as API:
            API._get_hosts_information()



    def _collect_data_using_snmp(self) -> None:
        with SNMP_Fetcher(self._data) as self._snmp_fetcher:
            print('>> Collecting data from devices using SNMP')
            self._start_async_loop()

            self._run_tasks('Enterprise name', OID_Manager.SYS_DESCRIPTION, 'manufacturer')
            self._run_tasks('Enterprise ID', OID_Manager.SYS_OBJECT_ID, 'oid')
            self._run_tasks('Firmware Version', OID_Manager.FIRMWARE_VERSION, 'firmware')

            self._close_jobs()

    

    def _start_async_loop(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._snmp_fetcher = SNMP_Fetcher(self._data)



    def _run_tasks(self, message:str, oid:str, key:str) -> list[tuple]:
        print(f'{" "*6} - Collecting {message}')
        return self._loop.run_until_complete(self._fetch_all_snmp(oid, key))



    async def _fetch_all_snmp(self, oid:str, key:str) -> list[tuple]:
        tasks:list[asyncio.Task] = [self._snmp_fetcher.snmpget(ip, oid, key) for ip in self._data.hosts]
        return await asyncio.gather(*tasks)



    def _close_jobs(self) -> None:
        self._snmp_fetcher.finish_engine()

        pending = asyncio.all_tasks(self._loop)
        if pending:
            self._loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        
        self._loop.close()


    
    def _display_result(self) -> None:
        for i in self._data.hosts:
            print(i, self._data.hosts[i])




if __name__ == '__main__':
    with Main() as infraaudit:
        ...