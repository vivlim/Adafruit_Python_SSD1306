import subprocess
import socket
import os
import sys

from command_output_view import CommandOutputView

from vertical_list_view import VerticalListView
from usb_gadget import manage_gadgets, gadget_defs


class RootMenu(VerticalListView):
    def __init__(self):
        items = [
                {"label": "gadget test",
                 "action": self.menu_gadget_test},
                {"label": "dmesg",
                 "action": self.menu_dmesg},
                {"label": "Throw exception",
                 "action": self.menu_throw},
                {"label": "Poweroff",
                 "action": self.menu_do_poweroff},
                {"label": "git status",
                 "action": self.menu_git_status},
                {"label": "git pull",
                 "action": self.menu_git_pull},
                {"label": "git reset --hard",
                 "action": self.menu_git_reset_hard},
                {"label": "reload",
                 "action": self.menu_reload},
                {"label": "IP Address: {ip}",
                 "format_values": self.menu_get_ip},
                {"label": "exit",
                 "action": self.menu_exit},
        ]
        super().__init__(items)

    def menu_do_poweroff(self):
        poweroff_menu = VerticalListView([
            {"label": "actually nah I'm good",
             "action": lambda: self.view_manager.remove_top_view()},
            {"label": "yes I really want to poweroff",
             "action": lambda: os.system("shutdown -h now")}
        ])
        self.view_manager.add_view(poweroff_menu)

    def menu_throw(self):
        raise NotImplementedError("awoo")

    def menu_gadget_test(self):
        gadget = gadget_defs.base + gadget_defs.keyboard
        manage_gadgets.create_gadget("viv2", gadget)

    def menu_dmesg(self):
        self.view_manager.add_view(CommandOutputView(["dmesg"]))

    def menu_git_status(self):
        self.view_manager.add_view(CommandOutputView(["git", "status"]))

    def menu_git_pull(self):
        self.view_manager.add_view(CommandOutputView(["git", "pull"]))

    def menu_git_reset_hard(self):
        reset_hard_menu = VerticalListView([
            {"label": "actually nah I'm good",
             "action": lambda: self.view_manager.remove_top_view()},
            {"label": "yes I really want to git reset --hard",
             "action": lambda: self.view_manager.add_view(CommandOutputView(["git", "reset", "--hard"]))}
        ])
        self.view_manager.add_view(reset_hard_menu)

    def menu_reload(self):
        os.execv(sys.executable, ["python3"] + sys.argv)

    def menu_exit(self):
        exit()

    def menu_get_ip(self):
        # IP retrieval from https://stackoverflow.com/a/1267524
        IP = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
        return {'ip': IP}


