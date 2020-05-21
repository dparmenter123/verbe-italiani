DROP TABLE IF EXISTS forms;

CREATE TABLE IF NOT EXISTS forms (
  form TEXT PRIMARY KEY,
  display TEXT,
  level TEXT,
  key INTEGER
  );

INSERT into forms values ('INDICATIVO_PRESENTE', 'Indicativo: Presente', 'A0', 0);
INSERT into forms values ('INDICATIVO_PASSATO_PROSSIMO', 'Indicativo: Passato Prossimo', 'A1', 1);

INSERT into forms values ('INDICATIVO_IMPERFETTO', 'Indicativo: Imperfetto', 'A2', 2);
INSERT into forms values ('INDICATIVO_FUTURO_SEMPLICE', 'Indicativo: Futuro Semplice', 'A2', 3);
INSERT into forms values ('CONDIZIONALE_PRESENTE', 'Condizionale: Presente', 'A2', 4);
INSERT into forms values ('CONGIUNTIVO_PRESENTE', 'Congiuntivo: Presente', 'A2', 5);

INSERT into forms values ('CONGIUNTIVO_IMPERFETTO', 'Congiuntivo: Imperfetto', 'B1', 6);
INSERT into forms values ('INDICATIVO_TRAPASSATO_PROSSIMO', 'Indicativo: Trapassato Prossimo', 'B1', 8);
INSERT into forms values ('CONGIUNTIVO_PASSATO', 'Congiuntivo: Passato', 'B1', 9);
INSERT into forms values ('CONGIUNTIVO_TRAPASSATO', 'Congiuntivo: Trapassato', 'B1', 10);
INSERT into forms values ('CONDIZIONALE_PASSATO', 'Condizionale: Passato', 'B1', 11);

INSERT into forms values ('INDICATIVO_PASSATO_REMOTO', 'Indicativo: Passato Remoto', 'B2', 7);
INSERT into forms values ('INDICATIVO_TRAPASSATO_REMOTO', 'Indicativo: Traassato Remoto', 'B2', 12);
INSERT into forms values ('INDICATIVO_FUTURO_ANTERIORE', 'Indicativo: Futuro Anteriore', 'B2', 13);

DROP TABLE IF EXISTS freq;
CREATE TABLE IF NOT EXISTS freq (
  freq INTEGER,
  verb TEXT PRIMARY KEY
  );

.mode csv
.import ling/top10k.csv freq
#select * from freq order by freq desc LIMIT 50;

DROP TABLE IF EXISTS irregular;
CREATE TABLE IF NOT EXISTS irregular (
  verb TEXT PRIMARY KEY
  );

.mode csv
.import lists/irregular.dat irregular
#select verb, 1, 0 from irregular;

DROP TABLE if EXISTS master;
CREATE TABLE IF NOT EXISTS master (
  verb TEXT PRIMARY KEY
  );

.mode csv
.import lists/master_verb_list.dat master

# get the top N verbs
#select master.verb, freq.freq from master INNER JOIN freq WHERE master.verb = freq.verb ORDER BY freq.freq DESC LIMIT 50;

DROP TABLE IF EXISTS reflexive;
CREATE TABLE IF NOT EXISTS reflexive (
  verb TEXT PRIMARY KEY,
  reflexive TEXT
  );

.import lists/reflexive.dat reflexive
# check for nulls
#select reflexive.*, master.verb from reflexive LEFT JOIN master ON master.verb = reflexive.verb WHERE master.verb IS NULL;


DROP TABLE IF EXISTS temp1;
create table temp1 AS select verb FROM (select verb from master where verb NOT IN ( select verb from irregular )) ;

DROP TABLE IF EXISTS appdb;
CREATE TABLE appdb AS
select *
FROM (
    select irregular.verb, 99999999 as freq, 1 AS irregular, 0 AS reflexive from irregular
  )
UNION
select *
FROM (
    select temp1.verb, freq.freq AS freq, 0 AS irregular, 0 AS reflexive from temp1 INNER JOIN freq WHERE temp1.verb = freq.verb ORDER BY freq.freq
  )
UNION
select *
  FROM (
    select reflexive.reflexive, freq.freq AS freq, 0 AS irregular, 1 AS reflexive from reflexive INNER JOIN freq WHERE reflexive.verb = freq.verb 
  );

DROP TABLE IF EXISTS temp1;

# save to the CSV
.mode csv
.output appdb.csv
select * from appdb ORDER BY freq DESC;;
.output stdout

DROP TABLE IF EXISTS cards;
CREATE TABLE cards (
  verb TEXT,
  pos INTEGER,
  form TEXT,
  conjugation TEXT
  );

DROP TABLE IF EXISTS carddeck;
CREATE TABLE carddeck (
  card INTEGER PRIMARY KEY,
  level TEXT,
  repetitions INTEGER,
  easiness REAL,
  interval INTEGER,
  nextdate INTEGER
  );
