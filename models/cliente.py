from typing import List
from models.utente import Utente
from models.metodo_pagamento import MetodoPagamento

class Cliente(Utente):
    def __init__(self, id_utente: int, nome: str, cognome: str, email: str,
                 password: str, numero_telefono: str,
                 metodi_pagamento: List[MetodoPagamento] = None):
        super().__init__(id_utente, nome, cognome, email, password, numero_telefono)
        self._metodi_pagamento = metodi_pagamento if metodi_pagamento is not None else []
        self._prodotti_carrello = []
        self._ordini = []

    @property
    def metodi_pagamento(self) -> List[MetodoPagamento]:
        return self._metodi_pagamento

    def aggiungi_metodo_pagamento(self, metodo: MetodoPagamento):
        self._metodi_pagamento.append(metodo)

    def rimuovi_metodo_pagamento(self, metodo: MetodoPagamento):
        if metodo in self._metodi_pagamento:
            self._metodi_pagamento.remove(metodo)

    @property
    def prodotti_carrello(self) -> List:
        return self._prodotti_carrello

    @property
    def ordini(self) -> List:
        return self._ordini

    def aggiungi_al_carrello(self, prodotto_carrello):
        self._prodotti_carrello.append(prodotto_carrello)

    def rimuovi_dal_carrello(self, prodotto_carrello):
        if prodotto_carrello in self._prodotti_carrello:
            self._prodotti_carrello.remove(prodotto_carrello)

    def svuota_carrello(self):
        self._prodotti_carrello.clear()

    def aggiungi_ordine(self, ordine):
        self._ordini.append(ordine)

    def get_ruolo(self) -> str:
        return "Cliente"