DROP TABLE iF  EXISTS appdb;

CREATE TABLE IF NOT EXISTS appdb (
  verb TEXT PRIMARY KEY,
  freq INTEGER,
  irregular INTEGER DEFAULT 0,
  reflexive INTEGER DEFAULT 0,
  level TEXT DEFAULT "A1"
  );


CREATE TABLE IF NOT EXISTS forms (
  form TEXT PRIMARY KEY,
  display TEXT,
  level TEXT,
  key INTEGER
  );


CREATE TABLE IF NOT EXISTS freq (
  freq INTEGER,
  verb TEXT PRIMARY KEY
  );

CREATE TABLE IF NOT EXISTS irregular (
  verb TEXT PRIMARY KEY
  );

CREATE TABLE IF NOT EXISTS master (
  verb TEXT PRIMARY KEY
  );


CREATE TABLE IF NOT EXISTS reflexive (
  verb TEXT PRIMARY KEY,
  reflexive TEXT
  );

CREATE TABLE IF NOT EXISTS cards (
  verb TEXT,
  pos INTEGER,
  form TEXT,
  conjugation TEXT
  );

CREATE TABLE IF NOT EXISTS carddeck (
  card INTEGER PRIMARY KEY,
  level TEXT,
  repetitions INTEGER,
  easiness REAL,
  interval INTEGER,
  nextdate INTEGER
  );
