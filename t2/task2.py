import mysql.connector
import queries2
import csv


conn = mysql.connector.connect(user='root', password='1234',
                              host='localhost',
                              database='eestech_challenge')
cursor = conn.cursor()

def get_first_n_rows(list, n, col):
    new_list = []
    i = 0
    while i < n:
        new_list.append(list[i])
        i += 1
    while i < len(list) and list[i][col] == list[i - 1][col]:
        new_list.append(list[i])
        i += 1
    return new_list


def get_first_n_songs(cur):
    num = 200
    ret = []
    print("Q")
    cur.execute(queries2.getSongs)
    print("EX")
    i = 0
    for name, count in cur:
        i += 1
        ret.append([name, count])
    while i < 100 or i == num:
        print("W",i)
        num *= 2
        cur.execute(queries2.getSongs)
        i = 0
        ret = []
        for row in cur:
            i += 1
            ret.append([name, count])
    return ret




def recordsByGenres():
    with open('recordsByGenres.csv', 'w') as csvfile:
        print 'recordsByGenres'
        try:
            writer = csv.writer(csvfile)
            data = [['Genre', 'Number of records']]
            cursor.execute(queries2.numberOfRecordsByGenres)
            for genre, count in cursor:
                data.append([genre, count])
            writer.writerows(data)
        except:
            print "error"

def recordsByStyles():
    with open('recordsByStyles.csv', 'w') as csvfile:
        print 'recordsByStyles'
        #try:
        writer = csv.writer(csvfile)
        data = [['Styles', 'Number of records']]
        cursor.execute(queries2.numberOfRecordsByStyles)
        for style, count in cursor:
            data.append([style.encode("utf-8"), count])
        writer.writerows(data)
        #except Exception:
        #    print "error", e


def albumsAndVersions():
    with open('albumsAndVersions.csv', 'w') as csvfile:
        print 'albumsAndVersions'
        try:
            writer = csv.writer(csvfile)
            data = [['Album name', 'Number of versions']]
            cursor.execute(queries2.numbersOfAlbumVersions)
            albums = []
            for name, raid, count in cursor:
                albums.append([name.encode("utf-8"), count])
            albums = get_first_n_rows(albums, 10, 1)
            for i in range(len(albums)):
                data.append(albums[i])
            writer.writerows(data)
        except:
            print "error"

def personsAndRecords():
    with open('personsAndRecords.csv', 'w') as csvfile:
        print 'personsAndRecords'
        try:
            writer = csv.writer(csvfile)
            data = [['Best persons by credits', 'Credits','Best persons by vocals', 'Vocals', 'Best persons by writings and arrangements', 'Writings and arrangements']]
            credit = []
            cursor.execute(queries2.personsAndCredits)
            for name, count in cursor:
                credit.append([name, count])
            credit = get_first_n_rows(credit, 50, 1)
            vocals = []
            cursor.execute(queries2.personsAndVocals)
            for name, count in cursor:
                vocals.append([name, count])
            vocals = get_first_n_rows(vocals, 50, 1)
            writings = []
            cursor.execute(queries2.personsAndWritings)
            for name, count in cursor:
                writings.append([name, count])
            writings = get_first_n_rows(writings, 50, 1)
            for i in range(max(len(credit), len(vocals), len(writings))):
                row = []
                if i < len(credit):
                    row.append(credit[i][0].encode("utf-8"))
                    row.append(credit[i][1])
                else:
                    row.append('')
                    row.append('')
                if i < len(vocals):
                    row.append(vocals[i][0].encode("utf-8"))
                    row.append(vocals[i][1])
                else:
                    row.append('')
                    row.append('')
                if i < len(writings):
                    row.append(writings[i][0].encode("utf-8"))
                    row.append(writings[i][1])
                else:
                    row.append('')
                    row.append('')
                data.append(row)
            writer.writerows(data)
        except:
            print "error"

def songsOnAlbums():
    with open('songsOnAlbums.csv', 'w') as csvfile:
        print 'songsOnAlbums'
        #try:
        writer = csv.writer(csvfile)
        data = [['Songs', 'Number of albums']]
        """
        cursor.execute(queries2.getSongs)
        songs = []
        for name, count in cursor:
            songs.append([name, count])
        songs = get_first_n_rows(songs, 100, 1)
        """
        songs = get_first_n_songs(cursor)
        data += songs
        writer.writerows(data)
        with open('albumFormatsForSongs.csv', 'w') as csvfile2:
            #try:
            writer2 = csv.writer(csvfile2)
            data2 = [['Song number', 'Album name', 'Formats', 'Country', 'Year', 'Genre', 'Style']]
            albums = []
            for i in range(len(songs)):
                print i
                oldCursor = []
                cursor.execute(queries2.albumsBySong, songs[i][0])
                for idRecord, recordName, country, year in cursor:
                    oldCursor += [[idRecord, recordName, country, year]]
                for idRecord, recordName, country, year in oldCursor:
                    strs = []
                    cursor.execute(queries2.formatsByRecords, idRecord)
                    str = ''
                    for row in cursor:
                        str += str(row)
                        str += ', '
                    str = str[:-2]
                    strs.append(str)
                    cursor.execute(queries2.genresByRecords, idRecord)
                    str = ''
                    for row in cursor:
                        str += str(row)
                        str += ', '
                    str = str[:-2]
                    strs.append(str)
                    cursor.execute(queries2.stylesByRecords, idRecord)
                    str = ''
                    for row in cursor:
                        str += str(row)
                        str += ', '
                    str = str[:-2]
                    strs.append(str)
                    albums.append([i, recordName, strs[0], country, year, strs[1], strs[2]])
            data2 += albums
            writer2.writerows(data2)
            #except:
            #    print "error1"
        #except:
        #    print "error2"

if __name__ == '__main__':

    #recordsByGenres()
    #recordsByStyles()
    #albumsAndVersions()
    #personsAndRecords()
    songsOnAlbums()


cursor.close()
conn.close()
