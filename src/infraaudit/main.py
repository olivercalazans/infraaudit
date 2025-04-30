# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from zabbix.api_zabbix import API_ZABBIX
import secrets.secrets as secrets


class Main:
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance


    __slots__ = ('_hosts')

    def __init__(self):
        self._hosts:dict = None


    def __enter__(self):
        self._get_host_information_by_zabbix_api()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return False


    def _get_host_information_by_zabbix_api(self) -> list:
        with API_ZABBIX() as API:
            data:list[dict] = API._get_hosts_information()
            self._hosts     =  self._select_devices(data)



    @staticmethod
    def _select_devices(data:list[dict]) -> list:
        return {device['host']: {'id': device['hostid'], 'name':device['name']} for device in data if secrets.IPS in device['host']}

    


if __name__ == '__main__':
    with Main() as infraaudit:
        for i in infraaudit._hosts.items():
            print(i)