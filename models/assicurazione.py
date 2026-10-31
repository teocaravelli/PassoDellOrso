from datetime import date
from models.prodotto import Prodotto

class Assicurazione(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float, immagine: str, is_disponibile: bool, data_inizio: date = None, data_fine: date = None):
        super().__init__(id_prodotto, nome, descrizione, prezzo, immagine, is_disponibile)
        self._data_inizio = data_inizio
        self._data_fine = data_fine

    def set_periodo_copertura(self, data_inizio: date, data_fine: date) -> None:
        self._data_inizio = data_inizio
        self._data_fine = data_fine