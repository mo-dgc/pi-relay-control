#!/usr/bin/env python3

import RPi.GPIO as gpio
from flask import Flask, render_template, request

app = Flask(__name__)

gpio.setwarnings(False)
#@TODO: Get from config.yaml
gpio.setmode(gpio.BCM)

pins = {
        17: {"name":"GPIO 0", "state":gpio.LOW},
        18: {"name":"GPIO 1", "state":gpio.LOW},
        27: {"name":"GPIO 2", "state":gpio.LOW},
        22: {"name":"GPIO 3", "state":gpio.LOW}
        }

for pin in pins:
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, gpio.LOW)


@app.route("/")
def main():
    for pin in pins:
        pins[pin]["state"] = gpio.input(pin)
    templateData = { "pins": pins }
    return render_template("main.html", **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]["name"]

    if action == "on":
        gpio.output(changePin, gpio.HIGH)
        message = "Turned {} on.".format(deviceName)

    if action == "off":
        gpio.output(changePin, gpio.LOW)
        messsage = "Turned {} off".format(deviceName)

    for pin in pins:
        pins[pin]["state"] = gpio.input(pin)

    templateData = { "pins": pins }
    return render_template("main.html", **templateData)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)



