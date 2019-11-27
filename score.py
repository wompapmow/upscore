class Song(object):
    def __init__(self, parts, update=False):
        self.name = ' '.join(map(str, reversed(parts[6:])))
        self.chart = parts[5]
        self.difficulty = parts[4].strip('()')
        self.rank = parts[3]
        self.score = int(parts[2].replace(',', '')[:7])
        self.combo = parts[1]
        self.playcount = int(parts[0].strip('()')[-4:])
        self.upscore = 0
        self.uprank = None
        self.upcombo = None
        if self.rank == '-':
            self.rank = ''

    def __lt__(self, other):
        return self.upscore < other.upscore

    def diff(self, other):
        if other.score > self.score:
            self.upscore = other.score-self.score
            if other.rank != self.rank:
                self.uprank = other.rank
            if other.combo != self.combo:
                self.upcombo = other.combo

def output(before, after):
    songs = {}

    for line in before.splitlines():
        try:
            song = Song(line.split()[::-1])
            songs[f'{song.name} {song.chart}'] = song
        except:
            pass

    for line in after.splitlines():
        try:
            song = Song(line.split()[::-1])
            k = f'{song.name} {song.chart}'
            if songs[k]:
               songs[k].diff(song)
        except:
            pass

    return sorted(songs.values(), reverse=True)
        # return f'{song.name} {song.chart} {song.difficulty}: +{song.upscore}'
