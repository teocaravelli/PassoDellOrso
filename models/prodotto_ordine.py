from models.prodotto import Prodotto

class ProdottoOrdine:
    def __init__(self, prodotto: Prodotto, quantita: int):
        self._prodotto = prodotto
        self._quantita = quantita

    @property
    def prodotto(self) -> Prodotto:
        return self._prodotto

    @property
    def quantita(self) -> int:
        return self._quantita