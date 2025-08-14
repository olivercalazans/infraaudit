# MIT License
# Copyright (c) 2025 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...

import getpass
import requests
import sys
from _secrets.secrets import Secret_Data
from models.data      import Data


class API_ZABBIX():

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ('_data', '_token')

    def __init__(self, data:Data):
        self._data:Data = data
        self._token:str = None



    def __enter__(self):
        self._get_hosts_information()
        self._data.filter_devices()
        return self
    

    
    def __exit__(self, exc_type, exc_value, traceback) -> list:
        return False    



    def _get_hosts_information(self) -> None:
        data_received:bool = False
        while data_received is False:
            try:
                self._get_api_token()
                self._get_information_from_zabbix()
            except Exception as e:
                print(f'[ERROR]: {e}')
                sys.exit()
            else:
                data_received = True



    def _get_api_token(self) -> None:
        auth_payload:dict = self._get_token_request_payload()
        
        response = requests.post(Secret_Data.ZABBIX_URL, json=auth_payload)
        response.raise_for_status()
        response = response.json()

        if 'error' in response:
            raise Exception(response['error']['data'])

        self._token = response["result"]



    @staticmethod
    def _get_token_request_payload() -> dict:
        password:str = getpass.getpass()
        return {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user":Secret_Data.USER,
                "password": password,
            },
            "id": 1
        }



    def _get_information_from_zabbix(self) -> None:
        print('>> Retrieving data from Zabbix API')
        hosts_payload:dict = self._get_hosts_information_resquest_payload()
        
        response = requests.post(Secret_Data.ZABBIX_URL, json=hosts_payload)
        response.raise_for_status()
        response = response.json()

        self._data.responses = response['result']
    


    def _get_hosts_information_resquest_payload(self) -> dict:
        return {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host", "name"],
                "selectInterfaces": ["ip"],
                "filter": {"status": 0}
            },
            "auth": self._token,
            "id": 2
        }