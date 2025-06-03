# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import _secrets.snmp_secrets as snmp_secrets
from models.data import Data


class SNMP_Fetcher:

    _instance:"SNMP_Fetcher" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    ENGINE:SnmpEngine       = SnmpEngine()
    COMMUNITY:CommunityData = CommunityData(snmp_secrets.COMMUNITY)
    CONTEXT:ContextData     = ContextData()



    __slots__ = ('_data')

    def __init__(self, data:Data):
        self._data:Data = data

    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finish_engine()
        return False



    async def snmpget(self, ip:str, oid:str, key:str) -> None:
        result = await get_cmd(
            self.ENGINE,
            self.COMMUNITY,
            await UdpTransportTarget.create((ip, 161)),
            self.CONTEXT,
            ObjectType(ObjectIdentity(oid)),
            lookupMib=False,
            lexicographicMode=False,
        )
        
        error_indication, error_status, error_index, var_binds = result

        value = str(error_indication or error_status or var_binds[-1][-1])
        await self._data.add_value(ip, key, value)



    @classmethod
    def finish_engine(cls) -> None:
        if cls.ENGINE:
            cls.ENGINE.transport_dispatcher.close_dispatcher()
            cls.ENGINE = None




