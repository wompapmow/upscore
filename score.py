class Song(object):
    def __init__(self, parts, update=False):
        self.name = ' '.join(map(str, reversed(parts[6:])))
        self.chart = parts[5]
        self.difficulty = parts[4].strip('()')
        self.grade = parts[3]
        self.score = int(parts[2].replace(',', '')[:7])
        self.combo = parts[1]
        self.playcount = int(parts[0].strip('()')[-4:])
        self.upscore = 0

    def __lt__(self, other):
        return self.upscore < other.upscore

    def diff(self, other_score):
        if other_score > self.score:
            self.upscore = other_score-self.score

def output(before, after):
    songs = {}

    for line in before.splitlines():
        song = Song(line.split()[::-1])
        songs[f'{song.name} {song.chart}'] = song

    for line in after.splitlines():
        song = Song(line.split()[::-1])
        k = f'{song.name} {song.chart}'
        if songs[k]:
           songs[k].diff(song.score)

    return sorted(songs.values(), reverse=True)
        # return f'{song.name} {song.chart} {song.difficulty}: +{song.upscore}'
