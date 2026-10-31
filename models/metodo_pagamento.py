from datetime import date

class MetodoPagamento:
    def __init__(self, codice_carta: str, cvv: str, data_scadenza: date, nome: str):
        self._codice_carta = codice_carta
        self._cvv = cvv
        self._data_scadenza = data_scadenza
        self._nome = nome

    @property
    def codice_carta(self) -> str:
        return self._codice_carta

    def is_scaduta(self) -> bool:
        return date.today() > self._data_scadenza