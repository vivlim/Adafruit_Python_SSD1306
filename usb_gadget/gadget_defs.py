# refs
# https://events.static.linuxfound.org/sites/events/files/slides/USB%20Gadget%20Configfs%20API_0.pdf
# http://andrewnicolaou.co.uk/posts/2016/pi-zero-midi-3-two-things-at-once
# https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/

base = {
    'idVendor': 0x1d6b,  # Linux Foundation
    'idProduct': 0x0104,  # Multifunction Composite Gadget
    'bcdDevice': 0x0100,  # v1.0.0
    'bcdUSB': 0x0200,  # USB2
    'strings/0x409/serialnumber': "feedfacedeadbeef",
    'strings/0x409/manufacturer': "viviridian",
    'strings/0x409/product': "Composite Raspberry Pi USB device",
    'configs/c.1/strings/0x409/configuration': "Config 1: ECM network",
    'configs/c.1/MaxPower': 250
}

keyboard = {
    'functions/hid.usb0/protocol': 1,
    'functions/hid.usb0/subclass': 1,
    'functions/hid.usb0/report_length': 8
}
