import pickle, mysql.connector, re

from parseMusic import MusicParser

i = 0
"""conn = mysql.connector.connect(user='root', password='1234',
                                  host='localhost',
                                  database='eestech_challenge')"""
conn = None
parser = MusicParser()


def processHTML(url, urlcont):
    global i
    parser.feed(urlcont)
    RAID = re.search('^.*com/([^/]+)/.*$', url)
    ID = re.search('^.*/([^/]+)$', url)
    # print "\n\n", url
    parser.apply(RAID.group(1), ID.group(1), conn)
    parser.reset()
    # i += 1
    # if i > 0:
    #     exit(0)


fi = open("albums_merged.pickle", "rb")
albums_map = pickle.load(fi)
fi.close()

files = ["caches_nocroatia.pickle", "caches_croatia.pickle"]
fi = open(files[1], "rb")
caches = pickle.load(fi)
fi.close()

co = 0
for country in albums_map:
    for url in albums_map[country]:
        if url in caches:
            co += 1
            if co % 50 == 0:
                print '\r' + str(co)
            processHTML(url, caches[url])

if conn:
    conn.close()
