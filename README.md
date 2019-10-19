BestMovies
-------------
This repo contains two scripts:

One that builds a list of the top rated movies
from imdb based on data from https://datasets.imdbws.com/ and a provided filter.

Another that uses said list and outputs magnet links from rarbg for the top
n movies. (Filtering links based on size & seeders)


How to Use
----------------
```
cd BestMovies
wget https://datasets.imdbws.com/title.basics.tsv.gz
wget https://datasets.imdbws.com/title.ratings.tsv.gz
pip3 -U install rarbgapi
python3 ./rarbg_top_imdb.py
```
