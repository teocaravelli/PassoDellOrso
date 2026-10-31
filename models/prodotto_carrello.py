from models.prodotto import Prodotto

class ProdottoCarrello:
    def __init__(self, prodotto: Prodotto, quantita: int):
        self._prodotto = prodotto
        self._quantita = quantita

    @property
    def prodotto(self) -> Prodotto:
        return self._prodotto

    @property
    def quantita(self) -> int:
        return self._quantita

    @quantita.setter
    def quantita(self, valore: int) -> None:
        self._quantita = valore

    def calcola_subtotale(self) -> float:
        return self._prodotto.prezzo * self._quantita