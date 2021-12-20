#!/bin/bash

# damit das Script beim Booten des Rechners ausgeführt wird, muss folgender Eintrag
# als User "pi" vorgenommen werden:
# crontab -e
# @reboot /home/pi/scrabble-scraper/script/scrabscrap.sh &

export DISPLAY=:0

# working directory is $PROJECT/work
SCRIPTPATH=$(dirname "$0")
PROJECT="$(cd "$SCRIPTPATH/.." && pwd)"
WORKDIR=$PROJECT/work

# ensure to try wlan access
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo wpa_supplicant -B -i "wlan0" -c /etc/wpa_supplicant/wpa_supplicant.conf >/dev/null 2>&1
sleep 2

# create directories
mkdir -p "$WORKDIR/log"
mkdir -p "$WORKDIR/web"

# copy defaults if not exists
cp -n "$PROJECT/python/default/scrabble.ini" "$WORKDIR/scrabble.ini"
cp -n "$PROJECT/python/default/ftp-secret.ini" "$WORKDIR/ftp-secret.ini"
cp -n "$PROJECT/python/default/log.conf" "$WORKDIR/log.conf"

# start app
export PYTHONPATH=$PROJECT/python/scrabscrap
source /usr/local/bin/virtualenvwrapper.sh
workon cv

cd "$WORKDIR"
python -m scrabscrap >> "$WORKDIR/log/game.log"
