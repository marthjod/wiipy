import errno
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


class Device(object):
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
        pressed = 1
        fd = self.dev.get_fd()

        p = poll()
        p.register(fd, POLLIN)
        evt = xwiimote.event()

        while True:
            p.poll()

            try:
                self.dev.dispatch(evt)
                code, state = evt.get_key()

                if evt.type == xwiimote.EVENT_KEY and state == pressed:
                    logger.debug(self.key_map.get(code))
                elif evt.type == xwiimote.EVENT_ACCEL:
                    x, y, z = evt.get_abs(0)
                    logger.debug("({x}, {y}, {z})".format(x=x, y=y, z=z))

            except IOError as e:
                if e.errno != errno.EAGAIN:
                    logger.error(e)
