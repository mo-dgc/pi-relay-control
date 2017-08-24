# Simple RPi Relay control

Setting up RPi to control little 4 Relay Module board.  Using this script scheduled via cron every minute to handle the schedule.

# Installation

Clone the repo:
```
$ git clone https://github.com/mo-dgc/pi-relay-control.git ~/relays
```

Create cron job to run the script every minute.  Create ```/etc/cron.d/relays``` with the following:

```
* *	* * *	root    /home/pi/relays/relays.py --config /home/pi/relays/relays.yaml >> /tmp/relays.log 2>&1
```


# Configuration

Edit the ```relays.yaml``` file.  

### Main config fields:

* ```mode``` should be one of BOARD or BCM.
* ```relays``` per relay configuration

### Relay fields:

* ```description``` Name of the relay
* ```pin``` PIN/GPIO Port to use - this will differ depending on if you are using BOARD or BCM.  See ```gpio readall``` for the pins.
* ```auto``` Wether relay is auto (scheduled) or manaual
* ```schedule``` Schedules for this relay

### Schedules:

* ```start``` Time to start in 24 hour HH:MM format
* ```stop``` Time to stop in 24 hour HH:MM format

You can have multiple on/off times per relay.  The following example would turn on the relay from 8:00 to 8:10, then again from 9:00 to 9:10.  There is no set limit to the number of schedules.  If any of the schedules result in the relay being on during the current time, the relay will turn on.

```yaml
relays:
  0:
    description: "Example"
    pin: 17
    auto: True
    schedule:
      - start: "8:00"
        stop: "8:10"
      - start: "9:00"
        stop: "9:10"
```
