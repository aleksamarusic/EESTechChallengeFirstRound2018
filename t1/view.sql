create view PesmaBroj(ime, broj)
as
SELECT s.name, count(*)
FROM song s, record r, format f, record_format rf
WHERE
		r.idRecord = rf.idRecord
        AND rf.idFormat = f.idFormat
        AND f.name = 'Album'
        AND r.idRecord=s.idRecord
group by s.name
order by count(*) desc