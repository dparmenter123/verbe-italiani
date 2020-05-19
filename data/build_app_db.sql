DROP TABLE IF EXISTS forms;

CREATE TABLE IF NOT EXISTS forms (
  form TEXT PRIMARY KEY,
  level TEXT
  );

INSERT into forms values ('INDICATIVO_PRESENTE', 'A0');
INSERT into forms values ('INDICATIVO_PASSATO_PROSSIMO', 'A1');

INSERT into forms values ('INDICATIVO_FUTURO_SEMPLICE', 'A2');
INSERT into forms values ('INDICATIVO_IMPERFETTO', 'A2');
INSERT into forms values ('CONDIZIONALE_PRESENTE', 'A2');
INSERT into forms values ('CONGIUNTIVO_PRESENTE', 'A2');

INSERT into forms values ('INDICATIVO_TRAPASSATO_PROSSIMO', 'B1');
INSERT into forms values ('CONGIUNTIVO_IMPERFETTO', 'B1');
INSERT into forms values ('CONGIUNTIVO_PASSATO', 'B1');
INSERT into forms values ('CONGIUNTIVO_TRAPASSATO', 'B1');
INSERT into forms values ('CONDIZIONALE_PASSATO', 'B1');

INSERT into forms values ('INDICATIVO_PASSATO_REMOTO', 'B2');
INSERT into forms values ('INDICATIVO_TRAPASSATO_REMOTO', 'B2');
INSERT into forms values ('INDICATIVO_FUTURO_ANTERIORE', 'B2');


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
