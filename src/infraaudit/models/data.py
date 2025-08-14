# MIT License
# Copyright (c) 2025 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from dataclasses import dataclass, field
from _secrets.secrets import Secret_Data


@dataclass(slots=True)
class Data:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    responses:list     = field(default_factory=list)
    hosts:dict         = field(default_factory=dict)
    removed_hosts:dict = field(default_factory=dict)
    information:set    = field(default_factory=lambda: {i:set() for i in Secret_Data.get_ip_prefixes()})



    def filter_devices(self) -> None:
        print('>> Filtering for specific devices')
        for device in self.responses:
            ip:str = device['interfaces'][0]['ip']
            
            if self._get_ip_prefix(ip) in Secret_Data.get_ip_prefixes():
                self.hosts[ip] = {'name': device['name']}

        self.responses.clear()

    

    @staticmethod
    def _get_ip_prefix(ip:str) -> str:
        return '.'.join(ip.split('.')[:3]) + '.'



    def prune_offline_devices(self) -> None:
        len_all_hosts:int = len(self.hosts)
        for result in self.responses:
            if not result[-1]:
                self._add_offline_device_to_the_list(result[:-1])
        
        self._display_removed_devices(len(self.removed_hosts), len_all_hosts)
        self.responses.clear()

    

    def _add_offline_device_to_the_list(self, result:list) -> None:
        ip, error_indication, error_status, error_index = result
        error:str              = str(error_indication or error_status or error_index)
        device:dict            = self.hosts.pop(ip)
        self.removed_hosts[ip] = {**device, 'error': error}
    


    @staticmethod
    def _display_removed_devices(removed_hosts:int, all_hosts:int) -> None:
        result:int = all_hosts - removed_hosts
        print(f'>> Active hosts: {result}/{all_hosts}')



    def update_information(self) -> None:
        for  ip, error_indication, error_status, error_index, var_binds in self.responses:

            if error_indication or error_status or error_index:
                self.hosts[ip]['error'] = str(error_indication or error_status or error_index)
                continue
    
            self._update_device_information(ip, var_binds)
        self.responses.clear()
    


    def _update_device_information(self, ip:str, var_binds:object) -> None:
        values:list                    = [str(i[-1]).strip() for i in var_binds]
        manufacturer:str               = values.pop(0)
        info:tuple                     = tuple(values)
        self.hosts[ip]['manufacturer'] = manufacturer
        self.hosts[ip]['info']         = info
        prefix:str                     = self._get_ip_prefix(ip)
        self.information[prefix].add(info)