import os

import Data
import sys
import argparse
from Utils import *
from Utils import io
from set import *

root_parser = argparse.ArgumentParser(add_help=False)
root_parser.description = 'It is a tool to connect your devices easily.'

# Setting brunch
set_parser = argparse.ArgumentParser(parents=[root_parser], add_help=False)
set_parser.add_argument('--setting', action='store_true', help='Set your basic information.')

# SSH brunch
ssh_parser = argparse.ArgumentParser(parents=[root_parser], add_help=False)
ssh_parser.description = "sample: msk --ssh [dev]|[target]"
ssh_parser.add_argument('--ssh', action='store_true', help='Connect the SSH Server.')
ssh_sub_parser = argparse.ArgumentParser(parents=[ssh_parser], add_help=False)
ssh_sub_parser.add_argument('-d', '--device', nargs='?', default='', dest='device', type=str,
                            help="The device's name you have stored in database.")
ssh_sub_parser.add_argument('-l', '--link', nargs='?', default='', dest='link', type=str,
                            help="Input the username@host:port")

# SCP brunch
scp_parser = argparse.ArgumentParser(parents=[root_parser], add_help=False)
scp_parser.description = "sample: msk --scp this [target] [path]"
scp_parser.add_argument('--scp', action='store_true', help="Transform the document by SCP")
scp_sub_parser = argparse.ArgumentParser(parents=[scp_parser], add_help=False)
scp_sub_parser.add_argument('-i', '--this', nargs='?', default='', dest='this', type=str,
                            help='The path of the document that you want to transfrom.')
scp_sub_parser.add_argument('-a', '--that', nargs='?', default='', dest='that', type=str,
                            help='The destination of the document (default=~/Downloads)')
scp_sub_parser.add_argument('-t', '--target', nargs='?', default='', dest='target', type=str,
                            help='Input the username@host:port')

# Documents brunch
hist_parser = argparse.ArgumentParser(parents=[root_parser], add_help=False)
hist_parser.add_argument('-H', '--history', action='store_true', help="List the connection history.")
hist_parser.add_argument('-L', '--list', action='store_true', help="List all connect.")

# show brunch
show_parser = argparse.ArgumentParser(parents=[set_parser, ssh_sub_parser, scp_sub_parser, hist_parser], add_help=False)
show_parser.description = 'sample: msk --scp this [that] [path]' + '\n' + \
                          '        msk --ssh [dev]|[target]'


def search_all() -> None:
    show_default_dev(io.get_default(), io.get_list())
    func_1(io.get_list())


def add_dev() -> None:
    dev = func_2()
    io.add_data(dev[0], dev[1], dev[2])


def remove_dev() -> None:
    name = func_3()
    io.del_data(name)


def change_default() -> None:
    name = fun_4()
    io.set_default(name)
    print('      ' + 'Change successful!')


def i_set(sel: str) -> None:
    # Delete the connected history.
    if sel == '4':
        print('      确定删除历史记录吗？')
        print('      MAKE SURE YOU ARE DELETING THE DATA')
        print('      本当にデータを消すことは決まりましたが？')
        tas = input('      Please input    YES/n       :   ')
        if tas == "YES":
            io.delete_history()
            print('------ Delete Successful.------ ')
        else:
            print('cancel')
            sys.exit()
    # Delete a device.
    elif sel == '3':
        se = str(input('      Please entry the device you want to delete: '))
        if se in dev_name_list:
            io.del_data(se)
            print('------ Delete Successful.------ ')
        else:
            print("      There's no such device.")
        show_setting()
        i_set(input())
    # Add a device.
    elif sel == '2':
        add_dev()
        print('      ' + 'Adding successful!')
        search_all()
        show_setting()
        i_set(input())
    # Change default device.
    elif sel == '1':
        change_default()
        show_setting()
        i_set(input())
    # Exit
    elif sel == '0':
        sys.exit()


