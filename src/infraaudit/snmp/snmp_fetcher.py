# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from pysnmp.hlapi.v3arch.asyncio import *
from oid.oid_manager             import OID_Manager
import _secrets.snmp_secrets as snmp_secrets


class SNMP_Fetcher:

    ENGINE:SnmpEngine       = SnmpEngine()
    COMMUNITY:CommunityData = CommunityData(snmp_secrets.COMMUNITY)
    CONTEXT:ContextData     = ContextData()


    @classmethod
    async def snmpget(cls, ip: str) -> tuple[str, str]:
        result = await get_cmd(
            cls.ENGINE,
            cls.COMMUNITY,
            await UdpTransportTarget.create((ip, 161)),
            cls.CONTEXT,
            ObjectType(ObjectIdentity(OID_Manager.SYS_OBJECT_ID)),
            lookupMib=False,
            lexicographicMode=False,
        )
        
        error_indication, error_status, error_index, var_binds = result
        
        if error_indication:
            return (ip, str(error_indication))
        
        if error_status:
            print(f'{error_status.prettyPrint()} at {ip} {error_index and var_binds[int(error_index)-1][0] or "?"}')
            return (ip, error_status)
        
        return (ip, str(var_binds[-1][-1]))