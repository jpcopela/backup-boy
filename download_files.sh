#!/bin/bash

DEVICE_NAME=$1
MNTPT=$2

cd "$MNTPT/$DEVICE_NAME"

gphoto2 --get-all-files --skip-existing -q