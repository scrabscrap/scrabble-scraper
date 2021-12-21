#!/bin/bash

export DISPLAY=:0

# working directory is $PROJECT/work
SCRIPTPATH=$(dirname "$0")
PROJECT="$(cd "$SCRIPTPATH/.." && pwd)"
WORKDIR=$PROJECT/work


# end hotspot
sudo $SCRIPTPATH/hotspot-off.sh

# start scrabscrap
sudo reboot