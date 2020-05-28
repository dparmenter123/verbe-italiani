DROP TABLE iF  EXISTS appdb;

CREATE TABLE IF NOT EXISTS appdb (
  verb TEXT PRIMARY KEY,
  freq INTEGER,
  irregular INTEGER DEFAULT 0,
  reflexive INTEGER DEFAULT 0,
  level TEXT DEFAULT "A1"
  );


DROP TABLE IF EXISTS forms;
CREATE TABLE IF NOT EXISTS forms (
  form TEXT PRIMARY KEY,
  display TEXT,
  level TEXT,
  simple INTEGER,
  key INTEGER
  );

DROP TABLE IF EXISTS freq;
CREATE TABLE IF NOT EXISTS freq (
  freq INTEGER,
  verb TEXT PRIMARY KEY
  );

DROP TABLE IF EXISTS irregular;
CREATE TABLE IF NOT EXISTS irregular (
  verb TEXT PRIMARY KEY
  );

DROP TABLE IF EXISTS master;
CREATE TABLE IF NOT EXISTS master (
  verb TEXT PRIMARY KEY
  );


DROP TABLE IF EXISTS reflexive;
CREATE TABLE IF NOT EXISTS reflexive (
  verb TEXT PRIMARY KEY,
  reflexive TEXT
  );

DROP TABLE IF EXISTS cards;
CREATE TABLE IF NOT EXISTS cards (
  verb TEXT,
  pos INTEGER,
  form TEXT,
  conjugation TEXT
  );

DROP TABLE IF EXISTS carddeck;
CREATE TABLE IF NOT EXISTS carddeck (
  card INTEGER PRIMARY KEY,
  level TEXT,
  repetitions INTEGER,
  easiness REAL,
  interval INTEGER,
  nextdate INTEGER
  );
