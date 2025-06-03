# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...



class OID_Manager:

    ENTERPRISE:str       = '1.3.6.1.4.1'
    SYS_DESCRIPTION:str  = '1.3.6.1.2.1.1.1.0'
    SYS_OBJECT_ID:str    = '1.3.6.1.2.1.1.2.0'
    FIRMWARE_VERSION:str = '1.3.6.1.4.1.25053.1.1.3.1.1.1.1.1.3.1'


    @staticmethod
    def get_enterprise_id(oid:str) -> str:
        return oid.split('.')[6]
    