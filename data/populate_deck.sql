DROP TABLE IF EXISTS deck;

CREATE TABLE deck (
  verb TEXT,
  pos INTEGER,
  conjugation TEXT,
  form TEXT,
  form_level TEXT,
  verb_level TEXT,
  repetitions INTEGER,
  interval INTEGER,
  easiness FLOAT,
  next_practice INTEGER
  );

-- irregular + simple
INSERT into deck 
SELECT c.verb, c.pos, c.conjugation, c.form, forms.level AS 'form_level', f.level AS 'verb_level',
  0 AS 'repetitions', 
  0 AS 'interval',
  2.5 AS 'easiness',
  0 AS 'next_practice'
FROM conjugations c
INNER JOIN forms ON forms.form = c.form
INNER JOIN facts f on f.verb = c.verb
WHERE f.irregular
AND forms.simple
AND c.pos IN (0,1,2,4,5,6)
ORDER BY c.verb, verb_level, form_level
;

-- regular + simple
INSERT into deck
SELECT c.verb, NULL as 'pos', c.conjugation, c.form, forms.level AS 'form_level', f.level AS 'verb_level',
  0 AS 'repetitions',
  0 AS 'interval',
  2.5 AS 'easiness',
  0 AS 'next_practice'
FROM conjugations c
INNER JOIN forms ON forms.form = c.form
INNER JOIN facts f on f.verb = c.verb
WHERE NOT f.irregular
AND forms.simple
AND c.pos IN (0)
ORDER BY c.verb, verb_level, form_level
;

-- passato prossimo
INSERT into deck
SELECT c.verb, NULL as 'pos', c.conjugation, c.form, forms.level AS 'form_level', f.level AS 'verb_level',
  0 AS 'repetitions',
  0 AS 'interval',
  2.5 AS 'easiness',
  0 AS 'next_practice'
FROM conjugations c
INNER JOIN forms ON forms.form = c.form
INNER JOIN facts f on f.verb = c.verb
WHERE c.form IN ('INDICATIVO_PASSATO_PROSSIMO')
AND c.pos IN (0)
ORDER BY c.verb, verb_level, form_level
;

-- not simple, not passato prossimo
INSERT into deck
SELECT c.verb, NULL as 'pos', c.conjugation, c.form, forms.level AS 'form_level', f.level AS 'verb_level' ,
  0 AS 'repetitions',
  0 AS 'interval',
  2.5 AS 'easiness',
  0 AS 'next_practice'
FROM conjugations c
INNER JOIN forms ON forms.form = c.form
INNER JOIN facts f on f.verb = c.verb
WHERE NOT forms.simple AND NOT c.form IN ('INDICATIVO_PASSATO_PROSSIMO')
AND c.pos IN (0)
ORDER BY RANDOM()
LIMIT 1000
;

