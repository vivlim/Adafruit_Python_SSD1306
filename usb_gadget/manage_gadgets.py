import os
import pathlib
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
        target_dir.mkdir(parents=True, exist_ok=True)  # make sure target_dir exists
        target_file.write_text(str(gadget_def[rel_path]))
        print("{}: {}", rel_path, gadget_def[rel_path])

    for conf in (gadget_path / "configs").iterdir():
        for func in (gadget_path / "functions").iterdir():
            (conf / func.name).symlink_to(func)  # symlink all defined functions into config

    for udc_driver in pathlib.Path("/sys/class/udc").iterdir():
        (gadget_path / "UDC").write_text(udc_driver.name)


