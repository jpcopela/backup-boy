#!/bin/bash

#find connected USB mass storage devices
MOUNTED_DRIVE=$(find /dev/disk/by-path/ -name "*usb*part*")

while [ -z $MOUNTED_DRIVE ]; do
    sleep 1
    MOUNTED_DRIVE=$(find /dev/disk/by-path/ -name "*usb*part*")
done

sleep 1 #wait for the drive to mount

#get the mount point
USB_PATH=$(readlink -f $MOUNTED_DRIVE) #get the path of the usb drive
MNT_INFO=$(mount | grep $USB_PATH) #get the mount info
MNTPT=$(echo $MNT_INFO | cut -d ' ' -f3) #get the mount point

echo $MNTPT