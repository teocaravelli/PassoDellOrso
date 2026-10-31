from datetime import datetime
from models.prodotto import Prodotto
from models.enums import Livello

class Lezione(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float, immagine: str, is_disponibile: bool, data: datetime, livello: Livello, quantita: int):
        super().__init__(id_prodotto, nome, descrizione, prezzo, immagine, is_disponibile)
        self._data = data
        self._livello = livello
        self._quantita = quantita

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