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

select c.verb, c.pos, c.conjugation, c.form, forms.level AS 'form-level', f.level AS 'verb-level' from conjugations c
INNER JOIN forms ON forms.form = c.form
INNER JOIN facts f on f.verb = c.verb
WHERE f.level IN ('A1')
AND forms.level in ('A0', 'A1')
AND f.irregular
ORDER BY RANDOM()

select * from deck
--WHERE form_level in ('A0', 'A1') AND verb_level IN ('A1')
--WHERE form_level in ('A0', 'A1', 'A2') AND verb_level IN ('A1', 'A2')
--WHERE form_level in ('A0', 'A1', 'A2', 'B1') AND verb_level IN ('A1', 'A2', 'B1')
 WHERE form_level in ('A0', 'A1', 'A2', 'B1', 'B2') AND verb_level IN ('A1', 'A2', 'B1', 'B2')
ORDER BY RANDOM()
;