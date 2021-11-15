#!/bin/bash

export DISPLAY=:0

# working directory is $PROJECT/work
SCRIPTPATH=$(dirname "$0")
PROJECT="$(cd "$SCRIPTPATH/.." && pwd)"
WORKDIR=$PROJECT/work

# create directories
mkdir -p "$WORKDIR/log"
mkdir -p "$WORKDIR/web"

# copy defaults if not exists
cp -n "$PROJECT/python/default/scrabble.ini" "$WORKDIR/scrabble.ini"
cp -n "$PROJECT/python/default/ftp-secret.ini" "$WORKDIR/ftp-secret.ini"
cp -n "$PROJECT/python/default/log.conf" "$WORKDIR/log.conf"

# start hotspot
sudo $SCRIPTPATH/hotspot-on.sh

# wait for hotspot
sleep 2

# start app
export PYTHONPATH=$PROJECT/python/scrabscrap:$PROJECT/python/config-hotspot
source /usr/local/bin/virtualenvwrapper.sh
workon cv

cd "$PROJECT/python/config-hotspot"
python server.py >> "$WORKDIR/log/hotspot.log"
