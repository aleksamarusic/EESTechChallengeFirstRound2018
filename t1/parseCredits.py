import re
import queries
from HTMLParser import HTMLParser


class ArtistData:
    def __init__(self):
        self.credits = 0
        self.vocal = 0
        self.arrangement = 0
        self.p_type = [("div", []), ("ul", ["facets_nav"]), ("li", []), ("h3", []), ("a", [])]
        self.p_type1 = [("div", []), ("ul", ["facets_nav"]), ("li", []), ("a", [])]
        self.p_credits = [("div", []), ("ul", ["facets_nav"]), ("li", []), ("h3", []), ("a", []), ("span", [])]
        self.p_credits1 = [("div", []), ("ul", ["facets_nav"]), ("li", []), ("a", []), ("span", [])]

    def print_data(self):
        print "all:",  self.credits
        print "vocal", self.vocal
        print "arrangement", self.arrangement


class CreditsParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dat = ArtistData()
        self.lastTagOpen = False
        self.blockStack = []
        self.tagStack = []
        self.profileTag = ""
        self.column = ""

    def feed(self, data):
        print "Starting"
        HTMLParser.feed(self, data)

    def apply(self, name, version, conn):
        if conn:
            self.dat.albumVersion = version

            cursor = conn.cursor()
            cursor.execute(queries.insertIntoPerson, (
                self.dat.credits, self.dat.vocal, self.dat.arrangement,
            ))
        else:
            self.dat.print_data()

    def reset(self):
        HTMLParser.reset(self)
        self.dat = ArtistData()
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
        if tag in ["meta"]:
            return
        # tag - div, a, ...
        attrs = dict(attrs)
        # attrs - [{'name': 'name1'}, {'id': 'id1'}, ...]
        self.lastTagOpen = True
        self.blockStack.append((tag, attrs.values()))
        # determine next Tag
        if self.check_stack(self.dat.p_type) or self.check_stack(self.dat.p_type1) and "data-credit-subtype" in attrs:
            self.tagStack.append("type")
            self.profileTag = attrs["data-credit-subtype"]
        elif self.check_stack(self.dat.p_credits) or self.check_stack(self.dat.p_credits1):
            self.tagStack.append("span")
        else:
            self.tagStack.append("")

    def handle_endtag(self, tag):
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
        if self.get_top_tag() == "span":
            if self.profileTag == "All":
                self.dat.credits = data.strip()
            elif self.profileTag == "Writing-Arrangement":
                self.dat.arrangement = data.strip()
            elif self.profileTag == "Vocals":
                self.dat.vocal = data.strip()
