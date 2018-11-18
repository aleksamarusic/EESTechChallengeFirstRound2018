#!/usr/bin/env python3
import threading
import random
import pickle
import time
import loadDatabase
from urllib.error import HTTPError

gg = 0
cache = dict()
albums = dict()
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

albfi = None
try:
    albfi = open("albums.pickle", "rb")
    albums = pickle.load(albfi)
except:
    print("NO CACHE")
finally:
    if albfi is not None:
        albfi.close()


import urllib.request
from html.parser import HTMLParser


class NemaGrada(Exception): pass  # U slučaju da ne nađe mesto


class ParserZaVreme(HTMLParser):


    def __init__(self):
        HTMLParser.__init__(self)
        self.urls = []
        self.next = None

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = None
        cls = False
        nx = None
        for attr in attrs:
            if attr[0].strip() == "class":
                if "search_result_title" in attr[1]:
                    cls = True
                elif "pagination_next" in attr[1]:
                    nx = True
                else:
                    return
            elif attr[0].strip() == "href":
                href = attr[1].strip()
        if cls:
            self.urls.append("https://www.discogs.com" + href)
        elif nx:
            self.next = "https://www.discogs.com" + href
        pass

    def reset_data(self):
        self.urls = []
        self.next = None

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


def page_getter(pgid, country, asc):
    global lock
    if asc:
        asc = "asc"
    else:
        asc = "desc"
    url = "https://www.discogs.com/search/?sort=title%2C" + asc + "&page=" + str(pgid) + "&country_exact=" + country
    stranica = geturl(url)
    if stranica is None:
        failures.append(pgid)
        return
    parser = ParserZaVreme()
    parser.feed(stranica)
    print("DONE: ", pgid)
    ok_pages.append(pgid)
    lock.acquire()
    if country in albums:
        albums[country].update(parser.urls)
    else:
        albums[country] = set(parser.urls)
    lock.release()


def album_getter(alb_url, rd=0):
    global gg
    global lock
    if alb_url in cache:
        return
    sem.acquire()
    url = alb_url
    print("GETTING")
    stranica = geturl(url)
    if stranica is None:
        if rd == 2:
            print("ENDFAIL")
            failures.append(alb_url)
            sem.release()
            return
        else:
            sem.release()
            print("SLEEPFAIL")
            time.sleep(5)
            album_getter(alb_url, rd + 1)
            return
    sem.release()
    print("DONE: ", gg)


def get_list_of_albums(country, no_of_pages, stride=50, asc=True):
    for i in range(1, no_of_pages, stride):
        threads = []
        for j in range(i, i + stride):
            threads.append(threading.Thread(target=page_getter, args=(j, country, asc)))
            threads[-1].start()
        for thread in threads:
            thread.join()


tc = 0


def get_album_html(albums, stride):
    global tc
    print(len(albums))
    threads = []
    for album in albums:
        if album in cache:
            continue
        threads.append(threading.Thread(target=album_getter, args=(album,), daemon=True))
        threads[-1].start()
        tc += 1
        if tc >= stride:
            for thread in threads:
                thread.join()
            tc = 0
            threads = []
            time.sleep(3)
    for thread in threads:
        thread.join()


goon = True


def saver():
    while goon:
        fi = open("cache.pickle", "wb")
        pickle.dump(cache, fi)
        fi.close()
        time.sleep(1)


if __name__ == "__main__":
    cacher = threading.Thread(target=saver)
    cacher.start()
    print(len(cache))
    try:
        get_album_html(albums["Montenegro"], 5000)
    except Exception as ex:
        print(ex)
        exit(0)
        pass
    finally:
        goon=False
        cacher.join()
        print(failures)
        print(len(failures))
        print(c404)
        fi = open("cache.pickle", "wb")
        pickle.dump(cache, fi)
        fi.close()
        #fi = open("albums.pickle", "wb")
        #pickle.dump(albums, fi)
        #fi.close()
        goon = False
