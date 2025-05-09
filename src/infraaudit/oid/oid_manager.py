# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


import os
from functools import lru_cache


class OID_Manager:

    FILE_PATH:str     = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'oid_enterprise_list.txt')
    ENTERPRISE:str    = '1.3.6.1.4.1'
    SYS_OBJECT_ID:str = '1.3.6.1.2.1.1.2.0'


    @staticmethod
    def get_enterprise_id(oid:str) -> str:
        return oid.split('.')[6]
    

    @staticmethod
    @lru_cache(maxsize=20)
    def get_enterprise_name_by_oid(oid:str) -> str:
        with open(OID_Manager.FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if oid in line:
                    return line.split('=')[-1]