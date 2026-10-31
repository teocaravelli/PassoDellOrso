from datetime import date
from models.prodotto import Prodotto
from models.enums import TipologiaAttrezzatura, Livello

class Attrezzatura(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float, immagine: str, is_disponibile: bool, brand: str, data: date, livello: Livello, quantita: int, taglia: str, tipologia: TipologiaAttrezzatura):
        super().__init__(id_prodotto, nome, descrizione, prezzo, immagine, is_disponibile)
        self._brand = brand
        self._data = data
        self._livello = livello
        self._quantita = quantita
        self._taglia = taglia
        self._tipologia = tipologia

    @property
    def quantita(self) -> int:
        return self._quantita

    @quantita.setter
    def quantita(self, valore: int) -> None:
        self._quantita = valore

    def incrementa_quantita(self, quantita: int) -> None:
        self._quantita += quantita

    def decrementa_quantita(self, quantita: int) -> None:
        self._quantita -= quantita