#!/bin/bash

#searches for gphoto2 supported cameras and gets their info
CONNECTED=$(gphoto2 --auto-detect -q | grep 'usb:')

while [ -n $CONNECTED ]; do
    sleep 1
    CONNECTED=$(gphoto2 --auto-detect -q| grep 'usb:')
done

DEVICE_KEY=$(gphoto2 --auto-detect -q)
DEVICE_ID=${DEVICE_KEY#*usb:}
BUS=$(echo $DEVICE_ID | cut -b 1-3) #bus number
DEVICE_NO=$(echo $DEVICE_ID | cut -b 5-7) #device number

DEVICE_INFO=$(lsusb -s $BUS:$DEVICE_NO)
DEVICE_NAME=${DEVICE_INFO#*ID * }

echo $DEVICE_NAME