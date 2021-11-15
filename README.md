# Das Projekt ScrabScrap

Die Idee zum Scrabble Scraper ist vor einem Scrabble Turnier in Hamburg
2019 entstanden.  Da viele Partien parallel gespielt werden, ist es
nicht einfach, in den Spielverlauf paralleler Partien nachträglich
hineinzufinden.

Die Anforderungen waren schnell gestellt. Mit einer Kamera das Spielfeld
beobachten und die gelegten Buchstaben erkennen.
... naja und dann noch das Punktezählen, die Zeitnahme, die
verschiedenen Spielsituationen (z.B. Anzweifeln) usw.

Als Basis sollte ein Raspberry PI 3 verwendet werden, da hier recht viel
Bastelmaterial zur Verfügung steht und die Kosten für Anschaffung sich
in Grenzen hält. Ziel ist, bei der Hardware möglichst unter 100,-- €
zu bleiben. Die Nutzung vom Raspberry PI führte im Laufe des Projektes
allerdings zu nötigen Optimierungen, da die Performance (gerade für
Bildverarbeitung) nicht gerade üppig ist.

Ich selbst habe vor diesem Projekt noch keine Erfahrungen in Python,
OpenCV, React sammeln können. Vermutlich können daher einige Lösungen
in den jeweiligen Programmiersprachen angemessener implementiert
werden. Hier bitte ich um Verbessungsverschläge - am Besten als
pull-requests.

Die Dokumentation ist derzeit komplett in Deutsch (meist auch im Code).
Da viele Teile des Projekte zur Zeit auf das deutsche Scrabble Spiel
optimiert sind, habe ich zunächst auf eine englische Dokumentation
verzichtet. Auch um einen Sprachen-Misch-Masch zu vermeiden. Sofern
nicht modifizierte Code-Teile verwendet werden, habe ich die
ursprünglichen Kommentare erhalten. Sollte hier Dritt-Code ohne Referenz
enthalten sein - das will ich beim Studium von einigen Tutorial-Seiten
nicht ausschließen - dann bitte ich um eine kurze Information. Ich
ergänze dann die Quellen.

*Disclaimer:* das Projekt ist kein offizielles Projekt von J.W. Spear &
Sons Limited, Mattel oder Scrabble Deutschland.

SCRABBLE® is a registered trademark of J.W. Spear & Sons Limited

