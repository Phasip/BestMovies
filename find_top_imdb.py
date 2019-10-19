#!/usr/bin/python3
# Function: best_movies_imdb 
# Input: a filter function (see default_filter)  and the files from https://datasets.imdbws.com/
# Output: A generator that returns dicts of the form: {'tconst': 'tt0252487', 'numVotes': '34359', 'averageRating': '9.4'}

import gzip
def default_imdb_filter(d,dict_type):
    #basics  -> tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
    if dict_type == 'basics':
        if d['isAdult'] != "0":
            return False
        if d['titleType'] != "movie":
            return False
            
    #ratings -> tconst	averageRating	numVotes
    if dict_type == 'ratings':
        if float(d['averageRating']) < 7:
            return False
        if int(d['numVotes']) < 50000:
            return False
            
    return True
    
def best_movies_imdb(fltr=default_imdb_filter, ratings='title.ratings.tsv.gz', basics='title.basics.tsv.gz'):
    line_map = {}
    r = []
    
    with gzip.open(ratings,'rt') as f:
        hdr = (f.readline().strip()).split("\t")
        for line in f:
            line = str(line)
            vals = line.strip().split("\t")
            d = dict(zip(hdr, vals))
            if fltr is not None and not fltr(d,'ratings'):
                continue
            line_map[d['tconst']] = d

    with gzip.open(basics,'rt') as f:
        hdr = (f.readline().strip()).split("\t")
        for line in f:
            vals = line.strip().split("\t")
            d = dict(zip(hdr, vals))
            if fltr is not None and not fltr(d,'basics'):
                continue
            if d['tconst'] in line_map:
                r.append(line_map[d['tconst']])
            
    for line in sorted(r,reverse=True,key=lambda x:float(x['averageRating'])):
        yield line

if __name__ == "__main__":
    for d in best_movies_imdb():
        print("%s\t%s\t%s"%(d['tconst'],d['averageRating'],d['numVotes'],))
