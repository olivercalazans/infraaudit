# MIT License
# Copyright (c) 2024 Oliver Calazans
# Repository: https://github.com/olivercalazans/infraaudit
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software...


from api_zabbix import API_ZABBIX


class Main:

    __slots__ = ('_hosts')

    def __init__(self):
        self._hosts = self._get_host_information_by_zabbix_api()


    @staticmethod
    def _get_host_information_by_zabbix_api() -> dict:
        with API_ZABBIX() as API:
            return API.hosts
