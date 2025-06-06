# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from asyncio     import Lock
from dataclasses import dataclass, field
from _secrets    import main_secrets


@dataclass(slots=True)
class Data:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    _lock:Lock         = Lock()
    hosts:dict         = None
    information:dict   = field(default_factory=dict)
    removed_hosts:dict = field(default_factory=dict)



    def filter_devices(self, data:list[dict]) -> None:
        print('>> Filtering for specific devices')
        self.hosts = {
            device['host']: {'name': device['name']}
            for device in data if main_secrets.IPS in device['host']
        }


    
    async def add_value(self, ip:str, values:list) -> None:
        async with self._lock:
            manufacturer:str               = values.pop(0)
            info:tuple                     = tuple(values) 
            self.hosts[ip]['manufacturer'] = manufacturer
            self.hosts[ip]['info']         = info
            self.information[info]         = None


    
    async def remove_host(self, ip:str, error:str) -> None:
        async with self._lock:
            print(ip, error)
            device:dict            = self.hosts.pop(ip)
            self.removed_hosts[ip] = {**device, 'error': error}