# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import asyncio
import _secrets.main_secrets as main_secrets
from zabbix.api_zabbix import API_ZABBIX
from snmp.snmp_fetcher import SNMP_Fetcher
from oid.oid_manager   import OID_Manager


class Main:
    
    _instance:"Main" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance


    __slots__ = ('_hosts')

    def __init__(self):
        self._hosts:dict = {}


    def __enter__(self):
        self._get_host_information_by_zabbix_api()
        self._get_information_by_snmp()
        for i in self._hosts: print(i)
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return False


    def _get_host_information_by_zabbix_api(self) -> None:
        with API_ZABBIX() as API:
            data:list[dict] = API._get_hosts_information()
        self._select_devices(data)


    def _select_devices(self, data:list[dict]) -> None:
        self._hosts.update({
            device['host']: {'id': device['hostid'], 'name':device['name']}
            for device in data if main_secrets.IPS in device['host']
        })
    

    def _get_information_by_snmp(self) -> None:
        asyncio.run(self._fetch_all_snmp())


    async def _fetch_all_snmp(self) -> None:
        tasks:list[asyncio.Task] = [SNMP_Fetcher().snmpget(ip) for ip in self._hosts]
        results:list[tuple]      = await asyncio.gather(*tasks)
        self._add_oid_and_manufacturer(results)
        
    
    def _add_oid_and_manufacturer(self, results:list[tuple]) -> None:
        for ip, sys_obj_id in results:
            oid:str                         = OID_Manager.get_enterprise_id(sys_obj_id) 
            self._hosts[ip]['oid']          = oid
            self._hosts[ip]['manufacturer'] = OID_Manager.get_enterprise_name_by_oid(oid)


if __name__ == '__main__':
    with Main() as infraaudit:
        ...