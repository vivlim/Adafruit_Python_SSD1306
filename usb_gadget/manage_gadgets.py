import os
import shutil
import pathlib
from time import sleep


def create_gadget(name, gadget_def):
    usb_gadget_root = pathlib.Path("/sys/kernel/config/usb_gadget")
    #usb_gadget_root = pathlib.Path("/tmp/usb_gadget")
    gadget_path = usb_gadget_root / name

    #TODO: consider whether I actually want this
#    try:
# need recursive rmdir. shutil won't cut it with pathlib
#        shutil.rmtree(gadget_path)
#    except FileNotFoundError:
#        pass
    gadget_path.mkdir(exist_ok=True)
    for rel_path, target_value in gadget_def:
        target_file = gadget_path / rel_path
        target_dir = target_file.parent

        # create path
        attempts = 5
        while not target_dir.is_dir() and attempts > 0:
            attempts = attempts - 1
            try:
                target_dir.mkdir(parents=True, exist_ok=True)  # make sure target_dir exists
            except (FileNotFoundError, FileExistsError):
                print("Failed to create directory {}. attempts left: {}".format(target_dir, attempts))
                sleep(2)

        # write the value
        print("{}: {}".format(rel_path, str(target_value)))
        attempts = 5
        while attempts > 0:
            attempts = attempts - 1
            try:
                attempt_to_write(target_file, target_value)
            except (PermissionError, ValueError) as e:
                print("failed due to {}. attempts left: {}".format(e, attempts))
                sleep(2)

    for conf in (gadget_path / "configs").iterdir():
        for func in (gadget_path / "functions").iterdir():
            (conf / func.name).symlink_to(func)  # symlink all defined functions into config

    for udc_driver in pathlib.Path("/sys/class/udc").iterdir():
        (gadget_path / "UDC").write_text(udc_driver.name)


def attempt_to_write(target_file, data):
    if isinstance(data, bytes):
        target_file.write_bytes(data)
        result = target_file.read_bytes()
        if result != data:
            raise ValueError("Written bytes were not the same when read ({})".format(result))
    else:
        target_file.write_text(str(data))
        result = target_file.read_text().rstrip()
        if result != str(data):
            raise ValueError("Written data was not the same when read ({})".format(result))