if __name__ == '__main__':
    # initialize and check
    argvs = sys.argv[1:]
    io.check_file()
    dev_dict = io.get_list()
    dev_name_list = dev_dict.keys()
    # logic
    if len(argvs) == 0:
        show_parser.print_help()
    elif argvs[0] == '--setting':
        show_setting()
        select = str(input())
        i_set(select)
        # Show the device list.
    elif argvs[0] == '-L' or argvs[0] == '--list':
        search_all()
    elif argvs[0] == '-H' \
                     '' or argvs[0] == '--history':
        search_all_history(io.get_history())
    elif argvs[0] == '--ssh':
        arg = ssh_sub_parser.parse_args().__dict__
        if arg['link'] != '':
            info = arg['link'].split('@')
            if len(info) == 2:
                io.take_history('Temporary', info[1], info[0], 'ssh')
            else:
                io.take_history('Temporary', '? ? ?', '? ? ?', 'ssh')
            os.system('ssh ' + arg['link'])
        elif arg['device'] != '':
            d = arg['device']
            if d in dev_name_list:
                io.take_history(d, dev_dict[d].remote_host, dev_dict[d].remote_name, 'ssh')
                os.system('ssh ' + dev_dict[d].remote_name + "@" + dev_dict[d].remote_host)
            else:
                print('      Device is no exist, please check the setting.')
                search_all()
        else:
            d = io.get_default()
            if d in dev_name_list:
                io.take_history(d, dev_dict[d].remote_host, dev_dict[d].remote_name, 'ssh')
                os.system('ssh ' + dev_dict[d].remote_name + "@" + dev_dict[d].remote_host)
            else:
                show_default_dev(io.get_default(), io.get_list())
                print('      The default setting is error.')
    elif argvs[0] == '--scp':
        arg = scp_sub_parser.parse_args().__dict__
        i = arg['this'] + ' '
        com = 'scp -r '
        def_that = '~/Documents'
        if arg['target'] != '':
            tar = arg['target']
            info = arg['target'].split('@')
            if arg['that'] != '':
                if arg['target'] in dev_name_list:
                    io.take_history(arg['target'], dev_dict[arg['target']].remote_host,
                                    dev_dict[arg['target']].remote_name, 'scp')
                    com = com + i + dev_dict[arg['target']].remote_name + '@' + dev_dict[
                        arg['target']].remote_host + ":" + arg['that']
                elif len(info) == 2:
                    io.take_history('Temporary', info[1], info[0], 'scp')
                    com = com + i + arg['target'] + ":" + arg['that']
                else:
                    io.take_history('Temporary', '? ? ?', '? ? ?', 'scp')
                    com = com + i + arg['target'] + ":" + arg['that']
            else:
                if arg['target'] in dev_name_list:
                    io.take_history(arg['target'], dev_dict[arg['target']].remote_host,
                                    dev_dict[arg['target']].remote_name, 'scp')
                    com = com + i + dev_dict[arg['target']].remote_name + '@' + dev_dict[
                        arg['target']].remote_host + ":" + def_that
                elif len(info) == 2:
                    io.take_history('Temporary', info[1], info[0], 'scp')
                    com = com + i + arg['target'] + ":" + def_that
                else:
                    io.take_history('Temporary', '? ? ?', '? ? ?', 'scp')
                    com = com + i + arg['target'] + ":" + def_that
        else:
            d = io.get_default()
            if d in dev_name_list:
                if arg['that'] != '':
                    io.take_history(d, dev_dict[d].remote_host, dev_dict[d].remote_name, 'scp')
                    com = com + i + dev_dict[d].remote_name + '@' + dev_dict[d].remote_host + ":" + arg['that']
                else:
                    io.take_history(d, dev_dict[d].remote_host, dev_dict[d].remote_name, 'scp')
                    com = com + i + dev_dict[d].remote_name + '@' + dev_dict[d].remote_host + ":" + def_that
        print(com)
        os.system(com)
    elif argvs[0] == '-v' or argvs[0] == '--version':
        print('      ' + 'This version is: ' + io.version)
    else:
        show_parser.print_help()
    pass
