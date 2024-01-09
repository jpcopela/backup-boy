#!/bin/bash

#if the mass storage device does not have a folder for the camera, create one
DEVICE_NAME=$1
MNTPT=$2

cd $MNTPT

if [ ! -d "$DEVICE_NAME" ]; then
    mkdir "$DEVICE_NAME"
fi