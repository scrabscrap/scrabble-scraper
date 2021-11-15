#!/bin/bash

# working directory is $PROJECT/work
SCRIPTPATH=$(dirname "$0")
PROJECT="$(cd "$SCRIPTPATH/.." && pwd)"
WORKDIR=$PROJECT/work

# create directories
mkdir -p "$WORKDIR/log"
mkdir -p "$WORKDIR/web"

# hotspot off
sudo $SCRIPTPATH/hotspot-off.sh

# wait for wlan
sleep 10

# update unix
# test internet connection with ping to cloudflare
if ping -q -w 1 -c 1 1.1.1.1 > /dev/null; then
    sudo apt-get update > $WORKDIR/log/update.log
    sudo apt-get dist-upgrade >> $WORKDIR/log/update.log
fi

# hotspot on
sudo $SCRIPTPATH/hotspot-on.sh
