import os
import xml.etree.ElementTree as et
from Data import UserInfo


def check_file() -> None:
    if not os.path.exists('config.xml'):
        file = open('config.xml', 'a')
        file.close()
        init_xml()



# constructor:
# - Root
# -- Default attr=device_name
# -- List
# --- Device attr=name
# ---- local_host
# ---- local_name
# ---- remote_host
# ---- remote_name

def init_xml() -> None:
    root = et.Element('Data')
    default = et.SubElement(root, 'Default')
    default.set('device_name', '')
    et.SubElement(root, 'List')
    tree = et.ElementTree(root)
    tree.write('config.xml')


def add_data(device: str, local_host: str, local_name: str, remote_host: str, remote_name: str) -> None:
    tree = et.parse('config.xml')
    root = tree.getroot()
    for item in root.iter('List'):
        dev = et.SubElement(item, 'Device')
        dev.set('device_name', device)
        lh = et.SubElement(dev, 'Local_host')
        lh.text = local_host
        ln = et.SubElement(dev, 'Local_name')
        ln.text = local_name
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


def get_list() -> dict:
    tree = et.parse('config.xml')
    root = tree.getroot()
    re = {}
    for item in root.iter('List'):
        if len(list(item.iter())) == 0:
            return re
        else:
            for ite in root.iter('Device'):
                lh, ln, rh, rn = '', '', '', ''
                for attr in list(ite.iter()):
                    if attr.tag == "Device":
                        continue
                    elif attr.tag == "Local_host":
                        lh = attr.text
                    elif attr.tag == "Local_name":
                        ln = attr.text
                    elif attr.tag == "Remote_host":
                        rh = attr.text
                    elif attr.tag == "Remote_name":
                        rn = attr.text
                re[ite.attrib['device_name']] = UserInfo(
                    lh, ln, rh, rn
                )
            return re
