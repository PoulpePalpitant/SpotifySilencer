#!/usr/bin/env python3.9

import os   # File manip
import random
from math import fabs, trunc
from time import (sleep, time)

# Mute windows
import pygetwindow as gw
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# import simpleaudio as sa
from pydub import AudioSegment  # Conversion en mp3
from pygame import mixer        # audio player


"""
Dependencys: Downloader ffmpeg et installer sur le path
pip install p
"""

# HOW IT WORKS:
# Pour savoir quand muter l'application, on utilise simplement le titre de la fenêtre.
# Si le nom de la fenêtre est 'Spotify Free' ou 'Advertisement', ça veut dire que spotify est en mode pause ou qu'une publicité joue.
# Il semblerait qu'avoir le focus sur le fenêtre quand une publicité joue change parfois le nom de la fenêtre pour 'Spotify Free' à la place.
# Autrement, si la fenêtre fait jouer de la musique, le titre de la fenêtre change pour le nom de la chanson et l'artiste
# Il peut aussi arriver qu'une publicité change le titre de la fenêtre pour un autre nom quand c'est une pub. Dans ces cas, le silencer ne fonctionnera pas....

# Idées pour rendre ça plus nice:
# Faire 1 seul petit bip (ou autre jolie son) quand la fenêtre est pausé pour signifier qu'une playlist est terminé.
# Remplacer le son de la pub par autres affaires custom, aux choix de l'utilisateur
# Trouver un moyen de détecter si spotify en mode pause, pour ne pas faire jouer du beat si c'est le cas 
# - qu'aucun son ne sort de la fenêtre?
# Ton programme est confu quand ya deux mixer(pub audio et pub video)

# Si tu veux que le script ne génère pas de console, même après la génération du fichier exe, change l'extension pour .pyw
# --------------------------------------------------------------------------------------------------------------------------------------- --- -

def GetDaMusica():
    musicaDirectori = os.getcwd() + "\\audio\\"
    daSong = random.choice(os.listdir(musicaDirectori))
    daPath = musicaDirectori + daSong
    return daPath

def ExtractFileExtension(path):
    format = os.path.splitext(path)[1]
    format = ''.join(format.split('.', 1))  # enlève le tit point
    return format

def ConvertSongToMp3(directory, fileName):
    format = ExtractFileExtension(fileName)
    path = directory + fileName

    if format == "mp3":
        return 
    
    print("Converting \"" + fileName + "\" to mp3")

    audio = None
    if format == "wav":
        audio = AudioSegment.from_wav(path)
    elif format == "ogg":
        audio = AudioSegment.from_ogg(path)
    elif format == "flv":
        audio = AudioSegment.from_flv(path)
    elif format == "mp4":
        audio = AudioSegment.from_file(path, format)
    elif format == "wma":
        audio = AudioSegment.from_file(path, format)
    elif format == "aac":
        audio = AudioSegment.from_file(path, format)
    elif format == "m4a":
        audio = AudioSegment.from_file(path, format)
    
    if audio:
        songNameWithoutExtension = os.path.splitext(path)[0]
        audio.export(songNameWithoutExtension + ".mp3", format="mp3")
        os.remove(path)
    else:
        print("File format couldn't be converted to mp3")
    
def ConvertSongsToMp3(directory):
    print("Converting all audio files to mp3. This may take awhile...")
    progressCallback = None

    for f in os.listdir(directory):
        ConvertSongToMp3(directory, f)
    
    print("Files are done!")
    
def FindSpotifyWindow():
    for i in range(2):
        if i % 2 == 0:
            # Retourne une liste de fenêtre avec ce nom
            spotify = gw.getWindowsWithTitle('Spotify Free')
        else:
            # Les deux noms faciles à trouver
            spotify = gw.getWindowsWithTitle('Advertisement')

        if spotify != []:
            print('Fenêtre spotté!')
            return spotify[0]

    print("Fenêtre introuvable. Pèse sur pause et je vais la trouver (:")
    return None


def FindVolumeControl():
    volumControl = id = None
    
    sessions = AudioUtilities.GetAllSessions()
    for s in sessions:
        if s.Process:
            if s.Process.name() == 'Spotify.exe':
                volumControl = s.SimpleAudioVolume
                id = s.ProcessId
                break

    # Spotify n'apparaît dans le mixer de windows qu'uniquement si elle à produit du son.
    if volumControl == None:
        print("Volume de spotify non détecté. Pèse sur Play et je vais le trouver :)")
    else:
        print("Volume spotté!")

    return volumControl, id

def MuteVideoAdsIfPlaying(id):
    volumControlForVideoAds = None    
    sessions = AudioUtilities.GetAllSessions()
    
    for s in sessions:
        if s.Process:
            if s.Process.name() == 'Spotify.exe':
                if s.ProcessId != id:
                   volumControlForVideoAds = s.SimpleAudioVolume
                   break   

    if volumControlForVideoAds == None:
        return False

    volumControlForVideoAds.SetMute(1,None)
    print("Volume de publicité vidéo spotté, et muté à tout jamais")
    return True


def IsAdPlaying(windowTitle):
    possibleNames = ["Advertisement", "Spotify", "Spotify Free"]

    for n in possibleNames:
        if windowTitle == n:  # Pas de chanson qui joue
            return True
    return False

def SongPlaying(windowTitle):
    """
        Quand une chanson joue, le format du windowTitle est toujours le même:
        Artist - Song name
        La string " - " est toujours présente. 
        Lorsqu'une pub joue ou que l'application est en pause, cette string n'est jamais ou très très rarement utilisé
    """
    theUltimateCharacter = ' - '
    return theUltimateCharacter in windowTitle


if __name__ == '__main__':
    spotifyWindow = FindSpotifyWindow()
    volumControl, spotifyProcessId = FindVolumeControl()  # Va permettre de muté Spotify dans le mixer de windows
    videoAdsAreMuted = False  
    mixer.init()
    
    # Converti tout les fichiers du folder audio en mp3, si possible
    ConvertSongsToMp3((os.getcwd() + "\\audio\\"))

    while(True):
        if spotifyWindow == None:
            spotifyWindow = FindSpotifyWindow()

        if volumControl == None:
            volumControl, spotifyProcessId = FindVolumeControl()


        if volumControl != None and spotifyWindow != None:
            if not SongPlaying(spotifyWindow.title):  # Pas de chanson qui joue, alors ad ou pause
                if videoAdsAreMuted == False:
                    videoAdsAreMuted = MuteVideoAdsIfPlaying(spotifyProcessId)

                if volumControl.GetMute() == False:
                    volumControl.SetMute(1, None)   # mute
                    print("Ad playing, or paused...")
                    if spotifyWindow.title != 'Spotify Free':  # Fais pas jouer de beat au cas où c'était un pause
                        intermission = GetDaMusica()
                        mixer.music.load(intermission)
                        mixer.music.play()
                        print("--- Playing intermission ---\n")
                        print(f'"---{intermission}---\n"')
            else:
                if volumControl.GetMute() == True:
                    volumControl.SetMute(0, None)   # unmute
                    print("--- Intermission ended ---\n")
                    print("Song playing")
                    mixer.music.fadeout(1000)

        sleep(1.5)
