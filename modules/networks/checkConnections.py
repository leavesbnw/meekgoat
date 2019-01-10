# -*- coding: UTF-8 -*-
from core.module import BaseModule
from collections import Counter
from prettytable import PrettyTable
import psutil


class Module(BaseModule):
    meta = {
            'name': 'CheckNetConnections',
            'author': 'BNW (bannianwei@comisys.net)',
            'version': 'v1.0.0',
            'description': '统计当前服务器的端口连接数'
    }

    def register_options(self):
        self.register_option(name='PORT',
                             value=62715,
                             required=True,
                             description='Get Port Connections')

    def module_run(self, args):
        stats = {}
        ports = set()
        netstat = psutil.net_connections()
        if isinstance(args.PORT, str) and args.PORT.lower() == 'null':
            self.perror("Please gave one or more port")
            return
        for p in args.PORT.split(','):
            if p.isdigit():
                ports.add(p)
            else:
                self.perror("Ports must be number")
                return
        # initialize dict
        for p in ports:
            if int(p)>=0 and int(p)<=65535:
                stats[p] = Counter()
            else:
                self.perror("%s is not a number" % p)
                return
        for i, sconn in enumerate(netstat):
            for p in ports:
               if int(p) == sconn.laddr.port:
                   if sconn.status == 'ESTABLISHED' and len(sconn.raddr) != 0:
                       stats[p][sconn.raddr.ip] += 1
        if stats:
            for p in stats:
                print('')
                self.draw(p, stats[p])
                print('')

    def draw(self, port, stats):
        count = 0
        if stats:
            tb = PrettyTable()
            tb.field_names = ['IP', 'COUNT']
            for s in stats:
                count += stats[s]
                tb.add_row([s, stats[s]])
            print(tb)
        print('Summary: port={} sum={}'.format(port, count))
