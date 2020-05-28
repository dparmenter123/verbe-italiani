select c.*, f.level from cards c
INNER JOIN forms f ON f.form = c.form
INNER JOIN appdb a ON a.verb = c.verb
WHERE f.simple AND a.irregular
AND a.level = 'A1'
and pos in (0)
ORDER BY f.level;
# why are there no F1 levels?


select  c.verb, NULL as pos, c.form, NULL as conjugation from cards c
INNER JOIN forms f ON f.form = c.form
INNER JOIN appdb a ON a.verb = c.verb
WHERE c.pos = 0 AND NOT a.irregular AND f.simple
AND a.level IN ('A1');

select  c.verb, NULL as pos, c.form, NULL as conjugation from cards c
INNER JOIN forms f ON f.form = c.form
INNER JOIN appdb a ON a.verb = c.verb
WHERE c.pos = 0  AND NOT f.simple
AND a.level = 'A1'

