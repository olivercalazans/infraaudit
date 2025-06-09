# MIT License
# Copyright (c) 2025 Oliver Calazans
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



    responses:list     = field(default_factory=list)
    _lock:Lock         = Lock()
    hosts:dict         = None
    information:set    = field(default_factory=set)
    removed_hosts:dict = field(default_factory=dict)



    def filter_devices(self, data:list[dict]) -> None:
        print('>> Filtering for specific devices')
        self.hosts = {
            device['host']: {'name': device['name']}
            for device in data if main_secrets.IPS in device['host']
        }


    
    async def add_response(self, response:tuple) -> None:
        async with self._lock:
            self.responses.append(response)



    def prune_offline_devices(self) -> None:
        len_all_hosts:int = len(self.hosts)
        for ip, error_indication, error_status, error_index, _ in self.responses:
            if error_indication or error_status or error_index:
                error:str              = str(error_indication or error_status or error_index)
                device:dict            = self.hosts.pop(ip)
                self.removed_hosts[ip] = {**device, 'error': error}
        self.responses.clear()
        print(f'    - Removed hosts: {len(self.removed_hosts)} ({len_all_hosts} -> {len_all_hosts - len(self.removed_hosts)})')


    
    def update_information(self) -> None:
        for  ip, error_indication, error_status, error_index, var_binds in self.responses:

            if error_indication or error_status or error_index:
                self.hosts[ip]['error'] = str(error_indication or error_status or error_index)
                continue

            values:list = [str(i[-1]).strip() for i in var_binds]
            manufacturer:str               = values.pop(0)
            info:tuple                     = tuple(values) 
            self.hosts[ip]['manufacturer'] = manufacturer
            self.hosts[ip]['info']         = info
            self.information.add(info)
        self.responses.clear()
