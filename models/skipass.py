from datetime import date
from models.prodotto import Prodotto
from models.enums import FormulaTemporale

class SkiPass(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float, immagine: str, is_disponibile: bool, formula_temporale: FormulaTemporale, data_inizio: date = None, data_fine: date = None):
        super().__init__(id_prodotto, nome, descrizione, prezzo, immagine, is_disponibile)
        self._formula_temporale = formula_temporale
        self._data_inizio = data_inizio
        self._data_fine = data_fine

    @property
    def formula_temporale(self) -> FormulaTemporale:
        return self._formula_temporale

    def set_periodo_validita(self, data_inizio: date, data_fine: date) -> None:
        self._data_inizio = data_inizio
        self._data_fine = data_fine