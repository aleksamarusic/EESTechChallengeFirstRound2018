from parseMusic import MusicParser
from parseCredits import CreditsParser

# import mysql.connector

files1 = ["example.html", "page.html", "simple.html"]
files2 = ["example1.html", "example2.html"]

"""conn = mysql.connector.connect(user='root', password='1234',
                                  host='localhost',
                                  database='eestech_challenge')"""
conn = None

with open(files1[0], "r") as inFile:
    parser = MusicParser()
    parser.feed(inFile.read())
    parser.apply("asd", 123, conn)
    parser.reset()

print
print

with open(files2[1], "r") as inFile:
    parser = CreditsParser()
    parser.feed(inFile.read())
    parser.apply("asd", 123, conn)
    parser.reset()

if conn:
    conn.close()
