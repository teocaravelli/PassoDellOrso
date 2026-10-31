from datetime import datetime
from typing import List
from models.metodo_pagamento import MetodoPagamento
from models.prodotto_ordine import ProdottoOrdine
from models.enums import StatoOrdine

class Ordine:
    def __init__(self, id_ordine: int, metodo_pagamento: MetodoPagamento, prezzo_totale: float, prodotti: List[ProdottoOrdine]):
        self._data = datetime.now()
        self._id_ordine = id_ordine
        self._metodo_pagamento = metodo_pagamento
        self._prezzo_totale = prezzo_totale
        self._prodotti = prodotti
        self._stato = StatoOrdine.IN_CORSO

    @property
    def id_ordine(self) -> int:
        return self._id_ordine

    @property
    def prezzo_totale(self) -> float:
        return self._prezzo_totale

    @property
    def stato(self) -> StatoOrdine:
        return self._stato

    @stato.setter
    def stato(self, valore: StatoOrdine) -> None:
        self._stato = valore

    def set_prezzo_totale(self, valore: float) -> None:
        self._prezzo_totale = valore

    def set_prodotti(self, prodotti: List[ProdottoOrdine]) -> None:
        self._prodotti = prodotti

    def aggiungi_prodotto_ordine(self, prodotto_ordine: ProdottoOrdine) -> None:
        self._prodotti.append(prodotto_ordine)

    def calcola_prezzo_totale(self) -> float:
        totale = sum(po.prodotto.prezzo * po.quantita for po in self._prodotti)
        self._prezzo_totale = totale
        return self._prezzo_totale

    def get_dettagli(self) -> str:
        return f"Ordine {self._id_ordine} effettuato in data {self._data.strftime('%d/%m/%Y')} - Stato: {self._stato.value}"
