## Installation des Raspberry PI

### Erstellen einer Boot SD

* RPI Imager (Raspberry Pi OS (32bit))
* pc> touch \<volumes\>/boot/ssh *=> ssh aktivieren*

Nach dem Einlegen und Starten des Raspberry PI kann man sich per ssh einloggen:

```
ssh pi@<ip-Adresse-des-rpi>
```

Das Default-Passwort ist: raspberry

> Bitte schnellstmöglich ändern

### Aktualisiere den Raspberry PI

```bash
sudo apt-get update
sudo apt-get dist-upgrade
# rpi4: check eeprom
# sudo rpi-eeprom-update
# if update: sudo rpi-eeprom-update -a
# if update: sudo reboot

#cleanup
sudo apt-get -y clean
sudo apt-get -y autoremove

# Raspberry PI Konfiguration
sudo raspi-config
#    1. Wifi
#    2. Hostname
#    3. Splash Screen: off
#    4. Camera: on
#    5. ssh: on
#    6. vnc: on
#    7. gpu: 128
#    8. locale: de_DE.UTF-8
#    9. timezone: europe/berlin
#    10. Keyboard: de
```

### Installation von OpenCV

> In Anlehnung an [pyimagesearch](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/)
> 
> ACHTUNG: der gesamte Build-Vorgang dauert mehrere Stunden!

```bash
sudo apt-get install build-essential cmake unzip pkg-config \
  libjpeg-dev libpng-dev libtiff-dev \
  libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
  libxvidcore-dev libx264-dev \
  libgtk-3-dev \
  libcanberra-gtk* \
  libatlas-base-dev gfortran

cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.4.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.4.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.5.4 opencv
mv opencv_contrib-4.5.4 opencv_contrib

wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip

echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

source ~/.profile

# environment for opencv
mkvirtualenv cv -p python3

# requirement for opencv
pip install numpy

# build opencv
cd ~/opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D ENABLE_NEON=ON \
-D ENABLE_VFPV3=ON \
-D BUILD_TESTS=OFF \
-D OPENCV_ENABLE_NONFREE=ON \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D BUILD_EXAMPLES=OFF ..


sudo nano /etc/dphys-swapfile
# set size to absolute value, leaving empty (default) then uses computed value
#   you most likely don't want this, unless you have an special disk situation
# CONF_SWAPSIZE=100
# => CONF_SWAPSIZE=2048

sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

# do not close at 99% / 100% ... wait until end of process
# rpi 3 => ca. 6 hour
# on remote access perhaps use 'nohup make -j$(nproc) &'
# and tail -f nohup.out
make -j$(nproc)

sudo make install
sudo ldconfig

# reset swapsize to 100
sudo nano /etc/dphys-swapfile
# set size to absolute value, leaving empty (default) then uses computed value
#   you most likely don't want this, unless you have an special disk situation
# CONF_SWAPSIZE=2048
# => CONF_SWAPSIZE=100
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start


# use python 3.9 !
cd ~/.virtualenvs/cv/lib/python3.9/site-packages/
ln -s /usr/local/lib/python3.9/site-packages/cv2/python-3.9/cv2.cpython-37m-arm-linux-gnueabihf.so cv2.so
cd ~
```    

### Installation der Python Libs

*Erstinstallation*

```bash
workon cv
pip install imutils visual-logging gpiozero wiringpi picamera flask flask_bootstrap 
```

*Update der Libs*

```bash
workon cv
pip install numpy --upgrade
pip install imutils --upgrade
pip install visual-logging --upgrade
pip install gpiozero --upgrade
! pip install RPi.GPIO --upgrade
pip install wiringpi --upgrade
pip install picamera --upgrade
pip install flask --upgrade
pip install flask_bootstrap --upgrade
```

### Installation von ScrabScrap

```bash
cd ~
git clone github.com/scrabble-scraper/scrabble-scraper.git
mkdir -p ~/scrabble-scraper/work/log
mkdir -p ~/scrabble-scraper/work/web
cp ~/scrabble-scraper/python/default/* ~/scrabble-scraper/work
```

Manchmal werden die Attribute zum Ausführen der Scripte nicht korrekt übernommen. In
diesem Fall folgendes eingeben.

```bash
cd ~/scrabble-scraper/script
chmod +x *.sh
```

Eine erste Konfiguration kann dann in dem Verzeichnis `~/scrabble-scraper/work` vorgenommen werden. Folgende Dateien sollten kopiert bzw. angepasst werden:

* scrabble.ini
* ftp-secret.ini
* log.conf



### Installation des HotSpots

In Anlehnung an [Raspberry Pi - Auto WiFi Hotspot Switch Internet](https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/157-raspberry-pi-auto-wifi-hotspot-switch-internet)


#### Installation hostap

```bash
sudo apt-get update
sudo apt-get dist-upgrade

sudo apt-get -y install hostapd dnsmasq
sudo systemctl unmask hostapd
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq

sudo nano /etc/hostapd/hostapd.conf
```

