INSERT into forms values ('INDICATIVO_PRESENTE', 'Indicativo: Presente', 'A0', 1, 0);
INSERT into forms values ('INDICATIVO_PASSATO_PROSSIMO', 'Indicativo: Passato Prossimo', 'A1', 0, 55);

INSERT into forms values ('INDICATIVO_IMPERFETTO', 'Indicativo: Imperfetto', 'A2', 1, 20);
INSERT into forms values ('INDICATIVO_FUTURO_SEMPLICE', 'Indicativo: Futuro Semplice', 'A2', 1, 30);
INSERT into forms values ('CONDIZIONALE_PRESENTE', 'Condizionale: Presente', 'A2', 1, 40);
INSERT into forms values ('CONGIUNTIVO_PRESENTE', 'Congiuntivo: Presente', 'A2', 1, 50);

INSERT into forms values ('CONGIUNTIVO_IMPERFETTO', 'Congiuntivo: Imperfetto', 'B1', 1, 51);
INSERT into forms values ('INDICATIVO_TRAPASSATO_PROSSIMO', 'Indicativo: Trapassato Prossimo', 'B1', 0, 80);
INSERT into forms values ('CONGIUNTIVO_PASSATO', 'Congiuntivo: Passato', 'B1', 0, 90);
INSERT into forms values ('CONGIUNTIVO_TRAPASSATO', 'Congiuntivo: Trapassato', 'B1', 0, 100);
INSERT into forms values ('CONDIZIONALE_PASSATO', 'Condizionale: Passato', 'B1', 0, 110);

INSERT into forms values ('INDICATIVO_PASSATO_REMOTO', 'Indicativo: Passato Remoto', 'B2', 1, 52);
INSERT into forms values ('INDICATIVO_TRAPASSATO_REMOTO', 'Indicativo: Traassato Remoto', 'B2', 0, 120);
INSERT into forms values ('INDICATIVO_FUTURO_ANTERIORE', 'Indicativo: Futuro Anteriore', 'B2', 0, 130);

.mode csv
.import ling/top10k.csv freq

.import lists/irregular.dat irregular

.import lists/master_verb_list.dat master

.import lists/reflexive.dat reflexive

INSERT INTO facts
  SELECT m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "A1" FROM master m
  INNER JOIN freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 100;

INSERT INTO facts
  SELECT m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "A2" FROM master m
  INNER JOIN freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 100 OFFSET 100;

INSERT INTO facts
  SELECT m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "B1" FROM master m
  INNER JOIN freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 200 OFFSET 200;

INSERT INTO facts
  SELECT m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "B2" FROM master m
  INNER JOIN freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 400 OFFSET 400;

UPDATE facts set irregular=1 WHERE facts.verb IN (
  SELECT a.verb FROM facts a INNER JOIN irregular i ON i.verb = a.verb
  );

INSERT INTO facts
  select r.reflexive, a.freq, a.irregular, 1, a.level from facts a
  inner join reflexive r ON r.verb = a. verb;

UPDATE facts
  SET LEVEL = "A1"
  WHERE verb = 'bere';
