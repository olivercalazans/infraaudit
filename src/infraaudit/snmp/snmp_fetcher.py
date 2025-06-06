# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from pysnmp.hlapi.v3arch.asyncio import *
import _secrets.snmp_secrets as snmp_secrets
from models.data import Data


class SNMP_Fetcher:

    _instance:"SNMP_Fetcher" = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ('_data', '_ENGINE', '_COMMUNITY', '_CONTEXT')

    def __init__(self, data:Data):
        self._data:Data               = data
        self._ENGINE:SnmpEngine       = SnmpEngine()
        self._COMMUNITY:CommunityData = CommunityData(snmp_secrets.COMMUNITY)
        self._CONTEXT:ContextData     = ContextData()

    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._finish_engine()
        return False



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
        
        error_indication, error_status, error_index, var_binds = result

        if error_indication or error_index:
            error = error_indication or error_index
            await self._data.remove_host(ip, error)
            return

        value = [str(i[-1]).strip() for i in var_binds]
        await self._data.add_value(ip, value)



    def _finish_engine(self) -> None:
        if self._ENGINE:
            self._ENGINE.transport_dispatcher.close_dispatcher()
            self._ENGINE = None




