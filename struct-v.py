# write_progressions_struct.py
# Creates progressions_struct.mid using only the stdlib (struct, no MIDI libs)

import struct

# --- Progressions as lists ---
progressions = [
    ["F#m", "G#dim", "F#"],
    ["D", "G#dim", "F#m"],
    ["D", "G#dim", "C#m"],
    ["D", "G#dim", "Bm"],
    ["A", "G#dim", "C#m"],
]

# --- Chord definitions (triads) ---
CHORDS = {
    "F#m": ["F#", "A", "C#"],
    "G#dim": ["G#", "B", "D"],
    "F#": ["F#", "A#", "C#"],  # major; change to F#m above when needed
    "D": ["D", "F#", "A"],
    "C#m": ["C#", "E", "G#"],
    "Bm": ["B", "D", "F#"],
    "A": ["A", "C#", "E"],
}

# --- Note name -> MIDI number (octave 4 triads) ---
NOTE_TO_MIDI = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
    "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71,
}

# helpers
def vlq(n: int) -> bytes:
    buf = n & 0x7F
    out = []
    while n >> 7:
        n >>= 7
        out.insert(0, 0x80 | (n & 0x7F))
    out.append(buf)
    return bytes(out)

def meta(delta, meta_type, data=b""):
    return vlq(delta) + bytes([0xFF, meta_type]) + vlq(len(data)) + data

def note_on(delta, note, vel, ch=0):
    return vlq(delta) + bytes([0x90 | ch, note, vel])

def note_off(delta, note, vel, ch=0):
    return vlq(delta) + bytes([0x80 | ch, note, vel])

def program_change(delta, program, ch=0):
    return vlq(delta) + bytes([0xC0 | ch, program])

def mthd(num_tracks=1, division=480):
    return b"MThd" + struct.pack(">IHHH", 6, 0, num_tracks, division)

def mtrk(data: bytes):
    return b"MTrk" + struct.pack(">I", len(data)) + data

# build one track
division = 480
events = bytearray()
events += meta(0, 0x51, struct.pack(">I", 500000)[1:])  # tempo 120 bpm (500000 us/qn)
events += program_change(0, 0)  # Acoustic Grand

chord_len = division  # one quarter note
gap = division // 2   # short gap between chords

for prog in progressions:
    for symbol in prog:
        notes = [NOTE_TO_MIDI[n] for n in CHORDS[symbol]]
        for n in notes:
            events += note_on(0, n, 96)
        events += note_off(chord_len, notes[0], 64)
        for n in notes[1:]:
            events += note_off(0, n, 64)
        # gap
        events += vlq(gap)  # rest before next chord
    # slightly longer rest between progressions
    events += vlq(division)

events += meta(0, 0x2F)  # end of track

with open("progressions_struct.mid", "wb") as f:
    f.write(mthd(1, division))
    f.write(mtrk(bytes(events)))

print("Wrote progressions_struct.mid")
