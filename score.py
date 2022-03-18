rank_types = ('AAA','AA+','AA','AA-','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','E','-')
combo_types = ('MFC','PFC','FC','GFC','Life4','NoFC')

class Song(object):

    def __init__(self, old_val, new_val):
        # These values stay constant, can use either old or new
        self.name = ' '.join(map(str, reversed(old_val[6:])))
        self.chart = old_val[5]
        self.difficulty = old_val[4].strip('()')
        self.maxcombo = 0 # need to parse this from fmt_scores()
        # tuple (old, new)  - could consider a third bool value to encapsulate improvement instead of separate values (eg upscore) but tuples are immutable?
        self.ranks = (old_val[3], new_val[3])
        self.scores = self.fmt_scores(old_val[2], new_val[2]) # returns tuple like others
        self.combos = (old_val[1], new_val[1])
        self.plays = self.fmt_playcounts(old_val[0], new_val[0]) # returns tuple like others
        self.upscore, self.uprank, self.upcombo = self.diff()  # returns bool
#        self.uprank = self.check_uprank()

    def diff(self):
        upscore = uprank = upcombo = 0
        if self.scores[0] < self.scores[1]:
            upscore = self.scores[1] - self.scores[0]
        if self.ranks[0] != self.ranks[1]:
        #if rank_types.index(self.ranks[0]) < rank_types.index(self.ranks[1]) this logic isn't exactly necessary as SM A is smart about overwriting good values only; similar tuple exists for combos
            uprank = True
        if self.combos[0] != self.combos[1]:
            upcombo = True 
        return upscore, uprank, upcombo

# Overriding built-in to accomodate using sorted()
#    def __lt__(self):
#        return self.upscore < updated.upscore

    # could probably clean these up using named tuples
    def fmt_scores(self, old, new):
        return (int(old.replace(',', '')[:7]), int(new.replace(',', '')[:7]))
    
    def fmt_playcounts(self, old, new):
        return (int(old.strip('()')[-4:]), int(new.strip('()')[-4:]))


def output(prev, updated):  # could probably change this to stale, updated
    songs_changed = []
    songs_prev = prev.splitlines()
    songs_updated = updated.splitlines()  
    assert len(songs_prev) == len(songs_updated) # add error handling to this

    for idx in range(len(songs_prev)):
        song = Song(songs_prev[idx].split()[::-1], songs_updated[idx].split()[::-1])
        if song.upscore or song.uprank or song.upcombo:
            songs_changed.append(song)

    return sorted(songs_changed, key=lambda x: x.upscore, reverse=True) # add secondary sort for difficult or fullcombo