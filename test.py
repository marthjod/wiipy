import argparse
import logging
import sys
import xwiimote

from device import Device


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
    c = Device(dev=dev)

    logger.info("Controller ready (rumbling for {msecs} milliseconds)".format(msecs=rumble_msecs))
    c.rumble(rumble_msecs)

    battery = c.get_battery_level()
    logger.info("Battery at {lvl}%".format(lvl=battery))

    c.read(logger)


if __name__ == '__main__':
    main()
