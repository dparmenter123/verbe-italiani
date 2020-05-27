.print 'count of irregular verbs'
select count(*) from irregular;

.print '22 most common irregular verbs
DROP table if EXISTS irregular_22;

CREATE TABLE irregular_22 AS
with temp2(verb) AS (
    with temp1(verb) AS (
        select i.verb from irregular i INNER JOIN freq f ON f.verb = i.verb ORDER BY freq DESC LIMIT 20
    )
    select verb from temp1 UNION
    select 'uscire' as v1 UNION
    select 'bere' as v2
    )

.print 'the next 78'
DROP TABLE IF EXISTS regular_78;
CREATE TABLE regular_78 AS
select m.verb, f.freq from master m
inner join freq f ON f.verb = m.verb
where m.verb NOT IN (select verb from irregular_22)
order by f.freq DESC
LIMIT 78;

.print 'add in the reflexive forms'

