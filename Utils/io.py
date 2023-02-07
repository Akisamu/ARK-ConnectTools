import os
import time
import xml.etree.ElementTree as et
from Data import UserInfo

version = '0.0.2'


def check_file() -> None:
    if not os.path.exists('config.xml'):
        file = open('config.xml', 'a')
        file.close()
        init_xml()


# constructor:
# - Root
# -- Default attr=device_name
# -- List
# --- Device attr=device_name
# ---- remote_host
# ---- remote_name
# -- History
# --- Record attr=[device_name],host,user,command,time

def init_xml() -> None:
    root = et.Element('Data')
    ver = et.SubElement(root, 'Version')
    ver.text = version
    default = et.SubElement(root, 'Default')
    default.set('device_name', '')
    et.SubElement(root, 'List')
    et.SubElement(root, 'History')
    tree = et.ElementTree(root)
    tree.write('config.xml')


def add_data(device: str, remote_host: str, remote_name: str) -> None:
    tree = et.parse('config.xml')
    root = tree.getroot()
    for item in root.iter('List'):
        dev = et.SubElement(item, 'Device')
        dev.set('device_name', device)
        rh = et.SubElement(dev, 'Remote_host')
        rh.text = remote_host
        rn = et.SubElement(dev, 'Remote_name')
        rn.text = remote_name
    tree.write('config.xml')


def set_default(device: str) -> None:
    tree = et.parse('config.xml')
    root = tree.getroot()
    for item in root.iter('Default'):
        item.set('device_name', device)
    tree.write('config.xml')


def get_default() -> str:
    tree = et.parse('config.xml')
    root = tree.getroot()
    for item in root.iter('Default'):
        return item.attrib['device_name']


def get_list() -> dict:
    tree = et.parse('config.xml')
    root = tree.getroot()
    re = {}
    for item in root.iter('List'):
        if len(list(item.iter())) == 0:
            return re
        else:
            for ite in root.iter('Device'):
                rh, rn = '', ''
                for attr in list(ite.iter()):
                    if attr.tag == "Device":
                        continue
                    elif attr.tag == "Remote_host":
                        rh = attr.text
                    elif attr.tag == "Remote_name":
                        rn = attr.text
                re[ite.attrib['device_name']] = UserInfo(
                    rh, rn
                )
            return re


def del_data(name: str):
    tree = et.parse('config.xml')
    root = tree.getroot()
    for item in root.iter('Device'):
        if item.attrib['device_name'] == name:
            for li in root.iter('List'):
                print(item)
                li.remove(item)
    tree.write('config.xml')


def take_history(device: str, remote_host: str, remote_name: str, com: str) -> None:
    tree = et.parse('config.xml')
    root = tree.getroot()
    for item in root.iter('History'):
        red = et.SubElement(item, 'Record')
        red.set('name', device)
        red.set('host', remote_host)
        red.set('user', remote_name)
        red.set('command', com)
        red.set('time', str(time.asctime(time.localtime(time.time()))))
    tree.write('config.xml')


def delete_history() -> None:
    tree = et.parse('config.xml')
    root = tree.getroot()
    for hist in root.iter('History'):
        root.remove(hist)
    et.SubElement(root, 'History')
    tree.write('config.xml')


def get_history() -> list:
    tree = et.parse('config.xml')
    root = tree.getroot()
    re = []
    for item in root.iter('History'):
        if len(list(item.iter())) == 0:
            return re
        else:
            for ite in root.iter('Record'):
                re.append({
                    'name': ite.attrib['name'],
                    'host': ite.attrib['host'],
                    'user': ite.attrib['user'],
                    'command': ite.attrib['command'],
                    'time': ite.attrib['time'],
                })
            return re
