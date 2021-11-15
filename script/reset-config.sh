#!/bin/bash

# working directory is $PROJECT/work
SCRIPTPATH=$(dirname "$0")
PROJECT="$(cd "$SCRIPTPATH/.." && pwd)"
WORKDIR=$PROJECT/work

sudo cp -f "$SCRIPTPATH/wpa_supplicant.conf" /etc/wpa_supplicant/wpa_supplicant.conf
