#!/usr/bin/env python

import pygame.midi
import time

pygame.midi.init()

print pygame.midi.get_default_output_id()
print pygame.midi.get_device_info(0)

player = pygame.midi.Output(0)

player.set_instrument(0)

print 'Playing...'

player.note_on(64, 127)
time.sleep(1)
player.note_off(64, 127)

print 'Played'

pygame.midi.quit()
