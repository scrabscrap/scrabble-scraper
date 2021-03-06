"""
 This file is part of the scrabble-scraper distribution (https://github.com/scrabscrap/scrabble-scraper)
 Copyright (c) 2020 Rainer Rohloff.
 
 This program is free software: you can redistribute it and/or modify  
 it under the terms of the GNU General Public License as published by  
 the Free Software Foundation, version 3.

 This program is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of 
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 General Public License for more details.

 You should have received a copy of the GNU General Public License 
 along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import atexit
import cv2
import os
import platform
import subprocess
import sys
import time
import numpy as np

# add scrabscrap to path
SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "../scrabscrap")
sys.path.append(os.path.dirname(SCRIPT_DIR))

import analyzer_classic
import analyzer_custom
from configparser import ConfigParser
from flask import render_template, redirect, request, Response, send_file
from flask import Flask
from flask_bootstrap import Bootstrap

# todo evtl. auch für die Werte den Standard-Parser nehmen
# noinspection PyUnresolvedReferences
from config import TM1637, CLK1, CLK2, DIO1, DIO2
# noinspection PyUnresolvedReferences
from hardware import led
# noinspection PyUnresolvedReferences
from hardware import videostream as vs
# noinspection PyUnresolvedReferences
from board import board

if TM1637:
    # noinspection PyUnresolvedReferences
    from hardware import tm1637

    display_left = tm1637.TM1637(clk=CLK1, dio=DIO1)
    display_right = tm1637.TM1637(clk=CLK2, dio=DIO2)
    display_left.show("   ")
    display_right.show("    ")
else:
    display_left = None
    display_right = None

APP = Flask(__name__)
APP.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(APP)
ROOT_PATH = os.path.abspath(APP.root_path + "/../..")

# global (test)
led_green = False
led_red = False
led_blue = False
led_yellow = False
cancel_stream = True
# properties

# config_scrabble = ConfigParser(defaults={'doubt_timeout':'','malus_doubt':'','max_time':'','ftp_active':''})
config_scrabble = ConfigParser()
config_scrabble.read(ROOT_PATH + "/work/scrabble.ini")
doubt_timeout = config_scrabble.get('scrabble', 'doubt_timeout', fallback='')
malus_doubt = config_scrabble.get('scrabble', 'malus_doubt', fallback='')
max_time = config_scrabble.get('scrabble', 'max_time', fallback='')
board_layout = config_scrabble.get('board', 'layout', fallback='')
video_rotade = config_scrabble.get('video', 'rotade', fallback='False')
ftp_active = config_scrabble.get('output', 'ftp', fallback='True')

config_ftp = ConfigParser()
config_ftp.read(ROOT_PATH + "/work/ftp-secret.ini")
ftp_server = config_ftp.get('ftp', 'ftp-server', fallback='')
ftp_user = config_ftp.get('ftp', 'ftp-user', fallback='')
ftp_password = config_ftp.get('ftp', 'ftp-password', fallback='')


####################
#  page main.html ##
####################
@APP.route('/')
@APP.route('/main.html')
def mainhtml():
    return render_template('main.html')


######################
#  page system.html ##
######################
@APP.route('/system.html')
def system():
    global ftp_server, ftp_password, ftp_user
    os_system = platform.system()
    arch = platform.machine()
    release = platform.release()
    user = os.getlogin()

    space = os.statvfs('.')
    freespace = int((space.f_frsize * space.f_bavail) / 1024 / 1024)

    config_ftp.read(ROOT_PATH + "/work/ftp-secret.ini")
    ftp_server = config_ftp.get('ftp', 'ftp-server', fallback='')
    ftp_user = config_ftp.get('ftp', 'ftp-user', fallback='')
    ftp_password = config_ftp.get('ftp', 'ftp-password', fallback='')

    return render_template('system.html', system=os_system,
                           release=release, arch=arch, user=user,
                           freespace=freespace,
                           ftp_server=ftp_server, ftp_user=ftp_user, ftp_password=ftp_password)


@APP.route('/wifi', methods=['POST'])
def set_wifi():
    ssid = request.form['ssid']
    passw = request.form['wifi_password']
    # todo set wifi
    subprocess.call("sudo sh -c 'wpa_passphrase " + ssid + " " + passw + ">> /etc/wpa_supplicant/wpa_supplicant.conf'",
                    shell=True)
    return redirect('/system.html')


@APP.route('/clear_wifi', methods=['POST'])
def clear_wifi():
    subprocess.call(ROOT_PATH + "/script/reset-wifi.sh", shell=True)
    return redirect('/system.html')


@APP.route('/ftp', methods=['POST'])
def set_ftp():
    global ftp_server, ftp_user, ftp_password
    ftp_server = request.form['ftp_server']
    ftp_user = request.form['ftp_user']
    ftp_password = request.form['ftp_password']
    config_ftp.set('ftp', 'ftp-server', ftp_server)
    config_ftp.set('ftp', 'ftp-user', ftp_user)
    config_ftp.set('ftp', 'ftp-password', ftp_password)
    with open(ROOT_PATH + '/work/ftp-secret.ini', 'w') as conf:
        config_ftp.write(conf)

    return redirect('/system.html')


@APP.route('/download_logs', methods=['POST', 'GET'])
def download_logs():
    # compess logs and serve
    import zipfile

    zf = zipfile.ZipFile(ROOT_PATH + "/work/log.zip", "w")
    for dirname, subdirs, files in os.walk(ROOT_PATH + "/work/log", topdown=False):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    return send_file(ROOT_PATH + "/work/log.zip", as_attachment=True)


@APP.route('/delete_logs', methods=['POST', 'GET'])
def delete_logs():
    # delete logs
    # print(APP.root_path)
    subprocess.call(ROOT_PATH + "/script/delete-logs.sh", shell=True)
    return redirect('/system.html')


@APP.route('/update_unix', methods=['POST', 'GET'])
def update_unix():
    display_left.show("UPDT")
    display_right.show("UNIX")
    # flag to update unix
    subprocess.call(ROOT_PATH + "/script/update-unix.sh", shell=True)
    display_left.show("    ")
    display_right.show("    ")
    return redirect('/system.html')


@APP.route('/update_scrabscrap', methods=['POST', 'GET'])
def update_scrabscrap():
    display_left.show("UPDT")
    display_right.show("APP ")
    # flag to update ScrabScrap
    subprocess.call(ROOT_PATH + "/script/update-scrabscrap.sh", shell=True)
    display_left.show("    ")
    display_right.show("    ")
    return redirect('/system.html')


########################
#  page scrabble.html ##
########################
@APP.route('/scrabble.html')
def scrabble():
    global doubt_timeout, malus_doubt, max_time, video_rotade, board_layout, ftp_active
    config_scrabble.read(ROOT_PATH + "/work/scrabble.ini")
    doubt_timeout = config_scrabble.get('scrabble', 'doubt_timeout', fallback='')
    malus_doubt = config_scrabble.get('scrabble', 'malus_doubt', fallback='')
    max_time = config_scrabble.get('scrabble', 'max_time', fallback='')
    video_rotade = config_scrabble.get('video', 'rotade', fallback='True')
    board_layout = config_scrabble.get('board', 'layout', fallback='')
    ftp_active = config_scrabble.get('output', 'ftp', fallback='True')

    return render_template('scrabble.html', doubt_timeout=doubt_timeout,
                           malus_doubt=malus_doubt, max_time=max_time, video_rotade=(video_rotade == 'True'),
                           board_layout=board_layout, ftp_active=(ftp_active == 'True'))


@APP.route('/max_time', methods=['POST'])
def set_max_time():
    global max_time
    config_scrabble['scrabble']['max_time'] = max_time = request.form['max_time']
    with open(ROOT_PATH + '/work/scrabble.ini', 'w') as conf:
        config_scrabble.write(conf)
    return redirect('/scrabble.html')


@APP.route('/doubt_timeout', methods=['POST'])
def set_doubt_timeout():
    global doubt_timeout
    config_scrabble['scrabble']['doubt_timeout'] = doubt_timeout = request.form['doubt_timeout']
    with open(ROOT_PATH + '/work/scrabble.ini', 'w') as conf:
        config_scrabble.write(conf)
    return redirect('/scrabble.html')


@APP.route('/malus_doubt', methods=['POST'])
def set_malus_doubt():
    global malus_doubt
    config_scrabble['scrabble']['malus_doubt'] = malus_doubt = request.form['malus_doubt']
    with open(ROOT_PATH + '/work/scrabble.ini', 'w') as conf:
        config_scrabble.write(conf)
    return redirect('/scrabble.html')


@APP.route('/video_rotade', methods=['POST'])
def set_video_rotade():
    global video_rotade
    if request.form.get('video_rotade'):
        config_scrabble['video']['rotade'] = video_rotade = 'True'
    else:
        config_scrabble['video']['rotade'] = video_rotade = 'False'
    with open(ROOT_PATH + '/work/scrabble.ini', 'w') as conf:
        config_scrabble.write(conf)
    return redirect('/scrabble.html')


@APP.route('/board_layout', methods=['POST'])
def set_board_layout():
    global board_layout
    config_scrabble['board']['layout'] = board_layout = request.form['board_layout']
    with open(ROOT_PATH + '/work/scrabble.ini', 'w') as conf:
        config_scrabble.write(conf)
    return redirect('/scrabble.html')


@APP.route('/ftp_upload', methods=['POST'])
def set_ftp_upload():
    global ftp_active
    if request.form.get('ftp_upload'):
        config_scrabble['output']['ftp'] = ftp_active = 'True'
    else:
        config_scrabble['output']['ftp'] = ftp_active = 'False'
    with open(ROOT_PATH + '/work/scrabble.ini', 'w') as conf:
        config_scrabble.write(conf)
    return redirect('/scrabble.html')


@APP.route('/reset_config', methods=['POST'])
def reset_config():
    # reset config
    subprocess.call(ROOT_PATH + "/script/reset-config.sh", shell=True)
    return redirect('/scrabble.html')


@APP.route('/delete_games', methods=['POST'])
def delete_games():
    # delete games
    subprocess.call(ROOT_PATH + "/script/delete-games.sh", shell=True)
    return redirect('/scrabble.html')


@APP.route('/download_games', methods=['POST', 'GET'])
def download_games():
    # compress games and serve
    import zipfile

    zf = zipfile.ZipFile(ROOT_PATH + "/work/games.zip", "w")
    for dirname, subdirs, files in os.walk(ROOT_PATH + "/work/web"):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    return send_file(ROOT_PATH + "/work/games.zip", as_attachment=True)


#####################
#  page video.html ##
#####################
cap = None
warp_image = None


@APP.route('/get_warp')
def get_warp():
    global warp_image

    return Response(warp_image, mimetype='image/jpeg')


@APP.route('/warp.html')
def show_warp():
    global cancel_stream
    global cap
    global warp_image

    cancel_stream = True
    if cap is None:
        cap = vs.get_video()
        cap.start()
        cap.read()
        atexit.register(cap.stop)

    time.sleep(0.5)
    picture = cap.picture()
    if board_layout == 'custom':
        analyzer = analyzer_custom.AnalyzerCustom()
    else:
        analyzer = analyzer_classic.AnalyzerClassic()
    warped = analyzer.warp(picture)
    _mark = board.overlay_grid(warped)
    # _resized = cv2.resize(_mark, (500, 500))
    _, buffer = cv2.imencode('.jpg', _mark)
    warp_image = buffer.tobytes()

    warp = ConfigParser()
    warp.read(ROOT_PATH + '/work/warp.ini')
    out = ""
    if warp.has_section('warp'):
        rect = np.zeros((4, 2), dtype="float32")
        rect[0][0] = warp['warp']['top-left-x']
        rect[0][1] = warp['warp']['top-left-y']
        rect[1][0] = warp['warp']['top-right-x']
        rect[1][1] = warp['warp']['top-right-y']
        rect[2][0] = warp['warp']['bottom-right-x']
        rect[2][1] = warp['warp']['bottom-right-y']
        rect[3][0] = warp['warp']['bottom-left-x']
        rect[3][1] = warp['warp']['bottom-left-y']
        out = "warp.ini {}".format(rect)

    return render_template('warp.html', out=out)


@APP.route('/warp_store', methods=['POST'])
def store_warp():
    warp = ConfigParser()
    warp.add_section('warp')
    warp['warp']['top-left-x'] = str(analyzer_custom.last_warp[0][0])
    warp['warp']['top-left-y'] = str(analyzer_custom.last_warp[0][1])
    warp['warp']['top-right-x'] = str(analyzer_custom.last_warp[1][0])
    warp['warp']['top-right-y'] = str(analyzer_custom.last_warp[1][1])
    warp['warp']['bottom-right-x'] = str(analyzer_custom.last_warp[2][0])
    warp['warp']['bottom-right-y'] = str(analyzer_custom.last_warp[2][1])
    warp['warp']['bottom-left-x'] = str(analyzer_custom.last_warp[3][0])
    warp['warp']['bottom-left-y'] = str(analyzer_custom.last_warp[3][1])
    with open(ROOT_PATH + '/work/warp.ini', 'w') as conf:
        warp.write(conf)
    return redirect('/warp.html')


@APP.route('/warp_delete', methods=['POST'])
def delete_warp():
    warp = ConfigParser()
    with open(ROOT_PATH + '/work/warp.ini', 'w') as conf:
        warp.write(conf)
    return redirect('/warp.html')


@APP.route('/video.html')
def video():
    global cap

    if cap is None:
        cap = vs.get_video()
        cap.start()
        cap.read()
        atexit.register(cap.stop)
    return render_template('video.html')


@APP.route('/video_feed')
def video_feed():
    global cap
    # write display image
    global cancel_stream
    cancel_stream = False
    return Response(gen_frames(cap),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@APP.before_request
def before_request():
    global cancel_stream
    cancel_stream = True


#  Show video stream from camera
def gen_frames(current_cap):
    import time
    global cancel_stream

    cancel_stream = False
    while True:
        if cancel_stream:
            print("cancel stream")
            break
        else:
            time.sleep(0.01)
            frame = current_cap.picture()  # read the camera frame
            frame = cv2.resize(frame, (500, 500))
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


####################
#  page test.html ##
####################
@APP.route('/test.html')
def test():
    return render_template('test.html', green=led_green, red=led_red, blue=led_blue, yellow=led_yellow, )


@APP.route('/green', methods=['POST'])
def green():
    # toogle green
    global led_green
    led_green = not led_green
    if led_green:
        led.green.on()
    else:
        led.green.off()
    return redirect('/test.html')


@APP.route('/red', methods=['POST'])
def red():
    # toogle red
    global led_red
    led_red = not led_red
    if led_red:
        led.red.on()
    else:
        led.red.off()
    return redirect('/test.html')


@APP.route('/blue', methods=['POST'])
def blue():
    # toogle blue
    global led_blue
    led_blue = not led_blue
    if led_blue:
        led.blue.on()
    else:
        led.blue.off()
    return redirect('/test.html')


@APP.route('/yellow', methods=['POST'])
def yellow():
    # toogle yellow
    global led_yellow
    led_yellow = not led_yellow
    if led_yellow:
        led.yellow.on()
    else:
        led.yellow.off()
    return redirect('/test.html')


@APP.route('/display', methods=['POST'])
def display():
    left = request.form['left']
    right = request.form['right']
    if display_left is not None:
        display_left.show(left)
        display_right.show(right)
    else:
        print("display not found")
    return redirect('/test.html')


#####################
#  page start.html ##
#####################
@APP.route('/start.html')
def starthtml():
    return render_template('start.html')


# noinspection PyUnresolvedReferences
@APP.route('/scrabscrap', methods=['POST'])
def reboot():
    if display_left is not None:
        display_left.show("RUN ")
        display_right.show("    ")

    global cap
    if cap is not None:
        cap.stop()
        cap.close()
    subprocess.call(ROOT_PATH + "/script/server-off.sh", shell=True)
    sys.exit(0)


if __name__ == "__main__":
    display_left.show("CFG ")
    display_right.show("AP  ")
    APP.run(host='0.0.0.0', port=8080, debug=True)
