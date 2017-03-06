Config Files used in this repository and documentation
======================================================
- /etc/fstab/
- /etc/mpd.conf
- /boot/config.txt
- /home/osmc/Script/soft_shutdown.py
- /etc/systemd/system/softshutdown.service


Install OSMC
============
Follow OSMC installation steps for Raspberry Pi 3 on [osmc](https://osmc.tv/) website


Basic config and tools
======================
- check this entry in /etc/sudoers (use visudo as root)
```
# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL
```
- then add user to sudo group and install basic tools
```bash
$ sudo adduser osmc sudo
$ sudo apt-get update && sudo apt-get -y install vim git
```
- Clone the git repo into /home/osmc
```bash
$ git clone https://github/gregsaun/rpi3_media
```

MPD and IQaudIO DAC Plus Installation
=====================================
- edit /boot/config.txt
```bash
$ sync
$ reboot
```
- install MPD packages
```bash
$ sudo apt-get -y update && sudo apt-get -y install alsa-utils mpd mpc
```
- edit /etc/mpd.conf
- edit /etc/fstab
- reboot


Config for GPIO
===============
To be able to run GPIO python code without being root user
- install GPIO and user/group
```bash
$ sudo apt-get install python-dev python-pip build-essential
$ export ARCH=arm
$ export CROSS_COMPILE=/usr/bin/
$ sudo pip install -U pip
$ sudo pip install RPi.GPIO
$ sudo groupadd -r -f gpio
$ sudo adduser osmc gpio
```
- go to /lib/udev/rules.d/
- check the first non-existing number in filenames, for example 51
- create file /lib/udev/rules.d/51-gpio.rules with following content:
```
SUBSYSTEM=="bcm2835-gpiomem", KERNEL=="gpiomem", GROUP="gpio", MODE="0660"
SUBSYSTEM=="gpio", KERNEL=="gpiochip*", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys/class/gpio/export /sys/class/gpio/unexport ; chmod 220 /sys/class/gpio/export /sys/class/gpio/unexport'"
SUBSYSTEM=="gpio", KERNEL=="gpio*", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value ; chmod 660 /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value'"
```


Soft shutdown and power led
===========================
- copy file etc/systemd/system/softshudown.service to same location as the path
- create and start the service : 
```bash
$ sudo chmod 755 /etc/systemd/system/softshutdown.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable softshutdown.service
$ sudo systemctl start test
```
- connect led with 1K resistor between GPIO's pin 13 and GND
- connect button between GPIO's pin 11 and GND
- reboot
