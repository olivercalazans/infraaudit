# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import asyncio
import _secrets.main_secrets as main_secrets
from snmp.snmp_fetcher import SNMP_Fetcher
from oid.oid_manager   import OID_Manager
from zabbix.api_zabbix import API_ZABBIX


class Main:
    
    _instance:"Main" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ('_hosts', '_removed_hosts', '_loop')

    def __init__(self):
        self._hosts:dict                     = {}
        self._removed_hosts:dict             = {}
        self._loop:asyncio.AbstractEventLoop = None



    def __enter__(self):
        self._retrieve_host_information_from_zabbix_api()
        self._collect_data_using_snmp()
        for i in self._hosts:print(i, self._hosts[i])
        print('===============================================')
        for i in self._removed_hosts:print(i, self._removed_hosts[i])
        return self



    def __exit__(self, exc_type, exc_value, traceback):
        return False



    def _retrieve_host_information_from_zabbix_api(self) -> None:
        print('>> Retrieving data from Zabbix API')
        with API_ZABBIX() as API:
            data:list[dict] = API._get_hosts_information()
            self._hosts     = self._filter_devices(data)



    @staticmethod
    def _filter_devices(data:list[dict]) -> None:
        print('>> Filtering for specific devices')
        return {
            device['host']: {'id': device['hostid'], 'name':device['name']}
            for device in data if main_secrets.IPS in device['host']
        }
    


    def _collect_data_using_snmp(self) -> None:
        print('>> Collecting data from devices using SNMP')
        self._start_async_loop()
        
        print(f'{" "*6} - Collecting Enterprise name')
        name_list:list[tuple] = self._loop.run_until_complete(self._fetch_all_snmp(OID_Manager.SYS_DESCRIPTION))
        
        print(f'{" "*6} - Collecting Enterprise ID')
        id_list:list[tuple] = self._loop.run_until_complete(self._fetch_all_snmp(OID_Manager.SYS_OBJECT_ID))

        self._close_jobs()
        self._add_manufacturer_name_and_id(name_list, id_list)



    def _close_jobs(self) -> None:
        SNMP_Fetcher.finish_engine()

        pending = asyncio.all_tasks(self._loop)
        if pending:
            self._loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        
        self._loop.close()


    
    def _start_async_loop(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)


    
    async def _fetch_all_snmp(self, oid:str) -> list[tuple]:
        tasks:list[asyncio.Task] = [SNMP_Fetcher().snmpget(ip, oid) for ip in self._hosts]
        return await asyncio.gather(*tasks)


    
    def _add_manufacturer_name_and_id(self, name_list:list[tuple], id_list:list[tuple]) -> None:
        for (ip, name), (_, id) in zip(name_list, id_list):
            if 'ERROR' in name or 'ERROR' in id:
                self._remove_host(ip, name)
                continue
            oid:str                         = OID_Manager.get_enterprise_id(id) 
            self._hosts[ip]['oid']          = oid
            self._hosts[ip]['manufacturer'] = name.strip()

    

    def _remove_host(self, ip:str, error:str)-> None:
        removed_host:dict                = self._hosts.pop(ip)
        self._removed_hosts[ip]          = removed_host
        self._removed_hosts[ip]['error'] = error



if __name__ == '__main__':
    with Main() as infraaudit:
        ...