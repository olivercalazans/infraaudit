# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from dataclasses     import dataclass, field
from _secrets        import main_secrets
from oid.oid_manager import OID_Manager


@dataclass(slots=True)
class Data:

    _instance:"Data" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance
    


    hosts:dict         = None
    removed_hosts:dict = field(default_factory=dict)



    def filter_devices(self, data:list[dict]) -> None:
        print('>> Filtering for specific devices')
        self.hosts = {
            device['host']: {'id': device['hostid'], 'name':device['name']}
            for device in data if main_secrets.IPS in device['host']
        }


    
    def add_manufacturer_name_and_id(self, name_list:list[tuple], id_list:list[tuple]) -> None:
        for (ip, name), (_, id) in zip(name_list, id_list):
            if 'ERROR' in name or 'ERROR' in id:
                self._remove_host(ip, name)
                continue
            oid:str                         = OID_Manager.get_enterprise_id(id)
            self.hosts[ip]['oid']          = oid
            self.hosts[ip]['manufacturer'] = name.strip()

    

    def _remove_host(self, ip:str, error:str)-> None:
        removed_host:dict                = self.hosts.pop(ip)
        self.removed_hosts[ip]          = removed_host
        self.removed_hosts[ip]['error'] = error