# rpi-button-box
Core program for a Raspberry Pi **button box controller** that uses the `gpiozero` Python library.  This repo is a companion to my blog post about [repurposing external HDD cases into buttons boxes](#).  

## Disclaimer
This is free and has **no warranty** whatsoever.  Use it at your own risk.  Misconfigured pins might damage your board.

# Wiring
<p align="center">
  <img src="imgs/button-box-wiring.jpg" style="width: 50%;">
</p>

# Requirements
* Raspberry Pi
  * 40 GPIO pins version
* Python3
  * `gpiozero`, `rpi.gpio`

# Installation
The button box controller was developed for the [Raspberry Pi OS](https://www.raspberrypi.org/software/) but it should work with other similar systems for single board computers.  The following instructions assuming you're logged in with a `sudo` user (e.g., `pi`).

1. Use `apt` to install required programs
```
sudo apt update
sudo apt install git python3 python3-pip
```
2. Clone the `rpi-button-box` repo in `/opt`
```
cd /opt
sudo git clone https://github.com/cgomesu/rpi-button-box.git
sudo chown -R pi rpi-button-box
```
3. Install Python libraries from `requirements.txt`
```
pip3 install -r /opt/rpi-button-box/requirements.txt
```
4. Test `button-box.py`
```
./opt/rpi-button-box/button-box.py -h
```
5. (Optional.) Allow `logrotate` (enabled by default) to manage the `button-box.log` log files:
```
sudo cp /opt/rpi-button-box/logrotate.d/button-box /etc/logrotate.d/
```

# Usage
```
./button-box.py -h
```
```
usage: button-box.py [-h] [--buzzer BUZZER] [--cmd {Popen,run}]
                     [--g1_pressed G1_PRESSED] [--g1_released G1_RELEASED]
                     [--s1_held S1_HELD] [--s1_released S1_RELEASED] [-i] [-d]

RPi button box controller. Repo: https://github.com/cgomesu/rpi-button-box

optional arguments:
  -h, --help            show this help message and exit
  --buzzer BUZZER       If installed, the buzzer's GPIO number.
  --cmd {Popen,run}     Popen: run external scripts in a NON-BLOCKING fashion.
                        run: run external scripts in a BLOCKING fashion.
                        Default=run
  --g1_pressed G1_PRESSED
                        /path/to/script to run when G1 is pressed. The
                        --btn_pressed arg is available to other PUSH buttons
                        as well.
  --g1_released G1_RELEASED
                        /path/to/script to run when G1 is released. The
                        --btn_released arg is available to other PUSH buttons
                        as well.
  --s1_held S1_HELD     /path/to/script to run when S1 is held. The
                        --btn_held arg is available to other SWITCHES as well.
  --s1_released S1_RELEASED
                        /path/to/script to run when S1 is released. The
                        --btn_released arg is available to other SWITCHES as
                        well.
  -i, --info            Show the board information.
  -d, --debug           Print additional messages to the terminal.
```

As mentioned, there are **hidden arguments** for passing external scripts to be executed upon a button event, such as pressing `G2`, or releasing `S3`.  More specifically, in addition to `--g1_*` and `--s1_*` args shown in the help output, the program accepts args for any of the other seven buttons, as follows

* script for `pressed` and `released` events: the **push buttons** `--g1_*`, `--b1_*`, `--r1_*`, `--g2_*`, `--b2_*`, and `--r2_*`,
* script for `held` and `released` events: the **switches** `--s1_*`, `--s2_*`, and `--s3_*`.

The script generates a `button-box.log` log file to keep track of controller-related events.

# Examples
* Output info about the board
```
./button-box.py -i
```

* Run the controller in debug mode and the buzzer (`GPIO4`)
```
./button-box.py -d --buzzer 4
```

* Run the controller with a buzzer and execute `/opt/rpi-button-box/scripts/template.sh` whenever the push button `R2` is **pressed**:
```
./button-box.py --buzzer 4 \
--r2_pressed '/opt/rpi-button-box/scripts/template.sh'
```

* Same as before, but don't wait for the external script to finish running (**non-blocking** command execution):
```
./button-box.py --buzzer 4 --cmd Popen \
--r2_pressed '/opt/rpi-button-box/scripts/template.sh'
```

# Run as a service
TBA
