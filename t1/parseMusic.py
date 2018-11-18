import re
import queries
from HTMLParser import HTMLParser
import mysql.connector.errors


class AlbumData:
    def __init__(self):
        self.bandName = ""
        self.p_bandName = [("div", []), ("h1", []), ("span", []), ("span", []), ("a", [])]
        self.albumName = ""
        self.p_albumName = [("div", []), ("h1", []), ("span", ["name"])]
        self.albumVersion = 0
        self.p_version = [("div", ["m_versions"]), ("h3", [])]
        self.p_attr = [("div", []), ("div", ["head"])]
        self.p_value = [("div", []), ("div", ["content"])]
        self.format = []
        self.country = ""
        self.released = ""
        self.genre = []
        self.style = []
        self.p_row = [("table", ["playlist"]), ("tr", [])]
        self.p_column = [("table", ["playlist"]), ("tr", []), ("td", [])]
        # ind: {id: "1", name: "", duration: ""}
        self.songs = {}
        self.p_blockquote = [("blockquote", [])]

    def print_data(self):
        print "band name:",  self.bandName
        print "album name:",  self.albumName
        print "album version:",  self.albumVersion
        print "format", self.format
        print "country", self.country
        print "released", self.released
        print "genre", self.genre
        print "style", self.style
        print "songs", self.songs


class MusicParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dat = AlbumData()
        self.lastTagOpen = False
        self.blockStack = []
        self.tagStack = []
        self.profileTag = ""
        self.column = ""

    def feed(self, data):
        HTMLParser.feed(self, data)

    def apply(self, name, version, conn):
        self.dat.albumVersion = version
        if self.dat.released != "":
            self.dat.released = re.search('.*([0-9]{4}).*', self.dat.released).group(1)
        else:
            self.dat.released = None
        if self.dat.country == "":
            self.dat.country = "Unknown"

        if conn:
            cursor = conn.cursor()

            for genre in self.dat.genre:
                try:
                    cursor.execute(queries.insertIntoGenre, {"genreName": genre, })
                except mysql.connector.errors.IntegrityError:
                    pass

            for style in self.dat.style:
                try:
                    cursor.execute(queries.insertIntoStyle, {"styleName": style, })
                except mysql.connector.errors.IntegrityError:
                    pass

            for format in self.dat.format:
                try:
                    cursor.execute(queries.insertIntoFormat, {"formatName": format, })
                except mysql.connector.errors.IntegrityError:
                    pass

            try:
                cursor.execute(queries.insertIntoCountry, {"countryName": self.dat.country, })
            except mysql.connector.errors.IntegrityError:
                pass

            year = 0
            if self.dat.released:
                year = int(self.dat.released)

            cursor.execute(queries.insertIntoRecord, (
                self.dat.albumName, name, version,
                self.dat.country, year,
            ))

            for song in self.dat.songs:
                try:
                    duration = 0
                    if self.dat.songs[song]["duration"] != "":
                        m = re.search('^([0-9]+):.*$', self.dat.songs[song]["duration"])
                        s = re.search('^.*:([0-9]+).*$', self.dat.songs[song]["duration"])
                        duration = int(m.group(1)) * 60 + int(s.group(1))
                    cursor.execute(queries.insertIntoSong, (
                        self.dat.songs[song]["name"], duration,
                    ))
                except AttributeError:
                    pass

            for rec_genre in self.dat.genre:
                cursor.execute(queries.insertIntoRecordGenre, (rec_genre, ))

            for rec_style in self.dat.style:
                cursor.execute(queries.insertIntoRecordStyle, (rec_style, ))

            for rec_format in self.dat.format:
                cursor.execute(queries.insertIntoRecordFormat, (rec_format, ))

            conn.commit()
            cursor.close()
            self.dat.print_data()
        else:
            print
            self.dat.print_data()

    def reset(self):
        HTMLParser.reset(self)
        self.dat = AlbumData()
        self.lastTagOpen = False
        self.blockStack = []
        self.tagStack = []
        self.profileTag = ""
        self.column = ""

    def check_stack(self, data):
        if len(data) > len(self.blockStack):
            return False
        for ind in range(len(data)):
            ind += 1
            if self.blockStack[-ind][0] != data[-ind][0]:
                return False
            for attr in data[-ind][1]:
                if attr not in self.blockStack[-ind][1]:
                    return False
        return True

    # The following methods are called when data or markup elements are encountered and they are meant to be overridden
    # in a subclass. The base class implementations do nothing (except for handle_startendtag()):

    def handle_starttag(self, tag, attrs):
        if tag in ["meta", "br"]:
            return
        # tag - div, a, ...
        attrs = dict(attrs)
        # attrs - [{'name': 'name1'}, {'id': 'id1'}, ...]
        self.lastTagOpen = True
        self.blockStack.append((tag, attrs.values()))
        # determine next Tag
        if self.check_stack(self.dat.p_attr):
            self.tagStack.append("get_label")
        elif self.check_stack(self.dat.p_value):
            self.tagStack.append("get_value")
        elif self.check_stack(self.dat.p_row) and "data-track-position" in attrs:
            self.tagStack.append("row")
            self.profileTag = attrs["data-track-position"]
        elif self.check_stack(self.dat.p_column) and ("class" in attrs):
            self.tagStack.append("column")
            self.column = attrs["class"]
        elif self.check_stack(self.dat.p_blockquote):
            self.tagStack.append("blockquote")
        else:
            self.tagStack.append("")

    def handle_endtag(self, tag):
        if tag in ["meta", "br"]:
            return
        self.lastTagOpen = False
        self.blockStack.pop()
        self.tagStack.pop()

    def get_top_tag(self):
        ind = 1
        while ind <= len(self.tagStack) and self.tagStack[-ind] == "":
            ind += 1
        if ind <= len(self.tagStack):
            return self.tagStack[-ind]
        else:
            return ""

    @staticmethod
    def clean(data):
        exp = re.compile('<.*?>')
        data = data.replace('\n', '')
        while "  " in data:
            data = data.replace("  ", ' ')
        return re.sub(exp, '', data.strip()).strip()

    def handle_data(self, data):
        # correct tag stack
        if self.check_stack(self.dat.p_bandName):
            self.dat.bandName = data.strip()
        elif self.check_stack(self.dat.p_albumName):
            self.dat.albumName = data.strip()
        elif self.check_stack(self.dat.p_version):
            m = re.search('([0-9]+)', data)
            if m:
                self.dat.albumVersion = int(m.group(1))

        # tagged block
        elif self.get_top_tag() == "get_label":
            self.profileTag = data.strip()
        elif self.get_top_tag() == "get_value":
            if self.profileTag == "Format:":
                self.dat.format += [x.strip() for x in data.strip().split(',')]
                while "" in self.dat.format:
                    self.dat.format.remove("")
                for i in range(15):
                    while str(i) in self.dat.format:
                        self.dat.format.remove(str(i))
            elif self.profileTag == "Country:":
                self.dat.country += data.strip()
            elif self.profileTag == "Released:" or self.profileTag == "Year:":
                self.dat.released += data.strip()
            elif self.profileTag == "Genre:":
                if self.lasttag == "a":
                    if data == "&":
                        self.dat.genre[-1] += data
                    elif len(self.dat.genre) > 0 and self.dat.genre[-1][-1] == "&":
                        self.dat.genre[-1] += data
                    else:
                        self.dat.genre += [data.strip()]
                    while ',' in self.dat.genre:
                        self.dat.genre.remove(",")
                else:
                    self.dat.genre += data.strip().split(',')
                while "" in self.dat.genre:
                    self.dat.genre.remove("")
            elif self.profileTag == "Style:":
                self.dat.style += data.strip().split(',')
                while "" in self.dat.style:
                    self.dat.style.remove("")
        elif self.get_top_tag() == "column":
            if self.profileTag not in self.dat.songs:
                self.dat.songs[self.profileTag] = {"ind": "", "name": "", "duration": ""}
            if self.column == "tracklist_track_pos":
                self.dat.songs[self.profileTag]["ind"] += data.strip()
            elif self.column == "track tracklist_track_title ":
                self.dat.songs[self.profileTag]["name"] += data.strip()
            elif self.column == "tracklist_track_duration":
                self.dat.songs[self.profileTag]["duration"] += data.strip()
