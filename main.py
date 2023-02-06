import Data
import sys
import argparse
from prettytable import PrettyTable
from Utils import *
from Utils import io

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
ssh_sub_parser.add_argument('-dev', nargs='?', default='', type=str, help="The device's name you have stored in database.")
ssh_sub_parser.add_argument('-target', nargs='?', default='', type=str, help="Input the username@host:port")

# SCP brunch
scp_parser = argparse.ArgumentParser(parents=[root_parser], add_help=False)
scp_parser.description = "sample: msk --scp this [target] [path]"
scp_parser.add_argument('--scp', action='store_true', help="Transform the document by SCP")
scp_sub_parser = argparse.ArgumentParser(parents=[scp_parser], add_help=False)
scp_sub_parser.add_argument('-this', nargs='?', default='', type=str, help='The path of the document that you want to transfrom.')
scp_sub_parser.add_argument('-that', nargs='?', default='', type=str, help='Input the username@host:port')
scp_sub_parser.add_argument('-path', nargs='?', default='', type=str, help='The destination of the document (default=~/Downloads)')

# show brunch
show_parser = argparse.ArgumentParser(parents=[set_parser, ssh_sub_parser, scp_sub_parser], add_help=False)
show_parser.description = 'sample: msk --scp this [that] [path]' + '\n' +\
                          '        msk --ssh [dev]|[target]'


def search_all() -> None:
    li = io.get_list()
    key_list = list(list(li.keys()))
    table = PrettyTable(['设备名称', '用户名', 'host'])
    for item in key_list:
        table.add_row([str(item), li[str(item)].remote_name, li[str(item)].remote_host])
    print(table)


if __name__ == '__main__':
    search_all()



    pass
    # if len(sys.argv[1:]) == 0:
    #     show_parser.print_help()
    # elif set_parser.parse_args().__dict__['setting']:
    #     pass
    # elif ssh_sub_parser.parse_args().__dict__['ssh']:
    #     pass
    # elif scp_sub_parser.parse_args().__dict__['scp']:
    #     pass
    # else:
    #     show_parser.print_help()



