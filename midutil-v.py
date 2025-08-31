# write_progressions_midiutil.py
# pip install midiutil

from midiutil import MIDIFile

progressions = [
    ["F#m", "G#dim", "F#"],
    ["D", "G#dim", "F#m"],
    ["D", "G#dim", "C#m"],
    ["D", "G#dim", "Bm"],
    ["A", "G#dim", "C#m"],
]

CHORDS = {
    "F#m": ["F#", "A", "C#"],
    "G#dim": ["G#", "B", "D"],
    "F#": ["F#", "A#", "C#"],
    "D": ["D", "F#", "A"],
    "C#m": ["C#", "E", "G#"],
    "Bm": ["B", "D", "F#"],
    "A": ["A", "C#", "E"],
}

NOTE_TO_MIDI = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
    "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71,
}

track = 0
channel = 0
tempo = 120
volume = 100

mf = MIDIFile(1)
mf.addTempo(track, 0, tempo)
mf.addProgramChange(track, channel, 0, 0)

t = 0.0
dur = 1.0  # quarter note
gap = 0.25

for prog in progressions:
    for symbol in prog:
        notes = [NOTE_TO_MIDI[n] for n in CHORDS[symbol]]
        for n in notes:
            mf.addNote(track, channel, n, t, dur, volume)
        t += dur + gap
    t += 0.5  # extra space between progressions

with open("progressions_midiutil.mid", "wb") as out:
    mf.writeFile(out)

print("Wrote progressions_midiutil.mid")
