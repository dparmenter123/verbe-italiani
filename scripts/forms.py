# Its job is to identify which forms are good prompts for the key form, so given a level and a form,
# we can pick a good prompt.

MATCHING_FORMS = {
    ("A1", "INDICATIVO_PASSATO_PROSSIMO"): ["'INDICATIVO_PRESENTE'"],
    ("A2", "INDICATIVO_PASSATO_PROSSIMO"): ["'INDICATIVO_PRESENTE'"],
    ("B1", "INDICATIVO_PASSATO_PROSSIMO"): ["'INDICATIVO_PRESENTE'"],
    ("B2", "INDICATIVO_PASSATO_PROSSIMO"): ["'INDICATIVO_PRESENTE'"],

    ("A2", "INDICATIVO_IMPERFETTO"): ["'INDICATIVO_PRESENTE'"] + ["'INDICATIVO_PASSATO_PROSSIMO'"],
    ("B1", "INDICATIVO_IMPERFETTO"): ["'INDICATIVO_PRESENTE'"] + ["'INDICATIVO_PASSATO_PROSSIMO'"],
    ("B2", "INDICATIVO_IMPERFETTO"): ["'INDICATIVO_PRESENTE'"] + ["'INDICATIVO_PASSATO_PROSSIMO'"],

    ("A2", "CONDIZIONALE_PRESENTE"): ["'INDICATIVO_PRESENTE'"],
    ("B1", "CONDIZIONALE_PRESENTE"): ["'INDICATIVO_PRESENTE'"],

    ("A2", "INDICATIVO_FUTURO_SEMPLICE"): ["'INDICATIVO_PRESENTE'"],
    ("B1", "INDICATIVO_FUTURO_SEMPLICE"): ["'INDICATIVO_PRESENTE'"],
    ("B2", "INDICATIVO_FUTURO_SEMPLICE"): ["'INDICATIVO_PRESENTE'"],

    ("A2", "CONGIUNTIVO_PRESENTE"): ["'INDICATIVO_PRESENTE'"],
    ("B1", "CONGIUNTIVO_PRESENTE"): ["'INDICATIVO_PRESENTE'"],
    ("B2", "CONGIUNTIVO_PRESENTE"): ["'INDICATIVO_PRESENTE'"],

    ("B1", "INDICATIVO_TRAPASSATO_PROSSIMO"): ["'INDICATIVO_PRESENTE'"] + ["'INDICATIVO_IMPERFETTO'"],
    ("B2", "INDICATIVO_TRAPASSATO_PROSSIMO"): ["'INDICATIVO_PRESENTE'"] + ["'INDICATIVO_IMPERFETTO'"],

    ("B1", "CONGIUNTIVO_IMPERFETTO"): ["'CONGIUNTIVO_PRESENTE'"],
    ("B2", "CONGIUNTIVO_IMPERFETTO"): ["'CONGIUNTIVO_PRESENTE'"],

    ("B1", "CONGIUNTIVO_PASSATO"): ["'CONGIUNTIVO_PRESENTE'"],
    ("B2", "CONGIUNTIVO_PASSATO"): ["'CONGIUNTIVO_PRESENTE'"],

    ("B1", "CONGIUNTIVO_TRAPASSATO"): ["'CONGIUNTIVO_PRESENTE'"],
    ("B2", "CONGIUNTIVO_TRAPASSATO"): ["'CONGIUNTIVO_PRESENTE'"],

    ("B2", "INDICATIVO_PASSATO_REMOTO"): ["'INDICATIVO_PRESENTE'"] + ["'INDICATIVO_PASSATO_REMOTO'"],
    ("B2", "INDICATIVO_TRAPASSATO_REMOTO"): ["'INDICATIVO_PRESENTE'"] + ["'INDICATIVO_PASSATO_REMOTO'"],
    ("B2", "INDICATIVO_FUTURO_ANTERIORE"): ["'INDICATIVO_FUTURO_SEMPLICE'"],
}