import threading
import random
import pickle
import time
from urllib.error import HTTPError

gg = 0
cache = dict()
lock = threading.Lock()
sem = threading.Semaphore(20)
c404 = 0

fi = None
try:
    fi = open("cache.pickle", "rb")
    cache = pickle.load(fi)
except:
    print("NO CACHE")
finally:
    if fi is not None:
        fi.close()

import urllib.request
from html.parser import HTMLParser


class ArtistParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = None
        cls = False
        nx = None
        for attr in attrs:
            if attr[0].strip() == "class":
                if "rollover_link" in attr[1]:
                    cls = True
                else:
                    return
            elif attr[0].strip() == "href":
                href = attr[1].strip()
        if cls:
            self.urls.add("https://www.discogs.com" + href)

    def reset_data(self):
        self.urls = set()

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


def geturl(url):
    global gg
    global c404
    global ccc
    if url in cache:
        return cache[url]
    else:
        try:
            request = urllib.request.urlopen(
                urllib.request.Request(url,
                                       headers={'User-Agent': "xkcd-" + str(random.randint(1, 1000000000000))}),
                timeout=5)
            response = request.read().decode(encoding="utf-8")
            cache[url] = response
            gg += 1
            return response
        except HTTPError as ex:
            if ex.code == 404:
                c404 += 1
            return None
        except Exception as ex:
            return None


ok_pages = []
failures = []
allurls = set()


def load_all_artists(piname):
    fi = open(piname, "rb")
    urls = pickle.load(fi)
    ap = ArtistParser()
    i = 0
    for url in urls:
        i += 1
        ap.feed(urls[url])
        allurls.update(ap.urls)
        ap.reset_data()
        print(i, len(allurls))
    del urls


if __name__ == "__main__":
    try:
        load_all_artists("cache.pickle")
    except Exception as ex:
        pass
    finally:
        fi = open("cache.pickle", "wb")
        pickle.dump(cache, fi)
        fi.close()

        fi = open("artisturls.pickle", "wb")
        pickle.dump(allurls, fi, 2)
        fi.close()
