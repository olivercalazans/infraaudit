# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import _secrets.snmp_secrets as snmp_secrets


class SNMP_Fetcher:

    LOCK:asyncio.Lock       = asyncio.Lock()

    ENGINE:SnmpEngine       = SnmpEngine()
    COMMUNITY:CommunityData = CommunityData(snmp_secrets.COMMUNITY)
    CONTEXT:ContextData     = ContextData()


    @classmethod
    async def snmpget(cls, ip:str, oid:str) -> tuple[str, str]:
        result = await get_cmd(
            cls.ENGINE,
            cls.COMMUNITY,
            await UdpTransportTarget.create((ip, 161)),
            cls.CONTEXT,
            ObjectType(ObjectIdentity(oid)),
            lookupMib=False,
            lexicographicMode=False,
        )
        
        error_indication, error_status, error_index, var_binds = result
        
        data = str(error_indication or error_status or var_binds[-1][-1])
    


    @classmethod
    def finish_engine(cls) -> None:
        if cls.ENGINE:
            cls.ENGINE.transport_dispatcher.close_dispatcher()
            cls.ENGINE = None




