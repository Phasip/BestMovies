#!/usr/bin/python3
# Function: best_magnet_links 
# Input: Parameters for best_movies_imdb, max result to return and a rarbg filter (see default_rarbg_filter)
# Output: A generator that returns tuples of the form: ('tt0252487', 'magnet:xxxx')

from find_top_imdb import best_movies_imdb, default_imdb_filter
import rarbgapi
import json
import sys

client = rarbgapi.RarbgAPI()

categories = ";".join(map(str,[
    rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_4K,
    rarbgapi.RarbgAPI.CATEGORY_MOVIE_H265_4K,
    rarbgapi.RarbgAPI.CATEGORY_MOVIE_H265_4K_HDR,
    rarbgapi.RarbgAPI.CATEGORY_MOVIE_FULL_BD,
    rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_1080P,
]))

def default_rarbg_filter(d):
    if int(d['ranked']) != 1:
        return False
    size_gb = float(d['size'])/(1024**3)
    if size_gb < 3 or size_gb > 16:
        return False
    return True

def best_magnet_links(max_count=1000,rarbg_filter=default_rarbg_filter, categories=categories, imdb_filter=default_imdb_filter, ratings='title.ratings.tsv.gz', basics='title.basics.tsv.gz'):
    for idx,d in enumerate(best_movies_imdb(fltr=imdb_filter,ratings=ratings, basics=basics)):
        if idx > max_count:
            break
        torrent_options = []
        for r in client.search(search_imdb=d['tconst'],format_="json_extended", category=categories):
            if rarbg_filter is not None and not rarbg_filter(r._raw):
                continue
            seeders = int(r._raw['seeders'])
            size = int(r._raw['size'])
            download = r.download
            torrent_options.append((seeders,size,download))
            
        if len(torrent_options) == 0:
            print("Failed to find: %s"%(d['tconst']), file=sys.stderr)
        else:
            best = sorted(torrent_options,reverse=True)[-1]
            yield (d['tconst'],best[2])

if __name__ == "__main__":
    for _,magnet in best_magnet_links():
        print(magnet)
