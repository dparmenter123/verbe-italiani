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

create table temp1 AS select verb FROM (select verb from master where verb NOT IN ( select verb from irregular )) ;

CREATE TABLE IF NOT EXISTS appdb AS
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
