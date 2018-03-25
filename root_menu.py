import subprocess
import socket
import os

from vertical_list_view import VerticalListView


class RootMenu(VerticalListView):
    def __init__(self, size):
        items = [
                {"label": "Hello world!"},
                {"label": "Throw exception",
                 "action": self.menu_throw},
                {"label": "Poweroff",
                 "action": self.menu_do_poweroff},
                {"label": "IP Address: {ip}",
                 "format_values": self.menu_get_ip}
                ]
        super().__init__(items, size)

    def menu_do_poweroff(self):
        os.system("shutdown -h now")

    def menu_throw(self):
        raise NotImplementedError("awoo")

    def menu_get_ip(self):
        # IP retrieval from https://stackoverflow.com/a/1267524
        IP = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
        return {'ip': IP}