Wer mehr über Scrabble erfahren möchte, kann als Einstiegspunkt
[Wikipedia: Scrabble](https://de.wikipedia.org/wiki/Scrabble)
nutzen.

Vielen Dank für die Unterstützung an
[Scrabble Deutschland eV](http://scrabble-info.de/) für die Tests,
Beratung und Diskussion bei der Umsetzung. Die Beispiele von den Partien
sind dabei auf verschiedenen Scrabble-Turnieren entstanden.


## Was ist zur Zeit umgesetzt

Mittels der Kamera wird ein Bild aufgezeichnet und dieses dann mittels
TemplateMatching durch OpenCV analysiert. Die erkannten Buchstaben 
werden dann Zügen zugeordnet. Dabei erfolgt eine Berechnung der Punktwerte
(Score). Die Umschaltung zwischen den Zügen erfolgt per Tastendruck.

Da die Analyse des Spielbrettes und die Berechnung der Punktwerte in
Near-Time erfolgen soll (die Zugfolge ist teilweise sehr schnell), müssen 
bei der Bildanalyse Kompromisse eingegangen werden. Um eine Entkopplung
zu erreichen werden Hintergrund-Threads in Form einer Queue genutzt, da 
es so möglich ist, bereits weitere Züge für eine Analyse aufzunehmen, 
ohne den aktuellen Zug bereits vollständig berechnet zu haben.

Zur Bestimmung der Spielzeit der einzelnen Spieler läuft für den
aktiven Spieler jeweils ein Timer mit. Wird eine "Pause" ausgelöst,
wird der Timer des aktiven Spielers angehalten. Wird die Pause
beendet, kann der aktive Spieler wieder eine Zug ausführen und
der Timer wird fortgesetzt. Die Stoppuhren der Spieler sollten auch in
Fehlersituationen möglichst weiter zur Verfügung stehen.

Anzweifeln eines Zuges erfolgt immer nachdem ein Spieler seinen Zug
beendet hat. Der Gegenspieler kann den zuletzt gelegten Zug innerhalb
von 20 Sekunden anzweifeln. In diesem Fall werden die Timer angehalten
und die Spieler / Schiedsrichter prüfen, ob der Zug fehlerhaft war.
Im Falle eines fehlerhaften Zuges werden die Steine wieder vom Spielfeld
entfernt und der Gegenspieler ist wieder am Zug. War das Anzweifeln
fehlerhaft, wird keine Änderung am Spielfeld vorgenommen. Der
Gegenspieler ist wieder am Zug und erhält Strafpunkte für das falsche
Anzweifeln.

Sofern ein offensichtlich fehlerhaftes Spielfeld erkannt wird (z.B.
Lücken zwischen den Buchstaben), wird in dies der Browser-Anzeige dies 
gekennzeichnet. Die Punkteberechnung kann dann nicht mehr korrekt durchgeführt 
werden.

Der Status des Spiels kann in einem Browser dargestellt werden.
Damit können sich interessierte Zuschauer in das Spiel zuschalten und
sich den bisherigen Spielverlauf anschauen. Hierzu muss die Browser-Anwendung
auf einem separatem Server gehostet werden. Jeweils nach einem Zug erfolgt
dann ein Upload des Spielstandes per FTP. Dies kann per Konfiguration ein- bzw.
ausgeschaltet werden.

Die Log-Informationen des Spiels werden rotierend gespeichert,
damit möglichst kein Überlauf der SD Karte eintritt.

Eine Korrektur der Züge/Steine wird unterstützt. Sofern ein Buchstabe bei
der Bildanalyse "besser" erkannt wird, wird geprüft, in welchem Zug dieser
Stein gesetzt wurde. In diesem und allen nachfolgenden Zügen wird dann der 
Stein korrigiert und eine Neuberechnung der Punkte ausgelöst.

Die Eingabe von Spielernamen kann vor dem Start des Spiels auf dem Scrabble-Brett
vorgenommen werden. Hierzu wird der Spielername vor Beginn des Spiels auf 
das Spielfeld gelegt, und dann über die Buchstabenerkennung als Spielername
gesetzt.

Das Spiel kann durch einen separaten Schalter zurückgesetzt werden bzw. der 
Rechner kann über einen weiteren Schalter neu gestartet werden.


## Hardware

Folgende Hardware habe ich für den Aufbau des ersten Prototypen verwendet
(Preise und Links Stand 6/2019):

*   [Scrabble Spiel (ca. 30,-- €)](https://www.amazon.de/Mattel-Y9598-Scrabble-Original-Kreuzwortspiel/dp/B009NFGI5Y)
*   [Raspberry Pi 3 (ca. 32,-- €)](https://www.amazon.de/Raspberry-Pi-Model-ARM-Cortex-A53-Bluetooth/dp/B01CD5VC92)
*   passendes Netzteil (ca. 10,-- €)
*   ggf. Gehäuse für den Raspberry PI (ca. 5,-- €)
*   [RPI Camera v1.3 (ca. 8,-- €)](https://www.amazon.de/gp/product/B01M6UCEM5)
*   [Kamera-Tasche (ca. 6,50 €)](https://www.amazon.de/gp/product/B00IJZJKK4/)
*   [Verlängerung Kamera-Anschluss (ca. 6,-- €)](https://www.amazon.de/gp/product/B071213Q35)
*   [Elektronik Bauteile für den Prototyp (ca. 13,-- €)](https://www.amazon.de/gp/product/B01J79YG8G)
*   [4 Bit Digital Tube LED Display Modul I2C mit Clock Display (ca. 7,50 € für 5 Stück)](https://www.amazon.de/AZDelivery-Digital-Display-Arduino-Raspberry/dp/B078S7Q6X7)
*   [EG STARTS 6X American Style Standard Arcade Tasten (ca. 10,-- €)](https://www.amazon.de/dp/B07GBSJX2H)
*   [RTC für den Raspberry PI (ca. 6,50€)](https://www.amazon.de/gp/product/B01M2B7HQB)
*   Tischlampe (ca. 20,-- €) als Halter für die Kamera
*   Tastatur, Maus, Monitor

*Hinweis:* Die (Amazon-)Links sind keine Affiliate-Links, sondern sind
Links auf die von mir verwendeten Produkte.

*Hinweis:* Den Kamera-Ausschnitt der Kamera-Tasche habe ich vergrößert,
da die Passgenauigkeit nicht besonders gut war.

*Hinweis:* sofern andere Produkte genutzt werden (z.B. eine USB WebCam)
müssen u.U. Anpassungen am Code vorgenommen werden. Ebenso müssten bei
der Verwendung der RPI Camera v2.1 Anpassungen in der Geometrie des
Aufbaus, als auch im Programm-Code vorgenommen werden.


# Lizenz

 This program is free software: you can redistribute it and/or modify  
 it under the terms of the GNU General Public License as published by  
 the Free Software Foundation, version 3.

 This program is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of 
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 General Public License for more details.

 You should have received a copy of the GNU General Public License 
 along with this program. If not, see \<http://www.gnu.org/licenses/\>.
