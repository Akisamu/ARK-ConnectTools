from prettytable import PrettyTable

sp = '      '


def func_1(li: dict) -> None:
    key_list = list(list(li.keys()))
    table = PrettyTable(['Devices', 'Users', 'host:[port]'])
    for item in key_list:
        table.add_row([str(item), li[str(item)].remote_name, li[str(item)].remote_host])
    print(table)
    return
    pass


def func_2() -> list:
    dev = [input(sp + "Please entry the device's name: "),
           input(sp + "Please entry the device's host & port: "),
           input(sp + "Please entry the user's name: ")]
    return dev


def func_3() -> str:
    return input(sp + "Please entry the device's name: ")


def fun_4() -> str:
    return input(sp + "Please entry the device's name: ")


# 什么b写法

def show_default_dev(name: str, dev: dict) -> None:
    key_list = dev.keys()
    if name in key_list:
        d = dev[name]
        table = PrettyTable(['Devices', 'Users', 'host:[port]'])
        table.title = 'The default device'
        table.add_row([name, d.remote_name, d.remote_host])
        print(table)


def search_all_history(li: list) -> None:
    table = PrettyTable(['Devices', 'host:[port]', 'User', 'Command', 'Time'])
    if len(li) != 0:
        for item in li:
            table.add_row([
                item['name'],
                item['host'],
                item['user'],
                item['command'],
                item['time']
            ])
        table.title = 'The records fo history login'
        print(table)


def show_setting() -> None:
    print(sp + "Please select what you want.")
    print(sp + '1.  Change default device.')
    print(sp + '2.  Add a device.')
    print(sp + '3.  Delete a device.')
    print(sp + '4.  Delete the connected history.')
    print(sp + '0.  Exit')
    return



