#!/bin/bash

#unmounts the external storage device, the camera is already unmounted
$MNTPT=$1
umount $MNTPT

while [ $? -ne 0 ]; do
    sleep 1
    umount $MNTPT
done

#kill the device NOT FOR TESTING
sudo halt -p