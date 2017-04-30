import sys
import logging
import errno
import argparse
from time import sleep
from select import poll, POLLIN
import xwiimote


def checked(func):
    def checked_call(self, *args, **kwargs):
        ret = None

        try:
            ret = func(self, *args, **kwargs)
        except SystemError as e:
            print(e)
        except KeyboardInterrupt:
            pass

        return ret

    return checked_call


class Controller(object):
    key_map = {
        xwiimote.KEY_LEFT: '<',
        xwiimote.KEY_RIGHT: '>',
        xwiimote.KEY_UP: '^',
        xwiimote.KEY_DOWN: 'v',
        xwiimote.KEY_A: 'A',
        xwiimote.KEY_B: 'B',
        xwiimote.KEY_PLUS: '+',
        xwiimote.KEY_MINUS: '-',
        xwiimote.KEY_HOME: 'HOME',
        xwiimote.KEY_ONE: '1',
        xwiimote.KEY_TWO: '2'
    }

    def __init__(self, dev):
        self.dev = dev
        self.dev.open(self.dev.available() | xwiimote.IFACE_WRITABLE)

    @checked
    def get_battery_level(self):
        return self.dev.get_battery()

    @checked
    def rumble(self, msecs):
        self.dev.rumble(True)
        sleep(1 / 1000.0 * msecs)
        self.dev.rumble(False)

    @checked
    def read(self, logger):
        PRESSED = 1
        fd = self.dev.get_fd()

        p = poll()
        p.register(fd, POLLIN)
        evt = xwiimote.event()

        while True:
            p.poll()

            try:
                self.dev.dispatch(evt)
                code, state = evt.get_key()

                if evt.type == xwiimote.EVENT_KEY and state == PRESSED:
                    logger.debug(self.key_map.get(code))
                elif evt.type == xwiimote.EVENT_ACCEL:
                    x, y, z = evt.get_abs(0)
                    logger.debug("({x}, {y}, {z})".format(x=x, y=y, z=z))

            except IOError as e:
                if e.errno != errno.EAGAIN:
                    logger.error(e)


def init_logging(name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    return logger


def get_first_wiimote(logger):
    ent = None

    try:
        ent = xwiimote.monitor(True, True).poll()
    except SystemError as e:
        logger.error("Unable to init monitor: ", e)

    return ent


def get_iface(ent, logger):
    dev = None

    try:
        dev = xwiimote.iface(ent)
    except IOError as e:
        logger.error("Unable to create interface: ", e)

    return dev


def main():
    rumble_msecs = 500

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()

    logger = init_logging(sys.argv[0])
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.info("Searching for device")
    ent = get_first_wiimote(logger)
    if not ent:
        sys.exit(1)

    dev = get_iface(ent, logger)
    if not dev:
        sys.exit(1)

    logger.info("Initializing controller")
    c = Controller(dev=dev)

    logger.info("Controller ready (rumbling for {msecs} milliseconds)".format(msecs=rumble_msecs))
    c.rumble(rumble_msecs)

    battery = c.get_battery_level()
    logger.info("Battery at {lvl}%".format(lvl=battery))

    c.read(logger)


if __name__ == '__main__':
    main()
