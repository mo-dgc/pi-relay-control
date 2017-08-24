#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import datetime
import yaml
import sys
import logging
import argparse

# Set up the logger
logger = logging.getLogger()
handler = logging.StreamHandler(stream=sys.stdout)
formatter_debug = logging.Formatter(
        '%(asctime)s [%(levelname)8s](%(funcName)s:%(lineno)d): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
formatter = logging.Formatter(
        '%(asctime)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def init():
    parser = argparse.ArgumentParser(description="Relay control")
    parser.add_argument("--config", action="store", default="relays.yaml",
        help="Configuration file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print Debug info.")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        handler.setFormatter(formatter_debug)
        logger.debug("Enabling DEBUG output")

    main(args)


def main(args):
    logger.debug(args)

    cfg = yaml.load(open(args.config, "r"))
    logger.debug("Config = {}".format(cfg))
    state = 0
    now = datetime.datetime.now().time()

    gpio.setwarnings(False)

    if cfg["mode"] == "BCM":
        gpio.setmode(gpio.BCM)
    elif cfg["mode"] == "BOARD":
        gpio.setmode(gpio.BOARD)
    else:
        logger.error("Invalid GPIO mode specified")
        raise SystemExit

    relays = cfg["relays"]
    for relay in relays:
        gpio.setup(relays[relay]["pin"], gpio.OUT)
        #gpio.output(relays[relay]["pin"], gpio.LOW)

        if relays[relay]["auto"]:
            logger.debug("Relay {} is auto.".format(relay))
            state = 0
            if relays[relay]["schedule"]:
                logger.debug("Evaluating Schedules for relay {}".format(relay))
                logger.debug("  now = {}".format(now))
                logger.debug(relays[relay]["schedule"])
                for sched in relays[relay]["schedule"]:
                    on_hour, on_min = map(int, sched["start"].split(":"))
                    off_hour, off_min = map(int, sched["stop"].split(":"))
                    on_time = datetime.time(hour=on_hour, minute=on_min)
                    off_time = datetime.time(hour=off_hour, minute=off_min)
                    logger.debug(" Schedule:")
                    logger.debug("     on_time = {}".format(on_time))
                    logger.debug("    off_time = {}".format(off_time))

                    if on_time < off_time:
                        # Same day on/off times
                        if now >= on_time and now < off_time:
                            state = 1
                    else:
                        # On/Off split days eg. on=10p, off=2a
                        if now >= on_time or now < off_time:
                            state = 1

                logger.debug(" state: {}".format(state))

            if state:
                if not gpio.input(relays[relay]["pin"]):
                    logger.info("Relay {} turning on.".format(relay))
                    gpio.output(relays[relay]["pin"], gpio.HIGH)
                else:
                    logger.debug("Relay {} is already on.".format(relay))
            else:
                if gpio.input(relays[relay]["pin"]):
                    logger.info("Relay {} turning off.".format(relay))
                    gpio.output(relays[relay]["pin"], gpio.LOW)
                else:
                    logger.debug("Relay {} is already off.".format(relay))

        else:
            logger.debug("Relay {} is manual.".format(relay))


if __name__ == "__main__":
    init()
