# MIT License
# Copyright (c) 2025 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import asyncio
from models.data       import Data
from snmp.snmp_fetcher import SNMP_Fetcher


class SNMP_Manager:

    _instance:"SNMP_Manager" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance
    


    ENTERPRISE:str      = '1.3.6.1.4.1'
    SYS_DESCRIPTION:str = '1.3.6.1.2.1.1.1.0'
    SYS_OBJECT_ID:str   = '1.3.6.1.2.1.1.2.0'
    
    # RUCKUS
    RUCKUS_FIRMWARE_VERSION:str = '1.3.6.1.4.1.25053.1.1.3.1.1.1.1.1.3.1'
    RUCKUS_AP_MODEL:str         = '1.3.6.1.4.1.25053.1.1.2.1.1.1.1.0'



    __slots__ = ('_data', '_loop', '_snmp_fetcher')

    def __init__(self, data):
        self._data:Data                      = data
        self._loop:asyncio.AbstractEventLoop = None
        self._snmp_fetcher:SNMP_Fetcher      = None

    

    def __enter__(self):
        self._start_async_loop_and_snmp_engines()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._snmp_fetcher.finish_engine()
        self._close_jobs()
        return False



    def _start_async_loop_and_snmp_engines(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._snmp_fetcher = SNMP_Fetcher(self._data)



    def _run_tasks(self, oids:list) -> list[tuple]:
        return self._loop.run_until_complete(self._fetch_all_snmp(oids))



    async def _fetch_all_snmp(self, oid:list) -> list[tuple]:
        tasks:list[asyncio.Task] = [self._snmp_fetcher.snmpget(ip, oid) for ip in self._data.hosts]
        return await asyncio.gather(*tasks)
    


    def _verify_which_devices_are_active(self) -> None:
        print('  # Verifying which devices are active')
        self._run_tasks([self.SYS_OBJECT_ID])
    


    def _get_ruckus_information(self) -> None:
        print('  # Collecting data from Ruckus APs')
        self._run_tasks([self.SYS_DESCRIPTION, self.RUCKUS_AP_MODEL, self.RUCKUS_FIRMWARE_VERSION])

    

    def _close_jobs(self) -> None:
        pending = asyncio.all_tasks(self._loop)
        if pending:
            try:
                self._loop.run_until_complete(
                    asyncio.wait_for(
                        asyncio.gather(*pending, return_exceptions=True), timeout=5
                    )
                )
            except:
                pass
        
        self._loop.close()
