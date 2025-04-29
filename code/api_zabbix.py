# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import requests
import _secrets


class API_ZABBIX():

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> list:
        return False    



    def _get_hosts_information(self) -> None:
        auth_token    = self._get_api_token()
        hosts_payload = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host", "name"],
                "selectInterfaces": ["ip"],
                "filter": {"status": 0}
            },
            "auth": auth_token,
            "id": 2
        }

        response = requests.post(_secrets.ZABBIX_URL, json=hosts_payload)
        response.raise_for_status()
        return response.json()["result"]


    
    def _get_api_token(self) -> None:
        auth_payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user":_secrets. USER,
                "password": _secrets.PASSWORD,
            },
            "id": 1
        }

        response = requests.post(_secrets.ZABBIX_URL, json=auth_payload)
        response.raise_for_status()
        return response.json()["result"]