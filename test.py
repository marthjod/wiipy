import os
import time
import xwiimote


def checked(func):
    def checked_call(self, *args, **kwargs):
        print("checked " + func.__name__)
        try:
            func(self, *args, **kwargs)
        except SystemError as e:
            print(e)

    return checked_call


class Controller(object):
    def __init__(self, dev):
        self.dev = dev
        self.dev.open(self.dev.available() | xwiimote.IFACE_WRITABLE)

    @staticmethod
    def action(func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except SystemError as e:
            print(e)

    @checked
    def get_battery_level(self):
        return self.dev.get_battery()

    @checked
    def rumble(self, msecs):
        self.dev.rumble(True)
        time.sleep(1 / 1000.0 * msecs)
        self.dev.rumble(False)


def get_first_wiimote():
    ent = None

    try:
        ent = xwiimote.monitor(True, True).poll()
    except SystemError as e:
        print("Unable to init monitor: ", e)

    return ent


def get_iface(ent):
    dev = None

    try:
        dev = xwiimote.iface(ent)
    except IOError as e:
        print("Unable to create interface: ", e)

    return dev


def main():
    ent = get_first_wiimote()
    if not ent:
        os._exit(1)

    dev = get_iface(ent)
    if not dev:
        os._exit(1)

    c = Controller(dev=dev)
    c.rumble(5000)


if __name__ == '__main__':
    main()
