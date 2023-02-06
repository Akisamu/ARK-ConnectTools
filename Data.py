

class UserInfo:

    def __init__(self, local_host='127.0.0.1', local_name='', remote_host='', remote_name=''):
        self.local_host = local_host
        self.local_name = local_name
        self.remote_host = remote_host
        self.remote_name = remote_name


# 'device_name': UserInfo
Device = {}


# ------------------------------ functions--------------------------------------------
def add_device(device_name: str, local_host: str, local_name: str, remote_host: str, remote_name: str) -> None:
    pass
    # Device.update({
    #     device_name: UserInfo(local_host, local_name, remote_host, remote_name)
    # })




