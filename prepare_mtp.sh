#!/bin/bash

#unmounts the mtp device
MTP_STR=$(ls /run/user/1000/gvfs/)
MTP_DEV_NAME=${MTP_STR#*mtp:host=}

#unmount the camera to be safe
gio mount -u "mtp://${MTP_DEV_NAME}"

#we need to kill some processes that use the device
#these are:
# 1. gvfs-gphoto2-volume-monitor
# 2. gvfs-mtp-volume-monitor
# 3. gvfsd-gphoto2 --spawner

pkill -f gphoto2
pkill -f gvfs.*mtp