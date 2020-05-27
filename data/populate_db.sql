INSERT into forms values ('INDICATIVO_PRESENTE', 'Indicativo: Presente', 'A0', 0);
INSERT into forms values ('INDICATIVO_PASSATO_PROSSIMO', 'Indicativo: Passato Prossimo', 'A1', 55);

INSERT into forms values ('INDICATIVO_IMPERFETTO', 'Indicativo: Imperfetto', 'A2', 20);
INSERT into forms values ('INDICATIVO_FUTURO_SEMPLICE', 'Indicativo: Futuro Semplice', 'A2', 30);
INSERT into forms values ('CONDIZIONALE_PRESENTE', 'Condizionale: Presente', 'A2', 40);
INSERT into forms values ('CONGIUNTIVO_PRESENTE', 'Congiuntivo: Presente', 'A2', 50);

INSERT into forms values ('CONGIUNTIVO_IMPERFETTO', 'Congiuntivo: Imperfetto', 'B1', 51);
INSERT into forms values ('INDICATIVO_TRAPASSATO_PROSSIMO', 'Indicativo: Trapassato Prossimo', 'B1', 80);
INSERT into forms values ('CONGIUNTIVO_PASSATO', 'Congiuntivo: Passato', 'B1', 90);
INSERT into forms values ('CONGIUNTIVO_TRAPASSATO', 'Congiuntivo: Trapassato', 'B1', 100);
INSERT into forms values ('CONDIZIONALE_PASSATO', 'Condizionale: Passato', 'B1', 110);

INSERT into forms values ('INDICATIVO_PASSATO_REMOTO', 'Indicativo: Passato Remoto', 'B2', 52);
INSERT into forms values ('INDICATIVO_TRAPASSATO_REMOTO', 'Indicativo: Traassato Remoto', 'B2', 120);
INSERT into forms values ('INDICATIVO_FUTURO_ANTERIORE', 'Indicativo: Futuro Anteriore', 'B2', 130);

.mode csv
.import ling/top10k.csv freq

.import lists/irregular.dat irregular

.import lists/master_verb_list.dat master

.import lists/reflexive.dat reflexive

INSERT INTO appdb
  select m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "A1" from master m
  inner join freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 100;

INSERT INTO appdb
  select m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "A2" from master m
  inner join freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 100 OFFSET 100;

INSERT INTO appdb
  select m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "A2" from master m
  inner join freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 200 OFFSET 200;

INSERT INTO appdb
  select m.verb, f.freq, 0 AS 'irregular', 0 AS 'reflexive', "A2" from master m
  inner join freq f ON f.verb = m.verb
  ORDER BY f.freq DESC
  LIMIT 400 OFFSET 400;

  update appdb set irregular=1 WHERE appdb.verb IN (
  select a.verb from appdb a inner join irregular i on i.verb = a.verb );

insert into appdb
  select r.reflexive, a.freq, a.irregular, 1, a.level from appdb a
  inner join reflexive r ON r.verb = a. verb;

UPDATE appdb
  set level = "A1"
  where verb = 'bere';
