from abc import ABC

class Prodotto(ABC):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float, immagine: str, is_disponibile: bool):
        self._id = id_prodotto
        self._nome = nome
        self._descrizione = descrizione
        self._prezzo = prezzo
        self._immagine = immagine
        self._is_disponibile = is_disponibile

    @property
    def id(self) -> int:
        return self._id

    @property
    def is_disponibile(self) -> bool:
        return self._is_disponibile

    @is_disponibile.setter
    def is_disponibile(self, valore: bool) -> None:
        self._is_disponibile = valore

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def prezzo(self) -> float:
        return self._prezzo

    @prezzo.setter
    def prezzo(self, valore: float) -> None:
        self._prezzo = valore

    @nome.setter
    def nome(self, valore: str) -> None:
        self._nome = valore