```
#2.4GHz setup wifi 80211 b,g,n
# ggf. wpa_passphrase anpassen

interface=wlan0
driver=nl80211
ssid=ScrabScrap-Hotspot
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=scrapscrab-wifi
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP TKIP
rsn_pairwise=CCMP

#80211n - Change GB to your WiFi country code
country_code=DE
ieee80211n=1
ieee80211d=1
```

```bash
sudo nano /etc/default/hostapd
```

ändere

```
#DAEMON_CONF=""
```
in

```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

dnsmasq Konfiguration

```
sudo nano /etc/dnsmasq.conf
```

am Ende einfügen

```
#AutoHotspot config
interface=wlan0
bind-dynamic 
server=8.8.8.8
domain-needed
bogus-priv
dhcp-range=192.168.50.150,192.168.50.200,12h
```

prüfe die Netzwerk-Interfaces

```bash
sudo nano /etc/network/interfaces
```

es darf nur folgender Code enthalten sein

```
# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source /etc/network/interfaces.d/*
```
#### ip forwarding

```bash
sudo nano /etc/sysctl.conf
```

```
# Uncomment the next line to enable packet forwarding for IPv4
#net.ipv4.ip_forward=1

and remove the # so it is

# Uncomment the next line to enable packet forwarding for IPv4
net.ipv4.ip_forward=1
```

#### dhcpcd

```bash
sudo nano /etc/dhcpcd.conf
```

am Ende einfügen

```
nohook wpa_supplicant
```

#### Service konfigurieren

Da in unserem Fall per Default immer das normale WLAN aktivert werden soll, muss
das Script zum Ausschalten des HotSpots beim Rechnerstart genutzt werden.

```bash
sudo ln -s /home/pi/scrabble-scraper/script/hotspot-off.sh /usr/bin/autohotspot
sudo chmod +x /usr/bin/autohotspot
sudo nano /etc/systemd/system/autohotspot.service
```

```
[Unit]
Description=Automatically generates an internet Hotspot when a valid ssid is not in range
After=multi-user.target
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/autohotspot
[Install]
WantedBy=multi-user.target
```

#### Ein-/Ausschalten des Hotspot

*Einschalten*

```bash
sudo /home/pi/scrabble-scraper/script/hotspot-on.sh
```

Nach dem Verbinden mit dem HotSpot kann der Raspberry PI per 

```bash
ssh pi@10.0.0.5
```
aufgerufen werden. Ist die Config-Anwendung gestartet, kann im Browser

```hmtl
http://10.0.0.5:8080
```
genutzt werden.

*Ausschalten*

```bash
sudo /home/pi/scrabble-scraper/script/hotspot-on.sh
```
Danach versucht der Raspberry PI sich mit den konfigurierten WLANs zu verbinden.


### Autostart von ScrabScrap

Damit die Anwendung direkt nach dem Einschalten des Rechners starten, sind folgende
Einstellungen vorzunehmen.

```bash
sudo nano /etc/crontab
```

Folgende Zeile ergänzen

```
@reboot pi /home/pi/scrabble-scraper/script/scrabscrap.sh
```

### Boot des Rechners (Grafisch oder Shell)

Falls keine grafische Umgebung benötigt wird, kann mit folgendem Befehl auf einen
Boot in die Text-Konsole umgeschaltet werden (ab dem nächsten Reboot). Damit werden sowohl Rechenleistung als auch RAM gespart.

```bash
sudo systemctl set-default multi-user.target
```

Wenn wieder auf den grafischen Desktop umgeschaltet werden soll, kann dies mit
folgendem Befehl erreicht werden.

```bash
sudo systemctl set-default graphical.target
```

### Prüfen der Kamera

```bash
vcgencmd get_camera
```
 
 Als Ergbenis muss hier `supported=1 detected=1` ausgegeben werden.
 
 ```bash
 cd ~
 raspistill -o test.jpg
 ```

### Installation der RTC

Die Installation der RTC habe ich anhand des Leitfadens
[Raspberry Pi RTC: Adding a Real Time Clock](https://pimylifeup.com/raspberry-pi-rtc/)
vorgenommen. Damit ist der Raspberry PI auch ohne Internet-Zugang mit einer Echtzeituhr versorgt.

 
### Einrichten der VNC Verbindung

Um den Raspberry PI ohne Tastatur und Monitor zu betreiben, kann der Zugang über VNC
genutzt werden. Dies kann entweder im lokalen Netz erfolgen oder per direkte Ethernet-Verbindung.

Damit die Verbindung mittel MacOS Bildschirmfreigabe funktioniert, müssen in VNC folgende
Einstellungen vorgenommen werden:

*   Security - Encryption: Prefer on
*   Security - Authentication: VNC password

Die restlichen Parameter können unverändert bleiben. Das VNC Kennwort wird dann für die
Verbindung verwendet.


### Bildschirmauflösung ohne Monitor

Als Default verwendet der Raspberry PI ohne Monitor eine Auflösung vpn 600x480. Das ist
für den Zugriff über VNC nicht hinreichend. Über das Tool Raspberry PI Configuration
kann eine feste Größe eingestellt werden (1024x768).


 
