from mingus.midi import fluidsynth

fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2')

fluidsynth.play_Note(64,0, 100)
