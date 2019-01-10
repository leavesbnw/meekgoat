#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
import textwrap
from argparse import Namespace
from core.framework import Option
try:
    from collections import UserList
except ImportError:
    from UserList import UserList


class BaseModule(object):
    def __init__(self):
        super(BaseModule, self).__init__()
        self.options = UserList()
        self.register_options()

    def show_info(self):
        # current = Framework._current
        try:
            # output a empty line for beauty
            print('')
            for item in ['name', 'path', 'author', 'version']:
                val = self.meta.get(item)
                if val:
                    print('%s: %s' % (item.title().rjust(10), val))
            # description
            print('')
            if 'description' in self.meta:
                desc = self.meta['description']
                print('Description:')
                print('%s%s' % (' '*2, textwrap.fill(desc, 80)))
                print('')
            # options
            print('Options:')
            self.show_options()
        except Exception as e:
            self.perror('%s' % e)
        return

    def show_options(self):
        """ List options """
        options = self.options
        print('')
        if options:
            v_mxlen = max([len(i['value'])
                           if i['value'] and len(i['value']) > 13
                           else 13 for i in options])
            n_mxlen = max([len(i['name'])
                           if len(i['name']) > 4
                           else 4 for i in options])
            pattern = '  {} {} {} {}'
            print(pattern.format('Name'.ljust(n_mxlen),
                                 'Current Value'.ljust(v_mxlen),
                                 'Required'.ljust(8),
                                 'Description'))
            print(pattern.format('-'*n_mxlen, '-'*v_mxlen, '-'*8, '-'*11))
            for item in options:
                key = item['name']
                val = item['value'] or 'NULL'
                rqd = 'YES' if item['required'] else 'NO'
                desc = item['description']
                print(pattern.format(key.ljust(n_mxlen),
                                     val.ljust(v_mxlen),
                                     rqd.ljust(8),
                                     desc))
        else:
            print("  No options found!")
        print('')

    def module_pre(self):
        pass

    def module_run(self, args):
        pass

    def module_post(self):
        pass

    def register_options(self):
        pass

    def register_option(self, name, value=None,
                        required=False, description=''):
        if not value:
            value = 'NULL'
        if isinstance(value, int):
            value = str(value)
        option = Option(name=name,
                        value=value,
                        required=required,
                        description=description)
        self.options.append(option)

    def set_option(self, args):
        k = args.key
        v = args.value or 'NULL'
        keys = [x['name'] for x in self.options]
        if args.key not in keys:
            print("The Key is not correct.Please use a correct key")
            return
        for item in self.options:
            if item['name'] == k:
                item['value'] = v

    def run(self):
        """ Run the module """
        namespace = Namespace()
        for item in self.options:
            setattr(namespace, item['name'], item['value'])
        self.module_pre()
        self.module_run(namespace)
        self.module_post()
