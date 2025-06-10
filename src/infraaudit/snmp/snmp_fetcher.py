# MIT License
# Copyright (c) 2025 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from asyncio                     import Lock
from pysnmp.hlapi.v3arch.asyncio import *
from models.data                 import Data
import _secrets.snmp_secrets as snmp_secrets


class SNMP_Fetcher:

    _instance:"SNMP_Fetcher" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ('_data', '_ENGINE', '_COMMUNITY', '_CONTEXT', '_lock')

    def __init__(self, data:Data):
        self._data:Data               = data
        self._ENGINE:SnmpEngine       = SnmpEngine()
        self._COMMUNITY:CommunityData = CommunityData(snmp_secrets.COMMUNITY)
        self._CONTEXT:ContextData     = ContextData()
        self._lock:Lock               = Lock()



    async def snmpget(self, ip:str, oids:str) -> None:
        result = await get_cmd(
            self._ENGINE,
            self._COMMUNITY,
            await UdpTransportTarget.create((ip, 161)),
            self._CONTEXT,
            *[ObjectType(ObjectIdentity(oid)) for oid in oids],
            lookupMib=False,
            lexicographicMode=False,
        )
        
        #error_indication, error_status, error_index, var_binds = result

        await self.add_response([ip, *result])

    

    async def add_response(self, response:list) -> None:
        async with self._lock:
            self._data.responses.append(response)



    def finish_engine(self) -> None:
        if self._ENGINE:
            self._ENGINE.transport_dispatcher.close_dispatcher()
            self._ENGINE = None




