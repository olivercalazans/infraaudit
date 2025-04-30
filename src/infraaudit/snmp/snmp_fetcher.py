# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from pysnmp.hlapi.v1arch    import get_cmd, CommunityData
from pysnmp.hlapi.transport import SnmpEngine
from pysnmp.hlapi.v3arch    import UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
import secrets.snmp_secrets as snmp_secrets


class SNMP_Fetcher:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object().__new__(cls)
        return cls._instance



    __slots__ = ('_sysObjectID', '_ip')

    def __init__(self):
        self._sysObjectID:str = '1.3.6.1.2.1.1.2.0'
        self._ip:str          = None



    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return False
    


    @staticmethod
    def _get_info_by_snmpget(ip:str, oid:str) -> str:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            get_cmd(
                SnmpEngine(),
                CommunityData(snmp_secrets.COMMUNITY, mpModel=1),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
        )
        if errorIndication:
            print(f'Erro: {errorIndication}')
        elif errorStatus:
            print(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex)-1][0] or "?"}')
        else:
            for varBind in varBinds:
                print(f'{varBind[0]} = {varBind[1]}')



SNMP_Fetcher()._get_info_by_snmpget('192.168.207.108', '1.3.6.1.2.1.1.2.0')
