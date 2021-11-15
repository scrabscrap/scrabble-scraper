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

# update scrabscrap
# test internet connection with ping to cloudflare
if ping -q -w 1 -c 1 1.1.1.1 > /dev/null; then
    cd $PROJECT
    git fetch > $WORKDIR/log/git.log
    git reset --hard origin/main >> $WORKDIR/log/git.log  
fi

# hotspot on
sudo $SCRIPTPATH/hotspot-on.sh
