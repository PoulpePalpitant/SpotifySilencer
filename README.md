# Spotify-silencer
Ce programme vise à muter la version gratuite de Spotify quand l'application fait jouer des publicités

Pour générer un EXE avec un fichier python:

pip install pyinstaller

En ligne de commande
	pyinstaller monfichier.py
	pyinstaller --clean monfichier.py		// pas de temp files
	pyinstaller --clean monfichier.py -F		// 1 seul file
	pyinstaller -F --add-binary "C:\Users\Moi\AppData\Local\Programs\Python\Python39.dll" myscript.py // ajoute le path de ta version de python



ou utiliser ça https://stackoverflow.com/questions/41570359/how-can-i-convert-a-py-to-exe-for-python


libs installed:
pip install pipwin // bad
pipwin install pyaudio // bad


pip install pygames // ok
pip install pydub  v0.25.1 // ok
pip install ffmpeg-python // to convert mp3