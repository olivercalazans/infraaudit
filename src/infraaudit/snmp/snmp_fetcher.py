# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import pysnmp


class SNMP_Fetcher:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance


    __slots__ = ('_sysObjectID', '_ip')

    def __init__(self):
        self._sysObjectID:str = '1.3.6.1.2.1.1.2.0'
        self._ip:str = None



    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return False