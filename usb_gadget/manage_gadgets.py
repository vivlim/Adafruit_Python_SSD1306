import os
import pathlib
from time import sleep


def create_gadget(name, gadget_def):
    usb_gadget_root = pathlib.Path("/sys/kernel/config/usb_gadget")
    gadget_path = usb_gadget_root / name
    try:
        gadget_path.rmdir()
    except FileNotFoundError:
        pass
    gadget_path.mkdir()
    for rel_path in gadget_def:
        target_file = gadget_path / rel_path
        target_dir = target_file.parent
        attempts = 5
        while not target_dir.is_dir() and attempts > 0:
            attempts = attempts - 1
            try:
                target_dir.mkdir(parents=True, exist_ok=True)  # make sure target_dir exists
            except (FileNotFoundError, FileExistsError):
                print("Failed to create directory {}. attempts left: {}".format(target_dir, attempts))
                sleep(2)
        data = gadget_def[rel_path]
        attempts = 5
        while not target_dir.is_dir() and attempts > 0:
            attempts = attempts - 1
            try:
                attempt_to_write(target_file, data)
            except (PermissionError, ValueError) as e:
                print("failed due to {}. attempts left: {}".format(e, attempts))
                sleep(2)
        print("{}: {}".format(rel_path, str(data)))

    for conf in (gadget_path / "configs").iterdir():
        for func in (gadget_path / "functions").iterdir():
            (conf / func.name).symlink_to(func)  # symlink all defined functions into config

    for udc_driver in pathlib.Path("/sys/class/udc").iterdir():
        (gadget_path / "UDC").write_text(udc_driver.name)


def attempt_to_write(target_file, data):
    if isinstance(data, bytes):
        target_file.write_bytes(data)
        os.system("fsync {}".format(target_file.absolute()))
        result = target_file.read_bytes()
        if result != target_file:
            raise ValueError("Written bytes were not the same when read")
    else:
        target_file.write_text(str(data))
        os.system("fsync {}".format(target_file.absolute()))
        result = target_file.read_text()
        if result != str(data):
            raise ValueError("Written data was not the same when read")
