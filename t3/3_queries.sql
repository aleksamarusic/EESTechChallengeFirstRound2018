-- 3a) Brojevi albuma grupisani po godinama
SELECT 
    (r.year DIV 10) * 10 AS 'Od',
    (r.year DIV 10) * 10 + 9 AS 'Do',
    COUNT(*) AS 'Broj albuma'
FROM
    record r,
    format f,
    record_format rf
WHERE
    r.idRecord = rf.idRecord
        AND rf.idFormat = f.idFormat
        AND f.name = 'Album'
        AND r.year >= 1900
GROUP BY (r.year DIV 10) * 10 , (r.year DIV 10) * 10 + 9;

-- 3b) 6 Najzastupljenijih zanrova
SELECT 
    *
FROM
    (SELECT 
        rg.idGenre AS 'idGenre', g.name AS 'name', COUNT(*) AS 'cnt'
    FROM
        record r, genre g, record_genre rg, format f, record_format rf
    WHERE
        r.idRecord = rg.idRecord
            AND g.idGenre = rg.idGenre
            AND r.idRecord = rf.idRecord
            AND rf.idFormat = f.idFormat
            AND f.name = 'Album'
    GROUP BY g.idGenre) gc
ORDER BY gc.cnt DESC
LIMIT 6;

-- 3c) Pesme po trajanju
SELECT 
    (s.duration DIV 90) * 90 + 1 AS 'Trajanje od',
    (s.duration DIV 90) * 90 + 90 AS 'Do',
    COUNT(*) AS 'Broj'
FROM
    song s
WHERE
    s.duration < 360
GROUP BY (s.duration DIV 90) * 90 + 1 , (s.duration DIV 90) * 90 + 90 
UNION SELECT 
    '>360' AS 'Trajanje od', NULL AS '', COUNT(*) AS 'Broj'
FROM
    song s
WHERE
    s.duration <= 360;

-- 3d) Broj cirilicnih albuma
SELECT 
    t1.cnt1 AS 'Cirilicnih',
    t1.cnt1 / (t1.cnt1 + t2.cnt2) * 100 AS '% cirilicnih',
    t2.cnt2 AS 'Latinicnih',
    t2.cnt2 / (t1.cnt1 + t2.cnt2) * 100 AS '% latinicnih'
