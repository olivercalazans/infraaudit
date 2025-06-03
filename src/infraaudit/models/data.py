# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from asyncio     import Lock
from dataclasses import dataclass
from _secrets    import main_secrets


@dataclass(slots=True)
class Data:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    _lock:Lock = Lock()
    hosts:dict = None



    def filter_devices(self, data:list[dict]) -> None:
        print('>> Filtering for specific devices')
        self.hosts = {
            device['host']: {'id': device['hostid'], 'name':device['name']}
            for device in data if main_secrets.IPS in device['host']
        }


    
    async def add_value(self, ip:str, key:str, value:str) -> None:
        async with self._lock:
            self.hosts[ip][key] = value.strip()