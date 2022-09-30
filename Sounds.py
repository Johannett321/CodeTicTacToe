import pygame


class AudioPlayer:
    music_player = None
    sound_effect_player = None

    def __init__(self):
        pygame.mixer.init()

    def play_menu_music(self):
        pygame.mixer.music.load("audio/menu.wav")
        pygame.mixer.music.play(loops=0)

    def play_battle_music(self):
        pygame.mixer.music.load("audio/battle.wav")
        pygame.mixer.music.play(loops=100)

    def play_winning_music(self):
        pygame.mixer.music.load("audio/win.wav")
        pygame.mixer.music.play(loops=0)

    def play_losing_music(self):
        pygame.mixer.music.load("audio/lose.wav")
        pygame.mixer.music.play(loops=0)

    def play_pop_sound_effect(self):
        pygame.mixer.Sound("audio/pop.wav").play()

    def stop_music(self):
        print("Test")
        pygame.mixer.music.stop()