FROM
    (SELECT 
        COUNT(*) AS 'cnt1'
    FROM
        record r, format f, record_format rf
    WHERE
        r.idRecord = rf.idRecord
            AND rf.idFormat = f.idFormat
            AND f.name = 'Album'
            AND (r.recordName LIKE '%А%'
            OR r.recordName LIKE '%Б%'
            OR r.recordName LIKE '%В%'
            OR r.recordName LIKE '%Г%'
            OR r.recordName LIKE '%Д%'
            OR r.recordName LIKE '%Ђ%'
            OR r.recordName LIKE '%Е%'
            OR r.recordName LIKE '%Ж%'
            OR r.recordName LIKE '%З%'
            OR r.recordName LIKE '%И%'
            OR r.recordName LIKE '%Ј%'
            OR r.recordName LIKE '%К%'
            OR r.recordName LIKE '%Л%'
            OR r.recordName LIKE '%Љ%'
            OR r.recordName LIKE '%М%'
            OR r.recordName LIKE '%Н%'
            OR r.recordName LIKE '%Њ%'
            OR r.recordName LIKE '%О%'
            OR r.recordName LIKE '%П%'
            OR r.recordName LIKE '%Р%'
            OR r.recordName LIKE '%С%'
            OR r.recordName LIKE '%Т%'
            OR r.recordName LIKE '%Ћ%'
            OR r.recordName LIKE '%У%'
            OR r.recordName LIKE '%Ф%'
            OR r.recordName LIKE '%Х%'
            OR r.recordName LIKE '%Ц%'
            OR r.recordName LIKE '%Ч%'
            OR r.recordName LIKE '%Џ%'
            OR r.recordName LIKE '%Ш%'
            OR r.recordName LIKE '%а%'
            OR r.recordName LIKE '%б%'
            OR r.recordName LIKE '%в%'
            OR r.recordName LIKE '%г%'
            OR r.recordName LIKE '%д%'
            OR r.recordName LIKE '%ђ%'
            OR r.recordName LIKE '%е%'
            OR r.recordName LIKE '%ж%'
            OR r.recordName LIKE '%з%'
            OR r.recordName LIKE '%и%'
            OR r.recordName LIKE '%ј%'
            OR r.recordName LIKE '%к%'
            OR r.recordName LIKE '%л%'
            OR r.recordName LIKE '%љ%'
            OR r.recordName LIKE '%м%'
            OR r.recordName LIKE '%н%'
            OR r.recordName LIKE '%њ%'
            OR r.recordName LIKE '%о%'
            OR r.recordName LIKE '%п%'
            OR r.recordName LIKE '%р%'
            OR r.recordName LIKE '%с%'
            OR r.recordName LIKE '%т%'
            OR r.recordName LIKE '%ћ%'
            OR r.recordName LIKE '%у%'
            OR r.recordName LIKE '%ф%'
            OR r.recordName LIKE '%х%'
            OR r.recordName LIKE '%ц%'
            OR r.recordName LIKE '%ч%'
            OR r.recordName LIKE '%џ%'
            OR r.recordName LIKE '%ш%')) t1,
    (SELECT 
        COUNT(*) AS 'cnt2'
    FROM
        record r, format f, record_format rf
    WHERE
        r.idRecord = rf.idRecord
            AND rf.idFormat = f.idFormat
            AND f.name = 'Album'
            AND NOT (r.recordName LIKE '%А%'
            OR r.recordName LIKE '%Б%'
            OR r.recordName LIKE '%В%'
            OR r.recordName LIKE '%Г%'
            OR r.recordName LIKE '%Д%'
            OR r.recordName LIKE '%Ђ%'
            OR r.recordName LIKE '%Е%'
            OR r.recordName LIKE '%Ж%'
            OR r.recordName LIKE '%З%'
            OR r.recordName LIKE '%И%'
            OR r.recordName LIKE '%Ј%'
            OR r.recordName LIKE '%К%'
            OR r.recordName LIKE '%Л%'
            OR r.recordName LIKE '%Љ%'
            OR r.recordName LIKE '%М%'
            OR r.recordName LIKE '%Н%'
            OR r.recordName LIKE '%Њ%'
            OR r.recordName LIKE '%О%'
            OR r.recordName LIKE '%П%'
            OR r.recordName LIKE '%Р%'
            OR r.recordName LIKE '%С%'
            OR r.recordName LIKE '%Т%'
            OR r.recordName LIKE '%Ћ%'
            OR r.recordName LIKE '%У%'
            OR r.recordName LIKE '%Ф%'
            OR r.recordName LIKE '%Х%'
            OR r.recordName LIKE '%Ц%'
            OR r.recordName LIKE '%Ч%'
            OR r.recordName LIKE '%Џ%'
            OR r.recordName LIKE '%Ш%'
            OR r.recordName LIKE '%а%'
            OR r.recordName LIKE '%б%'
            OR r.recordName LIKE '%в%'
            OR r.recordName LIKE '%г%'
            OR r.recordName LIKE '%д%'
            OR r.recordName LIKE '%ђ%'
            OR r.recordName LIKE '%е%'
            OR r.recordName LIKE '%ж%'
            OR r.recordName LIKE '%з%'
            OR r.recordName LIKE '%и%'
            OR r.recordName LIKE '%ј%'
            OR r.recordName LIKE '%к%'
            OR r.recordName LIKE '%л%'
            OR r.recordName LIKE '%љ%'
            OR r.recordName LIKE '%м%'
            OR r.recordName LIKE '%н%'
            OR r.recordName LIKE '%њ%'
            OR r.recordName LIKE '%о%'
            OR r.recordName LIKE '%п%'
            OR r.recordName LIKE '%р%'
            OR r.recordName LIKE '%с%'
            OR r.recordName LIKE '%т%'
            OR r.recordName LIKE '%ћ%'
            OR r.recordName LIKE '%у%'
            OR r.recordName LIKE '%ф%'
            OR r.recordName LIKE '%х%'
            OR r.recordName LIKE '%ц%'
            OR r.recordName LIKE '%ч%'
            OR r.recordName LIKE '%џ%'
            OR r.recordName LIKE '%ш%')) t2;

-- 3e) Albumi po brojevima zanrova

SELECT 
    t1.cnt as 'Broj zanrova', t1.ccnt as 'Broj albuma', t1.ccnt/t2.totalCnt*100 'as procenat'
FROM
    (SELECT 
        q.cnt AS 'cnt', COUNT(*) AS 'ccnt'
    FROM
        (SELECT 
        r.idRecord AS 'rid', COUNT(*) AS cnt
    FROM
        record r, genre g, record_genre rg, format f, record_format rf
    WHERE
        r.idRecord = rg.idRecord
            AND g.idGenre = rg.idGenre
            AND r.idRecord = rf.idRecord
            AND rf.idFormat = f.idFormat
            AND f.name = 'Album'
    GROUP BY r.idRecord , r.recordName
    HAVING COUNT(*)) q
    GROUP BY q.cnt) t1,
    (SELECT count(*) as 'totalCnt'
        FROM record r, format f, record_format rf
    WHERE
            r.idRecord = rf.idRecord
            AND rf.idFormat = f.idFormat
            AND f.name = 'Album'
    ) t2
WHERE t1.cnt<4

UNION
SELECT 
    '>=4' as 'Broj zanrova', sum(t1.ccnt) as 'Broj albuma', sum(t1.ccnt)/avg(t2.totalCnt)*100 'as procenat'
FROM
    (SELECT 
        q.cnt AS 'cnt', COUNT(*) AS 'ccnt'
    FROM
        (SELECT 
        r.idRecord AS 'rid', COUNT(*) AS cnt
    FROM
        record r, genre g, record_genre rg, format f, record_format rf
    WHERE
        r.idRecord = rg.idRecord
            AND g.idGenre = rg.idGenre
            AND r.idRecord = rf.idRecord
            AND rf.idFormat = f.idFormat
            AND f.name = 'Album'
    GROUP BY r.idRecord , r.recordName
    HAVING COUNT(*)) q
    GROUP BY q.cnt) t1,
    (SELECT count(*) as 'totalCnt'
        FROM record r, format f, record_format rf
    WHERE
            r.idRecord = rf.idRecord
            AND rf.idFormat = f.idFormat
            AND f.name = 'Album'
    ) t2
WHERE t1.cnt>=4