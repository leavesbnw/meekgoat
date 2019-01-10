# -*- coding: UTF-8 -*-
from core.module import BaseModule
import requests


class Module(BaseModule):
    meta = {
            'name': 'checknetip',
            'author': 'BNW (bannianwei@comisys.net)',
            'version': 'v1.0.0',
            'description': '获取IP信息，如果IP为空则获取出口IP的相关信息'
    }

    def register_options(self):
        self.register_option(name='IP',
                             value=None,
                             required=False,
                             description='Get IP information, if None return public IP')

    def module_run(self, args):
        ip = args.IP
        # user-agent must contain a 'curl' string
        headers = {
            'User-Agent': 'curl/7.60.0',
        }
        if ip is None:
            ip = ''
        elif isinstance(ip, str) and ip.lower() == 'null':
            ip = ''
        try:
            domain = 'http://www.cip.cc/'
            r = requests.get(domain + ip, headers=headers, timeout=2)
        except Exception as e:
            print(e)
            return
        print(r.text)
