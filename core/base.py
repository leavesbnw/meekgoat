#!/usr/bin/env python
# coding=utf-8

import cmd2
from core.framework import Framework
from argparse import ArgumentParser
try:
    from cmd2.cmd2 import with_argparser
except ImportError:
    from cmd2 import with_argparser


class Base(Framework, object):
    def __init__(self):
        super(Base, self).__init__()
        self._delete_or_hide_builtin_function()

    show_parser = ArgumentParser(usage='%(prog)s <command>')
    subshow_parser = show_parser.add_subparsers(title='command options',
                                                dest='subcmd',
                                                metavar='<command>')
    subshow_parser.add_parser('modules', help="show all modules")
    subshow_parser.add_parser('groups', help="show group information")
    subshow_parser.add_parser('info', help="show seleted module information")
    subshow_parser.add_parser('options', help="show current module options")

    @with_argparser(show_parser)
    def do_show(self, args):
        """ Show module informations """
        modules = self._loaded_modules
        if not args.subcmd:
            print('Usage: show <command>')
            return
        elif args.subcmd == 'modules':
            func = getattr(self, 'show_' + args.subcmd)
            func(modules)
        elif args.subcmd == 'groups':
            func = getattr(self, 'show_' + args.subcmd)
            func()
        elif args.subcmd == 'info':
            func = getattr(self, 'show_' + args.subcmd)
            func()
        elif args.subcmd == 'options':
            func = getattr(self, 'show_' + args.subcmd)
            func()
        else:
            print('no method help_show')

    search_parser = ArgumentParser()
    search_parser.add_argument('modname',
                               metavar='module_name',
                               help='the name of module you want to search')

    @with_argparser(search_parser)
    def do_search(self, args):
        """ Search module """
        modname = args.modname
        modules = self._loaded_modules
        selection = {}
        for x in modules:
            if modname.lower() in x.lower():
                selection[x] = modules[x]
        if selection:
            self.show_modules(selection)
        else:
            self.perror("Sorry, no module named '%s'" % modname)
        return

    # ===============================================
    # show methods
    # ===============================================

    def show_modules(self, args):
        modules = args
        # display modules
        print('')
        mxlen = max([len(item) for item in modules])
        print('{}{}{}'.format(' '*2, 'name'.ljust(mxlen + 5), 'description'))
        print('{}{}{}'.format(' '*2, '----'.ljust(mxlen + 5), '-'*11))
        for module in sorted(modules):
            mod_dsp = modules[module].meta['description']
            print('{}{}{}'.format(' '*2, module.ljust(mxlen + 5), mod_dsp))
        print('')

    def show_info(self):
        modname = self._current
        if not modname:
            self.perror("Please load  module before you use this subcommand!!")
            return
        try:
            modname.show_info()
        except AttributeError as e:
            self.perror("%s" % e.message)

    def show_options(self):
        modname = self._current
        if not modname:
            self.perror("Please load  module before you use this subcommand!!")
            return
        try:
            modname.show_options()
        except AttributeError as e:
            self.perror("%s" % e.message)

    # =================================================
    # protected methods
    # =================================================
    def _delete_or_hide_builtin_function(self):
        """ delete or hide built-in functions """
        # To remove built-in commands entirely,
        # delete their "do_*" function from the cmd2.Cmd class
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_alias
        try:
            do_macro = getattr(cmd2.Cmd, "do_macro")
            del cmd2.Cmd.do_macro
        except AttributeError:
            pass
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_pyscript
        del cmd2.Cmd.do_load
        try:
            do_unalias = getattr(cmd2.Cmd, "do_unalias")
            del cmd2.Cmd.do_unalias
        except AttributeError:
            pass

        # To hide commands from displaying in the help menu,
        # add them to the hidden_commands list
        self.hidden_commands.append('shortcuts')

    def do_mytest(self, args):
        pass

    def complete_mytest(self, *args):
        text, line, begidx, endidx = args
        modules = self._loaded_modules.keys()
        return [match for match in modules if match.startswith(text)]
