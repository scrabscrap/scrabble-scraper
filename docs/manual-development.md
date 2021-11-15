# Handbuch für Entwickler

## Entwicklungsumgebung

Empfohlene lokale Entwicklungsumgebung

* Visual Studio Code (mit den Python Plugins)
* Python 3.9
* lokal installiertes OpenCV 4.5.4

Die Verwendung eines separaten Systems zur Entwicklung führte im Code
dazu, RPI spezifische Bibliotheken optional einzubinden und
die Kamera mit Hilfe von aufgezeichneten Bildern zu ersetzen.
Die Entwicklungszyklen sind mit gespeicherten Bildern und einem
schnelleren Rechner halt kürzer.

## ScrabScrap und OpenCV

Installation auf dem Rasberry PI gemäß der Anleitung "manual-installation-rpi.md". 
Die Installation auf einem lokalen Entwicklungsrechner kann analog erfolgen. Hier 
müssen lediglich die RPI spezifischen Bibliotheken ausgelassen werden.

## Config-Anwendung mit Flask

Für die Konfiguration der Anwendung mittels eines HotSpots wird eine Web-Anwendung
mit Hilfe von Flask und Flask-Bootstrap zur Verfügung gestellt.
Hier können in der ersten Fassung grundsätzliche Einstellungen vorgenommen werden,
ohne das komplizierte ssh / vnc Verbindungen aufgebaut werden müssen.


## Web-Anwendung mit React

Die Web-App zur Online-Anzeige ist mit [React](https://reactjs.org/)
implementiert worden.

Als CSS Bibliothek wird [Bootstrap v4.3.1](https://getbootstrap.com)
ohne JavaScript genutzt. Die verwendete Version ist direkt in das
Projekt eingebunden. Die statischen Seiten, die erzeugt werden
(npm build), sind ebenfalls in git eingecheckt, damit die Anwendung auch ohne
"react"-Umgebung genutzt werden kann.

### Installation auf dem Web-Server

Die Anwendung kann einfach auf einem Web-Server zur Verfügung gestellt werden. 
Damit die aktuellen Daten auf den Server geladen werden können, muss ein FTP-Zugang
zu dem Unterverzeichnis "web" der React-Anwendung zur Verfügung gestellt werden und
in der Konfigurationsdatei "ftp-secret.ini" konfiguriert werden.

## Software

Segment-Anzeige der gespielten Zeit (Basis ist der TM1637) ist hier
übernommen worden:

*   [Github depklyon](https://github.com/depklyon/raspberrypi-python-tm1637)

Für die Bildanalysen und die Umsetzung mit OpenCV und Python sind einige
Code-Teile von

*   [pyimagesearch](https://www.pyimagesearch.com/)

genutzt worden.

Die Bibliothek gpiozero ist hier beschrieben:

*   [gpiozero](https://gpiozero.readthedocs.io)

Die Bibliothek flask ist hier beschrieben:

* [flask](https://palletsprojects.com/p/flask/)


## Erstellen der PDF Dokumentation

Installation unter MacOS kann mittels [homebrew](https://brew.sh/index_de) erfolgen. 
Die Installation und Benutzung für andere Plattformen kann unter 
[pandoc](https://pandoc.org/installing.html) nachgelesen werden.

```bash
brew install pandoc
brew install basictex

sudo tlmgr install framed fvextra
```

Die zusätzlichen Pakete sind notwendig, damit der "highlight-style" verwendet werden kann und 
der Source-Code am Zeilenende automatisch umgebrochen wird. Die Standard-Einstellung wird in 
einer separaten Datei abgelegt. Diese muss dann beim Erzeugen der PDF Datei mit eingebunden 
werden.

```yaml
geometry:
-    margin=2cm
header-includes:
 - \usepackage{fvextra}
 - \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}
```


Die Dokumente können dann aus dem Markdown mit folgendem Befehl erzeugt werden

```bash
./make_pdf.sh
```

Danach stehen die PDFs in dem Ordern "pdf" zur Verfügung.
