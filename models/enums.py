from enum import Enum

class Difficolta(Enum):
    AZZURRA = "azzurra"
    ROSSA = "rossa"
    NERA = "nera"

class StatoApertura(Enum):
    APERTA = "aperta"
    CHIUSA = "chiusa"
    MANUTENZIONE = "manutenzione"

class FormulaTemporale(Enum):
    GIORNALIERO = "giornaliero"
    SETTIMANALE = "settimanale"
    MENSILE = "mensile"
    STAGIONALE = "stagionale"

class Livello(Enum):
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZATO = "avanzato"
    ESPERTO = "esperto"

class TipologiaAttrezzatura(Enum):
    SCI = "sci"
    SNOWBOARD = "snowboard"
    SCARPONI = "scarponi"
    CASCO = "casco"
    TUTA = "tuta"

class StatoOrdine(Enum):
    IN_CORSO = "in_corso"
    COMPLETATO = "completato"
    RIMBORSO_RICHIESTO = "rimborso_richiesto"
    RIMBORSO_IN_ELABORAZIONE = "rimborso_in_elaborazione"
    RIMBORSO_COMPLETATO = "rimborso_completato"