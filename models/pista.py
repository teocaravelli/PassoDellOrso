from models.enums import Difficolta, StatoApertura

class Pista:
    def __init__(self, id_pista: int, nome: str, difficolta: Difficolta,
                 stato_apertura: StatoApertura = StatoApertura.APERTA):
        self._id_pista = id_pista
        self._nome = nome
        self._difficolta = difficolta
        self._stato_apertura = stato_apertura

    @property
    def id_pista(self) -> int:
        return self._id_pista

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def id_pista(self) -> int:
        return self._id_pista

    @nome.setter
    def nome(self, valore: str):
        self._nome = valore

    @property
    def difficolta(self) -> Difficolta:
        return self._difficolta

    @difficolta.setter
    def difficolta(self, valore: Difficolta):
        self._difficolta = valore

    @id_pista.setter
    def id_pista(self, valore: int):
        self._id_pista = valore

    @property
    def stato_apertura(self) -> StatoApertura:
        return self._stato_apertura

    @stato_apertura.setter
    def stato_apertura(self, valore: StatoApertura):
        self._stato_apertura = valore