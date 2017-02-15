#!/usr/bin/env python3

import sys

from getch import getch
import pyglet

SOUND_DIR = "media/buzzer_sound/"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def regain_control(dt):
    pyglet.app.exit()

def play_sound(media):
    media.play()
    pyglet.clock.schedule_once(regain_control, media.duration)
    pyglet.app.run()

class Buzzd(object):

    def __init__(self, t):
        self.teams = t
        self.mapping = -1 # team array + this offset means key return correct team
        self.quit_key = 'q'
        self.state = 'locked'

        # buzzer sounds
        buzz_team1 = pyglet.resource.media(SOUND_DIR + 'wooou.wav', streaming=False)
        buzz_team2 = pyglet.resource.media(SOUND_DIR + 'oh_shit_2.wav', streaming=False)
        buzz_team3 = pyglet.resource.media(SOUND_DIR + 'wooo_wooo.wav', streaming=False)
        self.buzz_teams = [buzz_team1, buzz_team2, buzz_team3]


    def Run(self):
        print("{} // {} // {}".format(*self.teams))
        print("Buzzd ready...\nState: locked")
        while True:

            # grab key events (blocking)
            key = getch()

            if self.state == 'game_on':
                if key in '123':
                    print("Win: {}{}{}".format(bcolors.FAIL,
                        self.teams[int(key) + self.mapping],
                        bcolors.ENDC))
                    play_sound(self.buzz_teams[int(key) + self.mapping])
                    self.state = 'locked'
                    #print("Locked!")

            if self.state == 'locked' and key == ' ':
                print("Game on!")
                self.state = 'game_on'

            if key == self.quit_key:
                break



if __name__ == "__main__":

    #import ipdb; ipdb.set_trace()
    b = Buzzd(sys.argv[1:4])
    b.Run()
