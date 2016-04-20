#!/bin/bash
# Copyright (C) 2012 by Kirik Konstantin <snegovick>

USAGE="usage: camera_prepare.sh <camera device>"

if [ -z $1 ]; then
    echo "abort: no device set"
    echo $USAGE
    exit
fi

if [ ! -e $1 ]; then
    echo "abort: no such device"
    echo $USAGE
    exit
fi

#v4l2-ctl -d $1 -L
#v4l2-ctl -d $1 -C exposure_auto   #query
#v4l2-ctl -d $1 -c exposure_auto=1 #set
v4l2-ctl -d $1 -C white_balance_temperature_auto
v4l2-ctl -d $1 -c white_balance_temperature_auto=0

v4l2-ctl -d $1 -C gain
v4l2-ctl -d $1 -c gain=255
v4l2-ctl -d $1 -C gain

v4l2-ctl -d $1 -C backlight_compensation
v4l2-ctl -d $1 -c backlight_compensation=0

v4l2-ctl -d $1 -C power_line_frequency
v4l2-ctl -d $1 -c power_line_frequency=1 # 50 hz
v4l2-ctl -d $1 -C power_line_frequency

v4l2-ctl -d $1 -C exposure_auto_priority
v4l2-ctl -d $1 -c exposure_auto_priority=0

v4l2-ctl -d $1 -C exposure_absolute
#v4l2-ctl -d $1 --streamoff
v4l2-ctl -d $1 -w -c exposure_absolute=166
#v4l2-ctl -d $1 --streamon
v4l2-ctl -d $1 -C exposure_absolute
