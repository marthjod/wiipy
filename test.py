import sys
import time
import logging
import xwiimote


def init_logging(name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    return logger


def checked(func):
    def checked_call(self, *args, **kwargs):
        ret = None

        try:
            ret = func(self, *args, **kwargs)
        except SystemError as e:
            print(e)

        return ret

    return checked_call


class Controller(object):
    def __init__(self, dev):
        self.dev = dev
        self.dev.open(self.dev.available() | xwiimote.IFACE_WRITABLE)

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
    logger = init_logging(sys.argv[0])
    msecs = 500

    ent = get_first_wiimote()
    if not ent:
        sys.exit(1)

    dev = get_iface(ent)
    if not dev:
        sys.exit(1)

    logger.info("Initializing controller")
    c = Controller(dev=dev)

    logger.info("Rumbling for {msecs} millseconds".format(msecs=msecs))
    c.rumble(msecs)

    battery = c.get_battery_level()
    logger.info("Battery at {lvl}%".format(lvl=battery))


if __name__ == '__main__':
    main()
