#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
from argparse import ArgumentParser
import cmd2
import sys
import imp
import os
import re
try:
    from cmd2.cmd2 import with_argparser, with_argument_list
except ImportError:
    from cmd2 import with_argparser, with_argument_list

try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict

try:
    from collections import UserList
except ImportError:
    from UserList import UserList


class Option(UserDict):
    pass

# ==================================
# FRAMEWORK CLASS
# ==================================


class Framework(cmd2.Cmd, object):
    """ Framework class. """

    # Should arguments passed on the command-line be processed as commands?
    allow_cli_args = False
    # Should output redirection and pipes be allowed
    allow_redirection = False
    # module_path = ''
    debug = True

    def __init__(self):

        # Set use_ipython to True to enable the "ipy" command
        # which embeds and interactive IPython shell
        super(Framework, self).__init__(use_ipython=False)
        self.doc_header = 'commands (type [help|?] <topic>)):'
        self._prompt = '(console)'
        self.continuation_prompt = ' > '
        self.prompt = self._prompt + self.continuation_prompt
        self._current = None  # An importent var
        self._loaded_modules = {}
        self.module_path = sys.path[0]
        self._load_modules()

    def do_run(self, args):
        """Run the module"""
        current_module = self._current
        if not current_module:
            self.perror('Please use the run command after use module!')
            return
        try:
            current_module.run()
        except AttributeError as e:
            self.perror("%s" % e.message)

    def do_show(self, args):
        """Show module information"""
        pass

    load_parser = ArgumentParser()
    load_parser.add_argument('modname',
                             metavar='module_name',
                             help="the name of module")

    @with_argparser(load_parser)
    def do_use(self, args):
        """Load specific module"""
        modname = args.modname
        # find any modules that contain modname
        if modname not in self._loaded_modules:
            self.perror("Invalid module name!")
            return
        self._current = self._loaded_modules[modname]
        self.prompt = '%s[%s]%s' % (self._prompt,
                                    modname.split('/')[-1],
                                    self.continuation_prompt)

    set_parser = ArgumentParser()
    set_parser.add_argument('key', help='the name of module options')
    set_parser.add_argument('value', help='the value of module options')

    @with_argparser(set_parser)
    def do_set(self, args):
        """ Set module options """
        modname = self._current
        if not modname:
            self.perror("Please load  module before you use this command!!")
            return
        try:
            modname.set_option(args)
        except AttributeError as e:
            self.perror("%s" % e.message)

    def perror(self, err):
        """
        Print error message to sys.stderr and if debug is true
        :param err: an Exception or error message to print out
        """
        super(Framework, self).perror(err, traceback_war=False)

    # ================================================
    # tab completion methods
    # ================================================
    def complete_use(self, *args):
        text, line, begidx, endidx = args
        modules = self._loaded_modules.keys()
        return [match for match in modules if match.startswith(text)]

    def _load_modules(self):
        # crawl the module directory and build the module tree
        path = os.path.join(self.module_path, 'modules')
        for dirpath, dirnames, filenames in os.walk(path):
            # remove hidden files and directories
            filenames = [f for f in filenames if not f[0] == '.']
            dirnames = [d for d in dirnames if not d[0] == '.']
            if len(filenames) > 0:
                for filename in [f for f in filenames if
                                 f.endswith('.py')]:
                    self._load_module(dirpath, filename)

    def _load_module(self, dirpath, filename):
        mod_name = filename.split('.')[0]
        mod_pname = '/'.join(re.split('modules/', dirpath)[-1].split('/') +
                             [mod_name])
        mod_lname = mod_pname.replace('/', '_')
        mod_loadpath = os.path.join(dirpath, filename)
        mod_file = open(mod_loadpath)
        try:
            # import the module into memory
            imp.load_source(mod_lname, mod_loadpath, mod_file)
            mod = __import__(mod_lname)
            # add the module to the framework's _loaded_modules
            self._loaded_modules[mod_pname] = mod.Module()
            return True
        except ImportError as e:
            self.perror('\'%s\' requires \'%s\'' % (mod_pname, e))
        except Exception as e:
            self.perror('Module \'%s\' disabled:\'%s\'' % (mod_pname, e))
        # remove the module from the framework's _loaded_modules
        self._loaded_modules.pop(mod_pname, None)
        mod_file.close()
        return False
