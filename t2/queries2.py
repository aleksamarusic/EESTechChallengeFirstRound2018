
selectAllGenres = "SELECT IDGenre FROM Genre"

# za dati zanr (zadat ID) vraca broj zapisa
numberOfRecordsByGivenGenre = "SELECT COUNT(IDRecord) FROM Record_genre WHERE IDGenre = %d"

selectAllStyles  = "SELECT IDStyle FROM Style"

# za dati zanr (zadat ID) vraca broj zapisa
numberOfRecordsByGivenStyle = "SELECT COUNT(IDRecord) FROM Record_style WHERE IDStyle = %d"

numberOfRecordsByGenres = "SELECT Genre.Name, COUNT(IDRecord) FROM Record_genre, Genre" \
                          " WHERE Record_genre.IDGenre = Genre.IDGenre GROUP BY Genre.Name"

numberOfRecordsByStyles = "SELECT Style.Name, COUNT(IDRecord) FROM Record_style, Style" \
                          " WHERE Record_style.IDStyle = Style.IDStyle GROUP BY Style.Name"

numbersOfAlbumVersions = "SELECT r.RecordName, r.RAID, COUNT(r.IDRecord) FROM Record r, Format f, Record_format rf" \
                         " WHERE r.IDRecord = rf.IDRecord AND rf.IDFormat = f.IDFormat AND f.Name = 'Album'" \
                         " GROUP BY r.RAID ORDER BY COUNT(r.IDRecord) DESC"

personsAndCredits = "SELECT Name, Credits FROM Person ORDER BY Credits DESC"

personsAndVocals = "SELECT Name, Vocals FROM Person ORDER BY Vocals DESC"

personsAndWritings = "SELECT Name, WritingArrangement FROM Person ORDER BY WritingArrangement DESC"

songsOnAlbums = "SELECT Song.Name, COUNT(Song.IDRecord) FROM Song, Country, Record_format, Format" \
                " WHERE Record_format.IDRecord = Song.IDRecord AND Format.IDFormat = Record_format.IDFormat AND Format.Name = 'Album'" \
                " GROUP BY Song.Name ORDER BY COUNT(Song.IDRecord)"

albumsBySong = "SELECT Record.IDRecord, Record.RecordName, Country.Name, Record.Year" \
               " FROM Record, Song, Country, Record_format, Format" \
               " WHERE Record.IDRecord = Song.IDRecord AND Record.IDCountry = Country.IDCountry" \
               " AND Record_format.IDRecord = Record.IDRecord AND Format.IDFormat = Record_format.IDFormat" \
               " AND Format.Name = 'Album' AND Song.Name = %s"

formatsByRecords = "SELECT Format.Name FROM Format, Record_format" \
                   " WHERE Format.IDFormat = Record_format.IDFormat AND Record_format.IDRecord = %s"

genresByRecords = "SELECT Genre.Name FROM Genre, Record_format" \
                  " WHERE Genre.IDGenre = Record_genre.IDGenre AND Record_genre.IDRecord = %s"

stylesByRecords = "SELECT Style.Name FROM Style, Record_style" \
                  " WHERE Style.IDStyle = Record_style.IDStyle AND Record_style.IDRecord = %s"

getSongs = "SELECT p2.ime, p2.broj FROM (SELECT * FROM PesmaBroj p1 LIMIT 200) p2" \
           " WHERE (SELECT COUNT(*) FROM PesmaBroj p3 WHERE p3.broj>p2.broj)<100"
