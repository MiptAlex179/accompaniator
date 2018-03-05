import pickle


class Note:
    """ Stores individual note
    Attributes:
        number: MIDI number of note
    """

    def __init__(self, number):
        self.number = number

    def freq(self):
        """ Returns frequency in Hz """
        return 2 ** ((self.number - 69) / 12.) * 440

    def __str__(self):
        return "%s" % (self.number)

    def __repr__(self):
        return self.__str__()

    number = None


class Chord:
    """Stores a chord and its length in 1/128 beats"""

    def __init__(self, notes_list, duration, velocity):
        self.notes = notes_list[:]
        self.velocity = velocity
        self.duration = duration

    def len(self):
        return self.duration

    def len_in_ms(self, bpm):
        """ Returns length of chord in ms given beats per minute"""
        return self.duration * bpm / (128 * 60 * 1000)

    def __str__(self):
        return "{%s %s %s}" % (self.duration, self.velocity, str(self.notes))

    def __eq__(self, other):
        return self.duration == other.duration and self.velocity == other.velocity and self.notes == other.notes

    def add_notes(self, notes_list):
        self.notes.extend(notes_list)

    duration = None
    notes = None
    velocity = None


class Track:
    """ Chords one by one """

    def __init__(self, chords=[], instrument=''):
        self.chords = chords[:]
        self.instrument = instrument

    def __str__(self):
        return "'%s' %s" % (self.track_name, self.program)

    def __repr__(self):
        return self.__str__()

    def merge_track(self, track2):
        for i in range(len(self.chords)):
            self.chords[i].add_notes(track2.chords[i].notes)
            self.instrument += " " + track2.instrument

    track_name = None
    program = None

class Instrument:
    def __init__(self, tracks=[], name=""):
        self.tracks = tracks[:]
        self.name = name

    def add_track(self, track):
        self.tracks.append(track)

    def __str__(self):
        ret = "'%s' of %d tracks" % (self.name, len(self.tracks))
        for track in self.tracks:
            ret += str(track) + '\n'

class Song:
    def __init__(self, instruments=[], bpm=0, name=""):
        self.instruments = instruments[:]
        self.name = name
        self.bpm = bpm

    def add_instrument(self, instr):
        self.instruments.append(instr)

    def del_instrument_num(self, instr_number):
        self.instruments.pop(instr_number)

    def del_instrument(self, instr):
        self.instruments.remove(instr)

    def find_instrument(self, instr_name):
        for instrument in self.instruments:
            if instrument.name == instr_name:
                return instrument
            else:
                instr = Instrument([], instr_name)
                self.add_instrument(instr)
                return self.instruments[-1]

    def del_track_num(self, track_number):
        for instrument in self.instruments:
            if len(instrument.tracks) < track_number:
                track_number -= len(instrument.tracks)
            else:
                instrument.tracks.pop(track_number)

    def del_track(self, track):
        for instrument in self.instruments:
            if track in instrument.tracks:
                instrument.tracks.remove(track)

    def dump(self, f):
        pickle.dump(self, f)

    def save(self, path):
        with open(path, 'wb') as f:
            self.dump(f)

    def undump(self, f):
        self.__dict__.update(pickle.load(f).__dict__)

    def load(self, path):
        with open(path, 'rb') as f:
            self.undump(f)

    def get_tracks(self):
        tracks = []
        for instument in self.instruments:
            tracks.append(instument.tracks)
        return tracks

    def __str__(self):
        ret = "'%s' %s %s\n" % (self.name, len(self.instruments), self.bpm)
        for t in self.instruments:
            ret += str(t) + '\n\n'
        return ret

    def __repr__(self):
        return self.__str__()

    name = None
    bpm = None
    key = None
    instruments = []
