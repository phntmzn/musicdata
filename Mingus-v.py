# write_progressions_mingus.py
# pip install mingus

from mingus.containers import NoteContainer, Bar, Track
from mingus.midi import MidiFileOut

progressions = [
    ["F#m", "G#dim", "F#"],
    ["D", "G#dim", "F#m"],
    ["D", "G#dim", "C#m"],
    ["D", "G#dim", "Bm"],
    ["A", "G#dim", "C#m"],
]

CHORDS = {
    "F#m": ["F#-4", "A-4", "C#-5"],
    "G#dim": ["G#-4", "B-4", "D-5"],
    "F#": ["F#-4", "A#-4", "C#-5"],
    "D": ["D-4", "F#-4", "A-4"],
    "C#m": ["C#-4", "E-4", "G#-4"],
    "Bm": ["B-3", "D-4", "F#-4"],
    "A": ["A-3", "C#-4", "E-4"],
}

track = Track()
bpm = 120

# 3 chords per bar (3/4), each a quarter note
for prog in progressions:
    bar = Bar(key='F#', meter=(3, 4))
    for symbol in prog:
        nc = NoteContainer(CHORDS[symbol])
        ok = bar.place_notes(nc, 4)
        if not ok:
            # if bar filled (shouldn't happen with 3 slots), start a new bar slot
            track.add_bar(bar)
            bar = Bar(key='F#', meter=(3, 4))
            bar.place_notes(nc, 4)
    track.add_bar(bar)
    # spacer bar (rest)
    spacer = Bar(key='F#', meter=(3, 4))
    track.add_bar(spacer)

MidiFileOut.write_Track("progressions_mingus.mid", track, bpm=bpm)
print("Wrote progressions_mingus.mid")
