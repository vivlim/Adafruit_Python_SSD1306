# refs
# https://events.static.linuxfound.org/sites/events/files/slides/USB%20Gadget%20Configfs%20API_0.pdf
# http://andrewnicolaou.co.uk/posts/2016/pi-zero-midi-3-two-things-at-once
# https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/

base = [
    ('idVendor', "0x1d6b"),  # Linux Foundation
    ('idProduct', "0x0104"),  # Multifunction Composite Gadget
    ('bcdDevice', "0x0100"),  # v1.0.0
    ('bcdUSB', "0x0200"),  # USB2
    ('bCountryCode', "8"),  # todo: is this ok?
    ('strings/0x409/serialnumber', "feedfacedeadbeef"),
    ('strings/0x409/manufacturer', "viviridian"),
    ('strings/0x409/product', "Composite Raspberry Pi USB device"),
    ('configs/c.1/strings/0x409/configuration', "Config 1: Very Good"),
    ('configs/c.1/MaxPower', "250")
]

keyboard = [
    ('functions/hid.usb0/protocol', "1"),
    ('functions/hid.usb0/subclass', "1"),
    ('functions/hid.usb0/report_length', "8"),
    ('functions/hid.usb0/report_desc', b"\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x03\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0")
]


# why in bcdUSB am I getting
#root@raspberrypi:/sys/kernel/config/usb_gadget/viv6# cat bcdDevice
#0x0409

#instead of bcdUSB 0x0200
