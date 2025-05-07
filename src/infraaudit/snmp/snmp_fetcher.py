# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from pysnmp.hlapi.v3arch     import *
import _secrets.snmp_secrets as snmp_secrets


class SNMP_Fetcher:

    ENGINE:SnmpEngine       = SnmpEngine()
    COMMUNITY:CommunityData = CommunityData(snmp_secrets.COMMUNITY)
    CONTEXT:ContextData     = ContextData()
    _sysObjectID:str        = '1.3.6.1.2.1.1.2.0'


    @classmethod
    async def _snmpget(cls, ip: str) -> str:
        result = await get_cmd(
            cls.ENGINE,
            cls.COMMUNITY,
            await UdpTransportTarget.create((ip, 161)),
            cls.CONTEXT,
            ObjectType(ObjectIdentity(cls._sysObjectID)),
            lookupMib=False,
            lexicographicMode=False,
        )
        
        errorIndication, errorStatus, errorIndex, varBinds = result
        
        if errorIndication:
            print(f'Erro: {errorIndication}')
        elif errorStatus:
            print(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex)-1][0] or "?"}')
        else:
            for varBind in varBinds:
                print(f'{varBind[0]} = {varBind[1]}')
