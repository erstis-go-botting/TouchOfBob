Installation Procedure
==========

###### Get Python 2.7!

Python kann hier heruntergeladen werden:

[Get Python 2.7](http://www.python.org/getit/)

Wir brauchen Python 2.7. Welche Version von 2.7 hängt vom verfügbaren Betriebsystem ab.


###### Get EasyInstall:

[Easy Install](https://pypi.python.org/pypi/setuptools#installation-instructions)

Hier kann EasyInstall heruntergeladen werden. 
Bei allen Betriebssytemen (alle = Windows, Linux, Mac) wird empfohlen ez_setup.py herunterzuladen und auszuführen. 

Dies ist aber auch unter obigem Link erklärt.

Um zu sehen, ob eine Installation erfolgreich war, kann man schauen ob im Installationsordner von Python (unter 
Windows: C:\Python27\) einen Ordner namens "Scripts" und darin easy_install.exe existiert.

EasyInstall kann so benützt werden:
[using easy install](https://pythonhosted.org/setuptools/easy_install.html#downloading-and-installing-a-package)

###### BeautifulSoup4 & Mechanize:

Für den Bot brauchen wir die Module BeautifulSoup4 (für das Parsing von html, yay!) und Mechanize (um einen Webbrowser
emulieren zu können).

Im Prinzip funktioniert die Installation dieser Module mit dem Befehl "easy\_install BeautifulSoup4" und "easy\_install 
mechanize".

Unter Windows muss man unter Umständen mit der Konsole zuerst in das "C:\Python27\Scripts" Verzeichnis navigieren, was mit dem 
"cd" Befehl geht. Alternativ dazu kann man auch den Ordner, in dem easy_install.exe liegt öffnen und mit Shift-Rechtsklick 
direkt eine Konsole vor Ort öffnen.

Um zu prüfen, ob die Installationen erfolgreich waren, kann man eine Pythonkonsole öffnen und die Befehle
"import mechanize" sowie "import BeautifulSoup" ausführen. Sollten beide Befehle keine Fehlermeldung zurückgeben,
könnte die Installation erfolgreich gewesen sein. Das ist toll!
