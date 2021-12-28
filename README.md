# Spotify-silencer
Ce programme vise à remplacer les publicités audio de la version gratuite de Spotify pas des sons paisibles et agréables ♥

## Comment ça marche?
Pour savoir quand muter l'application, on utilise simplement le titre de la fenêtre.
Quand une chanson joue, la fenêtre spotify change toujours son titre pour ce format
- nom_artist - nom_chanson

On utilise donc la string " - " pour détecter à quel moment muter la fenêtre.

# Idées pour optimisation:
- Différencier quand l'application est en pause et quand elle fait joué une publicité. 
- Faire 1 seul petit bip (ou autre jolie son) quand la fenêtre est pausé pour signifier qu'une playlist est terminé.
- Faire un launcher custom qui lance Spotify et SpotifySilencer en même temps
- Minimiser l'application dans le tray windows

- Faire un GUI/CLI. Ceci permettrait de:
	- Éditer le dossier audio pour ajouter et supprimer des chansons
	- Pouvoir Enable/disable le SpotifySilencer
	- Contrôle volume et (ironiquement) de muter le SpotifySilencer
	- Création de playlist à faire jouer durant les pubs
	- Donner l'option de pouvoir launcher ce programme au lancement de windows


Dependencys: 
 - pygames 	-> Audio player
 - pycaw 		-> Manipulation mixer windows
 - pydub  v0.25.1 -> Conversion mp3
 - ffmpeg-python // Conversion mp3. Installé sur le path